from __future__ import annotations

import datetime
import errno
import json
import logging
import tempfile
import time
from enum import Enum
from typing import Callable, Generator, Iterator, List, Optional, Union

import datarobot as dr
import pandas as pd
import requests
from datarobot.errors import AsyncProcessUnsuccessfulError
from dateutil.parser import parse

from dmm.constants import ColumnName, TimeBucket
from dmm.data_source.data_source_base import DataSourceBase
from dmm.time_bucket import (
    check_if_in_same_time_bucket,
    check_if_in_same_time_bucket_vectorized,
)
from dmm.utils import (
    hour_rounder_down,
    hour_rounder_up,
    wait_for_result_from_status_url,
    wait_for_result_raw,
)

logger = logging.getLogger(__name__)


class DataRobotSource(DataSourceBase):
    """
    A DataSourceBase that talks with DataRobot API. Internally, it performs relevant exports and fetches the data.

    Requested data may not fit into the memory, this source tries to fetch as relatively small chunks of data and be
    as lazy as possible.
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        deployment_id: str,
        start: datetime.datetime,
        end: datetime.datetime,
        model_id: str = None,
        max_rows: int = 100,
    ):
        super().__init__(max_rows)
        if max_rows <= 0:
            raise Exception(f"max_rows must be > 0, got {max_rows}")

        self._deployment_id = deployment_id
        self._start = start
        self._end = end
        self._model_id = model_id
        self._current_chunk_id = 0
        self._prev_chunk_datetime = None
        self._actuals_caches = {}

        api = DataRobotApiClient(token, base_url)
        self._api = api
        self._deployment = Deployment(self._api, deployment_id)
        self._prediction_data_provider = self._get_prediction_data_provider()
        self._actuals_data_provider = self._get_actuals_data_provider()
        self._association_id = api.get_association_id(deployment_id)

    def init(self, time_bucket: TimeBucket) -> DataRobotSource:
        """
        Init function will be called prior to calling getting data by the Metric Evaluator runner.

        Parameters
        ----------
        time_bucket: TimeBucket
        """
        self._time_bucket = time_bucket
        self.reset()
        return self

    def reset(self) -> None:
        """
        Resets the current state of data exports to the beginning of the data.
        """
        self._prediction_data_provider = self._get_prediction_data_provider()
        self._actuals_data_provider = self._get_actuals_data_provider()
        self._actuals_caches = {}

    def get_actuals_data(self) -> (pd.DataFrame, int):
        """
        Method to return a chunk of actuals data that can be sent to a metric object to be transformed.
        :return:
            - DataFrame: if there is more data to process, or None
            - int: ID of the time bucket
        """
        actuals_df, chunk_id = self._actuals_data_provider.get_data()
        return actuals_df, chunk_id

    def get_all_actuals_data(self) -> pd.DataFrame:
        """
        Returns all actuals data available for that source object in a single DataFrame.
        :return:
            DataFrame: Actuals data for all chunks.
        """
        return self._get_all(self.get_actuals_data)

    def get_prediction_data(self) -> (pd.DataFrame, int):
        """
        Method to return a chunk of prediction data that can be sent to a metric object to be transformed.
        :return:
            - DataFrame: if there is more data to process, or None
            - int: ID of the time bucket
        """
        prediction_df, chunk_id = self._prediction_data_provider.get_data()
        return prediction_df, chunk_id

    def get_all_prediction_data(self) -> pd.DataFrame:
        """
        Returns all prediction data available for that source object in a single DataFrame.
        :return:
            DataFrame: Prediction data for all chunks.
        """
        return self._get_all(self.get_prediction_data)

    def get_training_data(self) -> pd.DataFrame:
        """
        Method to return training data that can be sent to a metric object to be transformed.
        :return:
            DataFrame: if training data found otherwise None
        """
        training_data_provider = self._get_training_data_provider()
        training_df = training_data_provider.get_data()
        return training_df

    def get_data(self) -> (pd.DataFrame, int):
        """
        Method to return a chunk of data that can be sent to a metric object to be transformed.
        :return:
            - DataFrame: if there is more data to process, or None
            - int: ID of the time bucket
        """
        if self._prev_chunk_datetime is None and self._current_chunk_id != -1:
            self.reset()

        if not self._association_id:
            raise Exception(
                "Cannot import actuals: deployment's association id not found"
            )

        prediction_df, chunk_id = self._prediction_data_provider.get_data()
        if prediction_df is None:
            logger.info("data export for the given time range completed")
            return prediction_df, chunk_id

        last_prediction_timestamp = (
            self._prediction_data_provider.get_last_prediction_timestamp(prediction_df)
        )
        prediction_chunk_ts = self._prediction_data_provider.get_chunk_timestamp()
        prediction_df = self._format_prediction_df(prediction_df)

        actuals_export_start = hour_rounder_down(prediction_chunk_ts)
        actuals_export_end = hour_rounder_up(last_prediction_timestamp)
        self._remove_unwanted_actuals_caches(actuals_export_start)

        last_actuals_ts = self._get_last_actuals_timestamp_from_caches()
        # fetch new actuals data
        if not last_actuals_ts or actuals_export_end > last_actuals_ts:
            actuals_export_start = (
                last_actuals_ts if last_actuals_ts else actuals_export_start
            )
            actuals_data_provider = ActualsDataExportProvider(
                api=self._api,
                deployment_id=self._deployment_id,
                start=actuals_export_start,
                end=actuals_export_end,
                max_rows=self.max_rows,
            )
            actuals_df = self._get_corresponding_actuals(actuals_data_provider)
            actuals_df_from_caches = self._get_actuals_df_from_caches()
            if not actuals_df.empty:
                self._update_actuals_caches(actuals_df)
            actuals_df = pd.concat([actuals_df, actuals_df_from_caches])

        # get actuals data from the caches
        else:
            actuals_df = self._get_actuals_df_from_caches()

        df = (
            pd.merge(
                prediction_df,
                self._format_actuals_df_before_merge(actuals_df),
                on=ColumnName.ASSOCIATION_ID_COLUMN,
                how="left",
            )
            if not actuals_df.empty
            else prediction_df
        )
        self._update_chunk_info(prediction_chunk_ts)
        return df, self._current_chunk_id

    def _get_actuals_data_provider(self) -> ActualsDataExportProvider:
        """
        Retrieves a new instance of the ActualsDataExportProvider class.
        """
        return ActualsDataExportProvider(
            api=self._api,
            deployment_id=self._deployment_id,
            start=self._start,
            end=self._end,
            model_id=self._model_id,
            time_bucket=self._time_bucket,
            max_rows=self.max_rows,
        )

    def _get_prediction_data_provider(self) -> PredictionDataExportProvider:
        """
        Retrieves a new instance of the PredictionDataExportProvider class.
        """
        return PredictionDataExportProvider(
            api=self._api,
            deployment_id=self._deployment_id,
            start=self._start,
            end=self._end,
            model_id=self._model_id,
            time_bucket=self.time_bucket,
            max_rows=self.max_rows,
        )

    def _get_training_data_provider(self) -> TrainingDataExportProvider:
        """
        Retrieves a new instance of the TrainingDataExportProvider class.
        """
        return TrainingDataExportProvider(
            api=self._api,
            deployment_id=self._deployment_id,
            model_id=self._model_id,
        )

    def _update_chunk_info(self, chunk_dt: datetime.datetime) -> None:
        """
        Source must keep track of a small piece of state to differentiate time bucketed chunks.
        This method updates this state.

        Parameters
        ----------
        chunk_dt: datetime
            datetime of any event within the chunk
        """
        if self._prev_chunk_datetime and not check_if_in_same_time_bucket(
            self._prev_chunk_datetime, chunk_dt, self._time_bucket
        ):
            self._current_chunk_id += 1
        self._prev_chunk_datetime = chunk_dt

    @staticmethod
    def _get_corresponding_actuals(
        actuals_data_provider: ActualsDataExportProvider,
    ) -> pd.DataFrame:
        """
        Retrieves corresponding actuals for the time range from prediction data export.

        Parameters
        ----------
        actuals_data_provider: ActualsDataExportProvider
        """
        chunk_id = 0
        chunks = []
        while chunk_id != -1:
            actuals_df, chunk_id = actuals_data_provider.get_data()
            if actuals_df is not None:
                chunks.append(actuals_df)
        if chunks:
            actuals_df = pd.concat(chunks)
            return actuals_df
        else:
            return pd.DataFrame()

    def _format_prediction_df(self, pred_df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats data from prediction data export, before merging with actuals.
        Renames the columns to standardize the output names.

        Parameters
        ----------
        pred_df: pd.DataFrame
        """
        rename_columns = {
            ColumnName.DR_TIMESTAMP_COLUMN: ColumnName.TIMESTAMP,
        }
        association_id = self._api.get_association_id(self._deployment_id)
        if association_id:
            rename_columns.update({association_id: ColumnName.ASSOCIATION_ID_COLUMN})

        if self._deployment.type == DeploymentType.REGRESSION:
            prediction_col = ColumnName.DR_PREDICTION_COLUMN
        elif self._deployment.type == DeploymentType.BINARY_CLASSIFICATION:
            prediction_col = f"{ColumnName.DR_PREDICTION_COLUMN}_{self._deployment.positive_class_label}"
            # apply prediction threshold
            pred_df[prediction_col] = (
                pred_df[prediction_col] >= self._deployment.prediction_threshold
            )
        else:
            raise Exception(f"Unsupported deployment type {self._deployment.type}")

        rename_columns.update({prediction_col: ColumnName.PREDICTIONS})
        pred_df = pred_df.rename(rename_columns, axis=1)
        return pred_df

    def _format_actuals_df_before_merge(self, actuals_df: pd.DataFrame) -> pd.DataFrame:
        """
        Formats data from actuals data export, before merging with prediction data.
        Drops columns to avoid duplication

        Parameters
        ----------
        actuals_df: pd.DataFrame
        """
        if self._deployment.type == DeploymentType.BINARY_CLASSIFICATION:
            actuals_df = actuals_df[
                actuals_df.label.astype("str") == self._deployment.positive_class_label
            ]

        actuals_df = actuals_df.drop(
            [ColumnName.PREDICTIONS, ColumnName.TIMESTAMP], axis=1
        )
        return actuals_df

    def _remove_unwanted_actuals_caches(self, start_dt: datetime.datetime) -> None:
        """
        Removes actuals from caches, that are no longer needed.

        Parameters
        ----------
        start_dt: datetime
        """
        unwanted = [
            actuals_dt
            for actuals_dt in self._actuals_caches
            if parse(actuals_dt) < start_dt
        ]
        for unwanted_key in unwanted:
            del self._actuals_caches[unwanted_key]

    def _update_actuals_caches(self, actuals_df: pd.DataFrame) -> None:
        """
        Update the actuals cache with the newly exported actuals.
        Caches are stored like actuals in Postgres - aggregated over an hour.

        Parameters
        ----------
        actuals_df: pd.DataFrame
        """
        grouped_actuals = actuals_df.groupby(ColumnName.TIMESTAMP)
        for group, df in grouped_actuals:
            self._actuals_caches[group] = df

    def _get_actuals_df_from_caches(self) -> pd.DataFrame:
        """
        Returns all cached actuals in the form of the concatenated pandas data frame.
        If there are no actuals caches, returns an empty pandas data frame.
        """
        if self._actuals_caches:
            return pd.concat(self._actuals_caches.values())
        else:
            return pd.DataFrame()

    def _get_last_actuals_timestamp_from_caches(self) -> Optional[datetime.datetime]:
        """
        Returns last timestamp from caches, which means an hour which is the end of the hourly interval.
        """
        if self._actuals_caches:
            last_hourly_start = parse(list(self._actuals_caches)[-1])
            last_hourly_end = last_hourly_start + datetime.timedelta(hours=1)
            return last_hourly_end
        else:
            return None

    @staticmethod
    def _get_all(provider: Callable[[], (pd.DataFrame, int)]) -> pd.DataFrame:
        """
        Utility method that polls provider (matches get_prediction_data / get_actuals_data signature) and concatenates
        all available frames.
        """
        result, chunk_id = provider()
        while chunk_id != -1:
            df, chunk_id = provider()
            if df is not None:
                result = pd.concat([result, df])
        return result


