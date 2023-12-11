import os
import json
import logging
import datetime

import boto3

import utils as opensearch_utils

def lambda_handler(event, context):
    LABEL_DETECTION_MIN_CONFIDENCE = 99
    logging.debug(f"Event received: {event}")

    # extract details
    created_time = bucket_name = event['Records'][0]['eventTime']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    obj_key = event['Records'][0]['s3']['object']['key']
    logging.info(f"Extracted Bucket: {bucket_name}, Key: {obj_key}")
    
    # call rekognition
    rkgn_client = boto3.client('rekognition')
    rkgn_response = rkgn_client.detect_labels(
        Image={
            "S3Object": {
                "Bucket": bucket_name,
                "Name": obj_key
            }
        },
        MinConfidence=LABEL_DETECTION_MIN_CONFIDENCE
    )
    labels = [label_group["Name"] for label_group in rkgn_response["Labels"]]

    logging.debug(f"RKGN response: {rkgn_response}")
    logging.info(f"Extracted Labels: {labels}")
    
    # add custom labels
    s3 = boto3.client("s3")
    s3_resp = s3.head_object(Bucket=bucket_name, Key=obj_key)
    logging.debug(f"S3 Metadata Resp: {s3_resp}")
    
    custom_labels = s3_resp["Metadata"].get("x-amz-meta-customLabels", [])
    logging.info(f"Custom Labels: {custom_labels}")
    labels.extend(custom_labels)

    # add record to OpenSearch
    host = os.environ.get("OPENSEARCH_HOST_ENDPOINT")
    auth = (
        os.environ.get("OPENSEARCH_USER_ID"),
        os.environ.get("OPENSEARCH_PASSWD")
    )

    os_client = opensearch_utils.get_conn(host, auth)

    # docs for OpenSearch Index
    # https://opensearch.org/docs/latest/im-plugin/index/
    INDEX_NAME = os.environ.get("OPENSEARCH_INDEX_NAME")

    record = {
        "bucket": bucket_name,
        "objectKey": obj_key,
        "createdTimestamp": datetime.datetime.utcnow()\
            .isoformat(timespec="seconds") + "Z",
        "labels": ' '.join(labels).lower()
    }

    os_response = opensearch_utils.add_record(os_client, INDEX_NAME, record)
    logging.debug(f"RESP {os_response} for INSERT {record}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
