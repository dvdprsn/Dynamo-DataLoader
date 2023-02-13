import csv
import os
import table

NONECON = 'dpears04_NonEconomic'
ECON = 'dpears04_Economic'


def add_col(client, table_name, key, col_name, col_data):
    table = client.Table(table_name)

    try:
        table.update_item(
            Key={
                'CountryName': key
            },
            UpdateExpression='SET #attr1 = :val1',
            ConditionExpression='attribute_not_exists(#attr1)',
            ExpressionAttributeNames={
                '#attr1': col_name
            },
            ExpressionAttributeValues={
                ':val1': col_data
            }
        )
    except:
        return


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


def init_table(client, table_name, file):
    table = client.Table(table_name)
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        with table.batch_writer() as batch:
            for row in reader:
                batch.put_item(
                    Item={
                        'CountryName': row['Country Name']
                    }
                )


def load_un(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country Name' and row[key]:
                    add_col(client, NONECON,
                            row['Country Name'], key.replace(' ', ''), row[key])


def load_curpop(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country' and not key == 'Currency' and row[key]:
                    add_col(client, NONECON,
                            row['Country'], key.replace('Population ', ''), int(row[key]))
                elif key == 'Currency':
                    add_col(client, ECON,
                            row['Country'], key, row[key])


def load_capital(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country Name' and not key == 'ISO3':
                    add_col(client, NONECON,
                            row['Country Name'], key, row[key])


def load_area(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country Name' and not key == 'ISO3' and row[key]:
                    add_col(client, NONECON,
                            row['Country Name'], key, int(row[key]))


def load_gdppc(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country' and row[key]:
                    add_col(client, ECON,
                            row['Country'], key, int(row[key]))


def load_langs(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if None in row and 'Languages' in row:
                row[None].append(str(row['Languages']))
                row['Languages'] = ','.join(row[None])
                row.pop(None)
            for key in row:
                if not key == 'Country Name':
                    add_col(client, NONECON,
                            row['Country Name'], key, row[key])


def load(client, dir):
    print("loading data from files...")
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f) and not '.txt' in f:
            if 'area' in f:
                print('Loading areas...')
                load_area(client, f)
            elif 'capitals' in f:
                print('Loading capitals...')
                load_capital(client, f)
            elif 'curpop' in f:
                print('Loading population...')
                load_curpop(client, f)
            elif 'gdppc' in f:
                print('Loading gdppc...')
                load_gdppc(client, f)
            elif 'languages' in f:
                print('loading languages...')
                load_langs(client, f)
            elif 'un_shortlist' in f:
                print('Loading UN data...')
                load_un(client, f)
    print("Done!")


def load_single(client):
    inp = -1
    while inp not in range(1, 3):
        inp = int(input("Load data from (1) Prompts (2) add_data Folder > "))
    if inp == 2:
        print("Attempting to load data from the add_data directory")
        load(client, 'add_data')
        return

    inp = -1
    while inp not in range(1, 3):
        inp = int(input("Select Table (1) NonEconomic (2) Economic > "))
    table_name = None
    if inp == 1:
        table_name = NONECON
    elif inp == 2:
        table_name = ECON

    key = input("Enter Country Name or ISO3 > ")
    if len(key) == 3:
        try:
            key = table.query_from_iso3(client, key.upper())
        except:
            print("Item does not have an ISO3 value!")
            return

    key = key.title()
    try:
        cur_data = table.query_data(client, table_name, key)
    except:
        return

    col = input("Enter attribute name > ")
    if 'iso' in col.lower():
        col = col.upper()
    else:
        col = col.title()
    col = col.replace(' ', '')
    val = input("Enter attribute value > ")
    if col.lower() == 'languages':
        try:
            langs = cur_data['Languages'].split(',')
        except:
            add_col(client, table_name, key, 'Languages', val)
            return

        langs.append(str(val))
        try:
            update_col(client, table_name, key, 'Languages', ','.join(langs))
        except:
            print("Unable to add data")
        return
    try:
        if val.isdigit():
            val = int(val)
        add_col(client, table_name, key, col, val)
    except:
        print("Unable to add data")
