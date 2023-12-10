import os
import base64

import boto3

import utils as opensearch_utils

def lambda_handler(event, context):
    query = {
        "query": {
            "match": {
                "labels": "<TEST>"
            }
        }
    }

    # search OpenSearch
    host = os.environ.get("OPENSEARCH_HOST_ENDPOINT")
    auth = (
        os.environ.get("OPENSEARCH_USER_ID"),
        os.environ.get("OPENSEARCH_PASSWD")
    )

    os_client = opensearch_utils.get_conn(host, auth)

    # docs for OpenSearch Index
    # https://opensearch.org/docs/latest/im-plugin/index/
    INDEX_NAME = os.environ.get("OPENSEARCH_INDEX_NAME")

    os_resp = os_client.search(query, index=INDEX_NAME)

    # compile keys of matching photos
    matching_keys = list(map(
        lambda record: record['key'],
        os_resp['hits']['hits']
    ))

    # fetch objects from S3
    s3 = boto3.client("s3")
    photo_objects = []

    for key in matching_keys:
        resp = s3.get_object(Bucket="a3-photos", Key=key)
        photo_bytes = resp["Body"].read()
        encoded_bytes = base64.b64encode(photo_bytes)
        photo_objects.append(encoded_bytes.decode())
    
    return {
        'headers': {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
            "Content-Type": "image/png"
        },
        'statusCode': 200,
        'body': photo_objects,
        'isBase64Encoded': True
    }