class DataRobotExportBase:
    """
    The base class for exporting data via DataRobot API in the time bucket chunk manner.
    """

    def __init__(
        self,
        api: DataRobotApiClient,
        deployment_id: str,
        model_id: str | None,
        start: datetime.datetime,
        end: datetime.datetime,
        timestamp_col: str,
        max_rows: int,
        time_bucket: TimeBucket,
        start_export: Callable,
        get_export_dataset_ids: Callable,
    ):
        self._api = api
        self._deployment_id = deployment_id
        self._model_id = model_id
        self._deployment = Deployment(self._api, deployment_id)
        self._start = start
        self._end = end
        self._time_bucket = time_bucket
        self._max_rows = max_rows
        self._timestamp_col = timestamp_col
        self._start_export = start_export
        self._get_export_dataset_ids = get_export_dataset_ids
        self._time_bucket_chunks = self._get_time_bucket_chunks()

        self._current_chunk_id = 0
        self._prev_chunk_datetime = None

    def set_new_export_parameters(
        self,
        start: datetime.datetime,
        end: datetime.datetime,
        time_bucket: TimeBucket,
        max_rows: int,
    ) -> DataRobotExportBase:
        self._start = start
        self._end = end
        self._time_bucket = time_bucket
        self._max_rows = max_rows
        self.reset()
        return self

    def reset(self) -> None:
        self._current_chunk_id = 0
        self._prev_chunk_datetime = None
        self._time_bucket_chunks = self._get_time_bucket_chunks()

    def _get_time_bucket_chunks(self) -> TimeBucketChunks:
        return TimeBucketChunks(
            self._timestamp_col,
            PushBackFrameIterator(
                iter(
                    DataRobotChunksIterator(
                        api=self._api,
                        deployment_id=self._deployment_id,
                        model_id=self._model_id,
                        start_dt=self._start,
                        end_dt=self._end,
                        timestamp_col=self._timestamp_col,
                        start_export=self._start_export,
                        get_export_dataset_ids=self._get_export_dataset_ids,
                    )
                )
            ),
        )

    def _update_chunk_info(self, chunk_dt: datetime.datetime):
        """
        Source must keep track of a small piece of state to differentiate time bucketed chunks.
        This method updates this state.

        Parameters
        ----------
        chunk_dt: datetime
            datetime of any event within the chunk
        """
        if self._prev_chunk_datetime and not check_if_in_same_time_bucket(
            self._prev_chunk_datetime, chunk_dt, self._time_bucket
        ):
            self._current_chunk_id += 1
        self._prev_chunk_datetime = chunk_dt


