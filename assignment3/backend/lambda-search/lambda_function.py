import os
import json
import base64

import boto3

import utils

def lambda_handler(event, context):
    print(event["queryStringParameters"]["q"])

    # get keywords from Lex
    lex = boto3.client('lex-runtime')
    lex_resp = lex.post_text(
        botName="FindKeywords",
        botAlias="$LATEST",
        userId=os.environ.get("LEX_USERID"),
        inputText=event["queryStringParameters"]["q"].lower()
    )
    assert lex_resp['ResponseMetadata']['HTTPStatusCode'] == 200
    keywords = utils.process_lex_response(lex_resp)
    assert len(keywords) >= 1

    # search OpenSearch
    # query ref - https://opensearch.org/docs/latest/query-dsl/full-text/match/
    os_query = {
        "query": {
            "match": {
                "labels": ' '.join(map(lambda kw: kw + '~2', keywords)),
                # fuzziness - dogs will still match dog
            }
        }
    }

    host = os.environ.get("OPENSEARCH_HOST_ENDPOINT")
    auth = (
        os.environ.get("OPENSEARCH_USER_ID"),
        os.environ.get("OPENSEARCH_PASSWD")
    )

    os_client = utils.get_conn(host, auth)

    # docs for OpenSearch Index
    # https://opensearch.org/docs/latest/im-plugin/index/
    INDEX_NAME = os.environ.get("OPENSEARCH_INDEX_NAME")

    os_resp = os_client.search(os_query, index=INDEX_NAME)

    # compile keys of matching photos
    matching_keys = list(map(
        lambda record: record['_source']['objectKey'],
        os_resp['hits']['hits']
    ))

    response = {'photo_urls': []}
    for key in matching_keys:
        response['photo_urls'].append(f"https://a3-photos.s3.amazonaws.com/{key}")
    
    return {
        'headers': {
            "Access-Control-Allow-Origin" : "*", # Required for CORS support to work
        },
        'statusCode': 200,
        'body': json.dumps(response)
    }
