# import libs
import logging
from typing import List, Optional, Union, Dict, Literal, cast
from pythermodb_settings.models import Component, Temperature, ComponentKey
from pyreactlab_core.models.reaction import Reaction
from pyThermoCalcDB.reactions.source import (
    dH_rxn_STD,
    dS_rxn_STD,
    dG_rxn_STD,
    Keq,
    Keq_vh,
    Keq_vh_shortcut
)
# locals


# NOTE: setup logger
logger = logging.getLogger(__name__)


class RXNAdapter:
    """
    """

    def __init__(self, reaction: Reaction):
        self.reaction = reaction