class PredictionDataExportProvider(DataRobotExportBase):
    def __init__(
        self,
        api: DataRobotApiClient,
        deployment_id: str,
        start: datetime.datetime,
        end: datetime.datetime,
        model_id: str = None,
        timestamp_col: str = ColumnName.DR_TIMESTAMP_COLUMN,
        max_rows: int = 100,
        time_bucket: TimeBucket = TimeBucket.ALL,
    ):
        if max_rows <= 0:
            raise Exception(f"max_rows must be > 0, got {max_rows}")

        super().__init__(
            api=api,
            deployment_id=deployment_id,
            model_id=model_id,
            start=start,
            end=end,
            timestamp_col=timestamp_col,
            max_rows=max_rows,
            time_bucket=time_bucket,
            start_export=api.start_prediction_data_export,
            get_export_dataset_ids=api.get_prediction_export_dataset_ids,
        )

    def get_data(self) -> (pd.DataFrame, int):
        """
        Method to return a chunk of prediction data that can be sent to a metric object to be transformed.
        :return:
            - DataFrame: if there is more data to process, or None
            - int: ID of the time bucket
        """
        if self._time_bucket_chunks.finished():
            return None, -1

        chunk_df, chunk_ts = self._time_bucket_chunks.load_time_bucket_chunk(
            time_bucket=self._time_bucket, max_rows=self._max_rows
        )

        self._update_chunk_info(chunk_ts)
        return chunk_df, self._current_chunk_id

    def get_last_prediction_timestamp(
        self, prediction_df: pd.DataFrame
    ) -> datetime.datetime:
        last_timestamp = prediction_df[self._timestamp_col].iloc[-1]
        return parse(last_timestamp)

    def get_chunk_timestamp(self) -> datetime.datetime:
        return self._prev_chunk_datetime


