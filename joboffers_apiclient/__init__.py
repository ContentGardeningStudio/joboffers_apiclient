from .__about__ import __version__
from .cli import offers
from .main import get_offers

__all__ = [
    "__version__",
    "get_offers",
    "offers",
]
