import json
import os

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')

user_table_name = os.environ['USER_TABLE']
course_table_name = os.environ['COURSE_TABLE']

user_table = dynamodb.Table(user_table_name)
course_table = dynamodb.Table(course_table_name)


def lambda_handler(event, context):
    user_id = event["pathParameters"]["userid"]
    course_id = event["pathParameters"]["courseid"]
    request_body = json.loads(event["body"])

    title = request_body["title"]
    publish_date = request_body["publish_date"]
    author_name = request_body["author_name"]
    subject_area = request_body["subject_area"]

    last_login = __get_user_by_id(user_id)["last_login"]
    __add_course(user_id, last_login, course_id, title, publish_date, author_name, subject_area)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "Status": "User information updated"
            }
        ),
    }


def __add_course(user_id, last_login, course_id, title, publish_date, author_name, subject_area):
    course_doc = {
        'course_id': {
            'S': course_id
        },
        'title': {
            'S': title
        },
        'publish_date': {
            'S': publish_date
        },
        'author_name': {
            'S': author_name
        },
        'subject_area': {
            'S': subject_area
        }
    }

    client.transact_write_items(TransactItems=[
        {
            'Put': {
                'Item': course_doc,
                'TableName': 'CourseTable'
            }
        },
        {
            'Update': {
                'Key': {
                    "user_id": {
                        'S': user_id
                    },
                    "last_login": {
                        'N': str(last_login)
                    }
                },
                'UpdateExpression':
                "SET #attrName = list_append(#attrName, :course_id)",
                'TableName': user_table_name,
                'ExpressionAttributeNames': {
                    "#attrName": "fav_courses"
                },
                'ExpressionAttributeValues': {
                    ":course_id": {
                        'L': [{
                            'S': course_id
                        }]
                    }
                }
            }
        }
    ])

def __get_user_by_id(user_id):
    response = user_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id))

    return response['Items'][0]