class ActualsDataExportProvider(DataRobotExportBase):
    def __init__(
        self,
        api: DataRobotApiClient,
        deployment_id: str,
        start: datetime.datetime,
        end: datetime.datetime,
        model_id: str = None,
        timestamp_col: str = ColumnName.TIMESTAMP,
        max_rows: int = 100,
        time_bucket: TimeBucket = TimeBucket.ALL,
    ):
        if max_rows <= 0:
            raise Exception(f"max_rows must be > 0, got {max_rows}")

        super().__init__(
            api=api,
            deployment_id=deployment_id,
            model_id=model_id,
            start=start,
            end=end,
            timestamp_col=timestamp_col,
            max_rows=max_rows,
            time_bucket=time_bucket,
            start_export=api.start_actuals_export,
            get_export_dataset_ids=api.get_actuals_export_dataset_ids,
        )

    def get_data(self) -> (pd.DataFrame, int):
        """
        Method to return a chunk of actuals data that can be sent to a metric object to be transformed.
        :return:
            - DataFrame: if there is more data to process, or None
            - int: ID of the time bucket
        """
        supported_time_buckets = self.get_supported_time_buckets()
        if self._time_bucket not in supported_time_buckets:
            raise Exception(
                f"For actuals export {self._time_bucket} time bucket is not supported, "
                f"select time bucket from {supported_time_buckets}"
            )

        if self._time_bucket_chunks.finished():
            return None, -1

        chunk_df, chunk_ts = self._time_bucket_chunks.load_time_bucket_chunk(
            time_bucket=self._time_bucket, max_rows=self._max_rows
        )

        self._update_chunk_info(chunk_ts)
        return chunk_df, self._current_chunk_id

    @staticmethod
    def get_supported_time_buckets():
        return [
            TimeBucket.HOUR,
            TimeBucket.DAY,
            TimeBucket.WEEK,
            TimeBucket.MONTH,
            TimeBucket.ALL,
        ]


