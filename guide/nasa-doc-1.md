# PyThermoCalcDB-NASA Agent Guide

This guide documents the current example patterns for building a `ModelSource`
and using it with the NASA property and reaction helpers.

There are now two supported source-building workflows:

1. `examples/exp-4.py` imports a `ModelSource` built from inline
   `REFERENCE_CONTENT` in `examples/model_source/model_source_2.py`.
2. `examples/exp-6.py` imports a `ModelSource` built from the embedded NASA-9
   SQLite database in `examples/model_source/model_source_4.py`.

Prefer the SQLite workflow for new examples, because users can check component
availability and build a model source without maintaining hand-written
reference strings.

## SQLite Database Workflow

The database-backed workflow is implemented by these public helpers:

```python
from pythermocalcdb_nasa import (
    check_component_availability,
    build_reference_content_from_database,
    build_model_source_from_database,
)
```

### Build ModelSource From Database

This is the setup used in `examples/model_source/model_source_4.py`.

```python
from typing import List

from pyThermoLinkDB.models import ModelSource
from pythermodb_settings.models import Component, Temperature

from pythermocalcdb_nasa import (
    build_model_source_from_database,
    check_component_availability,
)

CO2 = Component(name="carbon dioxide", formula="CO2", state="g")
H2O = Component(name="dihydrogen monoxide", formula="H2O", state="g")
CO = Component(name="carbon monoxide", formula="CO", state="g")
H2 = Component(name="dihydrogen", formula="H2", state="g")
CH4 = Component(name="methane", formula="CH4", state="g")

components: List[Component] = [CH4, CO2, H2O, CO, H2]

availability_results = check_component_availability(components=components)

if availability_results["missing_components"]:
    raise ValueError(
        "Some components are missing from the NASA-9 database: "
        f"{availability_results['missing_components']}"
    )

model_source: ModelSource = build_model_source_from_database(
    components=availability_results["matched_components"],
    temperature=Temperature(value=298.15, unit="K"),
)

datasource = model_source.data_source
equationsource = model_source.equation_source
```

`build_model_source_from_database(...)` performs the same underlying model
source construction as the reference-string workflow:

1. read component rows from `pythermocalcdb_nasa/database/nasa9_all_phases.sqlite`;
2. build NASA-9 reference content from those rows;
3. build `ComponentThermoDB` objects from the generated reference content;
4. build and return a `pyThermoLinkDB.models.ModelSource`.

The returned `model_source` can be passed directly to `H_T`, `S_T`, `G_T`,
`Cp_T`, `dH_rxn_STD`, `dS_rxn_STD`, `dG_rxn_STD`, `Keq`, and
`Keq_vh_shortcut`.

### Database Helper Arguments

| Function | Argument | Required | Notes |
| --- | --- | --- | --- |
| `check_component_availability` | `components` | Yes | A `Component` or list of `Component` objects. |
| `check_component_availability` | `phase` | No | If omitted, each component's `state` is used when it is `g`, `l`, or `s`. |
| `build_reference_content_from_database` | `components` | Yes | List of `Component` objects. |
| `build_reference_content_from_database` | `temperature` | Yes | `Temperature(value=..., unit="K")` or numeric Kelvin value. |
| `build_model_source_from_database` | `components` | Yes | List of available components. |
| `build_model_source_from_database` | `temperature` | Yes | Used to select the database NASA-9 coefficient range. |
| `build_model_source_from_database` | `rules` | No | Optional PyThermoLinkDB source rules. |

The embedded database supports `g`, `l`, and `s` phases. Aqueous (`aq`)
components are not supported by the current NASA-9 database reader.

The database reader checks by component name and also falls back to formula
matching. This allows a component such as:

```python
Component(name="water", formula="H2O", state="g")
```

to match the database row stored as:

```python
Component(name="dihydrogen monoxide", formula="H2O", state="g")
```

## exp-6.py Pattern

`examples/exp-6.py` mirrors `examples/exp-4.py`, but imports from
`examples/model_source/model_source_4.py`, which builds its source from SQLite:

```python
from examples.model_source.model_source_4 import (
    CH4,
    CO2,
    H2O,
    CO,
    H2,
    model_source,
)
```

After importing those objects, `exp-6.py` creates the water-gas shift reaction:

