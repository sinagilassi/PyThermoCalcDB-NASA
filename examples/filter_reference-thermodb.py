# import libs
import os
from pathlib import Path
import logging
from typing import List
from pythermodb_settings.models import Component
from pyThermoDB import build_component_thermodb_from_reference, ComponentThermoDB
from pyThermoDB.thermodbX import build_component_thermodb_from_reference_source, ReferenceContentSource
from rich import print
from pythermodb_settings.references import extract_reference_components, check_reference_component_availability
# local
from reference_content_nasa import REFERENCE_CONTENT

# NOTE: logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NOTE: current file path
parent_path = os.path.dirname(os.path.abspath(__file__))
print(f"parent_path: {parent_path}")

# database
db_path = os.path.join(parent_path, 'thermodb')
print(f"db_path: {db_path}")

# source reference file path
reference_file_path = os.path.join(parent_path, 'reference_content.yaml')
print(f"reference_file_path: {reference_file_path}")

# yaml reference content source
reference_content_filtered = os.path.join(
    parent_path, 'reference_content_filtered.yaml')
print(f"reference_content_filtered: {reference_content_filtered}")

# -------------------------------------------------------------------
# SECTION: components to build thermodb for
# -------------------------------------------------------------------
# NOTE: components
components: List[Component] = [
    Component(name='benzene', formula='C6H6', state='g'),
    Component(name='toluene', formula='C7H8', state='g'),
    Component(name='ethanol', formula='C2H6O', state='g'),
    Component(name='methane', formula='CH4', state='g'),
    Component(name="methanol", formula='CH4O', state='g'),
    Component(name='propane', formula='C3H8', state='g'),
    Component(name='ethane', formula='C2H6', state='g'),
    Component(name='carbon dioxide', formula='CO2', state='g'),
    Component(name='carbon monoxide', formula='CO', state='g'),
    Component(name='dinitrogen', formula='N2', state='g'),
    Component(name='dioxygen', formula='O2', state='g'),
    Component(name='water', formula='H2O', state='g'),
    Component(name='dihydrogen', formula='H2', state='g'),
]

# -------------------------------------------------------------------
# SECTION: Check reference component availability
# -------------------------------------------------------------------
availability_results = check_reference_component_availability(
    reference=reference_file_path,
    component_keys=['C6H6', 'C7H8', 'C2H6O', 'CH4', 'CH4O',
                    'C3H8', 'C2H6', 'CO2', 'CO', 'N2', 'O2', 'H2O', 'H2'],
    component_key="Formula",
    separator_symbol="-",
    case=None,
    renumber=False
)
print(f"availability_results:")
print(availability_results)

# -------------------------------------------------------------------
# SECTION: extract reference components
# -------------------------------------------------------------------
result = extract_reference_components(
    reference_file=Path(reference_file_path),
    components=components,
    component_key="Name-Formula",    # or any ComponentKey variant
    separator_symbol="-",
    case=None,
    save_reference=True,
    output_path=reference_content_filtered,
    mode="log"
)
print(result["matched"], result["missing"], result["saved_to"])
