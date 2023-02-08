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
                        'Area': row['Area']
                    }
                )
    print("Data loaded successfully")


def bulk_new_data(client, table_name, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'Country' in row:
                row['Country Name'] = row.pop('Country')
            if None in row and 'Languages' in row:
                row[None].append(str(row['Languages']))
                row['Languages'] = ', '.join(row[None])
                row.pop(None)
            for key in row:
                if not key == 'Country Name':
                    update_col(client, table_name,
                               row['Country Name'], key.replace(" ", ""), row[key])


def update_col(client, table_name, key, col_name, col_data):
    table = client.Table(table_name)

    table.update_item(
        Key={
            'CountryName': key
        },
        UpdateExpression='SET #attr1 = :val1',
        ExpressionAttributeNames={
            '#attr1': col_name
        },
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


def get_pop_rank(client, table_name, year, country):
    table = client.Table(table_name)

    resp = table.get_item(Key={'CountryName': country})
    # Retrieve only the country name and the population for the given year
    resp = table.scan(ProjectionExpression='CountryName, #attr1',
                      ExpressionAttributeNames={'#attr1': year})
    items = resp['Items']
    items = [{'CountryName': item['CountryName'],
              year: int(item[year])} for item in items if item[year]]

    # https://stackoverflow.com/questions/3766633/how-to-sort-with-lambda-in-python
    items.sort(key=lambda x: x[year], reverse=True)
    rank = -1
    for i, item in enumerate(items):
        if item['CountryName'] == country:
            rank = i + 1
            break

    print(f"rank: {rank}")
    # print(items)


def gen_pop_table(client, table_name, country):
    for year in range(1971, 2019 + 1):
        get_pop_rank(client, table_name, str(year), country)
