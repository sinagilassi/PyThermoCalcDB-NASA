from pythermocalcdb_nasa import (
    H_T,
    build_model_source_from_database,
    check_component_availability,
)
from pythermodb_settings.models import Component, Temperature


def test_build_model_source_from_database_supports_existing_calculations():
    components = [
        Component(name="carbon dioxide", formula="CO2", state="g"),
        Component(name="water", formula="H2O", state="g"),
    ]
    temperature = Temperature(value=298.15, unit="K")

    availability = check_component_availability(components)

    assert availability["matched_components"] == components
    assert availability["missing_components"] == []

    model_source = build_model_source_from_database(
        components=components,
        temperature=temperature,
    )

    enthalpy = H_T(
        component=components[0],
        temperature=temperature,
        model_source=model_source,
        mode="silent",
    )

    assert enthalpy is not None
    assert enthalpy.unit == "J/mol"


def test_build_model_source_from_database_supports_formula_fallback():
    component = Component(name="water", formula="H2O", state="g")
    temperature = Temperature(value=298.15, unit="K")

    availability = check_component_availability(component)
    model_source = build_model_source_from_database(
        components=[component],
        temperature=temperature,
    )

    assert availability["matched_components"] == [component]
    assert model_source is not None
