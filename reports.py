from tabulate import tabulate
import table

NONECON = 'dpears04_NonEconomic'
ECON = 'dpears04_Economic'


def gen_single_report(client, country):
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


def gen_year_report(client, year):
    pass


def year_range(client, table, country):
    table = client.Table(table)
    resp = list(table.get_item(Key={'CountryName': country})['Item'].keys())
    resp = [int(i) for i in resp if i.isdigit()]
    resp.sort()
    return resp


def top_def_list(client, year):
    table = client.Table(NONECON)
    resp = table.scan(ProjectionExpression='CountryName, #attr1, #attr2',
                      ExpressionAttributeNames={'#attr1': year, '#attr2': 'Area'})
    items = resp['Items']
    items.sort(key=lambda x: x[year]/x['Area'], reverse=True)
    return items


def top_pop_list(client, year):
    table = client.Table(NONECON)
    resp = table.scan(ProjectionExpression='CountryName, #attr1',
                      ExpressionAttributeNames={'#attr1': year})
    items = resp['Items']

    # Get countries ranking for population
    items.sort(key=lambda x: x[year], reverse=True)
    return items


def top_area_list(client):
    table = client.Table(NONECON)
    resp = table.scan(ProjectionExpression='CountryName, #attr2',
                      ExpressionAttributeNames={'#attr2': 'Area'})
    items = resp['Items']
    items.sort(key=lambda x: x['Area'], reverse=True)
    return items


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
            if item[year] == -1:
                poprank = -1
                break
            poprank = i + 1
            break

    items.sort(key=lambda x: x[year]/x['Area'], reverse=True)
    denrank = -1
    for i, item in enumerate(items):
        if item['CountryName'] == country:
            if item[year] == -1:
                denrank = -1
                break
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