class TrainingDataExportProvider:
    def __init__(
        self,
        api: DataRobotApiClient,
        deployment_id: str,
        model_id: str = None,
    ):
        self._api = api
        self._deployment_id = deployment_id
        self._model_id = model_id

    def get_data(self) -> pd.DataFrame:
        """
        Method to return training data that can be sent to a metric object to be transformed.
        :return:
            DataFrame: if training data found otherwise None
        """
        response = self._api.start_training_data_export(
            self._deployment_id, self._model_id
        )

        if response.status_code != 202:
            raise Exception(
                f"DataRobot export API failed with {response.status_code}: {response.text}"
            )

        status_url = response.headers["Location"]
        export_id = status_url.split("/")[-2]

        dataset_id = self._api.get_training_export_dataset_id(status_url)

        dataset = self._api.fetch_dataset_sync(dataset_id)
        with tempfile.NamedTemporaryFile() as f:
            try:
                dataset.get_file(filelike=f)
            except OSError as e:
                if e.errno == errno.ENOSPC:
                    raise Exception(
                        f"We ran out of disk space for training data export: {export_id}"
                    )
                raise e
            try:
                result = pd.read_csv(f.name)
            except MemoryError:
                raise Exception(
                    f"We ran out of memory for training data export: {export_id}"
                )
        return result


class DeploymentType(Enum):
    """
    Supported deployment types (based on deployment.model.targetType)
    """

    REGRESSION = 0
    BINARY_CLASSIFICATION = 1


class Deployment:
    """
    Provides access to relevant deployment properties.
    """

    def __init__(self, api: DataRobotApiClient, deployment_id: str):
        self._deployment = api.get_deployment(deployment_id)
        if "modelPackage" not in self._deployment:
            raise Exception("We do not support deployments without model packages!")
        model_package_id = self._deployment["modelPackage"]["id"]
        self._model_package = api.get_model_package(model_package_id)
        if self._model_package["modelKind"]["isTimeSeries"]:
            raise Exception("Time series models are not yet supported")

    @property
    def target_column(self) -> str:
        return self._deployment["model"]["targetName"]

    @property
    def type(self) -> DeploymentType:
        target_type = self._deployment["model"]["targetType"]
        if target_type == "Binary":
            return DeploymentType.BINARY_CLASSIFICATION
        elif target_type == "Regression":
            return DeploymentType.REGRESSION
        else:
            raise Exception(f"Unsupported model target type {target_type}")

    @property
    def positive_class_label(self) -> str:
        if self.type != DeploymentType.BINARY_CLASSIFICATION:
            raise Exception(
                "Positive class label can only be retrieved for binary classification deployments"
            )
        # according to API spec - positive class comes first
        return self._model_package["target"]["classNames"][0]

    @property
    def prediction_threshold(self) -> float:
        if self.type != DeploymentType.BINARY_CLASSIFICATION:
            raise Exception(
                "Prediction threshold can only be retrieved for binary classification deployments"
            )
        return self._model_package["target"]["predictionThreshold"]


class PushBackFrameIterator:
    """
    Extends iterator functionality to push back elements.
    """

    def __init__(self, iterator: Iterator[pd.DataFrame]):
        self._buffer = []
        self._iterator = iterator
        self._finished = False

    def finished(self) -> bool:
        """
        Returns status of a load. True if the records were exhausted.
        """
        self._load_next()
        return not self._buffer and self._finished

    def next(self) -> Optional[pd.DataFrame]:
        """
        Returns next chunk from source or None if finished.
        """
        if self._buffer:
            return self._buffer.pop()
        self._load_next()
        return self._buffer.pop() if self._buffer else None

    def push_back(self, df: pd.DataFrame) -> None:
        """
        Pushes a frame back to the iterator. This frame should be returned on the next call to next.
        """
        self._buffer.append(df)

    def peek_row(self) -> Optional[pd.Series]:
        """
        Returns the first row from DataFrame to be returned without consuming the frame.
        """
        if self._buffer:
            return self._buffer[0].iloc[0]
        self._load_next()
        return self._buffer[0].iloc[0] if self._buffer else None

    def _load_next(self):
        if self._finished or self._buffer:
            return
        try:
            self._buffer.append(next(self._iterator))
        except StopIteration:
            self._finished = True


