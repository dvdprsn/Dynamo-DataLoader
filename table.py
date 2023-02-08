import csv
from boto3.dynamodb.conditions import Attr


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


def bulk_load_data(client, table_name, file):
    table = client.Table(table_name)
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        with table.batch_writer() as batch:
            for row in reader:
                batch.put_item(
                    Item={
                        'ISO3': row['ISO3'],
                        'CountryName': row['Country Name'],
                        'Area': int(row['Area'])
                    }
                )
    print("Data loaded successfully")


def bulk_new_data(client, table_name, file):
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if None in row and 'Languages' in row:
                row[None].append(str(row['Languages']))
                row['Languages'] = ', '.join(row[None])
                row.pop(None, None)
            for key in row:
                if not key == 'Country Name':
                    update_col(client, table_name,
                               row['Country Name'], key, row[key])


def update_col(client, table_name, key, col_name, col_data):
    table = client.Table(table_name)

    table.update_item(
        Key={
            'CountryName': key
        },
        UpdateExpression=f'SET {col_name} = :val1',
        ExpressionAttributeValues={
            ':val1': col_data
        }

    )


def query_data(client, table_name, key):
    table = client.Table(table_name)

    response = table.get_item(
        Key={
            'CountryName': key
        }
    )
    item = response.get('Item')
    if item:
        print(item)
        # print(f"{item['ISO3']} {item['CountryName']} {item['Area']}")
    else:
        print("No item found!")


def query_from_iso3(client, table_name, key):
    table = client.Table(table_name)
    response = table.scan(
        FilterExpression=Attr('ISO3').eq(key)
    )
    items = response['Items']
    print(items)


def get_all_data(client, table_name):
    table = client.Table(table_name)

    response = table.scan()
    items = response.get('Items')
    for item in items:
        print(f"{item}")

    print(f"Total Items: {response['Count']}")
