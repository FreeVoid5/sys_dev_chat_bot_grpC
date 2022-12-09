# カテゴリを取ってくる際に使う
# import recipe
import requests
import json
import env

# レストランのデータを取ってくる処理
def get_restaurant(keyword,range,lat,lng,budget):

    key = env.get_hp_key()
    #urlの作成
    url = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=' + key + '&keyword=' + keyword + '&lat=' +  lat + '&lng=' + lng + '&range=' + range +'&format=json&budget=' + budget#ランキングAPIのベースとなるURL
    # parameters = {
    #             'key' : key,  #APIを利用するために割り当てられたキーを設定します。
    #             'keyword' : keyword,#店名かな、店名、住所、駅名、お店ジャンルキャッチ、キャッチのフリーワード検索(部分一致)が可能です.
    #             'range' : range, #ある地点からの範囲内のお店の検索を行う場合の範囲を5段階で指定できます。
    #             'lat' : lat, #ある地点からの範囲内のお店の検索を行う場合の緯度です。
    #             'lng' : lng,#ある地点からの範囲内のお店の検索を行う場合の経度です。
    # }
    return requests.get(url).json()

def budget():
    key = env.get_hp_key()
    #urlの作成
    url = 'http://webservice.recruit.co.jp/hotpepper/budget/v1/?key=' + key + '&format=json'
    return requests.get(url).json()


word='すし'
yosan = 'B008,B003'

# .encode('utf-8')
# print(word)
# res = get_restaurant(keyword=word, range='3', lat='33.58494021588118', lng='130.42429733578305', budget=yosan)

# print(res)

nedan = {"~500":"B002",}
bud = budget()
# j2p_budget = json.loads()
for i in range(len(bud['results']['budget'])):
    print(bud['results']['budget'][i])