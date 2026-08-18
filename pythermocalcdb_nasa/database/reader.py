# import libs
from typing import Literal

from .connection import get_connection


Phase = Literal["g", "l", "s"]


TABLES: dict[Phase, tuple[str, ...]] = {
    "g": (
        "gas_nasa9_coeffs_min_0_max_1000",
        "gas_nasa9_coeffs_min_1000_max_6000",
        "gas_nasa9_coeffs_min_6000_max_20000",
    ),
    "l": (
        "liquid_nasa9_coeffs_min_0_max_1000",
        "liquid_nasa9_coeffs_min_1000_max_6000",
        "liquid_nasa9_coeffs_min_6000_max_20000",
    ),
    "s": (
        "solid_nasa9_coeffs_min_0_max_1000",
        "solid_nasa9_coeffs_min_1000_max_6000",
        "solid_nasa9_coeffs_min_6000_max_20000",
    ),
}


def component_available(
    component_name: str,
    component_formula: str | None = None,
    phase: Phase | None = None,
) -> bool:
    """
    Check whether a component exists in the NASA-9 database.

    Parameters
    ----------
    component_name : str
        Component name to search for.
    component_formula : str | None, optional
        Component formula to search for when the name is not present.
    phase : Phase | None, optional
        Component phase:

        - "g": gas
        - "l": liquid
        - "s": solid

        If None, all phases are searched.

    Returns
    -------
    bool
        True if the component exists, otherwise False.
    """
    if phase is None:
        tables = tuple(
            table
            for phase_tables in TABLES.values()
            for table in phase_tables
        )
    else:
        tables = TABLES[phase]

    with get_connection() as connection:
        for table in tables:
            row = connection.execute(
                f"""
                SELECT 1
                FROM {table}
                WHERE Name = ? COLLATE NOCASE
                   OR (? IS NOT NULL AND Formula = ? COLLATE NOCASE)
                LIMIT 1
                """,
                (
                    component_name,
                    component_formula,
                    component_formula,
                ),
            ).fetchone()

            if row is not None:
                return True

    return False


def get_available_phases(
    component_name: str,
) -> list[Phase]:
    """
    Return all phases available for a component.

    Parameters
    ----------
    component_name : str
        Component name.

    Returns
    -------
    list[Phase]
        Available phases.
    """
    available_phases: list[Phase] = []

    with get_connection() as connection:
        for phase, tables in TABLES.items():
            for table in tables:
                row = connection.execute(
                    f"""
                    SELECT 1
                    FROM {table}
                    WHERE Name = ? COLLATE NOCASE
                    LIMIT 1
                    """,
                    (component_name,),
                ).fetchone()

                if row is not None:
                    available_phases.append(phase)
                    break

    return available_phases


def read_component(
    component_name: str,
    phase: Phase,
    temperature: float,
    component_formula: str | None = None,
) -> dict | None:
    """
    Read NASA-9 data for a component at a specified temperature.

    Parameters
    ----------
    component_name : str
        Component name.
    phase : Phase
        Component phase.
    temperature : float
        Temperature in kelvin.
    component_formula : str | None, optional
        Component formula to search for when the name is not present.

    Returns
    -------
    dict | None
        Database row as a dictionary if found,
        otherwise None.
    """
    with get_connection() as connection:
        for table in TABLES[phase]:
            row = connection.execute(
                f"""
                SELECT *
                FROM {table}
                WHERE (
                    Name = ? COLLATE NOCASE
                    OR (? IS NOT NULL AND Formula = ? COLLATE NOCASE)
                  )
                  AND ? >= Tmin
                  AND ? <= Tmax
                LIMIT 1
                """,
                (
                    component_name,
                    component_formula,
                    component_formula,
                    temperature,
                    temperature,
                ),
            ).fetchone()

            if row is not None:
                return dict(row)

    return None


def search_components(
    query: str,
    phase: Phase | None = None,
    limit: int = 20,
) -> list[dict]:
    """
    Search components by partial name.

    Parameters
    ----------
    query : str
        Search text.
    phase : Phase | None, optional
        Restrict the search to one phase.
    limit : int, optional
        Maximum number of returned components.

    Returns
    -------
    list[dict]
        Matching components.
    """
    if phase is None:
        tables = tuple(
            table
            for phase_tables in TABLES.values()
            for table in phase_tables
        )
    else:
        tables = TABLES[phase]

    components: dict[tuple[str, str], dict] = {}

    with get_connection() as connection:
        for table in tables:
            rows = connection.execute(
                f"""
                SELECT DISTINCT
                    Name,
                    Formula,
                    State
                FROM {table}
                WHERE Name LIKE ? COLLATE NOCASE
                """,
                (f"%{query}%",),
            ).fetchall()

            for row in rows:
                item = dict(row)

                key = (
                    item["Name"].lower(),
                    item["State"],
                )

                components[key] = item

                if len(components) >= limit:
                    break

            if len(components) >= limit:
                break

    return list(components.values())[:limit]
