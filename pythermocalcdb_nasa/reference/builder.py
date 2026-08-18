# import libs
import logging

from typing import Any, Iterable

from pythermocalcdb_nasa.database import (
    Phase,
    read_component,
)

# NOTE: logger setup
logger = logging.getLogger(__name__)

REFERENCE_COLUMNS = [
    "No.",
    "Name",
    "Formula",
    "State",
    "Formula-Raw",
    "Phase-Flag",
    "Molecular-Weight",
    "Enthalpy-of-Formation",
    "Minimum-Temperature",
    "Maximum-Temperature",
    "dEnFo_IG_298",
    "a1",
    "a2",
    "a3",
    "a4",
    "a5",
    "a6",
    "a7",
    "b1",
    "b2",
]


REFERENCE_TEMPLATE = """
REFERENCES:
  CUSTOM-REF-1:
    DATABOOK-ID: 1
    TABLES:
      NASA9-1:
        TABLE-ID: 1
        DESCRIPTION: This table provides the 9-coefficient NASA polynomial parameters.
        DATA: []
        STRUCTURE:
          COLUMNS: [No., Name, Formula, State, Formula-Raw, Phase-Flag, Molecular-Weight, Enthalpy-of-Formation, Minimum-Temperature, Maximum-Temperature, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2]
          SYMBOL: [None, None, None, None, None, None, MW, EnFo_IG, Tmin, Tmax, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2]
          UNIT: [None, None, None, None, None, None, g/mol, J/mol, K, K, J/mol, 1, 1, 1, 1, 1, 1, 1, 1, 1]
          CONVERSION: [None, None, None, None, None, None, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        VALUES:
{values}
""".strip()


def database_row_to_reference_value(
    row: dict[str, Any],
    row_number: int,
) -> list[Any]:
    """
    Convert a database row to the exact VALUES structure
    required by the NASA reference template.

    Parameters
    ----------
    row : dict[str, Any]
        Database row.
    row_number : int
        Sequential row number inside the generated reference.

    Returns
    -------
    list[Any]
        Reference VALUES row.
    """
    return [
        row_number,
        row["Name"],
        row["Formula"],
        row["State"],
        row["formula_raw"],
        row["phase_flag"],
        row["MW"],
        row["EnFo_IG"],
        row["Tmin"],
        row["Tmax"],
        row["dEnFo_IG_298"],
        row["a1"],
        row["a2"],
        row["a3"],
        row["a4"],
        row["a5"],
        row["a6"],
        row["a7"],
        row["b1"],
        row["b2"],
    ]


def format_reference_value(
    value: list[Any],
) -> str:
    """
    Format one reference row as YAML list syntax.
    """
    return f"        - {repr(value)}"


def build_reference_from_rows(
    rows: Iterable[dict[str, Any]],
) -> str:
    """
    Build REFERENCE_CONTENT from database rows.

    Parameters
    ----------
    rows : Iterable[dict[str, Any]]
        Database rows.

    Returns
    -------
    str
        Complete reference content.
    """
    rows = list(rows)

    reference_values = [
        database_row_to_reference_value(
            row=row,
            row_number=index,
        )
        for index, row in enumerate(
            rows,
            start=1,
        )
    ]

    values_content = "\n".join(
        format_reference_value(value)
        for value in reference_values
    )

    return REFERENCE_TEMPLATE.format(
        values=values_content
    )


def build_reference_from_database(
    components: list[str],
    phase: Phase,
    temperature: float,
) -> str:
    """
    Read components from the NASA-9 database and construct
    REFERENCE_CONTENT.

    Parameters
    ----------
    components : list[str]
        Component names.
    phase : Phase
        Phase shared by the requested components.
    temperature : float
        Temperature in kelvin used to select the appropriate
        NASA-9 coefficient range.

    Returns
    -------
    str
        Generated reference content.

    Raises
    ------
    ValueError
        If a requested component cannot be found.
    """
    rows: list[dict] = []

    for component_name in components:
        row = read_component(
            component_name=component_name,
            phase=phase,
            temperature=temperature,
        )

        if row is None:
            raise ValueError(
                f"NASA-9 data not found for "
                f"component={component_name!r}, "
                f"phase={phase!r}, "
                f"temperature={temperature} K."
            )

        rows.append(row)

    return build_reference_from_rows(rows)
