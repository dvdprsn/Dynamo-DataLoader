import aws_client
import table


def main():
    db_client = aws_client.create_client()

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
    # table.create(db_client, params)
    # table.bulk_load_data(db_client, 'NonEconomic', 'data/shortlist_area.csv')
    # table.get_all_data(db_client, 'NonEconomic')
    # table.bulk_new_data(db_client, 'NonEconomic',
    #                     'data/shortlist_curpop.csv')
    #
    # table.get_all_data(db_client, 'NonEconomic')
    # table.query_from_iso3(db_client, 'NonEconomic', 'CAN')
    # table.get_pop_rank(db_client, 'NonEconomic', '2018', 'Canada')
    table.gen_pop_table(db_client, 'NonEconomic', 'Canada')


    # for building tables
    # If there are no previous rows and row empty dont show
    # If there are no additional rows and row empty dont show
if __name__ == "__main__":
    main()
