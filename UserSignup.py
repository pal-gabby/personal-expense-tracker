import boto3
import json
#UserSignUp
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('Users')

def lambda_handler(event, context):
    try:
        # Parse the incoming request body
        data = json.loads(event['body'])
        emailId = data.get('emailId')
        firstName = data.get('firstName')
        lastName = data.get('lastName')

        # Check for missing fields
        if not emailId or not firstName or not lastName:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'message': 'Missing required fields'})
            }

        # Check if user already exists
        response = users_table.get_item(Key={'emailId': emailId})
        if 'Item' in response:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'message': 'User already exists'})
            }

        # Add user to DynamoDB table
        users_table.put_item(Item={
            'emailId': emailId,
            'firstName': firstName,
            'lastName': lastName
        })

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
                },
            'body': json.dumps({'message': 'User sign-up successful'})
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
            'body': json.dumps({'message': 'Internal server error'})
        }
