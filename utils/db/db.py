from config.config import DYNAMODB_KEY
import boto3


dynamodb = boto3.client('dynamodb', region_name='us-west-2')

def update_db(batch_name: str):
    table_name = 'file-process-tracker'
    
    key = {
    'uuid': {'S': DYNAMODB_KEY}
    }
    
    data_to_insert = f"{{'{batch_name}':'completed'}}"
    
    response = dynamodb.update_item(
        TableName=table_name,
        Key=key,
        UpdateExpression='SET success_indexes = list_append(success_indexes, :data)',
        ExpressionAttributeValues={
        ':data': {'L': [{'S': data_to_insert}]}
        }
    )
