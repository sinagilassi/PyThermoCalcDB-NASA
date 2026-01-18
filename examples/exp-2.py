# import packages/modules
import os
from rich import print
import pyThermoLinkDB as ptdblink
from pyThermoLinkDB import load_and_build_model_source
from pyThermoLinkDB.models import ModelSource
import pyThermoDB as ptdb
from pythermodb_settings.models import (
    Component,
    ComponentRule,
    ComponentThermoDBSource,
    Temperature
)
# locals
from pythermocalcdb_nasa import H_T, S_T, G_T, Cp_T


import logging
logging.getLogger().setLevel(logging.ERROR)  # Only show errors and above

# check version
print(ptdblink.__version__)
print(ptdb.__version__)

# =======================================
# 🌍 LOAD THERMODB
# =======================================
# current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"current dir: {current_dir}")

# NOTE: thermodb configurations
# carbon dioxide gas thermodb file
CO2_thermodb_file = os.path.join(
    current_dir,
    'thermodb',
    'carbon dioxide-CO2-g-nasa-1.pkl'
)

# NOTE: components
# ! CO2
CO2 = Component(
    name='carbon dioxide',
    formula='CO2',
    state='g'
)

# methane gas thermodb
CH4_thermodb_file = os.path.join(
    current_dir,
    'thermodb',
    'methane-CH4-g-nasa-1.pkl'
)

# methane gas component
CH4 = Component(
    name='methane',
    formula='CH4',
    state='g'
)

# =======================================
# SECTION: create thermodb source
# ======================================
# NOTE: component thermodb
CO2_thermodb: ComponentThermoDBSource = ComponentThermoDBSource(
    component=CO2,
    source=CO2_thermodb_file
)

CH4_thermodb: ComponentThermoDBSource = ComponentThermoDBSource(
    component=CH4,
    source=CH4_thermodb_file
)

# =======================================
# 🏗️ LOAD & BUILD
# =======================================
# ! update thermodb rule

# ! with rules
# model_source2: ModelSource = load_and_build_model_source(
#     thermodb_sources=[
#         CO2_thermodb
#     ],
#     rules=thermodb_rules,
# )
# print(model_source2)

# ! without rules
model_source: ModelSource = load_and_build_model_source(
    thermodb_sources=[
        CO2_thermodb,
        CH4_thermodb
    ],
    original_equation_label=False
)
print(model_source)

# get data source and equation source
datasource = model_source.data_source
equationsource = model_source.equation_source

# =======================================
# ✅ TEST
# =======================================
# NOTE: enthalpy of CO2 at 300 K
temperature = Temperature(
    value=300.0,
    unit='K'
)

H_CO2_300K = H_T(
    component=CO2,
    temperature=temperature,
    model_source=model_source,
    mode="log",
)
print(f"H_CO2_300K: {H_CO2_300K}")

H_CO2_300K = H_T(
    component=CO2,
    temperature=temperature,
    model_source=model_source,
    basis="mass",
    mode="log",
)
print(f"H_CO2_300K: {H_CO2_300K}")

# NOTE: entropy of CH4 at 400 K
S_CH4_400K = S_T(
    component=CH4,
    temperature=Temperature(
        value=400.0,
        unit='K'
    ),
    model_source=model_source,
    basis="molar",
    mode="log"
)
print(f"S_CH4_400K: {S_CH4_400K}")

S_CH4_400K = S_T(
    component=CH4,
    temperature=Temperature(
        value=400.0,
        unit='K'
    ),
    model_source=model_source,
    basis="mass",
    mode="log"
)
print(f"S_CH4_400K: {S_CH4_400K}")

# NOTE: Gibbs free energy of CO2 at 500 K
G_CO2_500K = G_T(
    component=CO2,
    temperature=Temperature(
        value=500.0,
        unit='K'
    ),
    model_source=model_source,
    basis="molar"
)
print(f"G_CO2_500K: {G_CO2_500K}")

G_CO2_500K = G_T(
    component=CO2,
    temperature=Temperature(
        value=500.0,
        unit='K'
    ),
    model_source=model_source,
    basis="mass",
    mode="log"
)
print(f"G_CO2_500K: {G_CO2_500K}")

# NOTE: heat capacity of CH4 at 600 K
Cp_CH4_600K = Cp_T(
    component=CH4,
    temperature=Temperature(
        value=600.0,
        unit='K'
    ),
    model_source=model_source,
    mode="log",
)
print(f"Cp_CH4_600K: {Cp_CH4_600K}")

Cp_CH4_600K = Cp_T(
    component=CH4,
    temperature=Temperature(
        value=600.0,
        unit='K'
    ),
    model_source=model_source,
    basis="mass",
    mode="log",
)
print(f"Cp_CH4_600K: {Cp_CH4_600K}")
