# PyThermoCalcDB-NASA

**NASA-polynomial thermochemistry for species, reactions, and equilibrium calculations**

---

## Overview

**PyThermoCalcDB-NASA** is a scientific Python library for computing temperature-dependent thermodynamic properties of chemical species and chemical reactions using **NASA polynomial formulations (NASA-7 and NASA-9)**.

The package provides a reliable and reference-state-consistent calculation engine for:

- Ideal-gas heat capacity, enthalpy, entropy, and Gibbs free energy
- Reaction thermodynamics (ΔH°, ΔS°, ΔG°)
- Chemical equilibrium constants as a function of temperature

It is designed to integrate seamlessly with **PyThermoDB** for data access and with higher-level process modeling tools such as **PyThermoCalcDB** and **PyChemBalance**.

---

## Key Features

- NASA-7 and NASA-9 polynomial support
- Species thermodynamic properties:
  - \( C_p(T) \)
  - \( H^\circ(T) \)
  - \( S^\circ(T) \)
  - \( G^\circ(T) \)
- Reaction thermodynamics:
  - \( \Delta H^\circ(T) \)
  - \( \Delta S^\circ(T) \)
  - \( \Delta G^\circ(T) \)
- Equilibrium constant calculation:
  - \( K(T) = \exp(-\Delta G^\circ / RT) \)
- Strict reference-state consistency (ideal-gas standard state)
- Modular design with clean separation of **data** and **calculation**
- Suitable for chemical engineering, combustion, and reaction-equilibrium studies

---

## Package Philosophy

PyThermoCalcDB-NASA follows three core principles:

1. **Data ≠ Calculation**
   - Thermodynamic data is supplied by **PyThermoDB**
   - This package performs only calculations

2. **Reference-State Correctness**
   - All properties are computed relative to a clearly defined standard state
   - Reaction properties are derived rigorously from species properties

3. **Composable Design**
   - Designed to be embedded in balance solvers, equilibrium tools, and reactors
   - No hard coupling to a specific workflow

---

## Installation

```bash
pip install pythermocalcdb-nasa
```
## 🚀 Usage


## 🤝 Contributing

Contributions are highly welcome — bug fixes, new calculation routines, mixture models, extended unit tests, documentation, etc.

## 📝 License

This project is distributed under the Apache License, Version 2.0, which grants you broad freedom to use, modify, and integrate the software into your own applications or projects, provided that you comply with the conditions outlined in the license. Although Apache 2.0 does not require users to retain explicit author credit beyond standard copyright and license notices, I kindly request that if you incorporate this work into your own software, you acknowledge Sina Gilassi as the original author. Referencing the original repository or documentation is appreciated, as it helps recognize the effort invested in developing and maintaining this project.

## ❓ FAQ

For any question, contact me on [LinkedIn](https://www.linkedin.com/in/sina-gilassi/)

## 👨‍💻 Authors

- [@sinagilassi](https://www.github.com/sinagilassi)