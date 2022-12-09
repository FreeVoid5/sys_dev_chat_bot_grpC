import random


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

JankenCount = 0



def lambda_handler(event, context):
    global JankenCount
    print(event)
    intent_name = event['sessionState']['intent']['name'] # インテント名取得
    slots = get_slots(event)
    none_list = get_none_slot_list(slots) # 空きスロットのリスト取得
    
    if str(intent_name) == "Janken": # じゃんけんインテントの場合
        if none_list != []: # 空きスロットがある場合
            session_attributes = get_session_attributes(event)
            if JankenCount == 0:
                text = "じゃんけんポン！(0:グー、1:チョキ、2:パー)"
            else:
                text = "数値を入力してください！(0:グー、1:チョキ、2:パー)"
            JankenCount += 1
            message =  {
                'contentType': 'PlainText',
                'content': text
            }
            return elicit_slot(event, session_attributes, none_list[0], message)
        else:
            # try:
            #     user_hand = int(get_slot(event, "hand")) # ユーザ入力を取得
            #     if user_hand == 0:
            #         lex_hand = "パー"
            #     elif user_hand == 1:
            #         lex_hand = "グー"
            #     elif user_hand == 2:
            #         lex_hand = "チョキ"
            #     else:
            #         raise Exception
            # except:
            #     text = "あなたの反則負けです！"
            # else:
            #     text = "私の手は"+lex_hand+"です。あなたの負けです！"
            try:
                user_hand = int(get_slot(event, "hand"))
                hand = {0:"グー", 1:"チョキ", 2:"パー"}
                lex_hand = random.randrange(3)
                if(user_hand not in hand.keys()):
                    raise Exception
                elif (lex_hand - user_hand + 3) % 3  == 0:
                    text = f"私の手は{hand[lex_hand]}です。あいこです！"
                elif (lex_hand - user_hand + 3) % 3  == 1:
                    text = f"私の手は{hand[lex_hand]}です。あなたの勝ちです！"
                elif (lex_hand - user_hand + 3) % 3 == 2:
                    text = f"私の手は{hand[lex_hand]}です。あなたの負けです！"
            except:
                text = "あなたの反則負けです！"
            JankenCount = 0
            message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
            fulfillment_state = "Fulfilled"    
            session_attributes = get_session_attributes(event)
            return close(event, session_attributes, fulfillment_state, message)
            
    elif str(intent_name) == "Uranai": # 占いインテントの場合
        if none_list != []: # 空きスロットがある場合
            session_attributes = get_session_attributes(event)
            text = "好きな数字を教えてください！"
            message =  {
                'contentType': 'PlainText',
                'content': text
            }
            return elicit_slot(event, session_attributes, none_list[0], message)
        else: # スロットが全て埋まっている場合
            number = int(get_slot(event, "number")) # ユーザ入力を取得
            a = random.randrange(3)
            if (number + a)%3 == 0:
                text = "今日の運勢は最高です！"
            elif (number + a)%3 == 1:
                text = "今日の運勢は普通です！"
            else:
                text = "今日の運勢は最悪です！"
            message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
            fulfillment_state = "Fulfilled"    
            session_attributes = get_session_attributes(event)
            return close(event, session_attributes, fulfillment_state, message)