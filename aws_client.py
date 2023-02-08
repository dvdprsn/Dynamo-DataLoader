import boto3
import configparser


def create_client():
    config = configparser.ConfigParser()
    config.read("aws.conf")
    try:
        aws_access_key_id = config['default']['aws_access_key_id']
        aws_secret_access_key = config['default']['aws_secret_access_key']
    except:
        print("Config not found!")
        exit(0)

    try:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='ca-central-1'
        )
        db_client = session.resource('dynamodb')
    except:
        print("Unable to create AWS session!")
        exit(0)

    return db_client
