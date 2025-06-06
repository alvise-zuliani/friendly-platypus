from reportlab.platypus import Table, SimpleDocTemplate
from dataclasses import dataclass
from reportlab.lib.pagesizes import A4


class Side:
    TOP = 'TOP'
    RIGHT = 'RIGHT'
    BOTTOM = 'BOTTOM'
    LEFT = 'LEFT'


@dataclass(frozen=True)
class Padding:
    size: float
    side: Side


class HAlignment:
    LEFT = 'LEFT'
    CENTER = 'CENTER'
    RIGHT = 'RIGHT'


class VAlignment:
    TOP = 'TOP'
    MIDDLE = 'MIDDLE'
    BOTTOM = 'BOTTOM'


@dataclass(frozen=True)
class WidthUnit:
    multiplier: int


@dataclass(frozen=True)
class Cell:
    width: float | WidthUnit
    child: any
    padding: Padding | list[Padding] = None
    h_alignment: HAlignment = None
    v_alignment: VAlignment = None


@dataclass(frozen=True)
class Column:
    width: float | WidthUnit
    children: list
    padding: Padding | list[Padding] | None = None
    h_alignment: HAlignment = None
    v_alignment: VAlignment = None

    def build(self, col_unit=1.0):
        data = []
        for item in self.children:
            if isinstance(item, Cell):
                child = item.child
                if isinstance(child, Row):
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


class Row:
    def __init__(self, height: float = None, padding: Padding | list[Padding] = None, h_alignment: HAlignment = None,
    v_alignment: VAlignment = None, children: list[Cell] = None):
        self.height: float = height
        self.padding: Padding | list[Padding] = padding
        self.h_alignment: HAlignment = h_alignment
        self.v_alignment: VAlignment = v_alignment
        self.children: list= children

    @staticmethod
    def _is_cell_specific(index: int | None):
        return index is not None

    def _decode_padding(self, padding: Padding, index: int = None):
        if self._is_cell_specific(index):
            return [(padding.side, (index, 0), (index, 0), padding.size)]
        else:
            return [(padding.side, (0, 0), (-1, -1), padding.size)]

    def _decode_h_alignment(self, h_alignment: HAlignment, index: int = None):
        if self._is_cell_specific(index):
            return [('ALIGN', (index, 0), (index, 0), h_alignment)]
        else:
            return [('ALIGN', (0, 0), (-1, -1), h_alignment)]

    def _decode_v_alignment(self, v_alignment: VAlignment, index: int = None):
        if self._is_cell_specific(index):
            return [('VALIGN', (index, 0), (index, 0), v_alignment)]
        else:
            return [('VALIGN', (0, 0), (-1, -1), v_alignment)]

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

    def build(self, col_unit=1.0):
        data = [[]]
        cell_widths = []

        for content in self.children:
            child = content.child

            if isinstance(child, Row):
                built_child = child.build(col_unit=col_unit)

            elif isinstance(child, Column):
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


#@dataclass(frozen=True)
#class Column:
#    width: float | WidthUnit
#    children: list[Cell | Row]
#    padding: Padding | list[Padding] = None
#    h_alignment: HAlignment = None
#    v_alignment: VAlignment = None


#class MultiColumnLayout:
#    def __init__(self, height: float = None, padding: Padding | list[Padding] = None, h_alignment: HAlignment = None,
#        v_alignment: VAlignment = None, children: list[Cell] = None):
#       self.height: float = height
#        self.padding: Padding | list[Padding] = padding
#        self.h_alignment: HAlignment = h_alignment
#        self.v_alignment: VAlignment = v_alignment

#        self.children: list[Column] = children
#    def build(self, col_unit: float = 1.0):
#        data = []
#        for column in self.children:
#            data.append([column.children])
#        return Table(
#            data:
#        )



class PdfBuilder:
    def __init__(self, filename='example.pdf', page_size=A4, story=None):
        self.filename = filename
        self.page_size = page_size
        self.story = story


    def build(self):
        doc = SimpleDocTemplate(self.filename, pagesize=self.page_size)
        col_unit = doc.width / 12

        resolved_story = []
        for item in self.story:
            if isinstance(item, Row):
                resolved_story.append(item.build(col_unit=col_unit))
            else:
                resolved_story.append(item)

        doc.build(resolved_story)


