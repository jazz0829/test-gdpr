import boto3

def lambda_handler(event):
    try:
        athena_client = boto3.client('athena', region_name='eu-west-1')
        s3_client = boto3.client('s3', region_name='eu-west-1')
        query_execution_id = event['QueryExecutionId']
        response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']
        if status == 'SUCCEEDED':
            output_location = response['QueryExecution']['ResultConfiguration']['OutputLocation']
            path_parts = output_location.replace("s3://","").split("/")
            bucket_name = path_parts.pop(0)
            key = '/'.join(path_parts)
    return ""