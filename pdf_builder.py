from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def build(table):
    sample_style_sheet = getSampleStyleSheet()
    my_doc = SimpleDocTemplate('myfile.pdf')
    flowables = []
    paragraph_1 = Paragraph("A title", sample_style_sheet['Heading1'])
    flowables.append(paragraph_1)
    grid = [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold')]
    tH = ['Year', 'Population', 'Rank', 'Population Density', 'Rank']
    table.insert(0, tH)
    t = Table(table, style=TableStyle(grid))
    flowables.append(t)
    my_doc.build(flowables)
