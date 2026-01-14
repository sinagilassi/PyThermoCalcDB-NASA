# import libs
import logging
from typing import List, Optional, Union, Tuple, Dict, Literal, cast, Any
from pythermodb_settings.models import Component, Temperature, ComponentKey
from pyThermoLinkDB.thermo import Source
from pythermodb_settings.utils import set_component_id
# locals
from .hsg import HSG
from ..utils.tools import _select_nasa_type
from ..configs.constants import (
    NASA7_MIN,
    NASA7_MAX,
    NASA9_MIN,
    NASA9_MAX,
    TEMPERATURE_BREAK_NASA7_K,
    TEMPERATURE_BREAK_NASA9_K
)

# NOTE: setup logger
logger = logging.getLogger(__name__)


class HSGs:
    """
    Class for handling multiple HSG objects.
    """
    # SECTION: Attributes

    def __init__(
        self,
        source: Source,
        components: List[Component],
        component_key: ComponentKey,
        nasa_type: Literal["nasa7", "nasa9"]
    ) -> None:
        """

        """
        # NOTE: set
        self.source = source
        self.components = components
        self.component_key = component_key
        self.nasa_type = nasa_type

        # SECTION: set methods
        self.component_ids = [
            set_component_id(
                component=component,
                component_key=component_key
            )
            for component in components
        ]

        # SECTION: set nasa temperature break value
        nasa_temperature_break_value = TEMPERATURE_BREAK_NASA7_K if self.nasa_type == "nasa7" else TEMPERATURE_BREAK_NASA9_K
        self.nasa_temperature_break = Temperature(
            value=nasa_temperature_break_value,
            unit="K"
        )

    def get_hsgs(
        self,
        temperature: Optional[Union[float, Temperature]] = None
    ) -> Dict[str, HSG]:
        """

        """
        # NOTE: init
        hsgs: Dict[str, HSG] = {}

        # NOTE: loop components
        for id, component in zip(self.component_ids, self.components):
            # NOTE: get hsg
            hsg = HSG(
                source=self.source,
                component=component,
                component_key=cast(ComponentKey, self.component_key),
                nasa_type=cast(Literal["nasa7", "nasa9"], self.nasa_type),
            )

            # NOTE: set
            hsgs[id] = hsg

        # NOTE: return
        return hsgs

    def component_hsg(
        self,
        temperature: Temperature,
        prop_name: Literal["enthalpy", "entropy", "gibbs"] = "enthalpy"
    ):
        """

        """
        # SECTION: set methods
        if prop_name == "enthalpy":
            prop_func = HSG.calc_absolute_enthalpy
        elif prop_name == "entropy":
            prop_func = HSG.calc_absolute_entropy
        elif prop_name == "gibbs":
            prop_func = HSG.calc_gibbs_free_energy
        else:
            logger.error(f"Invalid prop_name: {prop_name}")
            return None

        # SECTION: select nasa type
        nasa_type_selected = _select_nasa_type(
            temperature=temperature,
            break_temp=self.nasa_temperature_break,
            nasa_type=cast(Literal['nasa7', 'nasa9'], self.nasa_type)
        )
        # >> cast
        nasa_type_selected = cast(
            Literal[
                "nasa7_min",
                "nasa7_max",
                "nasa9_min",
                "nasa9_max"
            ],
            nasa_type_selected
        )

        # SECTION: calc hsgs
        # NOTE: init
        hsgs_data: Dict[str, Any] = {}

        # NOTE: get hsgs
        hsgs = self.get_hsgs(temperature=temperature)

        # NOTE: loop hsgs
        for id, hsg in hsgs.items():
            # NOTE: calc
            temps, hsgs = prop_func(
                temperature=temperature,
                nasa_type=nasa_type_selected
            )

            # NOTE: set
            hsgs_data[id] = (temps, hsgs)

        # NOTE: return
        return hsgs_data
