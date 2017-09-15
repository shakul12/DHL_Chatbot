import requests
userId= "1"
userFeedback="hi"
data= '{"short_message":"feedback", "host":"chatbot","type":"feedback", "_userId":"%s", "_userFeedback":"%s"}'% (userId,userFeedback)
#data= '{"short_message":"Hello there", "host":"example.org", "facility":"test", "_foo":"bar"}'
req= requests.post('http://146.148.97.86:12201/gelf',data= data)
print req
print req.text