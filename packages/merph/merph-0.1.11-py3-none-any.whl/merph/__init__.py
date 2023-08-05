import importlib.metadata

from pint import UnitRegistry

from .data import IVESPA, Aubry, Mastin, Sparks

# from .gp import GP_example
from .notebooks import launch_jupyter_example
from .stats import QHstats

ureg = UnitRegistry()

__version__ = importlib.metadata.version("merph")
