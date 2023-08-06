class ColumnName:
    PREDICTIONS = "predictions"
    TARGET_VALUE = "target_value"
    ACTUALS = "actuals"
    TIMESTAMP = "timestamp"
    NR_SAMPLES = "samples"
    METRIC_VALUE = "value"
    DR_TIMESTAMP_COLUMN = "DR_RESERVED_PREDICTION_TIMESTAMP"
    DR_PREDICTION_COLUMN = "DR_RESERVED_PREDICTION_VALUE"
    ASSOCIATION_ID_COLUMN = "association_id"


class TimeBucket:
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    ALL = "all"


class DataGroups:
    SCORING = "scoring"
    PREDICTIONS = "predictions"
    ACTUALS = "actuals"
