from typing import Dict, List, Optional, Tuple

from fastapi import Depends, HTTPException, Query

from .complexity import ComplexityParameters
from .rca import RcaParameters

# TODO: Once fastapi@0.95.0 becomes more widespread,
# replace Query() default values with typing_extensions.Annotated[]
# @see https://fastapi.tiangolo.com/tutorial/query-params-str-validations/?h=validation#use-annotated-in-the-type-for-the-q-parameter


def parse_alias(
    aliases: List[str] = Query(
        [],
        alias="alias",
        description=(
            "Changes the label of a Level in the response tidy data dictionaries."
        ),
    ),
):
    """Alias dependency.

    Parses the alias parameter into a dict of {Level: Alias label}.

    The parameter is a list of strings, but each item is split by comma anyway
    to ensure compatibility with URLSearchParams of both formats:
    - `alias[]=label1:alias1&alias[]=label2:alias2`
    - `alias=label1:alias1,label2:alias2`
    """
    try:
        # Note keys and values are inverted,
        # this because values must be unique for DataFrame.rename()
        parsed_alias = {
            label: level
            for level, label in (
                item.split(":", maxsplit=2)
                for alias in aliases
                for item in alias.split(",")
            )
        }
    except ValueError:
        raise HTTPException(400, "Malformed 'alias' parameter")

    alias_dict = {
        level: label
        for label, level in parsed_alias.items()
    }
    alias_dict.update({
        f"{level} ID": f"{label} ID"
        for level, label in alias_dict.items()
    })
    return alias_dict


def parse_filter(
    output_filters: List[str] = Query(
        [],
        alias="filter",
        description=(
            "Limits the results returned by the output. Only members of a "
            "dimension matching one of the parameters will be kept in the response."
        ),
    )
):
    """Filter dependency.

    Parses the filter parameter into a dict of {Level: (Member IDs, ...)}.
    Each token in the parameter has the shape `Level:id1,id2...`
    """
    def guess_numeric(values: str):
        return tuple(
            int(item) if item.isnumeric() else item
            for item in values.split(",")
        )

    try:
        return {
            key: guess_numeric(values)
            for key, values in (
                filtr.split(":", maxsplit=2)
                for filtr in output_filters
            )
        }
    except ValueError:
        raise HTTPException(400, "Malformed 'filter' parameter")


def parse_threshold(
    threshold: List[str] = Query(
        [],
        description=(
            "Restricts the data to be used in the calculation, to rows where "
            "the sum of all values through the other dimension fulfills the condition."
        ),
    )
):
    """Threshold dependency.

    Parses the threshold parameter into a dict of {Level: (Comparison, Value)}.

    The parameter is a list of strings, but each item is split by comma anyway
    to ensure compatibility with URLSearchParams of both formats:
    - `threshold[]=level1:gte:10&threshold[]=level2:lt:20`
    - `threshold=level1:gte:10,level2:lt:20`
    """
    def parse_singleton(param: str):
        tokens = param.split(":")
        if len(tokens) == 2:
            level, comparison, value = tokens[0], "gte", tokens[1]
        elif len(tokens) == 3:
            level, comparison, value = tokens
        else:
            raise HTTPException(400,
                f"Malformed 'threshold' parameter, '{param}' is invalid"
            )

        if not value.isnumeric():
            raise HTTPException(400,
                f"Malformed 'threshold' parameter, '{value}' must be numeric"
            )
        value = int(value)

        try:
            return level, (comparison, value)
        except ValueError:
            raise HTTPException(400,
                f"Malformed 'threshold' parameter, '{comparison}' is not a valid "
                "comparison identifier"
            ) from None

    return dict(
        parse_singleton(param)
        for token in threshold
        for param in token.split(",")
    )


def prepare_rca_params(
    cube: str = Query(
        ...,
        description="The cube to retrieve the main data",
    ),
    activity: str = Query(
        ...,
        description="Productivity categories for the RCA calculation",
    ),
    location: str = Query(
        ...,
        description="Geographical categories for the RCA calculation",
    ),
    measure: str = Query(
        ...,
        description="Values to use for the RCA calculations",
    ),
    year: int = Query(
        ...,
        description="Year to restrict the source data",
    ),
    locale: Optional[str] = Query(
        None,
        description="Locale for the labels in the data"
    ),
    aliases: Dict[str, str] = Depends(parse_alias),
    threshold: Dict[str, Tuple[str, int]] = Depends(parse_threshold),
):
    return RcaParameters(
        activity=activity,
        cube=cube,
        location=location,
        measure=measure,
        year=year,
        locale=locale,
        aliases=aliases,
        threshold=threshold,
    )


def prepare_complexity_params(
    rca_params: RcaParameters = Depends(prepare_rca_params),
    iterations: int = Query(
        20,
        description=(
            "The number of iterations used to calculate the Complexity Indicators."
        ),
    ),
    cutoff: float = Query(
        1,
        alias="rca_cutoff",
        description=(
            "The threshold value at which a country's RCA is considered "
            "relevant for an economic activity, for the purpose of calculating "
            "the Complexity Indicators."
        ),
    ),
    ascending: Optional[bool] = Query(
        None,
        description=(
            "Outputs the results in ascending or descending order. "
            "If not defined, results will be returned sorted by level member."
        ),
    ),
    rank: bool = Query(
        False,
        description=(
            "Adds a 'Ranking' column to the data. "
            "This value represents the index in the whole result list, sorted by value."
        ),
    ),
):
    return ComplexityParameters(
        rca_params=rca_params,
        cutoff=cutoff,
        iterations=iterations,
        rank=rank,
        sort_ascending=ascending,
    )
