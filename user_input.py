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

RestaurantCount=0
Recipe=0
money=0

def user_input(event, context):
    global RestaurantCount
    global Recipe
    global money
    print(event)
    intent_name = event['sessionState']['intent']['name'] # インテント名取得
    slots = get_slots(event)
    none_list = get_none_slot_list(slots) # 空きスロットのリスト取得
    
    if str(intent_name) == "restaurant": # 飲食店インテントの場合
        if none_list != []: # 空きスロットがある場合
            session_attributes = get_session_attributes(event)
            if RestaurantCount == 0:
                text = "大ジャンルIDを1つ選択、もしくは入力してください"
                RestaurantCount +=1
            else:
                text = "中ジャンルIDを1つ選択、もしくは入力してください"
                money ="予算を入力してください"    
            message =  {
                'contentType': 'PlainText',
                'content': text
            }
            

            return elicit_slot(event, session_attributes, none_list[0], message)
        else:
            try:
                user_hand = int(get_slot(event, "hand")) # ユーザ入力を取得
                if user_hand == 0:
                    lex_hand = "パー"
                elif user_hand == 1:
                    lex_hand = "グー"
                elif user_hand == 2:
                    lex_hand = "チョキ"
                else:
                    raise Exception
            except:
                text = "ジャンル、IDが取得できませんでした"
            else:
                text = "こちらの飲食店がヒットしました"
            RestaurantCount = 0
            message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
            fulfillment_state = "Fulfilled"    
            session_attributes = get_session_attributes(event)
            return close(event, session_attributes, fulfillment_state, message)

    elif str(intent_name) == "recipe": # レシピインテントの場合
        if none_list != []: # 空きスロットがある場合
            session_attributes = get_session_attributes(event)
            if Recipe == 0:
                text = "大ジャンルIDを1つ選択、もしくは入力してください"
                Recipe +=1
            else:
                text = "中ジャンルIDを1つ選択、もしくは入力してください"   
            message =  {
                'contentType': 'PlainText',
                'content': text
            }
            return elicit_slot(event, session_attributes, none_list[0], message)
        else: # スロットが全て埋まっている場合
            number = int(get_slot(event, "number")) # ユーザ入力を取得
            if number%3 == 0:
                text = "今日の運勢は最高です！"
            elif number%3 == 1:
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
            



