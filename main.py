import aws_client
import table
import loaddata
import reports


def main():
    db_client = aws_client.create_client()

    # TODO: Change init_tables to only load keys and load un list with load() func
    # TODO: Change table names to dpears04_NonEconomic!
    # TODO: Ability to add new country
    # TODO: Delete single record
    # TODO: Function to build the decade data table - for each country create a list with its name and 10 years of data
    # TODO: Better error handling to prevent crashes
    # TODO: Clean up print statements
    # TODO: Add data shouldnt modify existing data

    # create the tables and init the keys
    # table.init_tables(db_client, 'data/un_shortlist.csv')
    # Load all provided CSVs from the data folder
    # loaddata.load(db_client)
    # Add a single data entry to a table
    # loaddata.load_single(db_client)
    reports.gen_single_report(db_client, 'Canada')


if __name__ == "__main__":
    main()
