# import packages/modules
from typing import List

from pyThermoLinkDB.models import ModelSource
from pythermodb_settings.models import Component, Temperature
from rich import print

from pythermocalcdb_nasa import (
    build_model_source_from_database,
    check_component_availability,
)


# =======================================
# CREATE COMPONENTS
# =======================================

CO2 = Component(
    name="carbon dioxide",
    formula="CO2",
    state="g",
)

H2O = Component(
    name="dihydrogen monoxide",
    formula="H2O",
    state="g",
)

CO = Component(
    name="carbon monoxide",
    formula="CO",
    state="g",
)

H2 = Component(
    name="dihydrogen",
    formula="H2",
    state="g",
)

CH4 = Component(
    name="methane",
    formula="CH4",
    state="g",
)

components: List[Component] = [
    CH4,
    CO2,
    H2O,
    CO,
    H2,
]


# ====================================================
# SECTION: check component availability
# ====================================================

availability_results = check_component_availability(
    components=components,
)

if availability_results["missing_components"]:
    raise ValueError(
        "Some components are missing from the NASA-9 database: "
        f"{availability_results['missing_components']}"
    )


# ====================================================
# SECTION: build model source from sqlite database
# ====================================================

database_temperature = Temperature(
    value=298.15,
    unit="K",
)

model_source: ModelSource = build_model_source_from_database(
    components=availability_results["matched_components"],
    temperature=database_temperature,
)


# ====================================================
# SECTION: THERMODB LINK CONFIGURATION
# ====================================================

datasource = model_source.data_source
equationsource = model_source.equation_source

print("ModelSource built from NASA-9 sqlite database.")
print(list(datasource.keys()))
