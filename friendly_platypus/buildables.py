from string import ascii_lowercase
from dataclasses import dataclass

from utils import *
from enums import Side, ListType
from models import Padding, Border, Width, Cell

from reportlab.platypus import Table, Paragraph

from utils import int_to_roman

default_style = [
      ('RIGHTPADDING', (0, 0), (-1, -1), 0),
      ('LEFTPADDING', (0, 0), (-1, -1), 0),
      ('TOPPADDING', (0, 0), (-1, -1), 0),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
      ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]


@dataclass(frozen=True)
class Column:
  children: list
  width: float | Width = Width(12)
  padding: Padding | list[Padding] | None = None
  h_alignment: str = None
  v_alignment: str = None

  def build(self, col_unit=1.0):

    data = []
    for item in self.children:
      child = item.child if isinstance(item, Cell) else item
      built = child.build(col_unit=col_unit) if hasattr(child, 'build') else child
      data.append([built])

    table_style = default_style
    apply_style(self, table_style)

    return Table(data, style=table_style)


class Row:
  def __init__(self, height: float = None, padding: Padding | list[Padding] = None, h_alignment: str = None,
               v_alignment: str = None, border: Border | list[Border] = None, children: list[Cell | Column] = None):
    self.height: float = height
    self.padding: Padding | list[Padding] = padding
    self.h_alignment: str = h_alignment
    self.v_alignment: str = v_alignment
    self.border: Border | list[Border] = border
    self.children: list = children

  @staticmethod
  def _is_cell_specific(index: int | None):
    return index is not None

  def _add_row_style(self, table_style):
    apply_style(self, table_style)

  def _add_cells_style(self, table_style):
    for index, cell in enumerate(self.children):
        if isinstance(cell, Cell):
            apply_style(cell, table_style, index=index)

  def build(self, col_unit=1.0):
    data = [[]]
    cell_widths = []

    for content in self.children:
      if isinstance(content, Cell):
        child = content.child
      else:
        child = content

      if hasattr(child, 'build') and callable(getattr(child, 'build')):
        built_child = child.build(col_unit=col_unit)
      else:
        built_child = child

      data[0].append(built_child)

      width_spec = getattr(content, 'width', Width(12))

      resolved_width = (
        width_spec.multiplier * col_unit
        if isinstance(width_spec, Width)
        else width_spec
      )
      cell_widths.append(resolved_width)

    table_style = default_style
    self._add_row_style(table_style)
    self._add_cells_style(table_style)

    return Table(
      data,
      colWidths=cell_widths,
      rowHeights=self.height,
      style=table_style
    )


class BulletList:
  def __init__(self, children: list, list_type: ListType = ListType.UNORDERED, row_heights: list[float] = None,
      padding=None, border=None, h_alignment=None, v_alignment=None):
    self.children = children
    self.list_type = list_type
    self.row_heights = row_heights
    self.padding = padding
    self.border = border
    self.h_alignment = h_alignment
    self.v_alignment = v_alignment

  def build(self, col_unit=1.0):

    bullet_generators = {
      ListType.NUMBERED: lambda i: str(i + 1),
      ListType.ROMAN: lambda i: int_to_roman(i + 1),
      ListType.LETTERED: lambda i: ascii_lowercase[i],
      ListType.CHECKBOX: lambda i: '\u2610',
      ListType.CHECK_MARKED: lambda i: '\u2713',
      ListType.UNORDERED: lambda i: '•',
    }

    bullet_fn = bullet_generators.get(self.list_type, lambda i: '•')

    entries = [
      [Paragraph(bullet_fn(index), style=paragraph.style), paragraph]
      for index, paragraph in enumerate(self.children)
    ]

    table_style = default_style + [
      ('VALIGN', (0, index), (0, index), 'TOP')
      for index, _ in enumerate(self.children)
    ]

    apply_style(self, table_style)

    return Table(
      entries,
      colWidths=[1 * col_unit, 11 * col_unit],
      rowHeights=self.row_heights,
      style=table_style
    )