```python
reaction = Reaction(
    name="Water-Gas Shift Reaction",
    reaction="CO(g) + H2O(g) => CO2(g) + H2(g)",
    components=[CO, H2O, CO2, H2],
)
```

Then it passes the same database-built `model_source` into every calculation:

```python
H_CO2_300K = H_T(
    component=CO2,
    temperature=Temperature(value=300.0, unit="K"),
    model_source=model_source,
)

S_CH4_400K = S_T(
    component=CH4,
    temperature=Temperature(value=400.0, unit="K"),
    model_source=model_source,
)

G_CO2_500K = G_T(
    component=CO2,
    temperature=Temperature(value=500.0, unit="K"),
    model_source=model_source,
)

Cp_CH4_600K = Cp_T(
    component=CH4,
    temperature=Temperature(value=600.0, unit="K"),
    model_source=model_source,
)
```

Reaction calls use the same pattern:

```python
dH_rxn_STD_WGS = dH_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit="K"),
    model_source=model_source,
    mode="log",
)

dS_rxn_STD_WGS = dS_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit="K"),
    model_source=model_source,
    mode="log",
)

dG_rxn_STD_WGS = dG_rxn_STD(
    reaction=reaction,
    temperature=Temperature(value=398.15, unit="K"),
    model_source=model_source,
    mode="log",
)

Keq_WGS = Keq(
    reaction=reaction,
    temperature=Temperature(value=1000.0, unit="K"),
    model_source=model_source,
    mode="log",
)
```

## Temperature Requirements

Every calculation takes a `Temperature` object:

```python
from pythermodb_settings.models import Temperature

temperature = Temperature(value=300.0, unit="K")
```

The current database builder selects one NASA-9 row per component using the
temperature passed to `build_model_source_from_database(...)`. The source can
then be used safely for calculations inside that selected row's range.

For `exp-6.py`, `model_source_4.py` builds at `298.15 K`, which selects the
`nasa9_200_1000_K` data range. The example calculations are therefore kept in
the 200-1000 K range:

| Calculation | Temperature | Database range needed |
| --- | --- | --- |
| `H_T(CO2)` | `300 K` | `nasa9_200_1000_K` |
| `S_T(CH4)` | `400 K` | `nasa9_200_1000_K` |
| `G_T(CO2)` | `500 K` | `nasa9_200_1000_K` |
| `Cp_T(CH4)` | `600 K` | `nasa9_200_1000_K` |
| `dH_rxn_STD(WGS)` | `398.15 K` | `nasa9_200_1000_K` for CO, H2O, CO2, H2 |
| `dS_rxn_STD(WGS)` | `398.15 K` | `nasa9_200_1000_K` for CO, H2O, CO2, H2 |
| `dG_rxn_STD(WGS)` | `398.15 K` | `nasa9_200_1000_K` for CO, H2O, CO2, H2 |
| `Keq(WGS)` | `1000 K` | `nasa9_200_1000_K` for CO, H2O, CO2, H2 |

The NASA range selector treats `1000 K` as part of the low range:

```python
T <= 1000 K -> nasa9_200_1000_K
1000 K < T <= 6000 K -> nasa9_1000_6000_K
T > 6000 K -> nasa9_6000_20000_K
```

If a calculation temperature is above `1000 K`, build a model source using a
temperature in the needed range, for example `Temperature(value=1500.0, unit="K")`.

## Build ModelSource From REFERENCE

`examples/exp-4.py` still demonstrates the older reference-string pattern. It
does not build a `ModelSource` directly. It imports components and
`model_source` from `examples/model_source/model_source_2.py`:

```python
from examples.model_source.model_source_2 import (
    CH4,
    CO2,
    H2O,
    CO,
    H2,
    model_source,
)
```

`model_source_2.py` builds `model_source` from
`examples.references.reference_3_1.REFERENCE_CONTENT`, an inline reference
string containing a `NASA9-1` table. Use this workflow only when an inline or
external reference string is the desired data source.

In this workflow, `REFERENCE_CONTENT` is the complete NASA reference source.
It must contain component rows with the same `Name`, `Formula`, and `State`
used by the `Component` objects, plus the NASA-9 symbols required by the
calculation layer.

The required builder sequence is:

