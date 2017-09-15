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
    PackageType = event['currentIntent']['slots']['PackageType']
    response= 'Selected package size is - '
    if PackageType=='EXPRESS ENVELOPE':
        response+= '12.6 x 9.4 (in)'
    elif PackageType=='EXPRESS LEGAL ENVELOPE':
        response+= '15 x 9.4 (in)'
    elif PackageType=='BOX #2 - SMALL (SMALL PIZZA)':
        response+= '12.5 x 11.1 x 1.5 (in)'
    elif PackageType=='BOX #3 - LARGE (LARGE ATLAS)':
        response+= '17.5 x 12.5 x 3.0 (in)'
        elif PackageType=='BOX #4 - LARGE TRI-TUBE':
        response+= '38.4 x 6.9 x 6.9 (in)'
    graylog(event,response)
    return build_response(response)

