import json
import os

import boto3
from boto3.dynamodb.conditions import Key

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')

user_table_name = os.environ['USER_TABLE']
user_table = dynamodb.Table(user_table_name)


def lambda_handler(event, context):
    user_id = event["pathParameters"]["userid"]
    print("Loading user ID " + user_id)
    user = __get_user_by_id(user_id)

    print("User is " + str(user))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "User ID": user["user_id"],
                "First Name": user["first_name"],
                "Last Name": user["last_name"],
                "Email Address": user["email_address"]
            }
        )
    }

def __get_user_by_id(user_id):
    last_login = __get_user_last_login_by_id(user_id)
    response = client.transact_get_items(TransactItems=[{
        'Get': {
            'Key': {
                "user_id": {
                    'S': user_id
                },
                "last_login": {
                    'N': str(last_login)
                }
            },
            'TableName': user_table_name
        }
    }])

    return response['Responses'][0]['Item']

def __get_user_last_login_by_id(user_id):
    response = user_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id))

    return response['Items'][0]["last_login"]