```python
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

## Required NASA-9 Data

Both workflows ultimately produce the same symbol pack in `model_source`.

For default molar NASA-9 calculations, each component needs:

```python
{
    "a1": ...,
    "a2": ...,
    "a3": ...,
    "a4": ...,
    "a5": ...,
    "a6": ...,
    "a7": ...,
    "b1": ...,
    "b2": ...,
}
```

`MW` is additionally required when `basis="mass"` is requested. The database
and generated reference content also carry values such as `EnFo_IG`, `Tmin`,
`Tmax`, and `dEnFo_IG_298`.

## Required NASA-7 Data

NASA-7 calculations use the same model-source structure, but each selected
NASA-7 range needs only seven polynomial coefficients:

```python
{
    "a1": ...,
    "a2": ...,
    "a3": ...,
    "a4": ...,
    "a5": ...,
    "a6": ...,
    "a7": ...,
}
```

For default molar NASA-7 calculations, `H_T`, `S_T`, `G_T`, `Cp_T`, and the
reaction helpers require `a1` through `a7` for every requested component.

`MW` is additionally required when `basis="mass"` is requested. `b1` and `b2`
are NASA-9-specific and are not required for `nasa_type="nasa7"`.

NASA-7 range labels follow the same temperature break structure:

| Range label | Temperature coverage |
| --- | --- |
| `nasa7_200_1000_K` | `T <= 1000 K` |
| `nasa7_1000_6000_K` | `1000 K < T <= 6000 K` |
| `nasa7_6000_20000_K` | `T > 6000 K` |

The embedded SQLite workflow currently builds NASA-9 reference content. Use
the reference-string workflow when supplying NASA-7 data.

## Species Functions

`H_T`, `S_T`, `G_T`, and `Cp_T` share the same public argument pattern:

```python
result = H_T(
    component=CO2,
    temperature=Temperature(value=300.0, unit="K"),
    model_source=model_source,
)
```

| Argument | Required | Default | Notes |
| --- | --- | --- | --- |
| `component` | Yes | None | Must be included in `model_source`. |
| `temperature` | Yes | None | Use a `Temperature` object. |
| `model_source` | Yes | None | Built from SQLite or reference content. |
| `component_key` | No | `"Name-Formula"` | Used by `Source`/PyThermoLinkDB to identify component data. |
| `nasa_type` | No | `"nasa9"` | Use `"nasa9"` for NASA-9 coefficients or `"nasa7"` for NASA-7 coefficients. |
| `basis` | No | `"molar"` | If set to `"mass"`, `MW` must be available. |
| `mode` | No | wrapper default | Optional timing/logging kwarg, e.g. `mode="log"`. |

## Reaction Functions

Reaction helpers require all reaction species to exist in the same
`model_source`:

```python
from pyreactlab_core.models.reaction import Reaction

reaction = Reaction(
    name="Water-Gas Shift Reaction",
    reaction="CO(g) + H2O(g) => CO2(g) + H2(g)",
    components=[CO, H2O, CO2, H2],
)
```

The reaction string uses formula/state tokens like `CO(g)` and `H2O(g)`.
Those formulas and states must match the `Component` objects.

| Function | What it calculates first | Required symbols for each reaction component |
| --- | --- | --- |
| `dH_rxn_STD` | Calls enthalpy for each component, then applies stoichiometry. | `a1`-`a7`, `b1`, `b2` |
| `dS_rxn_STD` | Calls entropy for each component, then applies stoichiometry. | `a1`-`a7`, `b1`, `b2` |
| `dG_rxn_STD` | Calls Gibbs free energy for each component, then applies stoichiometry. | `a1`-`a7`, `b1`, `b2` |
| `Keq` | Calls `dG_rxn_STD`, then calculates equilibrium constant. | `a1`-`a7`, `b1`, `b2` |

## Agent Checklist

1. Prefer `build_model_source_from_database(...)` for new examples.
2. Define `Component` objects with correct `name`, `formula`, and `state`.
3. Use `check_component_availability(...)` before building the source.
4. Build the source at a temperature in the range needed by the calculations.
5. Keep all property and reaction calls inside the selected NASA row range.
6. Pass the same `model_source` to all species and reaction helpers.
7. For reactions, include every reactant and product in `Reaction.components`.
8. Check each helper return value for `None` before using `.value` or `.unit`.
