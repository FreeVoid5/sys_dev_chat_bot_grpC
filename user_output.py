# import recipe
# import restaurant
# いずれ連結する時が来たら使うかも


def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']


def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None   


def get_none_slot_list(d):
    return [k for k, v in d.items() if v == None]


def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']
    return {}


def elicit_slot(intent_request, session_attributes, slot, message):
    return {
        'sessionState': {
            "activeContexts": [
                {
                    "name": "slot",
                    "contextAttributes": {
                        "last": slot
                    },
                    "timeToLive": {
                        "timeToLiveInSeconds": 20,
                        "turnsToLive": 20
                    }
                }
            ],
            'dialogAction': {
                'slotToElicit': slot,
                'type': 'ElicitSlot'
            },
            "intent": {
            "name": intent_request['sessionState']['intent']['name'],
            "slots": intent_request['sessionState']['intent']['slots']
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None, 
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }