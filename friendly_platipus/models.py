from dataclasses import dataclass

from reportlab.lib import colors
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


def simple_header(canvas, doc):
  canvas.saveState()
  canvas.setFont("Helvetica-Bold", 10)
  x = doc.leftMargin
  y = doc.height + doc.topMargin - 15  # near top of page
  canvas.drawString(x, y, "This is a Header")
  canvas.restoreState()

def simple_footer(canvas, doc):
  canvas.saveState()
  canvas.setFont("Helvetica", 9)
  x = doc.leftMargin
  y = 0.5 * inch  # half an inch from bottom
  canvas.drawString(x, y, f"Page {doc.page}")
  canvas.restoreState()