import logging
import os

import ceylon.ceylon
from art import text2art

from .agent import CeylonAIAgent, run_agent

my_art = text2art("Ceylon-AI", font='tarty1')  # Notice the space between "SPACE" and "ART"
print(my_art)
my_art = text2art("ceylon.ai", font='fancy144')  # Notice the space between "SPACE" and "ART"
print(my_art)
my_art = text2art("version 0.2.5", font='fancy144')  # Notice the space between "SPACE" and "ART"
print(my_art)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("RAKUN-MAS")

from .ceylon import *

__doc__ = ceylon.__doc__
if hasattr(ceylon, "__all__"):
    __all__ = ceylon.__all__

from .agent_manager import CeylonAI
from .agent import CeylonAIAgent, run_agent, Message
