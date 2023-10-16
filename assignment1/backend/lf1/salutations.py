import json

def greet(event):
  response = {
    "dialogAction": {
      "type": "ElicitIntent",
      "message": {
        "contentType": "PlainText",
        "content": "Hi! How many I help you today?"
      }
    }
  }
  
  return response

def thank(event):
  response = {
    "dialogAction": {
      "type": "Close",
      "fulfillmentState": "Fulfilled",
      "message": {
        "contentType": "PlainText",
        "content": "Thank you for using the concierge service! I hope to see you again."
      }
    }
  }
  
  return response
