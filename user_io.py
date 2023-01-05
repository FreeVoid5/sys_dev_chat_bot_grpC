import random


import time
import os
import json
from urllib import request, parse
h_key = os.environ.get('HOTPEPPER_API_KEY')
r_key = os.environ.get('RAKUTEN_API_KEY')

def req(url):
    with request.urlopen(url) as res:
        body = json.loads(res.read()) # レスポンスボディ
    #   headers = res.getheaders() # ヘッダー(dict)
    #   status = res.getcode() # ステータスコード
        # body = 0
        return body

def url_gen(base_url, param_dict):
    out = base_url + '?'
    # param_dict = 
    for param in param_dict.keys():
        out += str(param) + '=' + str(param_dict[param]) + '&'
    out = out[:-1]
    return out

def budget():
    url = 'http://webservice.recruit.co.jp/hotpepper/budget/v1/?key=' + h_key + '&format=json'
    return req(url)

def get_l_cat():
    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?format=json&applicationId=' + r_key + '&categoryType=large'
    return req(url)

hp_baseurl = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
rak_baseurl = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426'
recipe_baseurl = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426'

h_parameters = {
    'key' : h_key,
    'format' : 'json'
}

cat = ('large', 'medium', 'small')



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
cnt = 0


def lambda_handler(event, context):
    global JankenCount, cnt
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
            
    elif str(intent_name) == "Recipe": # レシピインテントの場合
        # if none_list != []: # 空きスロットがある場合
            session_attributes = get_session_attributes(event)
            if cnt == 0:
                # text = get_l_cat()
                # req('http://aso2101106.pecori.jp/something/DB.php?name=aaa&point=1&streak=1')
                # text = '数字を入力してください'
                # text = {"type": "location", "title": "my location", "address": "〒160-0004 東京都新宿区四谷一丁目6番1号", "latitude": 35.687574, "longitude": 139.72922}
                # text = json.dumps(text)
                r_parameters = {
                    'applicationId' : r_key,
                    'format' : 'json',
                    'categoryType' : cat[0],
                    'formatVersion' : 2
                }
                url = url_gen(rak_baseurl, r_parameters)
                res = req(url)
                text = ""
                for r in res['result']['large']:
                    # print("Id:" + r['categoryId'])
                    # print("name:" + r['categoryName'])
                    # print("url:" + r['categoryUrl'])
                    text = text + "Id:" + r['categoryId'] + "\n"
                    text = text + "name:" + r['categoryName'] + "\n"
                    # text = text + "url:" + r['categoryUrl'] + "\n"
                text = "以下のカテゴリ一覧から興味のあるカテゴリを選んでカテゴリIDを入力してください。" + text[:-1]
                cnt += 1
                message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
                return elicit_slot(event, session_attributes, none_list[0], message)
            elif cnt == 1:
                number = int(get_slot(event, "number")) # ユーザ入力を取得
                
                r_parameters = {
                    'applicationId' : r_key,
                    'format' : 'json',
                    'categoryType' : cat[1],
                    'formatVersion' : 2
                }
                
                url = url_gen(rak_baseurl, r_parameters)
                res2 = req(url)
                text = ""
                for r in res2['result']['medium']:
                    if str(number) == r['parentCategoryId']:
                        text += "Id:" + str(r['categoryId']) + "\n"
                        text += "name:" + str(r['categoryName']) + "\n"
                        # text += "url:" + str(r['categoryUrl']) + "\n"
                        # text += "pcat:" + str(r['parentCategoryId']) + "\n"
                text = "以下のカテゴリから詳細なカテゴリを選択してください。\n" + text[:-1]
                if text == "":
                    text = "該当するカテゴリは見つかりませんでした。"
                cnt += 1
                message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
                return elicit_slot(event, session_attributes, none_list[0], message)
            else:
                number = int(get_slot(event, "number2")) # ユーザ入力を取得
                r_parameters = {
                        'applicationId' : r_key,
                        'format' : 'json',
                        'categoryType' : cat[1],
                        'formatVersion' : 2
                }
                
                url = url_gen(rak_baseurl, r_parameters)
                res2 = req(url)
                cId = ""
                for r in res2['result']['medium']:
                    if str(number) == str(r['categoryId']):
                        cId = str(r['parentCategoryId']) + "-" + str(r['categoryId'])
                        break
                rc_parameters = {
                    'applicationId' : r_key,
                    'format' : 'json',
                    'formatVersion' : 2,
                    'categoryId' : cId
                }
                
                url = url_gen(recipe_baseurl, rc_parameters)
                time.sleep(0.5)
                res3 = req(url)
                text = ""
                for r in res3['result']:
                    text += "title:" + str(r['recipeTitle']) + "\n"
                    text += "url:" + str(r['recipeUrl']) + "\n"
                    text += '\n'
                text = "これらのレシピが見つかりました。\n\n" + text[:-2]
                if text == "":
                    text = "該当するレシピが見つかりませんでした。"
                # text = str(a) + 'a'
                print(text)
                cnt = 0
                message =  {
                        'contentType': 'PlainText',
                        'content': text
                    }
                fulfillment_state = "Fulfilled"    
                session_attributes = get_session_attributes(event)
                return close(event, session_attributes, fulfillment_state, message)