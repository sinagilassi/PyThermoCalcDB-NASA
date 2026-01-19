# 📂 Examples

Run any script from the project root, e.g. `python examples/exp-2.py`. The `examples/thermodb` directory already includes NASA pickles referenced by the scripts.

## 🧱 Load ThermoDB sources (`examples/exp-1.py`)

- Builds a `ModelSource` from CO₂ and CH₄ pickles using `load_and_build_model_source`.
- Prints the underlying NASA-9 segments (`200–1000 K`, `1000–6000 K`) to verify coefficients and labels.

## 🌡️ Species property evaluation (`examples/exp-2.py`)

- Loads CO₂ and CH₄ sources, then evaluates `H_T`, `S_T`, `G_T`, and `Cp_T` at several temperatures.
- Demonstrates both `"molar"` and `"mass"` bases plus optional logging via `mode="log"`.

## ⚖️ Reaction thermodynamics (`examples/exp-3.py`)

- Adds CO, H₂O, and H₂ sources and defines the water-gas shift reaction.
- Calculates `ΔH°(T)`, `ΔS°(T)`, `ΔG°(T)`, and `Keq(T)` using the high-level helpers.

## 🛠️ Build NASA pickles (`examples/build-thermodb.py`)

- Filters a NASA reference dataset and builds component ThermoDB pickles for a curated list of species.
- Uses `build_component_thermodb_from_reference_source` with `ignore_state_props` for NASA ranges, saving into `examples/thermodb`.

## 🔍 Filter reference content (`examples/filter_reference-thermodb.py`)

- Extracts a subset of species from `reference_content.yaml` into `reference_content_filtered.yaml`.
- Helps keep `build-thermodb.py` focused on the species needed by the examples and tests.

## 📦 Reference assets

- `reference_content.yaml` / `reference_content_filtered.yaml`: NASA reference data snapshots.
- `reference_content_nasa.py` / `_filtered.py`: Python equivalents used by the build scripts.
- Generated ThermoDB pickles live under `examples/thermodb` and are consumed directly by the calculation examples.
