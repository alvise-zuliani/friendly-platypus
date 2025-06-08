from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
from enums import HAlignment
from models import Font


class PageCounter:
  def __init__(self, font: Font = Font("Helvetica", 9, colors.black), h_alignment: str = HAlignment.LEFT):
    self.font: Font = font
    self.h_alignment: str = h_alignment

  def build(self, canvas, doc, y):
    canvas.saveState()
    canvas.setFont(self.font.name, self.font.size)
    canvas.setFillColor(self.font.color)
    text = f"Page {doc.page}"
    x = {
      HAlignment.LEFT: doc.leftMargin,
      HAlignment.CENTER: doc.pagesize[0] / 2 - stringWidth(text, self.font.name, self.font.size) / 2,
      HAlignment.RIGHT: doc.pagesize[0] - doc.rightMargin - stringWidth(text, self.font.name, self.font.size),
    }[self.h_alignment]
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
    x = {
      HAlignment.LEFT: doc.leftMargin,
      HAlignment.CENTER: doc.pagesize[0] / 2 - stringWidth(self.text, self.font.name, self.font.size) / 2,
      HAlignment.RIGHT: doc.pagesize[0] - doc.rightMargin - stringWidth(self.text, self.font.name, self.font.size),
    }[self.h_alignment]
    canvas.drawString(x, y, self.text)
    canvas.restoreState()
