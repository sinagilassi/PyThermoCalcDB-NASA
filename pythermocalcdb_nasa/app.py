# import libs
import logging
from pythermodb_settings.models import Temperature, Component, CustomProp
from pyThermoLinkDB.models import ModelSource

# NOTE: set up logger
logger = logging.getLogger(__name__)


def calc_En(
        component: Component,
        temperature: Temperature,
        model_source: ModelSource,
):
    pass
