from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from components import *

doc = SimpleDocTemplate("example.pdf")

story = [
    Row(
      children=[
        Cell(
          width=WidthUnit(3),
          child=Paragraph(text='Hello world')
        ),
        Cell(
          width=WidthUnit(3),
          child=Paragraph(text='Hello world')
        ),
        Cell(
          width=WidthUnit(3),
          child=Paragraph(text='Hello world')
        ),
      ]
    ),
  PageBreak(),
  Row(
      children=[
        Cell(
          width=WidthUnit(3),
          child=Paragraph(text='Hello world')
        ),
        Cell(
          width=WidthUnit(3),
          child=Row(
            children=[
              Cell(
                width=WidthUnit(3),
                child=Paragraph(text='Hello world')
              ),
              Cell(
                width=WidthUnit(3),
                child=Paragraph(text='Hello world')
              ),
            ]
          )
        ),
        Cell(
          width=WidthUnit(3),
          child=Paragraph(text='Hello world')
        ),
      ]
    )
]

PdfBuilder(story=story).build()