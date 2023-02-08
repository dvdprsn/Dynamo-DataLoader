from boto3.dynamodb.conditions import Attr
import loaddata


def create(client, dict_config):
    table = client.create_table(**dict_config)
    print("Creating Table... ")
    table.wait_until_exists()
    print("Table Created")
    return table


def delete(client, table_name):
    table = client.Table(table_name)
    table.delete()
    print("Deleting Table...")
    table.wait_until_not_exists()
    print("Table Deleted")


def create_nonecon(client, file):
    params = {
        'TableName': 'NonEconomic',
        'KeySchema': [
            {'AttributeName': 'CountryName', 'KeyType': 'HASH'},
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'CountryName', 'AttributeType': 'S'},
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }
    table = client.create_table(**params)
    print("Creating noneconomic table...")
    table.wait_until_exists()
    print("Table Created!")
    # print('init table')
    loaddata.init_table(client, 'NonEconomic', file)


def create_econ(client, file):
    params = {
        'TableName': 'Economic',
        'KeySchema': [
            {'AttributeName': 'CountryName', 'KeyType': 'HASH'},
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'CountryName', 'AttributeType': 'S'},
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }
    table = client.create_table(**params)
    print("Creating economic table...")
    table.wait_until_exists()
    print("Table created!")
    # print('init table')
    loaddata.init_table(client, 'Economic', file)


def init_tables(client, file):
    try:
        create_nonecon(client, file)
    except:
        print("Unable to create non economic table!")
    try:
        create_econ(client, file)
    except:
        print("Unable to create economic table")


def query_data(client, table_name, key):
    table = client.Table(table_name)

    response = table.get_item(Key={'CountryName': key})
    item = response.get('Item')
    if item:
        return item
        # print(f"{item['ISO3']} {item['CountryName']} {item['Area']}")
    else:
        print("No item found!")


def query_from_iso3(client, table_name, key):
    table = client.Table(table_name)
    response = table.scan(
        FilterExpression=Attr('ISO3').eq(key)
    )
    return response['Items'][0]['CountryName']


def get_all_data(client, table_name):
    table = client.Table(table_name)

    response = table.scan()
    items = response.get('Items')
    for item in items:
        print(f"{item}")

    print(f"Total Items: {response['Count']}")


def get_pop_rank(client, year, country):
    table = client.Table('NonEconomic')

    resp = table.get_item(Key={'CountryName': country})
    pop = 0
    try:
        pop = resp['Item'][year]
    except:
        pass
    # Retrieve only the country name and the population for the given year
    resp = table.scan(ProjectionExpression='CountryName, #attr1',
                      ExpressionAttributeNames={'#attr1': year})
    items = resp['Items']

    items.sort(key=lambda x: x[year], reverse=True)
    rank = -1
    for i, item in enumerate(items):
        if item['CountryName'] == country:
            if item[year] == -1:
                rank = -1
                break
            rank = i + 1
            break
    return f"year: {year}, pop: {pop}, rank: {rank}"


def gen_pop_table(client, country):
    outputTable = []
    for year in range(1970, 2019 + 1):
        out = get_pop_rank(client, str(year), country)
        outputTable.append(out)
    while '-1' in outputTable[0]:
        outputTable.pop(0)
    while '-1' in outputTable[-1]:
        outputTable.pop()
    for elem in outputTable:
        print(elem)
