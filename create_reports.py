from modules import aws_client, reports, table


def main():
    db_client = aws_client.create_client()

    selection = input('Generate (1) Global Report (2) Single Report > ')
    if selection == '1':
        year = input('Enter a year to create global report for > ')
        if not year.isdigit():
            print("Enter a valid year!")
            return
        reports.pdf_global(db_client, year)
    else:
        country_name = input("Enter country name or ISO3 > ").title()
        if len(country_name) == 3:
            try:
                country_name = table.query_from_iso3(db_client, country_name.upper())
            except:
                print("Item does not have an ISO3 value!")
                return
        reports.pdf_single(db_client, country_name)

    print("Report created")


if __name__ == "__main__":
    main()
