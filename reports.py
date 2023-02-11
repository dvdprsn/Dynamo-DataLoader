from tabulate import tabulate
import table
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

NONECON = 'dpears04_NonEconomic'
ECON = 'dpears04_Economic'


def pdf_single(client, country):
    country = country.title()
    resp = table.query_data(client, NONECON, country)
    data = gen_pop_table(client, country)

    grid = [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold')]
    # Build title component
    sample_style_sheet = getSampleStyleSheet()
    flowables = []
    my_doc = SimpleDocTemplate(f'{country}_report.pdf')
    paragraph_1 = Paragraph(country, sample_style_sheet['Heading1'])
    flowables.append(paragraph_1)
    p2 = Paragraph(f"[Offical Name: {resp['OfficialName']}]")
    flowables.append(p2)

    # Build extra info table
    areaTable = []
    areaTable.append(
        [f"Area: {resp['Area']} sq km ({get_area_rank(client, country)})"])
    areaTable.append(
        [f"Offical Languages: {resp['Languages']}\nCapital City: {resp['Capital']}"])
    t = Table(areaTable, style=TableStyle(grid))
    flowables.append(t)

    # Reset Grid style
    grid = [('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold')]
    # Build non economic table component
    p2 = Paragraph('Population', sample_style_sheet['Heading2'])
    flowables.append(p2)
    tH = ['Year', 'Population', 'Rank', 'Population Density', 'Rank']
    data.insert(0, tH)
    t = Table(data, repeatRows=1, style=TableStyle(grid))
    flowables.append(t)

    # Economic Section
    resp = table.query_data(client, ECON, country)
    data = gen_gdp_table(client, country)
    # Economic Header
    p2 = Paragraph('Economic Data', sample_style_sheet['Heading2'])
    flowables.append(p2)
    p2 = Paragraph(f"Currency: {resp['Currency']}")
    flowables.append(p2)
    # Build Economic Data Table
    tH = ['Year', 'GDPPC', 'Rank']
    data.insert(0, tH)
    t = Table(data, repeatRows=1, style=TableStyle(grid))
    flowables.append(t)

    my_doc.build(flowables)


def ascii_single(client, country):
    country = country.title()
    resp = table.query_data(client, NONECON, country)
    data = gen_pop_table(client, country)
    print(f"-==-{country}-==-\n{resp['OfficialName']}")
    print(
        f"Area: {resp['Area']} sq km ({get_area_rank(client, country)})")
    print("---------")
    print(f"Offical Languages: {resp['Languages']}")
    print(f"Capital City: {resp['Capital']}")

    print('-----Population Data-----')
    print(tabulate(data, headers=[
          'Year', 'Population', 'Rank', 'Population Density', 'Rank']))
    print('-----Economic Data------')

    resp = table.query_data(client, ECON, country)
    data = gen_gdp_table(client, country)
    print(f"Currency: {resp['Currency']}")
    print("-------------")
    print(tabulate(data, headers=['year', 'GDPPC', 'Rank']))


def ascii_year(client, year):
    tableECON = client.Table(ECON)
    resp = tableECON.scan()['Items']
    # year = str(year)
    # table = client.Table(NONECON)
    # respNon = table.scan(ProjectionExpression='CountryName, #attr1, #attr2',
    #                      ExpressionAttributeNames={'#attr1': str(year), '#attr2': 'Area'})
    # items = respNon['Items']
    # items = [key for key in items if year in key]

    # print(f"Year: {year}")
    # print(f"Number of countries: {len(items)}")
    #
    # print("Table of Countries Ranked by Population (largerst to smallest)")
    # print(tabulate(top_pop_list(str(year), items), headers=[
    #       'Country Name', 'Population', 'Rank']))
    #
    # print("\nTable of countries ranked by area (largest to smallest)")
    # print(tabulate(top_area_list(items), headers=[
    #       'Country Name', 'Area', 'Rank']))
    #
    # print("\nTable of Countries ranked by Density (largest to smallest)")
    # print(tabulate(top_den_list(str(year), items), headers=[
    #       'Country Name', 'Density', 'Rank']))
    #
    # List of all years within the table
    years = list(set([int(k) for d in resp for k in d.keys() if k.isdigit()]))
    decades = list(set([(year // 10) * 10 for year in years]))
    decades.sort()
    ls = []
    headers = ['Country Name']
    print("\nGDP Per Capita for all countries")
    resp.sort(key=lambda x: x['CountryName'])
    for decade in decades:
        for year in years:
            if str(year)[2] == str(decade)[2]:
                headers.append(str(year))
        for elem in resp:
            ls.append(decade_list(elem, headers))
        print(f"\n{decade}'s Table")
        print(tabulate(ls, headers=headers))
        headers = ['Country Name']
        ls = []


def decade_list(country, years):
    ls = [y for y in years if str(y).isdigit() and str(y) in country.keys()]
    toReturn = [country['CountryName']]
    for y in ls:
        toReturn.append(country[y])
    return toReturn


def year_range(client, table, country):
    table = client.Table(table)
    resp = list(table.get_item(Key={'CountryName': country})['Item'].keys())
    resp = [int(i) for i in resp if i.isdigit()]
    resp.sort()
    return resp


def top_den_list(year, items):
    # item = [key for key in items if year in key]
    items.sort(key=lambda x: x[year]/x['Area'], reverse=True)

    top_list = []
    for i, elem in enumerate(items):
        top_list.append(
            [elem['CountryName'], str(round(elem[year]/elem['Area'], 2)), i+1])
    return (top_list)


def top_pop_list(year, items):
    # item = [key for key in items if year in key]
    items.sort(key=lambda x: x[year], reverse=True)

    top_list = []
    for i, elem in enumerate(items):
        top_list.append([elem['CountryName'], str(elem[year]), i+1])
    return (top_list)


def top_area_list(items):
    items.sort(key=lambda x: x['Area'], reverse=True)
    top_list = []
    for i, elem in enumerate(items):
        top_list.append([elem['CountryName'], str(elem['Area']), i+1])
    return (top_list)


def get_area_rank(client, country):
    table = client.Table(NONECON)
    resp = table.scan(ProjectionExpression='CountryName, #attr2',
                      ExpressionAttributeNames={'#attr2': 'Area'})
    items = resp['Items']
    items.sort(key=lambda x: x['Area'], reverse=True)
    arearank = -1
    for i, item in enumerate(items):
        if item['CountryName'] == country:
            arearank = i + 1
            break

    return arearank


def get_pop_rank(client, year, country):
    table = client.Table(NONECON)

    resp = table.get_item(Key={'CountryName': country})
    pop = 0
    area = -1
    try:
        pop = resp['Item'][year]
    except:
        return [year, None, None, None, None]
    try:
        area = resp['Item']['Area']
    except:
        # If change data to blank could just return a dummy list manually created
        return [year, None, None, None, None]

    popden = pop/area

    # Retrieve only the country name and the population for the given year
    resp = table.scan(ProjectionExpression='CountryName, #attr1, #attr2',
                      ExpressionAttributeNames={'#attr1': year, '#attr2': 'Area'})
    items = resp['Items']
    # Filter out countries if they do not have a data entry for the given year (Not empty - just none existent)
    items = [key for key in items if year in key]
    # Get countries ranking for population
    items.sort(key=lambda x: x[year], reverse=True)
    poprank = -1
    for i, item in enumerate(items):
        if item['CountryName'] == country:
            # if item[year] == -1:
            #     poprank = -1
            #     break
            poprank = i + 1
            break

    items.sort(key=lambda x: x[year]/x['Area'], reverse=True)
    denrank = -1
    for i, item in enumerate(items):
        if item['CountryName'] == country:
            # if item[year] == -1:
            #     denrank = -1
            #     break
            denrank = i+1
            break
    return [year, str(pop), poprank, str(round(popden, 2)), denrank]


def gen_pop_table(client, country):
    outputTable = []
    years = year_range(client, NONECON, country)
    for year in range(years[0], years[-1] + 1):
        # Only add an entry if there exists a data entry for the given year
        # Not an empty data entry - this filters missing key
        # if year in years:
        out = get_pop_rank(client, str(year), country)
        outputTable.append(out)
    while None in outputTable[0]:
        outputTable.pop(0)
    while None in outputTable[-1]:
        outputTable.pop()
    # for elem in outputTable:
    #     print(elem)
    return outputTable


def get_gdp_rank(client, year, country):
    table = client.Table(ECON)

    resp = table.get_item(Key={'CountryName': country})
    gdp = 0

    try:
        gdp = resp['Item'][year]
    except:
        return [year, None, None, None, None]

    # Retrieve only the country name and the population for the given year
    resp = table.scan(ProjectionExpression='CountryName, #attr1',
                      ExpressionAttributeNames={'#attr1': year})
    items = resp['Items']
    # Filter out countries if they do not have a data entry for the given year (Not empty - just none existent)
    items = [key for key in items if year in key]
    # Get countries ranking for population
    items.sort(key=lambda x: x[year], reverse=True)
    gdprank = -1
    for i, item in enumerate(items):
        if item['CountryName'] == country:
            gdprank = i + 1
            break
    return [year, str(gdp), str(gdprank)]


def gen_gdp_table(client, country):

    # Only use one response here and pass in the return!
    outputTable = []
    years = year_range(client, ECON, country)
    for year in range(years[0], years[-1] + 1):
        # Only add an entry if there exists a data entry for the given year
        # Not an empty data entry - this filters missing key
        # if year in years:
        out = get_gdp_rank(client, str(year), country)
        outputTable.append(out)
    while None in outputTable[0]:
        outputTable.pop(0)
    while None in outputTable[-1]:
        outputTable.pop()
    # for elem in outputTable:
    #     print(elem)
    return outputTable
