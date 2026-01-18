# Methods & API

This page captures the core calculation surface. All functions live in `pythermocalcdb_nasa.app` and return `CustomProp` objects from `pythermodb_settings`.

## Common arguments
- `component` / `reaction`: `Component` or `Reaction` objects that carry identifiers.
- `temperature`: `Temperature` with `value` and `unit="K"`.
- `model_source`: built by `pyThermoLinkDB.load_and_build_model_source(...)` using component ThermoDB pickles.
- `nasa_type`: `"nasa7"` or `"nasa9"` (defaults to `"nasa9"`).
- `basis`: `"molar"` or `"mass"` for species properties.
- `component_key`: how components are keyed in your sources (e.g., `"Name-Formula"`).
- `mode` (optional kwarg): `"silent"`, `"log"`, or `"attach"` for timing logs from `measure_time`.

## Species thermodynamic properties
Use the functions below to evaluate NASA polynomials for a single component. The temperature range is selected automatically from the NASA coefficients based on breakpoints.

```python
from pythermocalcdb_nasa import H_T, S_T, G_T, Cp_T

# enthalpy, entropy, Gibbs free energy, and heat capacity
H = H_T(component=CO2, temperature=T300K, model_source=model_source, basis="molar")
S = S_T(component=CO2, temperature=T300K, model_source=model_source, basis="mass")
G = G_T(component=CO2, temperature=T500K, model_source=model_source)
Cp = Cp_T(component=CH4, temperature=T600K, model_source=model_source)
```

Return values include magnitude, units, and provenance metadata from the underlying NASA source. See `examples/exp-2.py` for a complete workflow that loads two pickles and queries properties at several temperatures.

## Reaction thermodynamics and equilibrium
Reaction-level helpers wrap component properties and the reaction stoichiometry from `pyreactlab_core`.

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
Keq_vh = Keq_vh_shortcut(
    reaction=reaction,
    temperature=T1000K,
    model_source=model_source,
    mode="log",
)
```

- `dH_rxn_STD`, `dS_rxn_STD`, `dG_rxn_STD` compute standard-state reaction properties using species NASA data.
- `Keq` derives the equilibrium constant from `ΔG°(T)`.
- `Keq_vh_shortcut` applies the van’t Hoff shortcut using `ΔH°(298 K)` and a reference `Keq_STD`.

The water-gas-shift example in `examples/exp-3.py` shows the full setup, including loading the required component pickles.

## Building a model source
All calculations require a `ModelSource`. The examples build it from local NASA pickles packaged in `examples/thermodb`:

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
