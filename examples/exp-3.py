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

# Initialize summary results list
summary_results = []
summary_results.append(f"pyThermoLinkDB version: {ptdblink.__version__}")
summary_results.append(f"pyThermoDB version: {ptdb.__version__}")
summary_results.append(f"Current directory: {current_dir}")
summary_results.append("")

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

# water gas thermodb
H2O_thermodb_file = os.path.join(
    current_dir,
    'thermodb',
    'dihydrogen monoxide-H2O-g-nasa-1.pkl'
)

# water gas component
H2O = Component(
    name='dihydrogen monoxide',
    formula='H2O',
    state='g'
)

# CO gas thermodb
CO_thermodb_file = os.path.join(
    current_dir,
    'thermodb',
    'carbon monoxide-CO-g-nasa-1.pkl'
)

# carbon monoxide gas component
CO = Component(
    name='carbon monoxide',
    formula='CO',
    state='g'
)

# H2 gas component
H2_thermodb_file = os.path.join(
    current_dir,
    'thermodb',
    'dihydrogen-H2-g-nasa-1.pkl'
)

H2 = Component(
    name='dihydrogen',
    formula='H2',
    state='g'
)

# SECTION: reaction
reaction = Reaction(
    name='Water-Gas Shift Reaction',
    reaction='CO(g) + H2O(g) => CO2(g) + H2(g)',
    components=[CO, H2O, CO2, H2]
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

CO_thermodb: ComponentThermoDBSource = ComponentThermoDBSource(
    component=CO,
    source=CO_thermodb_file
)

H2O_thermodb: ComponentThermoDBSource = ComponentThermoDBSource(
    component=H2O,
    source=H2O_thermodb_file
)

H2_thermodb: ComponentThermoDBSource = ComponentThermoDBSource(
    component=H2,
    source=H2_thermodb_file
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
        CH4_thermodb,
        CO_thermodb,
        H2O_thermodb,
        H2_thermodb
    ],
    original_equation_label=False
)
print(model_source)

# get data source and equation source
datasource = model_source.data_source
equationsource = model_source.equation_source

summary_results.append("=" * 40)
summary_results.append("MODEL SOURCE")
summary_results.append("=" * 40)
# summary_results.append(str(model_source))
summary_results.append("")

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

summary_results.append("=" * 40)
summary_results.append("TEST RESULTS - Individual Components")
summary_results.append("=" * 40)
summary_results.append(f"H_CO2_300K: {H_CO2_300K}")
summary_results.append(f"S_CH4_400K: {S_CH4_400K}")

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

summary_results.append(f"G_CO2_500K: {G_CO2_500K}")
summary_results.append(f"Cp_CH4_600K: {Cp_CH4_600K}")
summary_results.append("")

# =======================================
# NOTE: Dihydrogen (H2) properties
# =======================================
# enthalpy
H_H2 = H_T(
    component=H2,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"H_H2: {H_H2}")

# entropy
S_H2 = S_T(
    component=H2,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"S_H2: {S_H2}")

# Gibbs free energy
G_H2 = G_T(
    component=H2,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"G_H2: {G_H2}")

# heat capacity
Cp_H2 = Cp_T(
    component=H2,
    temperature=Temperature(
        value=298.15,
        unit='K'
    ),
    model_source=model_source
)
print(f"Cp_H2: {Cp_H2}")

Cp_H2 = Cp_T(
    component=H2,
    temperature=Temperature(
        value=298.15,
        unit='K'
    ),
    model_source=model_source,
    basis='mass'
)
print(f"Cp_H2: {Cp_H2}")

summary_results.append("\n" + "=" * 40)
summary_results.append("H2 (Dihydrogen) Properties at 1500K")
summary_results.append("=" * 40)
summary_results.append(f"H_H2: {H_H2}")
summary_results.append(f"S_H2: {S_H2}")
summary_results.append(f"G_H2: {G_H2}")
summary_results.append(f"Cp_H2 (molar, 298.15K): {Cp_H2}")

