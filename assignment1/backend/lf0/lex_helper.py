import json
import boto3

def converse(message):
    """
        :message - str
    """

    lex = boto3.client("lex-runtime")
    response = lex.post_text(
        botName='RecommendRestaurants',
        botAlias="Prod",
        userId="893578583822",
        inputText=message
    )
    
    return response
