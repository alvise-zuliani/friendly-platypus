from reportlab.pdfbase.pdfmetrics import stringWidth


def int_to_roman(num):
  val = [
    1000, 900, 500, 400,
    100, 90, 50, 40,
    10, 9, 5, 4,
    1
  ]
  syms = [
    'M', 'CM', 'D', 'CD',
    'C', 'XC', 'L', 'XL',
    'X', 'IX', 'V', 'IV',
    'I'
  ]
  roman = ''
  i = 0
  while num > 0:
    for _ in range(num // val[i]):
      roman += syms[i]
      num -= val[i]
    i += 1
  return roman

# style_utils.py
from enums import Side, HAlignment


def decode_padding(padding, index=None):
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
    cell_range = ((index, 0), (index, 0)) if index is not None else ((0, 0), (-1, -1))

    return [
        (f'{side}PADDING', cell_range[0], cell_range[1], padding.size)
        for side in resolved_sides
    ]

def decode_h_alignment(h_alignment, index=None):
    cell_range = ((index, 0), (index, 0)) if index is not None else ((0, 0), (-1, -1))
    return [('ALIGN', cell_range[0], cell_range[1], h_alignment)]

def decode_v_alignment(v_alignment, index=None):
    cell_range = ((index, 0), (index, 0)) if index is not None else ((0, 0), (-1, -1))
    return [('VALIGN', cell_range[0], cell_range[1], v_alignment)]

def decode_border(border, index=None):
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
    cell_range = ((index, 0), (index, 0)) if index is not None else ((0, 0), (-1, -1))

    return [
        (f'LINE{side}', cell_range[0], cell_range[1], border.width, border.color)
        for side in resolved_sides
    ]


def apply_style(component, table_style, index=None):
  """
  Apply padding, alignment, and border to a single component (or a list of styles).
  If index is provided, it scopes styles to a single cell.
  """
  if hasattr(component, 'padding') and component.padding:
    if isinstance(component.padding, list):
      for pad in component.padding:
        table_style += decode_padding(pad, index)
    else:
      table_style += decode_padding(component.padding, index)

  if hasattr(component, 'h_alignment') and component.h_alignment:
    table_style += decode_h_alignment(component.h_alignment, index)

  if hasattr(component, 'v_alignment') and component.v_alignment:
    table_style += decode_v_alignment(component.v_alignment, index)

  if hasattr(component, 'border') and component.border:
    if isinstance(component.border, list):
      for bord in component.border:
        table_style += decode_border(bord, index)
    else:
      table_style += decode_border(component.border, index)


def resolve_on_page_x(h_alignment: str, doc, text, font):
  return {
    HAlignment.LEFT: doc.leftMargin,
    HAlignment.CENTER: doc.pagesize[0] / 2 - stringWidth(text, font.name, font.size) / 2,
    HAlignment.RIGHT: doc.pagesize[0] - doc.rightMargin - stringWidth(text, font.name, font.size),
  }[h_alignment]