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
    En_IG_NASA9_polynomial_range,
    En_IG_NASA7_polynomial,
    En_IG_NASA7_polynomial_range,
)
from pyThermoCalcDB.thermo.entropy import (
    S_IG_NASA9_polynomial,
    S_IG_NASA9_polynomial_range,
    S_IG_NASA7_polynomial,
    S_IG_NASA7_polynomial_range,
)
from pyThermoCalcDB.thermo.gibbs import (
    GiFrEn_IG
)
# locals
from ..thermo.extractor import DataExtractor
from ..utils.tools import _require_coeffs

# NOTE: set up logger
logger = logging.getLogger(__name__)


class HSG(DataExtractor):
    """
    Class for extracting NASA polynomial coefficients from a data source.
    """
    # SECTION: Attributes
    req_coeffs_NASA7 = ("a1", "a2", "a3", "a4", "a5", "a6", "a7")
    req_coeffs_NASA9 = ("a1", "a2", "a3", "a4", "a5", "a6", "a7", "b1", "b2")

    def __init__(
            self,
            source: Source,
            component: Component,
            component_key: ComponentKey,
            nasa_type: Literal["nasa7", "nasa9"]
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
        nasa_type : Literal["nasa7", "nasa9"]
            The type of NASA polynomial to extract.
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
        # NOTE: extract NASA9 coefficients
        if nasa_type == "nasa9":
            self.nasa9min_coefficients: Optional[Dict[str, float]] = self._extract_nasa_coefficients(
                prop_name="nasa9_min",
            )
            self.nasa9max_coefficients: Optional[Dict[str, float]] = self._extract_nasa_coefficients(
                prop_name="nasa9_max",
            )

        # NOTE: extract NASA7 coefficients
        if nasa_type == "nasa7":
            self.nasa7min_coefficients: Optional[Dict[str, float]] = self._extract_nasa_coefficients(
                prop_name="nasa7_min",
            )
            self.nasa7max_coefficients: Optional[Dict[str, float]] = self._extract_nasa_coefficients(
                prop_name="nasa7_max",
            )

    def _extract_nasa_coefficients(
            self,
            prop_name: Literal["nasa7_min", "nasa7_max", "nasa9_min", "nasa9_max"],
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

    def calc_absolute_enthalpy(
            self,
            temperature: Temperature,
            nasa_type: Literal["nasa7_min", "nasa7_max", "nasa9_min", "nasa9_max"],
    ) -> Optional[float]:
        """
        Calculate the enthalpy at the specified temperature using the NASA polynomial coefficients.

        Parameters
        ----------
        temperature : Temperature
            The temperature at which to calculate the enthalpy.
        nasa_type : Literal["nasa7min", "nasa7max", "nasa9min", "nasa9max"]
            The type of NASA polynomial to use for the calculation.

        Returns
        -------
        Optional[float]
            The calculated enthalpy if coefficients are available, otherwise None.
        """
        try:
            if nasa_type == "nasa9_min":
                # ! get coeffs [NASA9 min]
                coeffs = self.nasa9min_coefficients
                # >> check coeffs
                if coeffs is None:
                    return None

                pack = _require_coeffs(coeffs, self.req_coeffs_NASA9)
            elif nasa_type == "nasa9_max":
                # ! get coeffs [NASA9 max]
                coeffs = self.nasa9max_coefficients
                # >> check coeffs
                if coeffs is None:
                    return None

                pack = _require_coeffs(coeffs, self.req_coeffs_NASA9)
            elif nasa_type == "nasa7_min":
                # ! get coeffs [NASA7 min]
                coeffs = self.nasa7min_coefficients
                # >> check coeffs
                if coeffs is None:
                    return None

                pack = _require_coeffs(coeffs, self.req_coeffs_NASA7)

            elif nasa_type == "nasa7_max":
                # ! get coeffs [NASA7 max]
                coeffs = self.nasa7max_coefficients
                # >> check coeffs
                if coeffs is None:
                    return None

                pack = _require_coeffs(coeffs, self.req_coeffs_NASA7)
            else:
                logger.error(f"Invalid NASA type: {nasa_type}")
                return None

            if coeffs is None:
                logger.warning(
                    f"No NASA coefficients available for type {nasa_type}.")
                return None

            # NOTE: pack coeffs
            if pack is None:
                return None

            # SECTION: calculate enthalpy
            if nasa_type == "nasa9_min":
                enthalpy = En_IG_NASA9_polynomial(
                    a1=pack["a1"],
                    a2=pack["a2"],
                    a3=pack["a3"],
                    a4=pack["a4"],
                    a5=pack["a5"],
                    a6=pack["a6"],
                    a7=pack["a7"],
                    b1=pack["b1"],
                    b2=pack["b2"],
                    temperature=temperature
                )
            elif nasa_type == "nasa9_max":
                enthalpy = En_IG_NASA9_polynomial(
                    a1=pack["a1"],
                    a2=pack["a2"],
                    a3=pack["a3"],
                    a4=pack["a4"],
                    a5=pack["a5"],
                    a6=pack["a6"],
                    a7=pack["a7"],
                    b1=pack["b1"],
                    b2=pack["b2"],
                    temperature=temperature
                )
            elif nasa_type == "nasa7_min":
                enthalpy = En_IG_NASA7_polynomial(
                    a1=pack["a1"],
                    a2=pack["a2"],
                    a3=pack["a3"],
                    a4=pack["a4"],
                    a5=pack["a5"],
                    a6=pack["a6"],
                    a7=pack["a7"],
                    temperature=temperature
                )
            elif nasa_type == "nasa7_max":
                enthalpy = En_IG_NASA7_polynomial(
                    a1=pack["a1"],
                    a2=pack["a2"],
                    a3=pack["a3"],
                    a4=pack["a4"],
                    a5=pack["a5"],
                    a6=pack["a6"],
                    a7=pack["a7"],
                    temperature=temperature
                )
            else:
                logger.error(f"Invalid NASA type: {nasa_type}")
                return None

            # NOTE: prepare return
            if enthalpy is None:
                logger.warning(
                    f"Enthalpy calculation returned None for type {nasa_type} at temperature {temperature}.")
                return None

            return enthalpy['result']
        except Exception as e:
            logger.exception(
                f"Error calculating enthalpy at {temperature} K using {nasa_type} coefficients: {e}")
            return None

    def calc_absolute_entropy(
            self,
            temperature: Temperature,
            nasa_type: Literal["nasa7_min", "nasa7_max", "nasa9_min", "nasa9_max"],
    ) -> Optional[float]:
        """
        Calculate the entropy at the specified temperature using the NASA polynomial coefficients.

        Parameters
        ----------
        temperature : Temperature
            The temperature at which to calculate the entropy.
        nasa_type : Literal["nasa7min", "nasa7max", "nasa9min", "nasa9max"]
            The type of NASA polynomial to use for the calculation.
        Returns
        -------
        Optional[float]
            The calculated entropy if coefficients are available, otherwise None.
        """
        try:
            if nasa_type == "nasa9_min":
                # ! get coeffs [NASA9 min]
                coeffs = self.nasa9min_coefficients
                # >> check coeffs
                if coeffs is None:
                    return None

                pack = _require_coeffs(coeffs, self.req_coeffs_NASA9)
            elif nasa_type == "nasa9_max":
                # ! get coeffs [NASA9 max]
                coeffs = self.nasa9max_coefficients
                # >> check coeffs
                if coeffs is None:
                    return None

                pack = _require_coeffs(coeffs, self.req_coeffs_NASA9)
            elif nasa_type == "nasa7_min":
                # ! get coeffs [NASA7 min]
                coeffs = self.nasa7min_coefficients
                # >> check coeffs
                if coeffs is None:
                    return None

                pack = _require_coeffs(coeffs, self.req_coeffs_NASA7)

            elif nasa_type == "nasa7_max":
                # ! get coeffs [NASA7 max]
                coeffs = self.nasa7max_coefficients
                # >> check coeffs
                if coeffs is None:
                    return None

                pack = _require_coeffs(coeffs, self.req_coeffs_NASA7)
            else:
                logger.error(f"Invalid NASA type: {nasa_type}")
                return None

            if coeffs is None:
                logger.warning(
                    f"No NASA coefficients available for type {nasa_type}.")
                return None

            # NOTE: pack coeffs
            if pack is None:
                return None

            # SECTION: calculate entropy
            if nasa_type == "nasa9_min":
                entropy = En_IG_NASA9_polynomial(
                    a1=pack["a1"],
                    a2=pack["a2"],
                    a3=pack["a3"],
                    a4=pack["a4"],
                    a5=pack["a5"],
                    a6=pack["a6"],
                    a7=pack["a7"],
                    b1=pack["b1"],
                    b2=pack["b2"],
                    temperature=temperature
                )
            elif nasa_type == "nasa9_max":
                entropy = En_IG_NASA9_polynomial(
                    a1=pack["a1
