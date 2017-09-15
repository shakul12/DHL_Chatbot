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
def lambda_handler(event, context):
	fromCurrency = event['currentIntent']['slots']['fromCurrency']
	toCurrency = event['currentIntent']['slots']['toCurrency']
	amount = float(event['currentIntent']['slots']['amount'])
	url = ('https://currency-api.appspot.com/api/%s/%s.json') % (fromCurrency, toCurrency)
	r = requests.get(url)
	if (r.json()['success'] == False):
		return build_response('Sorry, I was unable to understand the currency')
	finalAmount = str(amount) + ' ' + fromCurrency + ' = '
	finalAmount += str(amount*float(r.json()['rate'])) + ' ' + toCurrency
	graylog(event,finalAmount)
	return build_response(finalAmount)

def graylog(event, response):
	user_id= event['userId']
	identifiedIntent= event['currentIntent']['name']
	slot= event['currentIntent']['slots']
	userMessage= event['inputTranscript']
	data= '{"short_message":"chathistory", "host":"chatbot","type":"chathistory", "_userId":"%s", "_slot":"%s","_identifiedIntent":"%s","_userMessage":"%s","_botResponse":"%s"}'% (user_id,slot,identifiedIntent,userMessage,response)
	req= requests.post('http://146.148.97.86:12201/gelf',data= data)
