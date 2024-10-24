import boto3
from botocore.exceptions import ClientError
from json import loads



def put_object(bucket, key, body, tags, region_name, session):

    client = session.client(
        service_name='s3',
        region_name=region_name
    )

    try:
        client.put_object(
            Bucket = bucket,
            Key = key,
            Body = body,
            Tagging = tags
        )
        
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e


    