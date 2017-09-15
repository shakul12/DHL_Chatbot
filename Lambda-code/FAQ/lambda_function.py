import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr

knowledge_base_table= boto3.resource('dynamodb').Table('Knowledge_base')


def build_response(message):
    return {
        "dialogAction":{
            "type":"Close",
            "fulfillmentState":"Fulfilled",
            "message":{
                "contentType":"PlainText",
                "content":message
            }
        }
    }

def graylog(event, response):
        user_id= event['userId']
        identifiedIntent= event['currentIntent']['name']
        slot= event['currentIntent']['slots']
        userMessage= event['inputTranscript']
        data= '{"short_message":"chathistory", "host":"chatbot","type":"chathistory", "_userId":"%s", "_slot":"%s","_identifiedIntent":"%s","_userMessage":"%s","_botResponse":"%s"}'% (user_id,slot,identifiedIntent,userMessage,response)
        req= requests.post('http://146.148.97.86:12201/gelf',data= data)

def lambda_handler(event, context):
    intent_name= event['currentIntent']['name']
    intent_name= intent_name.split('_')[1]
    response= knowledge_base_table.get_item(Key={'ID':intent_name})['Item']['Answer']
    graylog(event, response)
    return build_response(response)

