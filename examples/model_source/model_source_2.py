# import packages/modules
import os
from rich import print
from typing import Callable, Dict, Optional, Union, List, Any
import pyThermoDB as ptdb
import pyThermoLinkDB as ptdblink
from pyThermoLinkDB import (
    build_components_model_source,
    build_model_source
)
from pyThermoLinkDB.models import ComponentModelSource, ModelSource
from pythermodb_settings.models import Component
from pyThermoDB import ComponentThermoDB
from pyThermoDB import build_component_thermodb_from_reference
from pyreactlab_core.models.reaction import Reaction
# locals
from examples.references.reference_3 import REFERENCE_CONTENT

# check version
print(ptdblink.__version__)
print(ptdb.__version__)

# =======================================
# 🌍 CREATE COMPONENTS
# =======================================
# NOTE: components
# ! carbon dioxide
CO2 = Component(
    name='carbon dioxide',
    formula='CO2',
    state='g'
)

# ! water
H2O = Component(
    name='dihydrogen monoxide',
    formula='H2O',
    state='g'
)

# ! carbon monoxide
CO = Component(
    name='carbon monoxide',
    formula='CO',
    state='g'
)

# ! dihydrogen
H2 = Component(
    name='dihydrogen',
    formula='H2',
    state='g'
)

# NOTE: components list
components: List[Component] = [CO]

# ====================================================
# SECTION: BUILD COMPONENT THERMODB
# ====================================================
# NOTE: ignore state properties
ignore_state_props = None

# ====================================================
# SECTION: build components thermodb
# ====================================================
thermodb_components: List[ComponentThermoDB] = []

for comp in components:
    thermodb_component = build_component_thermodb_from_reference(
        component_name=comp.name,
        component_formula=comp.formula,
        component_state=comp.state,
        reference_content=REFERENCE_CONTENT,
        check_labels=False
    )
    if thermodb_component is None:
        raise ValueError(f"thermodb_component for {comp.name} is None")
    thermodb_components.append(thermodb_component)


# NOTE: with partially matched rules
component_model_source: List[ComponentModelSource] = build_components_model_source(
    components_thermodb=thermodb_components,
    rules=None,
)
print(component_model_source)

# ====================================================
# SECTION: build model source
# ====================================================

# model source
model_source: ModelSource = build_model_source(
    source=component_model_source,
)
# ====================================================
# SECTION: THERMODB LINK CONFIGURATION
# ====================================================

# build datasource & equationsource
datasource = model_source.data_source
equationsource = model_source.equation_source
