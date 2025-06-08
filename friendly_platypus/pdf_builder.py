

from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, PageBreak


class PdfBuilder:
  def __init__(self, filename='example.pdf', page_size=A4, header=None, body=None, footer=None):
    self.filename = filename
    self.page_size = page_size
    self.header = header or self.noop
    self.body = body
    self.footer = footer or self.noop

  def noop(self, canvas, doc):
    pass

  def build_header(self, canvas, doc):
    self.header.build(canvas, doc, doc.pagesize[1] - doc.topMargin)

  def build_footer(self, canvas, doc):
    self.footer.build(canvas, doc, doc.bottomMargin)

  def build(self):
    doc = BaseDocTemplate(self.filename, pagesize=self.page_size)
    col_unit = doc.width / 12

    simple_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    simple_page = PageTemplate(
      id='simple',
      frames=[simple_frame],
      onPage=self.build_header,
      onPageEnd=self.build_footer)
    doc.addPageTemplates(simple_page)
    sized_body = []
    for item in self.body:
      if hasattr(item, 'build') and callable(getattr(item, 'build')):
        sized_body.append(item.build(col_unit=col_unit))
      else:
        sized_body.append(item)
        if isinstance(item, PageBreak):
          doc.addPageTemplates(simple_page)

    doc.build(sized_body)