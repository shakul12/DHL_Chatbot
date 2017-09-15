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
def lambda_handler(event, context):import math
import dateutil.parser
import datetime
import time
import os
import logging
from pymongo import MongoClient



logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

client = MongoClient('mongodb://146.148.97.86:27017')
db = client.dhl

def get_country(city_name):
    cities_data= db.cities.find()
    country_name=[]
    for d in cities_data:
        for key in d.keys():
            logger.debug('city_name={}'.format(city_name))
            if city_name in d[key]:
                country_name.append(key)
    return country_name

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

def build_response_card(title, subtitle, options):
    """
    Build a responseCard with a title, subtitle, and an optional set of options which should be displayed as buttons.
    """
    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message,
            'responseCard': response_card
        }
    }

def build_validation_result(is_valid, violated_slot, message_content, buttons):
    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content},
        'buttons': buttons
    }


def validate_action(origin_city,destination_city):
    origin_country= get_country(origin_city.title())
    destination_country= get_country(destination_city.title())
    if len(origin_country)>1:
        return build_validation_result(False, 'origin_country', 'Two countries for this city',origin_country)
    elif len(destination_country)>1:
        return build_validation_result(False, 'destination_country', 'Two countries for this city',destination_country)
    return build_validation_result(True, None, None,[])

def build_options(slot,buttons):
    """
    Build a list of potential options for a given slot, to be used in responseCard generation.
    """
    if slot in ['origin_city','destination_city']:
        button_list= []
        for btn in buttons:
            button_list.append({'text': btn, 'value': btn})
        return button_list
    
def perform_action(intent_request):
    """
    Performs dialog management and fulfillment 
    """
    #appointment_type = intent_request['currentIntent']['slots']['AppointmentType']
    #name = intent_request['currentIntent']['slots']['name']
    origin_city = intent_request['currentIntent']['slots']['origin_city']
    destination_city = intent_request['currentIntent']['slots']['destination_city']
    #date = intent_request['currentIntent']['slots']['Date']
    #appointment_time = intent_request['currentIntent']['slots']['Time']
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    #booking_map = json.loads(try_ex(lambda: output_session_attributes['bookingMap']) or '{}')
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        slots = intent_request['currentIntent']['slots']
        validation_result = validate_action(origin_city.lower(),destination_city.lower())
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message'],
                build_response_card(
                    'Specify {}'.format(validation_result['violatedSlot']),
                    validation_result['message']['content'],
                    build_options(validation_result['violatedSlot'],validation_result['buttons'])
                )
            )
    else:
        origin_zip = event['currentIntent']['slots']['origin_zip']
        destination_zip = event['currentIntent']['slots']['destination_zip']
        package_type = event['currentIntent']['slots']['package_type']
        api= 'http://146.148.97.86:8080/chats/quotation/'
        response= requests.post(api, data= {'origin_city':origin_city,'origin_zip':origin_zip,'destination_city':destination_city, 'destination_zip':destination_zip, 'package_type':package_type})
        return build_response(response.text)

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Quotation':
        return perform_action(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


def lambda_handler(event, context):
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)