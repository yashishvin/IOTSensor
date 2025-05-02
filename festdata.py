import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SensorAnalytics')

def lambda_handler(event, context):
    print("EVENT DUMP:", json.dumps(event, indent=2))
    
    sensor_type = event.get('pathParameters', {}).get('sensor_type', 'Accelerometer')

    try:
        response = table.query(
            KeyConditionExpression=Key('sensor_type').eq(sensor_type),
            ScanIndexForward=False,
            Limit=3
        )

        results = {}
        for item in response['Items']:
            results[item['metric_type']] = float(item['value'])

        return {
            'statusCode': 200,
            'headers': { "Content-Type": "application/json" },
            'body': json.dumps({
                'sensor_type': sensor_type,
                'analytics': results
            })
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({ 'error': str(e) })
        }

