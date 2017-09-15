import requests
#import boto3
#from boto3.dynamodb.conditions import Key, Attr

#dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")

#feedback_table= boto3.resource('dynamodb').Table('Feedback')


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
def lambda_handler(event, context):
    Feedback= event['currentIntent']['slots']['feedback_message']
    user_id= event['userId']
    #user_id='shakul'
    #type(str(user_id))
    #feedback_table.put_item(Item={'userId':user_id,'Feedback':Feedback})
    data= '{"short_message":"feedback", "host":"chatbot","type":"feedback", "_userId":"%s", "_userFeedback":"%s"}'% (user_id,Feedback)
    req= requests.post('http://146.148.97.86:12201/gelf',data= data)
    return build_response('Thanks for your feedback. It is very valuable for us.')
    #return build_response(type(user_id))