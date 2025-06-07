

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, PageTemplate, Frame, PageBreak

from row_builder import Row


class PdfBuilder:
  def __init__(self, filename='example.pdf', page_size=A4, body=None):
    self.filename = filename
    self.page_size = page_size
    self.body = body

  def build(self):
    doc = BaseDocTemplate(self.filename, pagesize=self.page_size)
    col_unit = doc.width / 12

    simple_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    simple_page = PageTemplate('simple', frames=[simple_frame])
    doc.addPageTemplates(simple_page)
    sized_body = []
    for item in self.body:
      if isinstance(item, Row):
        sized_body.append(item.build(col_unit=col_unit))
      else:
        sized_body.append(item)
        if isinstance(item, PageBreak):
          doc.addPageTemplates(simple_page)

    doc.build(sized_body)