import boto3
import requests
from boto3.dynamodb.conditions import Key, Attr

customer_table= boto3.resource('dynamodb').Table('CustomerCare')
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
    country = event['currentIntent']['slots']['country'].lower()
    try:
        response= customer_table.get_item(Key={'CountryName':country})['Item']['Answer']
    except:
        return build_response('Sorry unable to find desired customer care details. Please visit http://www.dhl.com/en/contact_center.html')
    graylog(event, response)
    return build_response('Below are the customer care details : \n'+response)
