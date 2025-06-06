import column
from enums import Side
from models import Padding, Border, WidthUnit, Cell

from reportlab.platypus import Table


class Row:
  def __init__(self, height: float = None, padding: Padding | list[Padding] = None, h_alignment: str = None,
               v_alignment: str = None, border: Border | list[Border] = None, children: list[Cell | column.Column] = None):
    self.height: float = height
    self.padding: Padding | list[Padding] = padding
    self.h_alignment: str = h_alignment
    self.v_alignment: str = v_alignment
    self.border: Border | list[Border] = border
    self.children: list = children

  @staticmethod
  def _is_cell_specific(index: int | None):
    return index is not None

  def _decode_padding(self, padding: Padding, index: int = None):
    side_map = {
      Side.TOP: ['TOP'],
      Side.RIGHT: ['RIGHT'],
      Side.BOTTOM: ['BOTTOM'],
      Side.LEFT: ['LEFT'],
      Side.INLINE: ['LEFT', 'RIGHT'],
      Side.BLOCK: ['TOP', 'BOTTOM'],
      Side.ALL: ['TOP', 'RIGHT', 'BOTTOM', 'LEFT'],
    }

    resolved_sides = side_map[padding.side]

    if self._is_cell_specific(index):
      cell_range = ((index, 0), (index, 0))
    else:
      cell_range = ((0, 0), (-1, -1))

    return [
      (f'{side}PADDING', cell_range[0], cell_range[1], padding.size)
      for side in resolved_sides
    ]

  def _decode_h_alignment(self, h_alignment: str, index: int = None):
    if self._is_cell_specific(index):
      return [('ALIGN', (index, 0), (index, 0), h_alignment)]
    else:
      return [('ALIGN', (0, 0), (-1, -1), h_alignment)]

  def _decode_v_alignment(self, v_alignment: str, index: int = None):
    if self._is_cell_specific(index):
      return [('VALIGN', (index, 0), (index, 0), v_alignment)]
    else:
      return [('VALIGN', (0, 0), (-1, -1), v_alignment)]

  def _decode_border(self, border: Border, index: int = None):
    side_map = {
      Side.TOP: ['ABOVE'],
      Side.RIGHT: ['AFTER'],
      Side.BOTTOM: ['BELOW'],
      Side.LEFT: ['BEFORE'],
      Side.INLINE: ['BEFORE', 'AFTER'],
      Side.BLOCK: ['ABOVE', 'BELOW'],
      Side.ALL: ['ABOVE', 'BELOW', 'BEFORE', 'AFTER'],
    }

    resolved_sides = side_map[border.side]
    if self._is_cell_specific(index):
      cell_range = ((index, 0), (index, 0))
    else:
      cell_range = ((0, 0), (-1, -1))

    return [
      (f'LINE{side}', cell_range[0], cell_range[1], border.width, border.color)
      for side in resolved_sides
    ]

  @staticmethod
  def _get_default_style():
    return [
      ('RIGHTPADDING', (0, 0), (-1, -1), 0),
      ('LEFTPADDING', (0, 0), (-1, -1), 0),
      ('TOPPADDING', (0, 0), (-1, -1), 0),
      ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
      ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]

  def _add_row_style(self, table_style):
    if self.padding:
      if isinstance(self.padding, list):
        for pad in self.padding:
          table_style += self._decode_padding(pad)
      else:
        table_style += self._decode_padding(self.padding)
    if self.h_alignment:
      table_style += self._decode_h_alignment(self.h_alignment)
    if self.v_alignment:
      table_style += self._decode_v_alignment(self.v_alignment)
    if self.border:
      if isinstance(self.border, list):
        for bord in self.border:
          table_style += self._decode_border(bord)
      else:
        table_style += self._decode_border(self.border)

  def _add_cells_style(self, table_style):
    for index, cell in enumerate(self.children):
      if cell.padding:
        if isinstance(cell.padding, list):
          for pad in cell.padding:
            table_style += self._decode_padding(pad, index)
        else:
          table_style += self._decode_padding(cell.padding, index)
      if cell.h_alignment:
        table_style += self._decode_h_alignment(cell.h_alignment, index)
      if cell.v_alignment:
        table_style += self._decode_v_alignment(cell.v_alignment, index)
      if cell.border:
        if isinstance(cell.border, list):
          for bord in cell.border:
            table_style += self._decode_border(bord, index)
        else:
          table_style += self._decode_border(cell.border, index)

  def build(self, col_unit=1.0):
    data = [[]]
    cell_widths = []

    for content in self.children:
      child = content.child

      if isinstance(child, Row):
        built_child = child.build(col_unit=col_unit)

      elif isinstance(child, column.Column):
        built_child = child.build(col_unit=col_unit)

      else:
        built_child = child  # Regular flowable like Paragraph, Spacer, etc.

      data[0].append(built_child)

      if isinstance(content.width, WidthUnit):
        resolved_width = content.width.multiplier * col_unit
      else:
        resolved_width = content.width
      cell_widths.append(resolved_width)

    table_style = self._get_default_style()
    self._add_row_style(table_style)
    self._add_cells_style(table_style)

    return Table(
      data,
      colWidths=cell_widths,
      rowHeights=self.height,
      style=table_style
    )