# import libs
import logging
from typing import Optional, Dict, List, Any, cast, Literal, Tuple
from pythermodb_settings.models import Temperature
import pycuc

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
    break_temp: Temperature,
    nasa_type: Literal['nasa7', 'nasa9']
) -> Literal["nasa7_min", "nasa7_max", "nasa9_min", "nasa9_max"]:
    """
    Select the appropriate NASA polynomial type based on temperature.
    """
    try:
        # >> convert break temp to Kelvin
        T = _to_Kelvin(temperature)

        # >> convert break temp to Kelvin
        T_break = _to_Kelvin(break_temp)

        if T <= T_break:
            return "nasa7_min" if nasa_type == "nasa7" else "nasa9_min"
        else:
            return "nasa7_max" if nasa_type == "nasa7" else "nasa9_max"
    except Exception as e:
        logger.exception(f"Error selecting NASA type: {e}")
        raise
