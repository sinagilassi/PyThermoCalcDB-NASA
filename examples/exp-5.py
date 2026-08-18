# import packages/modules
import os
from rich import print
import pyThermoLinkDB as ptdblink
import pyThermoDB as ptdb
from pythermodb_settings.models import (
    Temperature
)
from pyreactlab_core.models.reaction import Reaction
# locals
from pythermocalcdb_nasa import (
    H_T,
    S_T,
    G_T,
    Cp_T,
    dH_rxn_STD,
    dS_rxn_STD,
    dG_rxn_STD,
    Keq
)
# ! model source
from examples.model_source.model_source_1 import (
    CH4,
    CO2,
    H2O,
    CO,
    H2,
    model_source
)


import logging
logging.getLogger().setLevel(logging.ERROR)  # Only show errors and above

# check version
print(ptdblink.__version__)
print(ptdb.__version__)


# current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"current dir: {current_dir}")


# =======================================
# 🌍 REACTIONS
# =======================================
# SECTION: reaction
reaction = Reaction(
    name='Water-Gas Shift Reaction',
    reaction='CO(g) + H2O(g) => CO2(g) + H2(g)',
    components=[CO, H2O, CO2, H2]
)

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
)
print(f"H_CO2_300K: {H_CO2_300K}")

# NOTE: entropy of CH4 at 400 K
S_CH4_400K = S_T(
    component=CH4,
    temperature=Temperature(
        value=400.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"S_CH4_400K: {S_CH4_400K}")

# NOTE: Gibbs free energy of CO2 at 500 K
G_CO2_500K = G_T(
    component=CO2,
    temperature=Temperature(
        value=500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"G_CO2_500K: {G_CO2_500K}")

# NOTE: heat capacity of CH4 at 600 K
Cp_CH4_600K = Cp_T(
    component=CH4,
    temperature=Temperature(
        value=600.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"Cp_CH4_600K: {Cp_CH4_600K}")


# SECTION: reaction properties
# enthalpy change of reaction at standard conditions
dH_rxn_STD_WGS = dH_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit='K'),
    model_source=model_source,
    mode="log",
)
print(f"dH_rxn_STD_WGS: {dH_rxn_STD_WGS}")

# entropy change of reaction at standard conditions
dS_rxn_STD_WGS = dS_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit='K'),
    model_source=model_source,
    mode="log",
)
print(f"dS_rxn_STD_WGS: {dS_rxn_STD_WGS}")

# Gibbs free energy change of reaction at standard conditions
dG_rxn_STD_WGS = dG_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit='K'),
    model_source=model_source,
    mode="log",
)
print(f"dG_rxn_STD_WGS: {dG_rxn_STD_WGS}")

# Equilibrium constant of reaction at standard conditions
Keq_WGS = Keq(
    reaction=reaction,
    temperature=Temperature(value=1000, unit='K'),
    model_source=model_source,
    mode="log",
)
print(f"Keq_WGS: {Keq_WGS}")
