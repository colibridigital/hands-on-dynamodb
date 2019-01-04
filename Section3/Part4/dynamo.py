import os
import time
import uuid
import boto3
import hashlib
from boto3.dynamodb.conditions import Key
import traceback

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['USER_TABLE']
table = dynamodb.Table(table_name)


def get_user_by_id(user_id):
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )

    return response['Items']


def create_user(email_address, password, first_name, last_name):
    print("Using DynamoDB table: " + table_name)

    user_doc = {
        'user_id': uuid.uuid4().hex,
        'email_address': email_address,
        'first_name': first_name,
        'last_name': last_name,
        'password': __encrypt_password(password),
        'last_login': lambda: int(round(time.time() * 1000)),
    }
    try:
        table.put_item(
            Item=user_doc
        )
    except:
        print("Failed to write user to Dynamo")
        traceback.print_exc()

    return user_doc


def __encrypt_password(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
