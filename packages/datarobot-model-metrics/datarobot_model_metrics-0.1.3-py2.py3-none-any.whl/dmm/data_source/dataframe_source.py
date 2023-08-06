import pandas as pd
from dateutil.parser import parse

from dmm.constants import ColumnName, TimeBucket
from dmm.data_source.data_source_base import DataSourceBase
from dmm.time_bucket import check_if_in_same_time_bucket


class DataFrameSource(DataSourceBase):
    def __init__(
        self,
        df: pd.DataFrame,
        max_rows=100,
        timestamp_col: ColumnName = ColumnName.TIMESTAMP,
    ):
        super().__init__(max_rows)
        if max_rows <= 0:
            raise Exception("max_rows must be > 0, got {}".format(max_rows))

        self._df = df
        self._timestamp_col = timestamp_col
        self.reset()
        self._current_row = 0
        self._current_chunk_id = 0
        self._prev_chunk_datetime = None

    def init(self, time_bucket):
        self._time_bucket = time_bucket
        self.reset()
        return self

    def reset(self) -> None:
        self._current_row = 0
        self._current_chunk_id = 0

    def get_data(self) -> (pd.DataFrame, int):
        # In case we are already done with this DF
        if self._current_row >= self._df.shape[0]:
            return None, -1

        self._df.reset_index()
        chunk_df = pd.DataFrame(columns=self._df.columns)
        # We can always take at least 1 row into the chunk
        chunk_df = chunk_df.append(self._df.iloc[self._current_row])
        self._current_row += 1
        chunk_start_datetime = parse(chunk_df.iloc[0][self._timestamp_col])

        if self._prev_chunk_datetime:
            # This is for the case where the boundaries of chunks are aligned with the max rows
            if not check_if_in_same_time_bucket(
                self._prev_chunk_datetime, chunk_start_datetime, self._time_bucket
            ):
                self._current_chunk_id += 1

        self._prev_chunk_datetime = chunk_start_datetime

        if self._current_row >= self._df.shape[0]:
            return chunk_df, self._current_chunk_id

        search_start_row = self._current_row
        search_end_row = min(search_start_row + self._max_rows - 1, self._df.shape[0])
        chunk_id_to_return = self._current_chunk_id
        for loc in range(search_start_row, search_end_row):
            loc_datetime = parse(self._df.iloc[loc][self._timestamp_col])

            if check_if_in_same_time_bucket(
                chunk_start_datetime, loc_datetime, self._time_bucket
            ):
                chunk_df = chunk_df.append(self._df.iloc[self._current_row])
                self._current_row += 1
            else:
                self._current_chunk_id += 1
                break
        return chunk_df, chunk_id_to_return
