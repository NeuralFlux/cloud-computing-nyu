import json

def elicit_dining_slots(event):
  slot_priority = ["Location", "Cuisine", "NumberOfPeople", "Time", "Email"]
  slot_prompts = {
    "Location": "Where would you like to dine?",
    "Cuisine": "What cuisine do you prefer?",
    "NumberOfPeople": "How many members in the party?",
    "Time": "At what time would you like the reservation?",
    "Email": "May I have your email address to send the recommendations?"
  }
  
  fulfillment_state = False

  for slot in slot_priority:
    if event["currentIntent"]["slots"][slot] is None:
      message = '' if not event["currentIntent"]["slotDetails"][slot] else "I didn't catch that. "
      response = {
        "dialogAction": {
          "type": "ElicitSlot",
          "message": {
            "contentType": "PlainText",
            "content": message + slot_prompts[slot]
          },
          "intentName": event["currentIntent"]["name"],
          "slots": event["currentIntent"]["slots"],
          "slotToElicit": slot
        }
      }
      
      break
  else:
    response = {
      "dialogAction": {
        "type": "ElicitIntent",
        "message": {
            "contentType": "PlainText",
            "content": "Thank you for the responses! I will send the recommendations to your email in some time."
          },
      }
    }
    
    fulfillment_state = True
  
  return response, fulfillment_state
      
