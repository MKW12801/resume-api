import json
import boto3
from decimal import Decimal

def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('VisitorCounter')

        response = table.get_item(Key={"id": "counter"})
        count = response.get("Item", {}).get("count", 0)
        new_count = count + 1
        table.put_item(Item={"id": "counter", "count": new_count})

        return {
            "statusCode": 200,
            "body": json.dumps({
                "visitor_count": decimal_to_int(new_count)
            })
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": str(e)
        }
