# PyThermoCalcDB-NASA Agent Guide

This guide is based only on `examples/exp-4.py` and the model source it imports from `examples/model_source/model_source_2.py`.

`exp-4.py` does not build a `ModelSource` directly. It imports components and `model_source` from `model_source_2.py`. That module builds `model_source` from `examples.references.reference_3_1.REFERENCE_CONTENT`, an inline reference string containing a `NASA9-1` table.

## exp-4.py Pattern

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

After importing those objects, `exp-4.py` creates a reaction and passes the same `model_source` into every calculation:

```python
reaction = Reaction(
    name="Water-Gas Shift Reaction",
    reaction="CO(g) + H2O(g) => CO2(g) + H2(g)",
    components=[CO, H2O, CO2, H2],
)
```

## Build ModelSource From REFERENCE_CONTENT

This is the setup done in `examples/model_source/model_source_2.py`.

```python
from typing import List

from examples.references.reference_3_1 import REFERENCE_CONTENT
from pyThermoDB import ComponentThermoDB, build_component_thermodb_from_reference
from pyThermoLinkDB import build_components_model_source, build_model_source
from pyThermoLinkDB.models import ComponentModelSource, ModelSource
from pythermodb_settings.models import Component

CO2 = Component(name="carbon dioxide", formula="CO2", state="g")
H2O = Component(name="dihydrogen monoxide", formula="H2O", state="g")
CO = Component(name="carbon monoxide", formula="CO", state="g")
H2 = Component(name="dihydrogen", formula="H2", state="g")
CH4 = Component(name="methane", formula="CH4", state="g")

components: List[Component] = [CH4, CO2, H2O, CO, H2]

thermodb_components: List[ComponentThermoDB] = []

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

component_model_source: List[ComponentModelSource] = build_components_model_source(
    components_thermodb=thermodb_components,
    rules=None,
)

model_source: ModelSource = build_model_source(
    source=component_model_source,
)
```

Required builder arguments:

| Function | Argument | Required | Value in exp-4 workflow |
| --- | --- | --- | --- |
| `build_component_thermodb_from_reference` | `component_name` | Yes | `comp.name` |
| `build_component_thermodb_from_reference` | `component_formula` | Yes | `comp.formula` |
| `build_component_thermodb_from_reference` | `component_state` | Yes | `comp.state` |
| `build_component_thermodb_from_reference` | `reference_content` | Yes | `REFERENCE_CONTENT` string |
| `build_component_thermodb_from_reference` | `check_labels` | No | `False` |
| `build_components_model_source` | `components_thermodb` | Yes | List built in the loop |
| `build_components_model_source` | `rules` | No | `None` |
| `build_model_source` | `source` | Yes | `component_model_source` |

## What REFERENCE_CONTENT Must Contain

For the `exp-4.py` workflow, `REFERENCE_CONTENT` must contain rows for these species:

| Component object | Required row identity in reference |
| --- | --- |
| `CH4` | `Name="methane"`, `Formula="CH4"`, `State="g"` |
| `CO2` | `Name="carbon dioxide"`, `Formula="CO2"`, `State="g"` |
| `H2O` | `Name="dihydrogen monoxide"`, `Formula="H2O"`, `State="g"` |
| `CO` | `Name="carbon monoxide"`, `Formula="CO"`, `State="g"` |
| `H2` | `Name="dihydrogen"`, `Formula="H2"`, `State="g"` |

The relevant table in `reference_3_1.py` is `NASA9-1`. Its `SYMBOL` row maps the data columns to the symbols the calculation layer reads:

```yaml
SYMBOL: [None, None, None, None, None, None, MW, EnFo_IG, Tmin, Tmax, dEnFo_IG_298, a1, a2, a3, a4, a5, a6, a7, b1, b2]
```

The required reference columns are:

