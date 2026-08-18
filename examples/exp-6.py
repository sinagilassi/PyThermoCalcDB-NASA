# import packages/modules
import os
import sys
import logging

from rich import print
import pyThermoLinkDB as ptdblink
import pyThermoDB as ptdb
from pythermodb_settings.models import Temperature
from pyreactlab_core.models.reaction import Reaction

from pythermocalcdb_nasa import (
    H_T,
    S_T,
    G_T,
    Cp_T,
    dH_rxn_STD,
    dS_rxn_STD,
    dG_rxn_STD,
    Keq,
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from examples.model_source.model_source_4 import (
    CH4,
    CO2,
    H2O,
    CO,
    H2,
    model_source,
)


logging.getLogger().setLevel(logging.ERROR)

print(ptdblink.__version__)
print(ptdb.__version__)


current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"current dir: {current_dir}")


# =======================================
# REACTIONS
# =======================================

reaction = Reaction(
    name="Water-Gas Shift Reaction",
    reaction="CO(g) + H2O(g) => CO2(g) + H2(g)",
    components=[CO, H2O, CO2, H2],
)


# =======================================
# TEST
# =======================================

temperature = Temperature(
    value=300.0,
    unit="K",
)

H_CO2_300K = H_T(
    component=CO2,
    temperature=temperature,
    model_source=model_source,
)
print(f"H_CO2_300K: {H_CO2_300K}")

S_CH4_400K = S_T(
    component=CH4,
    temperature=Temperature(
        value=400.0,
        unit="K",
    ),
    model_source=model_source,
)
print(f"S_CH4_400K: {S_CH4_400K}")

G_CO2_500K = G_T(
    component=CO2,
    temperature=Temperature(
        value=500.0,
        unit="K",
    ),
    model_source=model_source,
)
print(f"G_CO2_500K: {G_CO2_500K}")

Cp_CH4_600K = Cp_T(
    component=CH4,
    temperature=Temperature(
        value=600.0,
        unit="K",
    ),
    model_source=model_source,
)
print(f"Cp_CH4_600K: {Cp_CH4_600K}")


# SECTION: reaction properties

dH_rxn_STD_WGS = dH_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit="K"),
    model_source=model_source,
    mode="log",
)
print(f"dH_rxn_STD_WGS: {dH_rxn_STD_WGS}")

dS_rxn_STD_WGS = dS_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit="K"),
    model_source=model_source,
    mode="log",
)
print(f"dS_rxn_STD_WGS: {dS_rxn_STD_WGS}")

dG_rxn_STD_WGS = dG_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit="K"),
    model_source=model_source,
    mode="log",
)
print(f"dG_rxn_STD_WGS: {dG_rxn_STD_WGS}")

Keq_WGS = Keq(
    reaction=reaction,
    temperature=Temperature(value=1000, unit="K"),
    model_source=model_source,
    mode="log",
)
print(f"Keq_WGS: {Keq_WGS}")