# =======================================
# NOTE: CH4 properties
# =======================================
# enthalpy
H_CH4 = H_T(
    component=CH4,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"H_CH4: {H_CH4}")

# entropy
S_CH4 = S_T(
    component=CH4,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"S_CH4: {S_CH4}")

# Gibbs free energy
G_CH4 = G_T(
    component=CH4,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"G_CH4: {G_CH4}")

# heat capacity
Cp_CH4 = Cp_T(
    component=CH4,
    temperature=Temperature(
        value=298.15,
        unit='K'
    ),
    model_source=model_source
)
print(f"Cp_CH4: {Cp_CH4}")

# mass basis
Cp_CH4 = Cp_T(
    component=CH4,
    temperature=Temperature(
        value=298.15,
        unit='K'
    ),
    model_source=model_source,
    basis='mass'
)
print(f"Cp_CH4: {Cp_CH4}")

summary_results.append("\n" + "=" * 40)
summary_results.append("CH4 (Methane) Properties at 1500K")
summary_results.append("=" * 40)
summary_results.append(f"H_CH4: {H_CH4}")
summary_results.append(f"S_CH4: {S_CH4}")
summary_results.append(f"G_CH4: {G_CH4}")
summary_results.append(f"Cp_CH4 (molar, 298.15K): {Cp_CH4}")

# =======================================
# NOTE: H2O properties
# =======================================
# enthalpy
H_H2O = H_T(
    component=H2O,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"H_H2O: {H_H2O}")

# entropy
S_H2O = S_T(
    component=H2O,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"S_H2O: {S_H2O}")

# Gibbs free energy
G_H2O = G_T(
    component=H2O,
    temperature=Temperature(
        value=1500.0,
        unit='K'
    ),
    model_source=model_source
)
print(f"G_H2O: {G_H2O}")

# heat capacity
Cp_H2O = Cp_T(
    component=H2O,
    temperature=Temperature(
        value=298.15,
        unit='K'
    ),
    model_source=model_source
)
print(f"Cp_H2O: {Cp_H2O}")

# mass basis
Cp_H2O = Cp_T(
    component=H2O,
    temperature=Temperature(
        value=298.15,
        unit='K'
    ),
    model_source=model_source,
    basis='mass'
)
print(f"Cp_H2O: {Cp_H2O}")

summary_results.append("\n" + "=" * 40)
summary_results.append("H2O (Water) Properties at 1500K")
summary_results.append("=" * 40)
summary_results.append(f"H_H2O: {H_H2O}")
summary_results.append(f"S_H2O: {S_H2O}")
summary_results.append(f"G_H2O: {G_H2O}")
summary_results.append(f"Cp_H2O (molar, 298.15K): {Cp_H2O}")

# =======================================
# SECTION: reaction properties
# =======================================
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

summary_results.append("\n" + "=" * 40)
summary_results.append("REACTION PROPERTIES")
summary_results.append("Reaction: CO(g) + H2O(g) => CO2(g) + H2(g)")
summary_results.append("=" * 40)
summary_results.append(f"dH_rxn_STD (398.15K): {dH_rxn_STD_WGS}")
summary_results.append(f"dS_rxn_STD (398.15K): {dS_rxn_STD_WGS}")
summary_results.append(f"dG_rxn_STD (398.15K): {dG_rxn_STD_WGS}")

# Equilibrium constant of reaction at standard conditions
Keq_WGS = Keq(
    reaction=reaction,
    temperature=Temperature(value=400, unit='K'),
    model_source=model_source,
    mode="log",
)
print(f"Keq_WGS: {Keq_WGS}")

summary_results.append(f"Keq (400K): {Keq_WGS}")
summary_results.append("")

# =======================================
# SECTION: Save summary to file
# =======================================
# Write all results to summary.txt
summary_file_path = os.path.join(current_dir, 'summary.txt')
with open(summary_file_path, 'w') as f:
    f.write('\n'.join(summary_results))

print(f"\n✅ Summary saved to: {summary_file_path}")
