import aws_client
import table
import loaddata
import reports


def main():
    db_client = aws_client.create_client()

    # table.init_tables(db_client, 'data/un_shortlist.csv')
    # loaddata.load(db_client)
    # table.gen_pop_table(db_client, 'NonEconomic', 'Canada')
    # loaddata.load_single(db_client)
    reports.gen_single_report(db_client, 'Canada')


    # for building tables
    # If there are no previous rows and row empty dont show
    # If there are no additional rows and row empty dont show
if __name__ == "__main__":
    main()
