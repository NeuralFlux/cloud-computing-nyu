import json
import time

from lex_helper import converse

def str_to_msg(string, msg_id):
    return {
      "type": "unstructured",
      "unstructured": {
        "id": f"{msg_id}",
        "text": string,
        "timestamp": str(time.time())
      }
    }

def lambda_handler(event, context):
    print(f"Inp: {event}")
    print(f"Inp: {context}")
    
    response = {
        "messages": []
    }

    msg_counter = 0
    for message in event["messages"]:
        lex_response = converse(message["unstructured"]["text"])
        response["messages"].append(str_to_msg(
            lex_response["message"],
            msg_counter
        ))
        
        msg_counter += 1

    print(f"Out: {response}")
    return response
