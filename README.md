# 🚀 PyThermoCalcDB-NASA

[![PyPI Downloads](https://static.pepy.tech/badge/pythermocalcdb-nasa/month)](https://pepy.tech/projects/pythermocalcdb-nasa)
![PyPI](https://img.shields.io/pypi/v/pythermocalcdb-nasa)
![Python Version](https://img.shields.io/pypi/pyversions/pythermocalcdb-nasa.svg)
![License](https://img.shields.io/pypi/l/pythermocalcdb-nasa)
[![Download on the App Store](https://img.shields.io/badge/Download_on_the_App_Store-0D0D0D?logo=apple&logoColor=white)](https://apps.apple.com/ca/app/mozithermocalc/id6759209992)

NASA-polynomial thermochemistry for species, reactions, and equilibrium calculations.

---

## 🧭 Overview

PyThermoCalcDB-NASA is a scientific Python library for evaluating NASA-7 and NASA-9 polynomial thermochemistry for ideal-gas species and reactions. It focuses on reference-state consistency while staying decoupled from how data is stored or sourced.

Calculations can also be done on your mobile with the MoziThermoCalc iOS app: [Download on the App Store](https://apps.apple.com/ca/app/mozithermocalc/id6759209992).

---

## ✨ Key Features

- NASA-7 and NASA-9 support with automatic temperature-break selection
- Species properties: `Cp(T)`, `H^0(T)`, `S^0(T)`, `G^0(T)` on molar or mass basis
- Reaction properties: `Delta H^0(T)`, `Delta S^0(T)`, `Delta G^0(T)` plus equilibrium constants `K(T)`
- Van't Hoff shortcut helper (`Keq_vh_shortcut`) using `Delta H^0(298 K)`
- Embedded NASA-9 SQLite database with component availability checks and direct `ModelSource` building
- The same thermochemistry calculations can be done on mobile via the MoziThermoCalc app
- Clean separation of data (PyThermoDB/LinkDB) from the calculation engine
- Returns `CustomProp` objects with units and metadata; optional timing logs via `mode`

---

## 📦 Installation

```bash
pip install pythermocalcdb-nasa
```

Examples rely on helper packages used for model-source and reaction handling:

```bash
pip install pythermodb-settings pythermodb pythermolinkdb pyreactlab-core rich
```

---

## ⚡ Quick start

Build a `ModelSource` from the embedded NASA-9 SQLite database and evaluate properties:

```python
from pythermodb_settings.models import Component, Temperature
from pyreactlab_core.models.reaction import Reaction
from pythermocalcdb_nasa import (
    Cp_T,
    Keq,
    build_model_source_from_database,
    check_component_availability,
)

CO2 = Component(name="carbon dioxide", formula="CO2", state="g")
CO = Component(name="carbon monoxide", formula="CO", state="g")
H2O = Component(name="dihydrogen monoxide", formula="H2O", state="g")
H2 = Component(name="dihydrogen", formula="H2", state="g")
CH4 = Component(name="methane", formula="CH4", state="g")

components = [CH4, CO2, H2O, CO, H2]

availability = check_component_availability(components)
if availability["missing_components"]:
    raise ValueError(f"Missing components: {availability['missing_components']}")

model_source = build_model_source_from_database(
    components=availability["matched_components"],
    temperature=Temperature(value=298.15, unit="K"),
)

# Species property
Cp = Cp_T(
    component=CH4,
    temperature=Temperature(value=600.0, unit="K"),
    model_source=model_source,
    mode="log",  # optional timing log
)
print(Cp)

# Reaction equilibrium
reaction = Reaction(
    name="Water-Gas Shift",
    reaction="CO(g) + H2O(g) => CO2(g) + H2(g)",
    components=[CO, H2O, CO2, H2],
)

Keq_T = Keq(
    reaction=reaction,
    temperature=Temperature(value=1000.0, unit="K"),
    model_source=model_source,
)
print(Keq_T)
```

---

## Build ModelSource From REFERENCE

If you already have NASA reference content, you can still build a `ModelSource`
through PyThermoDB and PyThermoLinkDB. This is the pattern used by
`examples/model_source/model_source_2.py`.

```python
from pyThermoDB import build_component_thermodb_from_reference
from pyThermoLinkDB import build_components_model_source, build_model_source

thermodb_components = []

for comp in components:
    thermodb_component = build_component_thermodb_from_reference(
        component_name=comp.name,
        component_formula=comp.formula,
        component_state=comp.state,
        reference_content=REFERENCE_CONTENT,
        check_labels=False,
    )
    if thermodb_component is None:
        raise ValueError(f"thermodb_component for {comp.name} is None")
    thermodb_components.append(thermodb_component)

component_model_source = build_components_model_source(
    components_thermodb=thermodb_components,
    rules=None,
)

model_source = build_model_source(source=component_model_source)
```

Use this workflow when you need NASA-7 data or a custom reference source. The
embedded SQLite helper currently builds NASA-9 model sources.

---

## Helper functions

Available helpers (all return `CustomProp` or `None`):

- `check_component_availability` - check whether components exist in the embedded NASA-9 database
- `build_reference_content_from_database` - build PyThermoDB-compatible reference content from SQLite rows
- `build_model_source_from_database` - build a ready `ModelSource` from the embedded NASA-9 database
- `H_T`, `S_T`, `G_T`, `Cp_T` - species properties on molar or mass basis
- `dH_rxn_STD`, `dS_rxn_STD`, `dG_rxn_STD` - reaction properties from stoichiometry
- `Keq`, `Keq_vh_shortcut` - equilibrium constants from `Delta G^0(T)` or Van't Hoff

---

## 📚 Examples

Run from the project root, e.g. `python examples/exp-2.py`:

- `examples/exp-1.py` - build `ModelSource` objects and inspect NASA segments
- `examples/exp-2.py` - evaluate `H_T`, `S_T`, `G_T`, and `Cp_T` for CO2/CH4
- `examples/exp-3.py` - water-gas shift reaction properties and `Keq(T)`
- `examples/exp-4.py` - water-gas shift calculations using a reference-built model source
- `examples/exp-6.py` - water-gas shift calculations using a SQLite-built model source
- `examples/model_source/model_source_3.py` - build a SQLite model source for random gas-phase components
- `examples/model_source/model_source_4.py` - build a SQLite model source for specific WGS components
- `examples/build-thermodb.py` - generate ThermoDB pickles from reference data
- `examples/filter_reference-thermodb.py` - subset the reference dataset for examples/tests

---

## 📖 Documentation

Documentation is available at [https://pythermocalcdb-nasa.readthedocs.io/en/latest/](https://pythermocalcdb-nasa.readthedocs.io/en/latest/).

---

## 🤝 Contributing

Contributions are welcome: bug fixes, new calculation routines, expanded examples, unit tests, or documentation improvements.

---

## ⚖️ License

This project is distributed under the Apache License, Version 2.0. If you incorporate this work into your own software, please acknowledge Sina Gilassi as the original author (a repository or documentation reference is appreciated).

---

## ❓ FAQ

Questions? Contact me on [LinkedIn](https://www.linkedin.com/in/sina-gilassi/).

---

## 👤 Authors

- [@sinagilassi](https://www.github.com/sinagilassi)
