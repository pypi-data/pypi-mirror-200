from ..comparison_level_composition import and_, not_, or_  # noqa: F401
from ..comparison_level_library import (
    ArrayIntersectLevelBase,
    ColumnsReversedLevelBase,
    DateDiffLevelBase,
    DistanceFunctionLevelBase,
    DistanceInKMLevelBase,
    ElseLevelBase,
    ExactMatchLevelBase,
    JaccardLevelBase,
    JaroWinklerLevelBase,
    LevenshteinLevelBase,
    NullLevelBase,
    PercentageDifferenceLevelBase,
)
from .spark_base import (
    SparkBase,
)


class null_level(SparkBase, NullLevelBase):
    pass


class exact_match_level(SparkBase, ExactMatchLevelBase):
    pass


class else_level(SparkBase, ElseLevelBase):
    pass


class columns_reversed_level(SparkBase, ColumnsReversedLevelBase):
    pass


class distance_function_level(SparkBase, DistanceFunctionLevelBase):
    pass


class levenshtein_level(SparkBase, LevenshteinLevelBase):
    pass


class jaro_winkler_level(SparkBase, JaroWinklerLevelBase):
    pass


class jaccard_level(SparkBase, JaccardLevelBase):
    pass


class array_intersect_level(SparkBase, ArrayIntersectLevelBase):
    pass


class percentage_difference_level(SparkBase, PercentageDifferenceLevelBase):
    pass


class distance_in_km_level(SparkBase, DistanceInKMLevelBase):
    pass


class datediff_level(SparkBase, DateDiffLevelBase):
    pass
