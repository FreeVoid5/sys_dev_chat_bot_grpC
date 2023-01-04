import os
import json
from urllib import request, parse
h_key = os.environ.get('HOTPEPPER_API_KEY')
r_key = os.environ.get('RAKUTEN_API_KEY')

def req(url):
    with request.urlopen(url) as res:
    #   body = json.loads(res.read()) # レスポンスボディ
    #   headers = res.getheaders() # ヘッダー(dict)
    #   status = res.getcode() # ステータスコード
        body = 0
        return body
      
def budget():
    url = 'http://webservice.recruit.co.jp/hotpepper/budget/v1/?key=' + h_key + '&format=json'
    return req(url)

def get_l_cat():
    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?format=json&applicationId=' + r_key + '&categoryType=large'
    return req(url)



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
    
    if str(intent_name) == "Restaurant": # じゃんけんインテントの場合
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
            
    elif str(intent_name) == "Recipe": # 占いインテントの場合
        if none_list != []: # 空きスロットがある場合
            session_attributes = get_session_attributes(event)
            # text = budget()
            req('http://aso2101106.pecori.jp/something/DB.php?name=aaa&point=1&streak=1')
            text = '数字を入力してください'
            # text = {"type": "location", "title": "my location", "address": "〒160-0004 東京都新宿区四谷一丁目6番1号", "latitude": 35.687574, "longitude": 139.72922}
            # text = json.dumps(text)
            message =  {
                'contentType': 'PlainText',
                'content': text
            }
            return elicit_slot(event, session_attributes, none_list[0], message)
        else: # スロットが全て埋まっている場合
            number = int(get_slot(event, "number")) # ユーザ入力を取得
            text = budget()
            message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
            fulfillment_state = "Fulfilled"    
            session_attributes = get_session_attributes(event)
            return close(event, session_attributes, fulfillment_state, message)