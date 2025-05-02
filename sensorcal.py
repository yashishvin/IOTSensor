import boto3
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
raw_table = dynamodb.Table('SensorData')
analytics_table = dynamodb.Table('SensorAnalytics')

def lambda_handler(event, context):
    now = datetime.utcnow()
    one_min_ago = int((now - timedelta(minutes=1)).timestamp() * 1000)
    now_ts = int(now.timestamp() * 1000)
    timestamp_str = str(now_ts)

    # Based on your simulator's labels
    sensor_labels = ["Accelerometer", "Gyroscope", "Battery", "GPS"]

    for sensor_type in sensor_labels:
        print(f"Processing sensor: {sensor_type}")
        try:
            response = raw_table.query(
                KeyConditionExpression=Key('sensor_type').eq(sensor_type) & Key('timestamp').between(str(one_min_ago), str(now_ts))
            )
            items = response.get('Items', [])
            print(f"{len(items)} items found for {sensor_type}")

            values = []
            for item in items:
                sensor_data = item.get("data", {})
                for v in sensor_data.get("values", []):
                    val = v.get("value")
                    if isinstance(val, (int, float, Decimal)):
                        values.append(Decimal(str(val)))

            if values:
                analytics_table.put_item(Item={
                    'sensor_type': sensor_type,
                    'metric_type': 'avg',
                    'timestamp': timestamp_str,
                    'value': sum(values) / Decimal(len(values))
                })
                analytics_table.put_item(Item={
                    'sensor_type': sensor_type,
                    'metric_type': 'min',
                    'timestamp': timestamp_str,
                    'value': min(values)
                })
                analytics_table.put_item(Item={
                    'sensor_type': sensor_type,
                    'metric_type': 'max',
                    'timestamp': timestamp_str,
                    'value': max(values)
                })
                print(f"Analytics stored for {sensor_type}")
            else:
                print(f"No values to analyze for {sensor_type}")

        except Exception as e:
            print(f"Error processing {sensor_type}: {str(e)}")

