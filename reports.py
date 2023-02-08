from tabulate import tabulate
import table


def gen_single_report(client, country):
    country = country.capitalize()
    resp = table.query_data(client, 'NonEconomic', country)
    data = gen_pop_table(client, country)
    print(f"-==-{country}-==-\n{resp['OfficialName']}")
    print(
        f"Area: {resp['Area']} sq km ({get_area_rank(client, country)})")
    print("---------")
    print(f"Offical Languages: {resp['Languages']}")
    print(f"Capital City: {resp['Capital']}")

    print('-----Population-----')
    print(tabulate(data, headers=[
          'Year', 'Population', 'Rank', 'Population Density', 'Rank']))
    pass


def gen_year_report(client, year):
    pass


def get_area_rank(client, country):
    table = client.Table('NonEconomic')
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
    table = client.Table('NonEconomic')

    resp = table.get_item(Key={'CountryName': country})
    pop = -1
    area = -1
    try:
        pop = resp['Item'][year]
        area = resp['Item']['Area']
    except:
        pass
    popden = pop/area
    # Retrieve only the country name and the population for the given year
    resp = table.scan(ProjectionExpression='CountryName, #attr1, #attr2',
                      ExpressionAttributeNames={'#attr1': year, '#attr2': 'Area'})
    items = resp['Items']

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
    for year in range(1970, 2019 + 1):
        out = get_pop_rank(client, str(year), country)
        outputTable.append(out)
    while '-1' in outputTable[0]:
        outputTable.pop(0)
    while '-1' in outputTable[-1]:
        outputTable.pop()
    # for elem in outputTable:
    #     print(elem)
    return outputTable
