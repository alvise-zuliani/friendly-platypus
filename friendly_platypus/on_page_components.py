from reportlab.lib import colors
from enums import HAlignment
from models import Font
from utils import resolve_on_page_x


class PageCounter:
  def __init__(self, font: Font = Font("Helvetica", 9, colors.black), h_alignment: str = HAlignment.LEFT):
    self.font: Font = font
    self.h_alignment: str = h_alignment

  def build(self, canvas, doc, y):
    canvas.saveState()
    canvas.setFont(self.font.name, self.font.size)
    canvas.setFillColor(self.font.color)
    text = f"Page {doc.page}"
    x = resolve_on_page_x(self.h_alignment, doc, text, self.font)
    if self.h_alignment == HAlignment.CENTER:
      canvas.drawCentredString(x, y, text)
    else:
      canvas.drawString(x, y, text)
    canvas.restoreState()


class Title:
  def __init__(self, text: str = 'Title', font: Font = Font("Helvetica-Bold", 12, colors.black), h_alignment: str = HAlignment.CENTER):
    self.text: str = text
    self.font: Font = font
    self.h_alignment: str = h_alignment

  def build(self, canvas, doc, y):
    canvas.saveState()
    canvas.setFont(self.font.name, self.font.size)
    canvas.setFillColor(self.font.color)
    x = resolve_on_page_x(self.h_alignment, doc, self.text, self.font)
    canvas.drawString(x, y, self.text)
    canvas.restoreState()


class Cerberus:
  def __init__(self, left_text: str = '', center_text: str = '', right_text: str = '',
               font: Font = Font("Helvetica-Bold", 12, colors.black), with_divider: bool = False, divider_gap=6):
    self.left_text: str = left_text
    self.center_text: str = center_text
    self.right_text: str = right_text
    self.font: Font = font
    self.with_divider: bool = with_divider
    self.divider_gap: int = divider_gap

  def build(self, canvas, doc, y):
    canvas.saveState()
    canvas.setFont(self.font.name, self.font.size)
    canvas.setFillColor(self.font.color)
    for align, text in [
      (HAlignment.LEFT, self.left_text),
      (HAlignment.CENTER, self.center_text),
      (HAlignment.RIGHT, self.right_text)
    ]:
      if text:
        x = resolve_on_page_x(align, doc, text, self.font)
        canvas.drawString(x, y, text)
    if self.with_divider:
      divider_y = y - self.divider_gap if y == doc.pagesize[1] - doc.topMargin else y + self.divider_gap
      canvas.line(doc.leftMargin, divider_y, doc.pagesize[0] - doc.rightMargin, divider_y)

    canvas.restoreState()
