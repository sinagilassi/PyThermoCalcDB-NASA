# 📚 Methods & API

Core calculations live in `pythermocalcdb_nasa.app` and return `CustomProp` objects from `pythermodb_settings`.

## 🧩 Common arguments

- `component` / `reaction`: `Component` or `Reaction` identifiers.
- `temperature`: `Temperature(value, unit="K")`.
- `model_source`: built via `pyThermoLinkDB.load_and_build_model_source(...)` from component ThermoDB pickles.
- `nasa_type`: `"nasa7"` or `"nasa9"` (default `"nasa9"`).
- `basis`: `"molar"` or `"mass"` for species properties.
- `component_key`: how components are keyed (e.g., `"Name-Formula"`).
- `mode` (kwarg): `"silent"`, `"log"`, or `"attach"` for timing logs.

## 🔥 Species thermodynamic properties

Use these to evaluate NASA polynomials for a single component. Temperature breakpoints are selected automatically.

| Function | Purpose | Args | Returns |
| --- | --- | --- | --- |
| `H_T` | Absolute enthalpy `H°(T)` | `component`, `temperature`, `model_source`, `basis`, `nasa_type`, `component_key`, `**kwargs` | `CustomProp` (value + unit + metadata) or `None` |
| `S_T` | Absolute entropy `S°(T)` | same as above | `CustomProp` or `None` |
| `G_T` | Gibbs free energy `G°(T)` | same as above | `CustomProp` or `None` |
| `Cp_T` | Heat capacity `Cp(T)` | same as above | `CustomProp` or `None` |

```python
from pythermocalcdb_nasa import H_T, S_T, G_T, Cp_T

H = H_T(component=CO2, temperature=T300K, model_source=model_source, basis="molar")
S = S_T(component=CO2, temperature=T300K, model_source=model_source, basis="mass")
G = G_T(component=CO2, temperature=T500K, model_source=model_source)
Cp = Cp_T(component=CH4, temperature=T600K, model_source=model_source)
```

See `examples/exp-2.py` for a full species workflow.

## ⚖️ Reaction thermodynamics and equilibrium

Helpers wrap species properties plus stoichiometry from `pyreactlab_core`.

| Function | Purpose | Args | Returns |
| --- | --- | --- | --- |
| `dH_rxn_STD` | Reaction enthalpy change `ΔH°(T)` | `reaction`, `temperature`, `model_source`, `nasa_type`, `component_key`, `**kwargs` | `CustomProp` or `None` |
| `dS_rxn_STD` | Reaction entropy change `ΔS°(T)` | same as above | `CustomProp` or `None` |
| `dG_rxn_STD` | Reaction Gibbs free energy `ΔG°(T)` | same as above | `CustomProp` or `None` |
| `Keq` | Equilibrium constant from `ΔG°(T)` | `reaction`, `temperature`, `model_source`, `nasa_type`, `component_key`, `**kwargs` | `CustomProp` or `None` |
| `Keq_vh_shortcut` | van’t Hoff shortcut using `ΔH°(298 K)` | `reaction`, `temperature`, `model_source`, `nasa_type`, `component_key`, `**kwargs` | `CustomProp` or `None` |

```python
from pythermocalcdb_nasa import dH_rxn_STD, dS_rxn_STD, dG_rxn_STD, Keq, Keq_vh_shortcut
from pyreactlab_core.models.reaction import Reaction

reaction = Reaction(
    name="Water-Gas Shift",
    reaction="CO(g) + H2O(g) => CO2(g) + H2(g)",
    components=[CO, H2O, CO2, H2],
)

dH = dH_rxn_STD(reaction=reaction, temperature=T398K, model_source=model_source)
dS = dS_rxn_STD(reaction=reaction, temperature=T398K, model_source=model_source)
dG = dG_rxn_STD(reaction=reaction, temperature=T398K, model_source=model_source)

Keq_T = Keq(reaction=reaction, temperature=T1000K, model_source=model_source)
Keq_vh = Keq_vh_shortcut(reaction=reaction, temperature=T1000K, model_source=model_source, mode="log")
```

`examples/exp-3.py` shows the full reaction workflow.

## 🏗️ Building a model source

All calculations require a `ModelSource`. The examples build it from NASA pickles packaged in `examples/thermodb`:

```python
from pythermodb_settings.models import Component, ComponentThermoDBSource
from pyThermoLinkDB import load_and_build_model_source

CO2 = Component(name="carbon dioxide", formula="CO2", state="g")
CO2_src = ComponentThermoDBSource(component=CO2, source="examples/thermodb/carbon dioxide-CO2-g-nasa-1.pkl")

model_source = load_and_build_model_source(
    thermodb_sources=[CO2_src],
    original_equation_label=False,  # normalize NASA labels
)
```

For generating new NASA pickles from a reference YAML, see `examples/build-thermodb.py`.
