import json
import boto3
from opensearchpy import OpenSearch

from boto3.dynamodb.conditions import Key, Attr

import random
from datetime import datetime

HOST = "https://search-restaurants-72sydqupvni7hi2nca44i6qbz4.us-east-1.es.amazonaws.com"
AUTH = ('auth9223', 'Auth9223#')
NUM_RECS = 3

def compose_email(suggestions, user_attr):
    location = user_attr["Location"]["StringValue"]
    num_guests = user_attr["NumberOfPeople"]["StringValue"]
    timing = datetime.strptime(user_attr["Time"]["StringValue"], "%H:%M")
    timing = datetime.strftime(timing, "%-I%p").lower()

    message = f"""Hello!\nHere are my top suggestions for restaurants in {location} for a party of {num_guests} at {timing}:\n\n"""

    for idx, suggestion in enumerate(suggestions):
        address = suggestion['address']['display_address'][0]
        message += f"{idx + 1}. {suggestion['name']}, located at {address}\n"
    
    message += "\nI hope you enjoy your outing!"
    
    return message


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
        email_body = compose_email(suggestions, msg.message_attributes)
        
        ses_resp = ses_client.send_email(
            Destination={
                'ToAddresses': [msg.message_attributes["Email"]["StringValue"]]
            },
            Message={
                'Subject': {
                    'Data': 'Your dining recommendations from Lex'
                },
                'Body': {
                    'Text': {
                        'Data': email_body
                    }
                }
            },
            Source="anudeep.tubati@nyu.edu"
        )
        print(f"SES: {ses_resp}")
        
        msg.delete()
    
    return {
        'statusCode': 200,
    }