class DataRobotApiClient:
    """
    Wrapper around dr.Client that exposes required operations against DataRobot API.
    """

    def __init__(self, token: str, base_url: str):
        self._client = dr.Client(token=token, endpoint=base_url)

    def start_prediction_data_export(
        self,
        deployment_id: str,
        start: datetime.datetime,
        end: datetime.datetime,
        model_id: Union[str, None],
    ) -> requests.Response:
        """
        Starts prediction data export between start (inclusive) and end (exclusive).
        We cannot assume anything about the order of returned records.

        Parameters
        ----------
        deployment_id: str
        start: datetime
            Inclusive start of the time range.
        end: datetime
            Exclusive end of the time range.
        model_id: Optional[str]
        """
        return self._client.post(
            f"deployments/{deployment_id}/predictionDataExports/",
            data={"start": start, "end": end, "modelId": model_id},
        )

    def start_actuals_export(
        self,
        deployment_id: str,
        start: datetime.datetime,
        end: datetime.datetime,
        model_id: Union[str, None],
    ) -> requests.Response:
        """
        Starts actuals data export between start (inclusive) and end (exclusive).
        We cannot assume anything about the order of returned records.

        Parameters
        ----------
        deployment_id: str
        start: datetime
            Inclusive start of the time range.
        end: datetime
            Exclusive end of the time range.
        model_id: Optional[str]
        """
        return self._client.post(
            f"deployments/{deployment_id}/actualsDataExports/",
            data={"start": start, "end": end, "modelId": model_id},
        )

    def start_training_data_export(
        self,
        deployment_id: str,
        model_id: Union[str, None],
    ) -> requests.Response:
        """
        Starts export of training data for the given model.
        If model_id is not given, export for current deployment champion.
        We cannot assume anything about the order of returned records.

        Parameters
        ----------
        deployment_id: str
        model_id: Optional[str]
        """
        return self._client.post(
            f"deployments/{deployment_id}/trainingDataExports/",
            data={"modelId": model_id},
        )

    def get_export_id_sync(self, start_export_response: requests.Response) -> str:
        """
        Waits until ready and fetches export_id after the export finishes. This method is blocking.

        Parameters
        ----------
        start_export_response: requests.Response
            Result of relevant start export call
        """
        export_id_response = wait_for_result_raw(self._client, start_export_response)
        export_id_response = json.loads(export_id_response)
        if export_id_response["status"] == "FAILED":
            raise AsyncProcessUnsuccessfulError(export_id_response["error"]["message"])
        return export_id_response["id"]

    def get_prediction_export_dataset_ids(
        self, deployment_id: str, export_id: str
    ) -> List[str]:
        """
        Export data can be fetched as datasets. This method fetches identifiers of these datasets.

        Parameters
        ----------
        deployment_id: str
        export_id: str
            Identifier of a completed export.
        """
        response = self._client.get(
            f"deployments/{deployment_id}/predictionDataExports/{export_id}"
        )
        data = response.json()["data"]
        if data:
            return [item["id"] for item in data]
        else:
            logger.info(f"no datasets found for prediction export id {export_id}")
            return []

    def get_actuals_export_dataset_ids(
        self, deployment_id: str, export_id: str
    ) -> List[str]:
        """
        Export data can be fetched as datasets. This method fetches identifiers of these datasets.

        Parameters
        ----------
        deployment_id: str
        export_id: str
            Identifier of a completed export.
        """
        response = self._client.get(
            f"deployments/{deployment_id}/actualsDataExports/{export_id}"
        )
        data = response.json()["data"]
        if data:
            return [item["id"] for item in data]
        else:
            logger.info(f"no datasets found for actuals export id {export_id}")
            return []

    def get_training_export_dataset_id(self, status_url: str) -> str:
        """
        Export data can be fetched as datasets. This method fetches identifier of this dataset.

        Parameters
        ----------
        status_url: str
        """
        export_id_response = wait_for_result_from_status_url(self._client, status_url)
        return json.loads(export_id_response)["datasetId"]

    def get_deployment(self, deployment_id: str) -> dict:
        """
        Fetches deployment metadata (model target name and type etc.)

        Parameters
        ----------
        deployment_id: str
        """
        return self._client.get(f"deployments/{deployment_id}").json()

    def get_model_package(self, model_package_id: str) -> dict:
        """
        Fetches model package info (to get time series info, prediction threshold etc.)

        Parameters
        ----------
        model_package_id: str
        """
        return self._client.get(f"modelPackages/{model_package_id}").json()

    def get_deployment_settings(self, deployment_id: str) -> dict:
        """
        Fetches deployment settings

        Parameters
        ----------
        deployment_id: str
        """
        return self._client.get(f"deployments/{deployment_id}/settings").json()

    def get_association_id(self, deployment_id: str) -> str:
        """
        Fetches association id for the given deployment, returns None if no association id

        Parameters
        ----------
        deployment_id: str
        """
        deployment_settings = self.get_deployment_settings(deployment_id)
        column_names = deployment_settings["associationId"]["columnNames"]
        association_id = column_names[0] if column_names else None
        return association_id

    @staticmethod
    def fetch_dataset_sync(dataset_id: str, max_wait_sec: int = 600) -> dr.Dataset:
        """
        Fetches dataset synchronously.

        Parameters
        ----------
        dataset_id: str
        max_wait_sec: int
            Maximum await time in seconds. Throws if waiting time exceeds this threshold.
        """
        start = time.time()
        while start + max_wait_sec > time.time():
            dataset = dr.Dataset.get(dataset_id)
            if dataset.processing_state == "COMPLETED":
                return dataset
            elif dataset.processing_state == "ERROR":
                raise ValueError(
                    "Dataset creation failed, most likely you requested range with no predictions"
                )
            time.sleep(5)
        raise Exception(f"Failed to fetch dataset within {max_wait_sec} seconds")


