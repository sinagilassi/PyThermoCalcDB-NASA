# import libs
import logging
from typing import Optional, Dict, List, Any, cast, Literal
from pyThermoLinkDB.models.component_models import ComponentEquationSource
from pythermodb_settings.models import Component, Temperature, ComponentKey
from pythermodb_settings.utils import set_component_id
from pyThermoLinkDB.thermo import Source
from pyThermoDB.core import TableEquation
from pyThermoCalcDB.thermo.enthalpy import (
    En_IG_NASA9_polynomial,
    En_IG_NASA9_polynomial_range
)
# locals
from ..thermo.extractor import DataExtractor

# NOTE: set up logger
logger = logging.getLogger(__name__)


class HSG(DataExtractor):
    """
    Class for extracting NASA polynomial coefficients from a data source.
    """
    # SECTION: Attributes

    def __init__(
            self,
            source: Source,
            component: Component,
            component_key: ComponentKey
    ):
        """
        Initialize the HSG extractor with the given data source and component key.

        Parameters
        ----------
        source : Source
            The data source from which to extract information.
        component : Component
            The component for which to extract data.
        component_key : ComponentKey
            The key type used to identify the component.
        """
        # LINK: initialize parent
        super().__init__(source=source)

        # NOTE: set component
        self.component = component
        # NOTE: set component key
        self.component_key = component_key

        # SECTION: set component id
        self.component_id: str = cast(
            str,
            set_component_id(
                component=self.component,
                component_key=self.component_key
            )
        )

        # SECTION: retrieve data
        self.nasa9min_coefficients: Optional[Dict[str, float]] = self._extract_nasa_coefficients(
            prop_name="nasa9min",
        )
        self.nasa9max_coefficients: Optional[Dict[str, float]] = self._extract_nasa_coefficients(
            prop_name="nasa9max",
        )

    def _extract_nasa_coefficients(
            self,
            prop_name: Literal["nasa9min", "nasa9max"],
    ) -> Optional[Dict[str, float]]:
        """
        Extract NASA polynomial coefficients for the specified property.

        Parameters
        ----------
        prop_name : Literal["nasa9min", "nasa9max"]
            The name of the property for which to extract the coefficients.

        Returns
        -------
        Optional[Dict[str, float]]
            A dictionary containing the NASA polynomial coefficients if available, otherwise None.
        """
        try:
            # NOTE: extract formation data
            # >> get equation source
            eq_src: ComponentEquationSource | None = self._get_equation_source(
                component=self.component,
                component_key=cast(ComponentKey, self.component_key),
                prop_name=prop_name,
            )

            if eq_src is None:
                return None

            # NOTE: get equation
            equation: TableEquation = eq_src.source

            # >> get coefficients
            coefficients: Dict[str, float] = equation.parms_values

            return coefficients
        except Exception as e:
            logger.exception(
                f"Error extracting NASA9 coefficients: {e}")
            return None

    def calculate_enthalpy(
            self,
            temperature: Temperature,
            nasa_type: Literal["nasa9min", "nasa9max"],
    ) -> Optional[float]:
        """
        Calculate the enthalpy at the specified temperature using the NASA polynomial coefficients.

        Parameters
        ----------
        temperature : Temperature
            The temperature at which to calculate the enthalpy.
        nasa_type : Literal["nasa9min", "nasa9max"]
            The type of NASA polynomial to use for the calculation.

        Returns
        -------
        Optional[float]
            The calculated enthalpy if coefficients are available, otherwise None.
        """
        try:
            if nasa_type == "nasa9min":
                coeffs = self.nasa9min_coefficients
            elif nasa_type == "nasa9max":
                coeffs = self.nasa9max_coefficients
            else:
                logger.error(f"Invalid NASA type: {nasa_type}")
                return None

            if coeffs is None:
                logger.warning(
                    f"No NASA coefficients available for type {nasa_type}.")
                return None

            # >> calculate enthalpy
            enthalpy = En_IG_NASA9_polynomial(
                temperature=temperature,
                coefficients=coeffs
            )

            return enthalpy
        except Exception as e:
            logger.exception(
                f"Error calculating enthalpy at {temperature} K using {nasa_type} coefficients: {e}")
            return None
