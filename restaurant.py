# カテゴリを取ってくる際に使う
import recipe

# レストランのデータを取ってくる処理
import requests
import json
def get_restaurant(key,keyword):
    
 
 
    #urlの作成
    urlbase = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=sample&large_area=Z011' #ランキングAPIのベースとなるURL
 
    parameters = {
                'key' : key,  #APIを利用するために割り当てられたキーを設定します。
                'keyword' : keyword, #店名かな、店名、住所、駅名、お店ジャンルキャッチ、キャッチのフリーワード検索(部分一致)が可能です.
                # 'range' : range, #ある地点からの範囲内のお店の検索を行う場合の範囲を5段階で指定できます。
                # 'lat' : lat, #ある地点からの範囲内のお店の検索を行う場合の緯度です。
                # 'lng' : lng, #ある地点からの範囲内のお店の検索を行う場合の経度です。


    }
 