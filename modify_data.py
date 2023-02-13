from modules import aws_client, loaddata


def main():
    db_client = aws_client.create_client()
    inp = input("(1) Add data (2) Delete data > ")
    if inp == '1':
        loaddata.load_single(db_client)
    else:
        loaddata.delete_data(db_client)


if __name__ == "__main__":
    main()
