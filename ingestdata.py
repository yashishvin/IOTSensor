import json
import boto3
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SensorData')

def lambda_handler(event, context):
    print("Received event:", event)

    # Event comes from IoT → JSON stringified payload
    if isinstance(event, str):
        event = json.loads(event)

    # Handle event from IoT Rule payload
    if isinstance(event, dict) and 'Records' in event:
        payload = event['Records']
    elif isinstance(event, list):
        payload = event
    else:
        payload = event

    try:
        for sensor in payload:
            label = sensor.get("label", "unknown")
            timestamp = str(int(datetime.utcnow().timestamp() * 1000))

            # Convert numeric values to Decimal
            for v in sensor.get("values", []):
                if isinstance(v.get("value"), float):
                    v["value"] = Decimal(str(v["value"]))
                elif isinstance(v.get("value"), int):
                    v["value"] = Decimal(v["value"])

            table.put_item(Item={
                "sensor_type": label,
                "timestamp": timestamp,
                "data": sensor
            })

        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as e:
        print("Error:", str(e))
        raise

