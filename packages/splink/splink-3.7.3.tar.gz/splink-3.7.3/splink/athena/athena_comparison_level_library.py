from ..comparison_level_composition import and_, not_, or_  # noqa: F401
from ..comparison_level_library import (
    ArrayIntersectLevelBase,
    ColumnsReversedLevelBase,
    DistanceFunctionLevelBase,
    DistanceInKMLevelBase,
    ElseLevelBase,
    ExactMatchLevelBase,
    LevenshteinLevelBase,
    NullLevelBase,
    PercentageDifferenceLevelBase,
)
from .athena_base import (
    AthenaBase,
)


class null_level(AthenaBase, NullLevelBase):
    pass


class exact_match_level(AthenaBase, ExactMatchLevelBase):
    pass


class else_level(AthenaBase, ElseLevelBase):
    pass


class columns_reversed_level(AthenaBase, ColumnsReversedLevelBase):
    pass


class distance_function_level(AthenaBase, DistanceFunctionLevelBase):
    pass


class levenshtein_level(AthenaBase, LevenshteinLevelBase):
    pass


class array_intersect_level(AthenaBase, ArrayIntersectLevelBase):
    pass


class percentage_difference_level(AthenaBase, PercentageDifferenceLevelBase):
    pass


class distance_in_km_level(AthenaBase, DistanceInKMLevelBase):
    pass
