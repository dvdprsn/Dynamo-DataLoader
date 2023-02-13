from modules import aws_client, loaddata


def main():
    db_client = aws_client.create_client()
    inp = input("(1) Add data (2) Delete data > ")
    if inp == '2':
        print("Delete Data Selected")
        loaddata.delete_data(db_client)
    else:
        print("Load New Data Selected")
        loaddata.load_single(db_client)


if __name__ == "__main__":
    main()
