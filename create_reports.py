from modules import aws_client, reports


def main():
    db_client = aws_client.create_client()

    selection = input('Generate (1) Global Report (2) Single Report > ')
    if selection == '1':
        year = input('Enter a year to create report for > ')
        if not year.isdigit():
            print("Enter a valid year!")
            return
        reports.pdf_global(db_client, year)
    else:
        country_name = input("Enter country name > ").title()
        reports.pdf_single(db_client, country_name)

    print("Report created")


if __name__ == "__main__":
    main()
