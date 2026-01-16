# import libs
import logging
from typing import Optional, Dict, List, Any, cast, Literal, Tuple
from pythermodb_settings.models import Temperature
import pycuc
# local
from pythermocalcdb_nasa.configs.constants import NASAType, NASARangeType

# NOTE: logger setup
logger = logging.getLogger(__name__)


def _require_coeffs(
    coeffs: Dict[str, Any],
    required: Tuple[str, ...]
) -> Optional[Dict[str, Any]]:
    missing = [k for k in required if k not in coeffs]
    if missing:
        logger.error(
            f"Missing coefficients for En_IG: {missing}. Required: {list(required)}")
        return None
    return {k: coeffs[k] for k in required}


def _to_Kelvin(temp: Temperature) -> float:
    return pycuc.convert_from_to(
        value=temp.value,
        from_unit=temp.unit,
        to_unit="K"
    )


def _select_nasa_type(
    temperature: Temperature,
    break_temp_min: Temperature,
    break_temp_max: Temperature,
    nasa_type: Literal['nasa7', 'nasa9']
) -> NASARangeType:
    """
    Select the appropriate NASA polynomial type based on temperature.
    """
    try:
        # >> convert break temp to Kelvin
        T = _to_Kelvin(temperature)

        # >> convert break temp to Kelvin
        T_break_min = _to_Kelvin(break_temp_min)
        T_break_max = _to_Kelvin(break_temp_max)

        if T <= T_break_min:
            return "nasa7_200_1000_K" if nasa_type == "nasa7" else "nasa9_200_1000_K"
        elif T_break_min < T <= T_break_max:
            return "nasa7_1000_6000_K" if nasa_type == "nasa7" else "nasa9_1000_6000_K"
        else:
            return "nasa7_6000_20000_K" if nasa_type == "nasa7" else "nasa9_6000_20000_K"
    except Exception as e:
        logger.exception(f"Error selecting NASA type: {e}")
        raise
