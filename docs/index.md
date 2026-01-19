# PyThermoCalcDB-NASA

NASA-polynomial thermochemistry for species, reactions, and equilibrium calculations.

## 🚀 What this library does

- Computes NASA-7/9 ideal-gas properties: `Cp(T)`, `H°(T)`, `S°(T)`, `G°(T)`
- Evaluates reaction thermodynamics and equilibrium constants
- Works with PyThermoDB/LinkDB data sources while keeping calculation logic separate from data storage
- Ships runnable examples and ready-to-use NASA pickles under `examples/thermodb`

## ⚡ Quick start

```bash
pip install pythermocalcdb-nasa
# examples rely on extra deps:
pip install pythermodb-settings pythermodb pythermolinkdb pyreactlab-core rich
```

```python
from pythermodb_settings.models import Component, ComponentThermoDBSource, Temperature
from pyThermoLinkDB import load_and_build_model_source
from pythermocalcdb_nasa import Cp_T

thermodb = ComponentThermoDBSource(
    component=Component(name="methane", formula="CH4", state="g"),
    source="examples/thermodb/methane-CH4-g-nasa-1.pkl",
)
model_source = load_and_build_model_source(
    thermodb_sources=[thermodb],
    original_equation_label=False,
)

Cp = Cp_T(
    component=thermodb.component,
    temperature=Temperature(value=600.0, unit="K"),
    model_source=model_source,
    mode="log",
)
print(Cp)  # CustomProp with value, unit, metadata
```

## 🧭 Documentation map

- Overview & quick start (this page)
- Methods & API: per-function guidance for species and reaction calculations
- Examples: how to run each script under `examples/`

## 🛠️ Build the docs locally

```bash
pip install -r docs/requirements.txt
mkdocs serve   # live preview at http://127.0.0.1:8000
mkdocs build   # outputs site/ for Read the Docs
```
