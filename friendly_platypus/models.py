from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.lib.units import inch

from enums import Side


@dataclass(frozen=True)
class Border:
    side: Side
    color: any = colors.black
    width: int = 1


@dataclass(frozen=True)
class Padding:
    size: float
    side: Side


@dataclass(frozen=True)
class WidthUnit:
  multiplier: int


@dataclass(frozen=True)
class Cell:
  width: float | WidthUnit
  child: any
  padding: Padding | list[Padding] = None
  h_alignment: str = None
  v_alignment: str = None
  border: Border | list[Border] = None


@dataclass(frozen=True)
class Font:
  name: str
  size: int
  color: str | Color
