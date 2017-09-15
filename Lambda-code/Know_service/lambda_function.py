import requests
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
    Service = event['currentIntent']['slots']['Service']
    response= 'Selected service details are - \n'
    if Service=='DHL EXPRESS 9:00':
        response+= 'Time-critical: delivery on the next possible day by 9:00 a.m.'
    elif Service=='DHL EXPRESS 10:30':
        response+= 'Time-critical: delivery on the next possible day by 10:30 a.m.'
    elif Service=='DHL EXPRESS 12:00':
        response+= 'Time-critical: delivery on the next possible day by 12:00 noon'
    elif Service=='DHL EXPRESS WORLDWIDE':
        response+= 'Time-sensitive: delivery by end of next possible day'
        elif Service=='DHL EXPRESS ENVELOPE':
        response+= 'Time-sensitive: documents by end of next possible day – documents weighing up to 10 oz/0.6 lbs'
    graylog(event,response)
    return build_response(response)





