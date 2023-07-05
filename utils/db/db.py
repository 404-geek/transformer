import boto3

dynamodb = boto3.client('dynamodb', region_name='us-west-2')


def update_db(uuid: str, index: int):
    table_name = 'file-process-tracker'

    key = {
        'uuid': {'S': uuid}
    }

    index = str(index)

    data_to_insert = f"{{'{index}':'completed'}}"

    response = dynamodb.update_item(
        TableName=table_name,
        Key=key,
        UpdateExpression='SET success_indexes = list_append(success_indexes, :data)',
        ExpressionAttributeValues={
            ':data': {'L': [{'S': data_to_insert}]}
        }
    )