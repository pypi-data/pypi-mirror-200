import logging
from typing import Dict, List, Tuple, Union

import pandas as pd

from dmm.constants import ColumnName, DataGroups, TimeBucket
from dmm.data_source.data_source_base import DataSourceBase
from dmm.metric.metric_base import MetricBase
from dmm.metric.sklearn_metric import SklearnMetric

logger = logging.getLogger(__name__)


class MetricEvaluatorStats:
    """
    This object contains stats about the metric evaluator.
    """

    def __init__(self):
        self.total_rows = 0
        self.nr_calls_to_score = 0
        self.nr_calls_to_reduce = 0

    def __str__(self):
        return "total rows: {}, score calls: {}, reduce calls: {}".format(
            self.total_rows, self.nr_calls_to_score, self.nr_calls_to_reduce
        )


class MetricEvaluator(object):
    """
    Evaluate a Model Metric using training data and scoring data. This class is
    used to "stream" data through the metric object and generate the metric values.
    """

    def __init__(
        self,
        metric: Union[str, MetricBase],
        source: DataSourceBase,
        time_bucket: TimeBucket,
        prediction_col: str = ColumnName.PREDICTIONS,
        actuals_col: str = ColumnName.ACTUALS,
        timestamp_col: str = ColumnName.TIMESTAMP,
        filter_actuals: bool = False,
        filter_predictions: bool = False,
        filter_scoring_data: bool = False,
    ):
        """
        Initialize the MetricEvaluator framework.
        :param metric: A single metric or a list of metrics. Metrics need to be based on ModelMetric class or a string
        representing a name of an SKLearn metric.
        :param source: A data source object that will be usd to get the data in chunks
        :param time_bucket: The time bucket size to use for evaluating metrics
        :param prediction_col: The name of the prediction column
        :param actuals_col: The name of the actuals column
        :param timestamp_col: The name of the timestamp column
        :param filter_actuals: whether the metric evaluator removes missing actuals values before scoring.
        :param filter_predictions: whether the metric evaluator removes missing predictions values before scoring.
        :param filter_scoring_data: whether the metric evaluator removes missing scoring values before scoring.
        """
        self._metrics = {
            metric.name: metric for metric in self._validate_and_convert_metrics(metric)
        }
        self._data_source = source
        if self._data_source is None:
            raise Exception("Can not evaluate a metric without a data source")

        self._time_bucket = time_bucket
        self._prediction_col = prediction_col
        self._actuals_col = actuals_col
        self._timestamp_col = timestamp_col
        self._groups_to_filter = self._get_groups_to_filter(
            filter_actuals, filter_predictions, filter_scoring_data
        )
        self._stats = MetricEvaluatorStats()

    def _validate_and_convert_metrics(
        self, metric: Union[str, MetricBase]
    ) -> List[MetricBase]:
        if not metric:
            raise ValueError("No metric(s) provided!")
        self._metrics = metric if isinstance(metric, list) else [metric]

        after_sklearn_conversion = []
        for metric in self._metrics:
            if metric is None:
                raise ValueError(
                    "A metric object in the list of metrics has a None value"
                )
            elif isinstance(metric, str):
                after_sklearn_conversion.append(SklearnMetric(metric))
            elif isinstance(metric, MetricBase):
                after_sklearn_conversion.append(metric)
            else:
                raise ValueError(
                    "One of the metrics provided is not based on MetricBase and is not an SKLearn metric"
                )
        return after_sklearn_conversion

    def reset_stats(self) -> None:
        """
        Reset the metric evaluator stats
        """
        self._stats = MetricEvaluatorStats()

    def stats(self) -> MetricEvaluatorStats:
        """
        Return MetricEvaluatorStats object with the current stats
        :return: MetricEvaluatorStats
        """
        return self._stats

    def _reduce_time_bucket_metric(
        self, time_bucket_metric_parts: Dict[str, List[float]]
    ) -> Dict[str, float]:
        """
        :param time_bucket_metric_parts:
        :return: Dict of metric name: reduced value
        """
        reduced_values = {}
        for metric_name, metric in self._metrics.items():
            reduced_values[metric_name] = metric.reduce_func()(
                time_bucket_metric_parts[metric_name]
            )
            self._stats.nr_calls_to_reduce += 1
        return reduced_values

    def _run_score(self, chunk_of_data: pd.DataFrame) -> Dict[str, float]:
        scored_values = {}
        predictions = (
            chunk_of_data[self._prediction_col].to_numpy()
            if self._prediction_col in chunk_of_data
            else None
        )
        actuals = (
            chunk_of_data[self._actuals_col].to_numpy()
            if self._actuals_col in chunk_of_data
            else None
        )

        for metric_name, metric in self._metrics.items():
            scored_values[metric_name] = metric.score(
                predictions=predictions if metric.need_predictions() else None,
                actuals=actuals if metric.need_actuals() else None,
                scoring_data=self._get_scoring_data(chunk_of_data)
                if metric.need_scoring_data()
                else None,
            )
            self._stats.nr_calls_to_score += 1
        return scored_values

    def fit(self, data: pd.DataFrame) -> None:
        for metric in self._metrics:
            metric.fit(data)

    def _validate_before_score(self) -> None:
        if self._data_source is None:
            raise Exception("Can not evaluate a metric without a data source")
        if self._metrics is None:
            raise ValueError("No metric was provided for evaluation")
        if not isinstance(self._metrics, list):
            raise ValueError("self._metric is not a list, this should not happen")
        for metric in self._metrics:
            if metric is None:
                raise ValueError("A metric object provided as None value")

    def _get_data_chunk(self) -> Tuple[pd.DataFrame, int, bool]:
        done = False
        chunk_of_data, time_bucket_id = self._data_source.get_data()

        if chunk_of_data is None:
            done = True
        else:
            if len(chunk_of_data) > self._data_source.max_rows:
                raise Exception("Chunk of data has too many rows")
            self._stats.total_rows += len(chunk_of_data)

        return chunk_of_data, time_bucket_id, done

    def _validate_data_chunk(self, data_chunk: pd.DataFrame) -> pd.DataFrame:
        for metric_name, metric in self._metrics.items():
            if metric.need_predictions() and self._prediction_col not in data_chunk:
                raise Exception(
                    f"Metric {metric_name} requires predictions, but data chunk is missing column "
                    f"{self._prediction_col}, columns present: {', '.join(data_chunk.columns)}"
                )
            if metric.need_actuals() and self._actuals_col not in data_chunk:
                raise Exception(
                    f"Metric {metric_name} requires actuals, but data chunk is missing column "
                    f"({self._actuals_col}), columns present: {', '.join(data_chunk.columns)}"
                )
        if self._groups_to_filter:
            data_chunk = self._drop_missing_values_from_data_chunk(data_chunk)
        return data_chunk

    def _drop_missing_values_from_data_chunk(
        self, data_chunk: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Remove missing values from a chunk of data based on selected groups to be filtered.
        """
        original_length = len(data_chunk)
        if (
            self._prediction_col in data_chunk
            and DataGroups.PREDICTIONS in self._groups_to_filter
        ):
            data_chunk = data_chunk.dropna(subset=[self._prediction_col])

        if (
            self._actuals_col in data_chunk
            and DataGroups.ACTUALS in self._groups_to_filter
        ):
            data_chunk = data_chunk.dropna(subset=[self._actuals_col])

        if DataGroups.SCORING in self._groups_to_filter:
            subset = [
                col_name
                for col_name in data_chunk.columns
                if col_name not in [self._actuals_col, self._prediction_col]
            ]
            data_chunk = data_chunk.dropna(subset=subset)

        if original_length != len(data_chunk):
            rows_difference = original_length - len(data_chunk)
            logger.warning(
                f"removed {rows_difference} rows out of {original_length} in the data chunk "
                f"before scoring, due to missing values in {self._groups_to_filter} data"
            )

        return data_chunk

    def _get_scoring_data(self, chunk_of_data: pd.DataFrame) -> pd.DataFrame:
        """
        Extract only data used in scoring
        """
        _chunk_of_data = chunk_of_data.copy()
        _chunk_of_data = _chunk_of_data.drop(
            columns=[
                self._actuals_col,
                self._prediction_col,
                self._timestamp_col,
                ColumnName.ASSOCIATION_ID_COLUMN,
            ],
            errors="ignore",
        )
        return _chunk_of_data

    @staticmethod
    def _get_groups_to_filter(
        filter_actuals: bool, filter_predictions: bool, filter_scoring_data: bool
    ) -> List[DataGroups]:
        groups_to_filter = []
        if filter_predictions:
            groups_to_filter.append(DataGroups.PREDICTIONS)
        if filter_actuals:
            groups_to_filter.append(DataGroups.ACTUALS)
        if filter_scoring_data:
            groups_to_filter.append(DataGroups.SCORING)
        return groups_to_filter

    def score(self) -> pd.DataFrame:
        """
        Steps to evaluate a metric
        1. Get Data from source
        2. Check that data is within the requested time window
        3. Chunk data into max_rows per metric and into time buckets
        4. Feed data to the metric transform
        5. Reduce transform results into the necessary time buckets
        6. Return Dataframe where there is a column per metric and a row per time bucket
        :return: a Dataframe with a row per time bucket in the data. For each time bucket there will be
                 the value of the metric, number of samples used to calculate the metric and the timestamp
        """
        self._data_source.init(self._time_bucket)

        done = False
        prev_time_bucket_id = None
        time_bucket_metric_nr_samples = 0
        time_bucket_timestamp = None

        time_bucket_scores = {metric: [] for metric in self._metrics}
        final_scores = {metric: [] for metric in self._metrics}

        output_nr_samples_list = []
        output_bucket_timestamp_list = []
        while not done:
            data_chunk, time_bucket_id, done = self._get_data_chunk()

            # Moved to a new time bucket so calling reduce on the previous values
            if time_bucket_id != prev_time_bucket_id:
                # We don't reduce in the first time we get data (as prev is None and id is not None)
                if prev_time_bucket_id is not None:
                    # Moved to a new time bucket (or done).. need to reduce
                    reduced_values = self._reduce_time_bucket_metric(time_bucket_scores)
                    output_nr_samples_list.append(time_bucket_metric_nr_samples)
                    output_bucket_timestamp_list.append(time_bucket_timestamp)
                    for metric, value in reduced_values.items():
                        final_scores[metric].append(value)
                        time_bucket_scores[metric].clear()
                time_bucket_metric_nr_samples = 0
                prev_time_bucket_id = time_bucket_id

            # Running the score and keeping the value until it is time to reduce
            # If we are done - we will not call the transform.
            if done:
                continue

            data_chunk = self._validate_data_chunk(data_chunk)
            if data_chunk.index.size == 0:
                logger.warning(f"data chunk is empty, skipping scoring...")
                continue

            for metric_name, value in self._run_score(data_chunk).items():
                time_bucket_scores[metric_name].append(value)
            time_bucket_metric_nr_samples += data_chunk.index.size
            time_bucket_timestamp = data_chunk[self._timestamp_col].iat[0]

        result_df = pd.DataFrame(
            {
                ColumnName.TIMESTAMP: output_bucket_timestamp_list,
                ColumnName.NR_SAMPLES: output_nr_samples_list,
                **final_scores,
            }
        )
        return result_df
