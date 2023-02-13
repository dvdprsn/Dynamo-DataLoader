from modules import aws_client, table, loaddata


def main():
    db_client = aws_client.create_client()
    # create the tables and init the keys
    table.init_tables(db_client, 'data/un_shortlist.csv')
    # Load all provided CSVs from the data folder
    loaddata.load(db_client, 'data')

    # Add a single data entry to a table
if __name__ == "__main__":
    main()