| Column role | Required for build? | Required for calculations? | Notes |
| --- | --- | --- | --- |
| `Name` | Yes | Indirectly | Used to find the component row. Must match `Component.name`. |
| `Formula` | Yes | Indirectly | Used to find the component row and reaction species. Must match `Component.formula`. |
| `State` | Yes | Indirectly | Used to find the component row and reaction species. Must match `Component.state`. |
| `MW` | Recommended | Only for `basis="mass"` | Molecular weight in `g/mol`. Not needed for default molar calls in `exp-4.py`. |
| `EnFo_IG` | No for current helpers | No | Present in reference data, but `H_T`, `S_T`, `G_T`, `Cp_T`, and reaction helpers do not directly read it. |
| `Tmin` | Recommended | Not directly read | Use it to validate the row's lower temperature limit. `exp-4.py` uses temperatures within 200-1000 K. |
| `Tmax` | Recommended | Not directly read | Use it to validate the row's upper temperature limit. `reference_3_1.py` has `Tmax=1000`. |
| `dEnFo_IG_298` | No for current helpers | No | Present in reference data, but not directly read by the functions used in `exp-4.py`. |
| `a1` to `a7` | Yes | Yes | Required NASA polynomial coefficients. |
| `b1`, `b2` | Yes for NASA9 | Yes for default `nasa_type="nasa9"` | Required NASA9 integration constants/coefficients. |

Important: `reference_3_1.py` only defines `NASA9-1`, which corresponds to 200-1000 K. Keep `exp-4.py` style calculations in that temperature range unless additional reference tables and mapping rules are added.

## How Data Is Read During Calculations

The `model_source` generated by `model_source_2.py` has component data entries such as:

- `CH4-g`
- `CO2-g`
- `H2O-g`
- `CO-g`
- `H2-g`

The calculation helpers create a `Source(model_source=model_source, component_key="Name-Formula")`, then `HSG` extracts symbols from the source.

For the `reference_3_1.py` workflow, the practical coefficient pack for each species is:

```python
{
    "MW": ...,
    "EnFo_IG": ...,
    "Tmin": ...,
    "Tmax": ...,
    "dEnFo_IG_298": ...,
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

Only `a1` through `a7`, `b1`, and `b2` are required for the default molar NASA9 property calculations. `MW` is additionally required when `basis="mass"` is requested.

## Temperature Requirements

Every calculation takes a `Temperature` object:

```python
from pythermodb_settings.models import Temperature

temperature = Temperature(value=300.0, unit="K")
```

In `exp-4.py`, the temperatures are:

| Calculation | Temperature | Reference range needed |
| --- | --- | --- |
| `H_T(CO2)` | `300 K` | `NASA9-1`, 200-1000 K |
| `S_T(CH4)` | `400 K` | `NASA9-1`, 200-1000 K |
| `G_T(CO2)` | `500 K` | `NASA9-1`, 200-1000 K |
| `Cp_T(CH4)` | `600 K` | `NASA9-1`, 200-1000 K |
| `dH_rxn_STD(WGS)` | `398.15 K` | `NASA9-1`, 200-1000 K for CO, H2O, CO2, H2 |
| `dS_rxn_STD(WGS)` | `398.15 K` | `NASA9-1`, 200-1000 K for CO, H2O, CO2, H2 |
| `dG_rxn_STD(WGS)` | `398.15 K` | `NASA9-1`, 200-1000 K for CO, H2O, CO2, H2 |
| `Keq(WGS)` | `1000 K` | `NASA9-1`, 200-1000 K for CO, H2O, CO2, H2 |

## Species Functions

`exp-4.py` uses four species property helpers.

```python
from pythermocalcdb_nasa import H_T, S_T, G_T, Cp_T
```

All four helpers share the same public argument pattern:

```python
result = H_T(
    component=CO2,
    temperature=Temperature(value=300.0, unit="K"),
    model_source=model_source,
)
```

Arguments:

| Argument | Required | Default | Notes |
| --- | --- | --- | --- |
| `component` | Yes | None | Must be one of the components used to build `model_source`. |
| `temperature` | Yes | None | Use `Temperature(value=..., unit="K")` as in `exp-4.py`. |
| `model_source` | Yes | None | Must be built from `REFERENCE_CONTENT`. |
| `component_key` | No | `"Name-Formula"` | Used by `Source`/PyThermoLinkDB to identify component data. |
| `nasa_type` | No | `"nasa9"` | Requires `a1`-`a7`, `b1`, `b2`. |
| `basis` | No | `"molar"` | If set to `"mass"`, `MW` must be available. |
| `mode` | No | wrapper default | Optional timing/logging kwarg, e.g. `mode="log"`. |

Reference data required by function:

| Function | Required symbols for default `basis="molar"`, `nasa_type="nasa9"` | Extra data for `basis="mass"` |
| --- | --- | --- |
| `H_T` | `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `a7`, `b1`, `b2` | `MW` |
| `S_T` | `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `a7`, `b1`, `b2` | `MW` |
| `G_T` | `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `a7`, `b1`, `b2` | `MW` |
| `Cp_T` | `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `a7`, `b1`, `b2` | `MW` |

Examples from `exp-4.py`:

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

## Reaction Functions

`exp-4.py` uses the water-gas shift reaction:

```python
from pyreactlab_core.models.reaction import Reaction

