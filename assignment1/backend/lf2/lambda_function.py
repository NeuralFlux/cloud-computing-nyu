import json
import boto3
from opensearchpy import OpenSearch

from boto3.dynamodb.conditions import Key, Attr

import random

HOST = "https://search-restaurants-72sydqupvni7hi2nca44i6qbz4.us-east-1.es.amazonaws.com"
AUTH = ('auth9223', 'Auth9223#')
NUM_RECS = 3


def lambda_handler(event, context):
    sqs = boto3.resource("sqs")
    queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/893578583822/RestaurantRecommendationQueue')

    opensearch_client = OpenSearch(
        hosts=[HOST], http_auth=AUTH, use_ssl=True, verify_certs=True
    )
    
    dynamo_client = boto3.resource("dynamodb")
    restaurants_table = dynamo_client.Table("yelp-restaurants")
    
    ses_client = boto3.client('ses', region_name='us-east-1')

    msgs = queue.receive_messages(MessageAttributeNames=["All"])
    print(msgs)
    
    for msg in msgs:
        print(msg.message_attributes)
        cuisine = msg.message_attributes["Cuisine"]["StringValue"]
        
        opensearch_query = {"query": 
            {"query_string":
                {"default_field": "restaurant.cuisine", "query": cuisine}
            }
        }
        opensearch_response = opensearch_client.search(
            opensearch_query,
            index="restaurants"
        )
        
        rids = list(map(
            lambda record: record["_id"],
            opensearch_response["hits"]["hits"]
        ))
        
        rid_samples = random.sample(rids, NUM_RECS)
        print(rid_samples)
        suggestions = []
        
        for rid in rid_samples:
            db_resp = restaurants_table.query(KeyConditionExpression=Key('restaurant_id').eq(rid))
            suggestions.append(
                db_resp["Items"][0]
            )
        
        print(suggestions)
        
    
    return {
        'statusCode': 200,
    }
