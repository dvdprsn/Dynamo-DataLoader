from boto3.dynamodb.conditions import Attr
from . import loaddata

NONECON = 'dpears04_NonEconomic'
ECON = 'dpears04_Economic'


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
        'TableName': NONECON,
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
    loaddata.init_table(client, NONECON, file)


def create_econ(client, file):
    params = {
        'TableName': ECON,
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
    loaddata.init_table(client, ECON, file)


def init_tables(client):
    file = 'data/un_shortlist.csv'
    exists = False
    try:
        create_nonecon(client, file)
    except:
        print("Unable to create non economic table!")
        exists = True
    try:
        create_econ(client, file)
    except:
        print("Unable to create economic table")
        exists = True
    return exists


def query_data(client, table_name, key):
    table = client.Table(table_name)

    response = table.get_item(Key={'CountryName': key})
    item = response.get('Item')
    if item:
        return item
    else:
        print("Item not found!")
        return


def query_from_iso3(client, key):
    table = client.Table(NONECON)
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
