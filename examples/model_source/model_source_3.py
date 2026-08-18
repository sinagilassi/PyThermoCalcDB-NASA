# import packages/modules
import random
from typing import List

from rich import print
from pyThermoLinkDB.models import ModelSource
from pythermodb_settings.models import Component, Temperature

from pythermocalcdb_nasa import (
    build_model_source_from_database,
    check_component_availability,
)
from pythermocalcdb_nasa.database import read_component, search_components


# ====================================================
# SECTION: select random components from sqlite database
# ====================================================

RANDOM_SEED = 42
COMPONENT_COUNT = 5
DATABASE_TEMPERATURE = Temperature(value=298.15, unit="K")

random.seed(RANDOM_SEED)

database_rows = search_components(
    query="",
    phase="g",
    limit=200,
)

component_pool = [
    row
    for row in database_rows
    if read_component(
        component_name=row["Name"],
        component_formula=row["Formula"],
        phase="g",
        temperature=DATABASE_TEMPERATURE.value,
    ) is not None
]

if len(component_pool) < COMPONENT_COUNT:
    raise ValueError(
        f"Expected at least {COMPONENT_COUNT} database components at "
        f"{DATABASE_TEMPERATURE.value} K, "
        f"found {len(component_pool)}."
    )

random_rows = random.sample(
    component_pool,
    k=COMPONENT_COUNT,
)

components: List[Component] = [
    Component(
        name=row["Name"],
        formula=row["Formula"],
        state=row["State"],
    )
    for row in random_rows
]

print("Random components:")
print(components)


# ====================================================
# SECTION: check component availability
# ====================================================

availability_results = check_component_availability(
    components=components,
)

print("Availability results:")
print(availability_results)

if availability_results["missing_components"]:
    raise ValueError(
        "Some random components are missing from the database: "
        f"{availability_results['missing_components']}"
    )


# ====================================================
# SECTION: build model source from sqlite database
# ====================================================

model_source: ModelSource = build_model_source_from_database(
    components=availability_results["matched_components"],
    temperature=DATABASE_TEMPERATURE,
)


# ====================================================
# SECTION: THERMODB LINK CONFIGURATION
# ====================================================

datasource = model_source.data_source
equationsource = model_source.equation_source

print("ModelSource built from sqlite database.")
print("Data source keys:")
print(list(datasource.keys()))
