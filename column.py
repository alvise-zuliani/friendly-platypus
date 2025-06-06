from dataclasses import dataclass

from reportlab.platypus import Table
from models import WidthUnit, Padding
import row_builder
from models import Cell


@dataclass(frozen=True)
class Column:
  children: list
  width: float | WidthUnit = WidthUnit(12)
  padding: Padding | list[Padding] | None = None
  h_alignment: str = None
  v_alignment: str = None

  def build(self, col_unit=1.0):
    data = []
    for item in self.children:
      if isinstance(item, Cell):
        child = item.child
        if isinstance(child, row_builder.Row):
          built = child.build(col_unit)
        elif isinstance(child, Column):
          built = child.build(col_unit)
        else:
          built = child
        data.append([built])
      else:
        data.append([item])

    return Table(
      data,
      style=[
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
      ]
    )