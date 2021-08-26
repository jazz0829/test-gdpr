import boto3
import traceback

def lambda_handler(event):
    try:
        query_settings = event['QuerySettings']
        sub_query = f"WITH sub_query as (SELECT ID FROM customerintelligence_raw.object_host_cig_accounts WHERE isanonymized = '1')"

        queries = []
        for table in event['Tables']:
            queries.append(f'select distinct {table["AccountIDColumn"]} as anonymized_id, "$path" as Path, '
                    f'ROW_NUMBER() OVER (Partition BY ID Order by {table["DateColumn"]} desc) as RowNumber from {table["Name"]} '
                    f'where {table["AccountIDColumn"]} in (select * from sub_query)')

        filter_query = f'SELECT anonymized_id, Path FROM (' + (' union '.join(queries)) + ') WHERE RowNumber > 1'
        
        athena_query = sub_query + filter_query

        athena_client = boto3.client('athena', region_name='eu-west-1')

        query_settings['QueryString'] = athena_query
        response = athena_client.start_query_execution(**query_settings)

        return {
            'Success': True, 'QueryExecutionId': response['QueryExecutionId']
        }
    except:
        return {'Success': False, 'Exception': traceback.format_exc()}