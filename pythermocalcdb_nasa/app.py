# import libs
import logging
from typing import Optional
from pythermodb_settings.models import Temperature, Component, CustomProp
from pyThermoLinkDB.models import ModelSource

# NOTE: set up logger
logger = logging.getLogger(__name__)


def H_T_(
        component: Component,
        temperature: Temperature,
        model_source: ModelSource,
) -> Optional[float]:
    """
    Calculate the enthalpy at a given temperature for the specified component using the provided model source.

    Parameters
    ----------
    component : Component
            The component for which the enthalpy is to be calculated.
    temperature : Temperature
            The temperature at which the enthalpy is to be calculated.
    model_source : ModelSource
            The model source containing the necessary data for the calculation.

    Returns
    -------
    Optional[float]
            The calculated enthalpy value if successful, otherwise None.
    """
    try:
        pass
    except Exception as e:
        logger.exception(f"Error calculating H_T_: {e}")
        return None
