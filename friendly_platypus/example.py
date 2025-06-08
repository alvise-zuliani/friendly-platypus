from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Paragraph, paragraph

from enums import *
from pdf_builder import *
from buildables import *
from on_page_components import *

text = 'The information contained in this document is provided for general informational purposes only and does not constitute legal, financial, or professional advice. All content is provided “as is” without any warranties. By accessing or using this content, you agree not to hold the authors or publishers liable for any loss or damages arising from its use.'

list = [
  text,
  text,
  text,
  text
]

PdfBuilder(
  filename="to_delete.pdf",
  page_size=A4,
  header=Cerberus(
    '13.5.2017',
    'Diario Oficial de la Union Europea',
    'C 189/15',
    with_divider=True
  ),
  body=[
    BulletList(
      [Paragraph(text) for text in list],
    )
  ],
  footer=PageCounter()
).build()