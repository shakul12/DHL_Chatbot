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
    org_city = event['currentIntent']['slots']['origin_city']
    dst_city = event['currentIntent']['slots']['destination_city']
    api= 'http://146.148.97.86:8080/chats/transitTime/'
    response= requests.post(api,data={'origin_city':org_city,'destination_city':dst_city})
    graylog(event,response.text)
    return build_response(response.text)