class DataRobotChunksIterator:
    """
    Uses DataRobot API to perform exports and read data in chunk-by-chunk fashion.
    """

    def __init__(
        self,
        api: DataRobotApiClient,
        deployment_id: str,
        model_id: str | None,
        start_dt: datetime.datetime,
        end_dt: datetime.datetime,
        timestamp_col: str,
        start_export: Callable,
        get_export_dataset_ids: Callable,
    ):
        self._deployment_id = deployment_id
        self._model_id = model_id
        self._start_dt = start_dt
        self._end_dt = end_dt
        self._timestamp_col = timestamp_col
        self._api = api
        self._start_export = start_export
        self._get_export_dataset_ids = get_export_dataset_ids

    def __iter__(self) -> Generator[pd.DataFrame, None, None]:
        """
        Returns an iterator over chunks for time range defined in the constructor. It returns data sorted by timestamp.
        The way it works is as follows
        - it is a generator to lazily fetch data from DR API,
        - it will try to perform a full export (start_dt to end_dt),
            - if this fails with PAYLOAD_TOO_LARGE, we cut interval in half and retry
        - due to sorting requirement, it has to load single successful export into the memory and iterate over it
        - it will perform subsequent exports once previous iteration is exhausted
        """
        interval = self._end_dt - self._start_dt
        start_dt = self._start_dt
        while start_dt != self._end_dt:
            df, interval = self._fetch_subset(start_dt, interval)
            start_dt += interval
            if df.empty:
                continue
            sorted_df = df.sort_values(by=self._timestamp_col)
            yield sorted_df

    def _fetch_subset(
        self, start_dt: datetime.datetime, interval: datetime.timedelta
    ) -> (pd.DataFrame, datetime.timedelta):
        export_type = self._get_export_type()
        if export_type:
            fetch_info = f"fetching the next {export_type} dataframe... {start_dt} - {start_dt + interval}"
        else:
            fetch_info = (
                f"fetching the next dataframe... {start_dt} - {start_dt + interval}"
            )
        logger.info(fetch_info)
        response, interval = self._get_export_response(start_dt, interval)
        try:
            export_id = self._api.get_export_id_sync(response)
        except AsyncProcessUnsuccessfulError as e:
            if export_type:
                fail_info = f"failed to export {export_type} data for {start_dt} - {start_dt + interval} interval: {str(e)}"
            else:
                fail_info = f"failed to export data for {start_dt} - {start_dt + interval} interval: {str(e)}"
            logger.info(fail_info)
            return pd.DataFrame(), interval

        result = pd.DataFrame()
        for dataset_id in self._get_export_dataset_ids(self._deployment_id, export_id):
            dataset = self._api.fetch_dataset_sync(dataset_id)
            with tempfile.NamedTemporaryFile() as f:
                try:
                    dataset.get_file(filelike=f)
                except OSError as e:
                    if e.errno == errno.ENOSPC:
                        raise Exception(
                            f"We ran out of disk space for interval {start_dt} - {start_dt + interval}. "
                            f"Consider fetching smaller chunks of data"
                        )
                    raise e
                try:
                    result = pd.concat([result, pd.read_csv(f.name)])
                except MemoryError:
                    raise Exception(
                        f"We ran out of memory for interval {start_dt} - {start_dt + interval}. "
                        f"Consider fetching smaller chunks of data"
                    )
        return result, interval

    def _get_export_response(
        self, from_dt: datetime.datetime, suggested_interval: datetime.timedelta
    ) -> (requests.Response, datetime.timedelta):
        # we try to increase interval to mitigate too aggressive shrinking
        interval = min(self._end_dt - from_dt, 2 * suggested_interval)
        response = self._start_export(
            self._deployment_id,
            from_dt,
            from_dt + interval,
            self._model_id,
        )

        while response.status_code == 413:
            interval /= 2
            logger.info(
                f"requested too many rows. trying smaller interval {from_dt} - {from_dt + interval}"
            )
            response = self._start_export(
                self._deployment_id, from_dt, from_dt + interval, self._model_id
            )

        if response.status_code != 202:
            raise Exception(
                f"DataRobot export API failed with {response.status_code}: {response.text}"
            )
        return response, interval

    def _get_export_type(self) -> str:
        if self._start_export == self._api.start_prediction_data_export:
            export_type = "prediction"
        elif self._start_export == self._api.start_actuals_export:
            export_type = "actuals"
        else:
            export_type = ""
        return export_type


