from reportlab.platypus import Paragraph, PageBreak, Spacer
from components import *

PdfBuilder(story=[
        # Header Row
        Row(children=[
            Cell(width=WidthUnit(12), child=Paragraph("John Doe - Software Engineer"),
                 padding=Padding(10, Side.BOTTOM))
        ]),

        Spacer(1, 10),

        # Contact Info
        Row(children=[
            Cell(width=WidthUnit(12), child=Paragraph("📍 City, Country | ✉️ email@example.com | ☎️ +123456789"),
                 padding=Padding(6, Side.BOTTOM))
        ]),

        Spacer(1, 12),

        # Main Content Split into 2 Columns: Education | Experience
        Row(children=[
            Cell(
                width=WidthUnit(4),
                child=Column(
                    width=WidthUnit(4),
                    children=[
                        Paragraph("<b>Education</b>"),
                        Spacer(1, 6),
                        Paragraph("B.Sc. in Computer Science<br/><i>University of Example</i> (2015–2019)"),
                        Spacer(1, 12),
                        Paragraph("M.Sc. in AI<br/><i>Another University</i> (2020–2022)")
                    ]
                )
            ),
            Cell(
                width=WidthUnit(8),
                child=Column(
                    width=WidthUnit(8),
                    children=[
                        Paragraph("<b>Experience</b>"),
                        Spacer(1, 6),
                        Paragraph("Software Engineer at TechCorp (2022–Present)"),
                        Paragraph("• Built scalable systems with Python & Django"),
                        Paragraph("• Led a team of 4 engineers"),
                        Spacer(1, 10),
                        Paragraph("Intern at StartupX (2021)"),
                        Paragraph("• Developed internal tools in Flask")
                    ]
                )
            )
        ]),

        Spacer(1, 16),

        # Skills Section
        Row(children=[
            Cell(
                width=WidthUnit(12),
                child=Column(
                    width=WidthUnit(12),
                    children=[
                        Paragraph("<b>Skills</b>"),
                        Spacer(1, 6),
                        Paragraph("Python, JavaScript, React, SQL, Docker, Git, Linux")
                    ]
                )
            )
        ])
    ]).build()