reaction = Reaction(
    name="Water-Gas Shift Reaction",
    reaction="CO(g) + H2O(g) => CO2(g) + H2(g)",
    components=[CO, H2O, CO2, H2],
)
```

Required reaction arguments:

| Argument | Required | Notes |
| --- | --- | --- |
| `name` | Yes | Human-readable label. |
| `reaction` | Yes | Formula/state tokens must match component formulas and states, e.g. `CO(g)`. |
| `components` | Yes | Must include every reactant and product. Each must also be in `model_source`. |

`exp-4.py` calls:

```python
from pythermocalcdb_nasa import dH_rxn_STD, dS_rxn_STD, dG_rxn_STD, Keq
```

Arguments shared by reaction helpers:

| Argument | Required | Default | Notes |
| --- | --- | --- | --- |
| `reaction` | Yes | None | Reaction object. |
| `temperature` | Yes | None | Target temperature. |
| `model_source` | Yes | None | Must contain all reaction species. |
| `component_key` | No | `"Name-Formula"` | Used to identify components in the source. |
| `nasa_type` | No | `"nasa9"` | Requires NASA9 coefficients for every reaction species. |
| `mode` | No | wrapper default | Optional timing/logging kwarg. |

Reference data required by reaction function:

| Function | What it calculates first | Required reference symbols for each reaction component |
| --- | --- | --- |
| `dH_rxn_STD` | Calls enthalpy for CO, H2O, CO2, H2, then applies stoichiometry. | `a1`-`a7`, `b1`, `b2` |
| `dS_rxn_STD` | Calls entropy for CO, H2O, CO2, H2, then applies stoichiometry. | `a1`-`a7`, `b1`, `b2` |
| `dG_rxn_STD` | Calls Gibbs free energy for CO, H2O, CO2, H2, then applies stoichiometry. | `a1`-`a7`, `b1`, `b2` |
| `Keq` | Calls `dG_rxn_STD`, then calculates equilibrium constant. | `a1`-`a7`, `b1`, `b2` for all reaction species |

Examples from `exp-4.py`:

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

## Notes On Other Reference Properties

`REFERENCE_CONTENT` includes `EnFo_IG`, `Tmin`, `Tmax`, and `dEnFo_IG_298` in addition to the NASA coefficients.

For the functions used in `exp-4.py`:

- `EnFo_IG` is loaded into `model_source.data_source`, but the helper functions shown here do not directly request it.
- `dEnFo_IG_298` is loaded, but the helper functions shown here do not directly request it.
- `Tmin` and `Tmax` are loaded, but NASA range selection in the code is based on hardcoded 1000 K and 6000 K breakpoints. Agents should still use `Tmin`/`Tmax` to validate that a requested temperature is covered by the available reference row.
- `MW` is loaded and is needed for mass-basis conversion. The default `exp-4.py` calls use molar basis, so `MW` is not needed for those exact calls but should remain in the reference data.

## Agent Checklist For exp-4.py Style Calls

1. Use `examples.references.reference_3_1.REFERENCE_CONTENT` or an equivalent reference string with the same NASA9 symbols.
2. Ensure each requested component has a matching `Name`, `Formula`, and `State` row.
3. Ensure each row has numeric `a1`, `a2`, `a3`, `a4`, `a5`, `a6`, `a7`, `b1`, and `b2` values.
4. Keep temperatures within the available row range. For `reference_3_1.py`, that means 200-1000 K.
5. Include `MW` when `basis="mass"` may be used.
6. Build `model_source` from `REFERENCE_CONTENT` before calling any calculation function.
7. Pass that same `model_source` to every species and reaction helper.
8. For reaction helpers, verify all reaction components are present in `model_source` and in `Reaction.components`.
9. Check each return value for `None` before using `.value` or `.unit`.