class TimeBucketChunks:
    """
    Builds chunks out of rows returned by PushBackFrameIterator.
    """

    def __init__(self, timestamp_column: str, chunks_iterator: PushBackFrameIterator):
        self._timestamp_column = timestamp_column
        self._chunks_iterator = chunks_iterator

    def finished(self) -> bool:
        """
        True if the records in underlying iterator were exhausted.
        """
        return self._chunks_iterator.finished()

    def load_time_bucket_chunk(
        self, time_bucket: TimeBucket, max_rows: int
    ) -> (pd.DataFrame, datetime.datetime):
        """
        Pulls rows from rows_iterator respecting two rules
        - all records must belong to the same time bucket
        - chunk cannot be larger than max_rows

        Parameters
        ----------
        time_bucket: TimeBucket
            All rows within a chunk fall into the same time bucket.
        max_rows: int
            Upperbound on the size of the chunk.
        """
        row = self._chunks_iterator.peek_row()
        if row is None:
            raise Exception(
                "fetch_time_bucket_chunk shouldn't be called against exhausted source"
            )
        self._validate_row(row)
        chunk_ts = parse(row[self._timestamp_column])

        chunks = []
        total_rows = 0
        while not self._chunks_iterator.finished() and total_rows < max_rows:
            df = self._chunks_iterator.next()
            same_chunk, others = self._partition_by_time_bucket(
                df, time_bucket, chunk_ts, max_rows - total_rows
            )
            chunks.append(same_chunk)
            total_rows += len(same_chunk)
            if not others.empty:
                self._chunks_iterator.push_back(others)
                break
        return pd.concat(chunks), chunk_ts

    def _partition_by_time_bucket(
        self,
        df: pd.DataFrame,
        time_bucket: TimeBucket,
        chunk_ts: datetime.datetime,
        max_rows: int,
    ) -> (pd.DataFrame, pd.DataFrame):
        """
        Returns a subframe with records that belong to the bucket defined by `chunk_ts` + `time_bucket` arguments.
        It respects `max_rows` constraint - thus some records from that bucket might end up in `others` frame.
        The remaining records are present in the latter data frame.
        Assumes that the rows in `df` are sorted by timestamp. `same_bucket` frame is always a prefix of `df`.
        """
        filter_condition = check_if_in_same_time_bucket_vectorized(
            pd.to_datetime(df[self._timestamp_column]), chunk_ts, time_bucket
        )
        same_bucket = df[filter_condition].iloc[:max_rows]
        others = df.iloc[len(same_bucket) :]
        return same_bucket, others

    def _validate_row(self, row: pd.Series) -> None:
        if self._timestamp_column not in row:
            logger.debug(
                "Got row without %s column: %s",
                self._timestamp_column,
                row.to_string(header=False, index=False),
            )
            raise Exception(f"Got row without {self._timestamp_column} column")
