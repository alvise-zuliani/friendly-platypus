from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate

from row_builder import Row


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