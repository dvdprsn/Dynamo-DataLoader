import csv
import os
import table

NONECON = 'dpears04_NonEconomic'
ECON = 'dpears04_Economic'


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
                        'ISO3': row['ISO3'],
                        'CountryName': row['Country Name'],
                        'OfficialName': row['Official Name'],
                        'ISO2': row['ISO2']
                    }
                )
    print("Data loaded successfully")


def load_curpop(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country' and not key == 'Currency' and row[key]:
                    update_col(client, NONECON,
                               row['Country'], key.replace('Population ', ''), int(row[key]))
                elif key == 'Currency':
                    update_col(client, ECON,
                               row['Country'], key, row[key])
                # elif not row[key]:
                #     update_col(client, NONECON,
                #                row['Country'], key.replace('Population ', ''), -1)


def load_capital(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country Name' and not key == 'ISO3':
                    update_col(client, NONECON,
                               row['Country Name'], key, row[key])


def load_area(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country Name' and not key == 'ISO3' and row[key]:
                    update_col(client, NONECON,
                               row['Country Name'], key, int(row[key]))
                # elif not row[key]:
                #     update_col(client, NONECON,
                #                row['Country'], key.replace('Population ', ''), -1)


def load_gdppc(client, file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if not key == 'Country' and row[key]:
                    update_col(client, ECON,
                               row['Country'], key, int(row[key]))
                # elif not row[key]:
                #     update_col(client, ECON,
                #                row['Country'], key.replace('Population ', ''), -1)


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
                    update_col(client, NONECON,
                               row['Country Name'], key, row[key])


def load(client):
    dir = 'data'
    print("Loading Data!")
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        if os.path.isfile(f) and not '.txt' in f:
            if 'area' in f:
                print('Loading areas')
                load_area(client, f)
            elif 'capitals' in f:
                print('Loading capitals')
                load_capital(client, f)
            elif 'curpop' in f:
                print('Loading populations')
                load_curpop(client, f)
            elif 'gdppc' in f:
                print('Loading gdppc')
                load_gdppc(client, f)
            elif 'languages' in f:
                print('loading languages!')
                load_langs(client, f)
    print("Done Loading data!")


def load_single(client):
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
        key = table.query_from_iso3(client, table_name, key.upper())

    key = key.title()

    try:
        cur_data = table.query_data(client, table_name, key)
    except:
        return
    col = input("Enter attribute name > ")
    val = input("Enter attribute value > ")
    if col.lower() == 'languages':
        langs = cur_data['Languages'].split(',')
        langs.append(str(val))
        try:
            update_col(client, table_name, key, 'Languages', ','.join(langs))
        except:
            print("Unable to add data")
        return
    try:
        if val.isdigit():
            val = int(val)
        update_col(client, table_name, key, col, val)
    except:
        print("Unable to add data")
