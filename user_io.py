import random

import re
import time
import os
import json
from urllib import request, parse
h_key = os.environ.get('HOTPEPPER_API_KEY')
r_key = os.environ.get('RAKUTEN_API_KEY')

def req(url):
    regex = r'[^\x00-\x7F]'
    matchedList = re.findall(regex,url)
    for m in matchedList:
        url = url.replace(m, parse.quote_plus(m, encoding="utf-8"))
    time.sleep(0.5)
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

def get_restaurant(keyword,range,lat,lng,budget):
    global h_key
    #urlの作成
    parameters = {
                'key' : h_key,  #APIを利用するために割り当てられたキーを設定します。
                'keyword' : keyword, #店名かな、店名、住所、駅名、お店ジャンルキャッチ、キャッチのフリーワード検索(部分一致)が可能です.
                'range' : range, #ある地点からの範囲内のお店の検索を行う場合の範囲を5段階で指定できます。
                'lat' : lat, #ある地点からの範囲内のお店の検索を行う場合の緯度です。
                'lng' : lng, #ある地点からの範囲内のお店の検索を行う場合の経度です。
                'budget' : budget,
                'format' : 'json',
    }
    url = url_gen(hp_baseurl, parameters)
    print(url)
    return req(url)



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

restCnt = 0
recipeCnt = 0
keyw = ""

def lambda_handler(event, context):
    global restCnt, recipeCnt, keyw
    print(event)
    intent_name = event['sessionState']['intent']['name'] # インテント名取得
    slots = get_slots(event)
    none_list = get_none_slot_list(slots) # 空きスロットのリスト取得
    
    if str(intent_name) == "Restaurant": # じゃんけんインテントの場合
        # if none_list != []: # 空きスロットがある場合
            session_attributes = get_session_attributes(event)
            # if restCnt == 0:
            #     text = "じゃんけんポン！(0:グー、1:チョキ、2:パー)"
            # else:
            #     text = "数値を入力してください！(0:グー、1:チョキ、2:パー)"
            # JankenCount += 1
            # message =  {
            #     'contentType': 'PlainText',
            #     'content': text
            # }
            # return elicit_slot(event, session_attributes, none_list[0], message)
            if restCnt == 0:
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
                restCnt += 1
                message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
                return elicit_slot(event, session_attributes, "hand", message)
            elif restCnt == 1:
                number = int(get_slot(event, "hand")) # ユーザ入力を取得
                
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
                restCnt += 1
                message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
                return elicit_slot(event, session_attributes, "num2", message)
            elif restCnt == 2:
                keyw = int(get_slot(event, "num2")) # ユーザ入力を取得
                bud = budget()
                text = ""
                for i in range(len(bud['results']['budget'])):
                        text += 'ID:' + bud['results']['budget'][i]['code'][-2:] + '\n'
                        text += '予算:' + bud['results']['budget'][i]['name'] + '\n'
                text = "以下の予算一覧から予算を選択してください。\n" + text[:-1]
                if text == "":
                    text = "該当するカテゴリは見つかりませんでした。"
                restCnt += 1
                message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
                return elicit_slot(event, session_attributes, "num3", message)
            else:
                number = get_slot(event, "num3") # ユーザ入力を取得
                number = "B0" + str(number)
                keyid = int(get_slot(event, "num2"))
                r_parameters = {
                        'applicationId' : r_key,
                        'format' : 'json',
                        'categoryType' : cat[1],
                        'formatVersion' : 2
                }
                
                url = url_gen(rak_baseurl, r_parameters)
                res2 = req(url)
                keyword = ""
                for r in res2['result']['medium']:
                    if str(keyid) == str(r['categoryId']):
                        keyword = r['categoryName']
                        break
                res3 = get_restaurant(keyword=keyword, range='3', lat='33.58494021588118', lng='130.42429733578305', budget=number)
                # res3 = req("https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=" + h_key + "&lat=33.583511&lng=130.41898336&keyword=牛肉&format=json")
                text = ""
                # text += '\n'
                for i in res3['results']['shop']:
                    text += "店名:" + i['name'] + "\n"
                    text += "住所:" + i['address'] + "\n"
                    text += "平均予算:" + (i['budget']['average'] if i['budget']['average'] != "" else "データなし") + "\n"
                    text += "url:" + i['urls']['pc'] + "\n\n"
                # print(res['results']['shop'][0]['name'])
                if text != "":
                    text = text[:-2]
                    text = "キーワードは" + keyword + "、予算は指定された予算で検索したところ、以下のお店が見つかりました。\n" + text
                else:
                    text = "キーワードは" + keyword + "、予算は指定された予算で検索したものの、条件に合うお店が見つかりませんでした。"
                restCnt = 0
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
            if recipeCnt == 0:
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
                recipeCnt += 1
                message =  {
                    'contentType': 'PlainText',
                    'content': text
                }
                return elicit_slot(event, session_attributes, none_list[0], message)
            elif recipeCnt == 1:
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
                recipeCnt += 1
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
                recipeCnt = 0
                message =  {
                        'contentType': 'PlainText',
                        'content': text
                    }
                fulfillment_state = "Fulfilled"    
                session_attributes = get_session_attributes(event)
                return close(event, session_attributes, fulfillment_state, message)