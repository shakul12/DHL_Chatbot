import requests
import os
from slackclient import SlackClient
import logging
token="xoxp-233611138913-234202388564-240801418833-ab5a2a8ff3b29bbd6a7f67f9643f9915"
os.environ['SLACK_TOKEN']= token

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
slack_client = SlackClient(SLACK_TOKEN)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
    user_id= event['userId']
    country = event['currentIntent']['slots']['Country']
    Email = event['currentIntent']['slots']['Email']
    Phone = event['currentIntent']['slots']['Phone']
    '''
    channels_call = slack_client.api_call("channels.list")
    if channels_call['ok']:
        channels_list= channels_call['channels']
    logger.debug(channels_list)
    for channel in channels_list:
        if channel['name']==country.lower():
            channel_id= channel['id']
    '''
    message= 'User with Email ID- %s and Phone No- %s from %s wants to connect with you'% (Email,Phone,country)
    slack_client.api_call("chat.postMessage", channel=country.lower(), text=message, username='DHL_Chatbot', icon_emoji=':robot_face:')
    response= 'Thanks for your request. DHL %s slack has been notified. they will revert back shortly.'% country
    graylog(event,response)
    return build_response(response)

