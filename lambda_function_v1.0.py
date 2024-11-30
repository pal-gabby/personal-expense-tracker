import json
import boto3
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ExpensesTable')

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))
    
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,user_id"
    }

    try:
        http_method = event.get('httpMethod', '')

        if http_method == 'OPTIONS':
            # Handle CORS preflight request
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight check successful'})
            }

        elif http_method == 'GET':
            # Handle GET request
            user_id = event['headers'].get('user_id', 'default_user')
            logger.info("Handling GET request for user_id: %s", user_id)
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
            )
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(response['Items'])
            }

        elif http_method == 'POST':
            # Handle POST request
            data = json.loads(event['body'])
            logger.info("Received POST data: %s", data)
            item = {
                'user_id': data.get('user_id', 'default_user'),
                'timestamp': datetime.utcnow().isoformat(),
                'amount': data['amount'],
                'category': data['category'],
                'description': data['description']
            }
            table.put_item(Item=item)
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Expense added successfully'})
            }

        else:
            logger.error("Unsupported HTTP method: %s", http_method)
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Unsupported HTTP method'})
            }

    except Exception as e:
        logger.exception("Error occurred: %s", str(e))
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Internal server error'})
        }
