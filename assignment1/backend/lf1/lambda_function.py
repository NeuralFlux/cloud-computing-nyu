import json
import boto3

from salutations import greet, thank
from dining_suggestion import elicit_dining_slots

def push_message(data):
  sqs_client = boto3.client("sqs")
  sqs_queue_url = sqs_client.get_queue_url(
              QueueName="RestaurantRecommendationQueue",
            ).get("QueueUrl")
            
  msg_attr = {}
  msg_attr["Location"] = {"DataType": "String", "StringValue": str(data["Location"])}
  msg_attr["Cuisine"] = {"DataType": "String", "StringValue": str(data["Cuisine"])}
  msg_attr["NumberOfPeople"] = {"DataType": "String", "StringValue": str(data["NumberOfPeople"])}
  msg_attr["Time"] = {"DataType": "String", "StringValue": str(data["Time"])}
  msg_attr["Email"] = {"DataType": "String", "StringValue": str(data["Email"])}
  
  queue_resp = sqs_client.send_message(
    QueueUrl=sqs_queue_url,
    DelaySeconds=10,
    MessageAttributes=msg_attr,
    MessageBody="Preferences for the recommendations"
  )
  
  return queue_resp

def lambda_handler(event, context):
  response = {}
  print(f"Inp event: {event}")
  print(f"Inp context: {context}")
  
  if event["currentIntent"]["name"] == "GreetingIntent":
    response = greet(event)

  elif event["currentIntent"]["name"] == "DiningSuggestionsIntent":
    response, fulfillment_state = elicit_dining_slots(event)

    if fulfillment_state:
      queue_resp = push_message(event["currentIntent"]["slots"])
      print("SQS resp", queue_resp)

  elif event["currentIntent"]["name"] == "ThankYouIntent":
    response = thank(event)
  
  print(f"Out response: {response}")

  return response