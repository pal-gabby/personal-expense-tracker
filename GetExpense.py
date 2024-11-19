import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
expenses_table = dynamodb.Table('Expenses')

# Utility function to convert Decimal to float
def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def lambda_handler(event, context):
    try:
        # Get the emailId from query parameters
        query_params = event.get('queryStringParameters', {})
        emailId = query_params.get('emailId')

        if not emailId:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'message': 'Email ID is required'})
            }

        # Query DynamoDB using the GSI on emailId
        response = expenses_table.query(
            IndexName='emailId-index',
            KeyConditionExpression=Key('emailId').eq(emailId)
        )

        # Convert Decimal values to float
        expenses = convert_decimal(response.get('Items', []))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'expenses': expenses})
        }

    except Exception as e:
        # Log the error to CloudWatch
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }
