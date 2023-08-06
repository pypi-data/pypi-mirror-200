from pathlib import Path

PACKAGEDIR = Path(__file__).parent.resolve()

from .flarefinder import load_from_lightkurve
