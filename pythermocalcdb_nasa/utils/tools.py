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
    break_temp: Temperature
) -> Literal["nasa-min", "nasa-max"]:
    """
    Select the appropriate NASA polynomial type based on temperature.
    """
    try:
        # >> convert break temp to Kelvin
        T = _to_Kelvin(temperature)

        # >> convert break temp to Kelvin
        T_break = _to_Kelvin(break_temp)

        if T <= T_break:
            return "nasa-min"
        else:
            return "nasa-max"
    except Exception as e:
        logger.exception(f"Error selecting NASA type: {e}")
        raise
