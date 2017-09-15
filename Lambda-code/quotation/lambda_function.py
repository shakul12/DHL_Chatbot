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
    origin_city = event['currentIntent']['slots']['origin_city']
    origin_zip = event['currentIntent']['slots']['origin_zip']
    destination_city = event['currentIntent']['slots']['destination_city']
    destination_zip = event['currentIntent']['slots']['destination_zip']
    package_type = event['currentIntent']['slots']['package_type']
    Weight = event['currentIntent']['slots']['Weight']
    Length = event['currentIntent']['slots']['Length']
    Width = event['currentIntent']['slots']['Width']
    Height = event['currentIntent']['slots']['Height']
    api= 'http://146.148.97.86:8080/chats/quotation/'
    response= requests.post(api, data= {'origin_city':origin_city,'origin_zip':origin_zip,'destination_city':destination_city, 'destination_zip':destination_zip, 'package_type':package_type, 'Weight':Weight,'Length':Length, 'Width':Width, 'Height':Height})
    graylog(event,response.text)
    return build_response(response.text)