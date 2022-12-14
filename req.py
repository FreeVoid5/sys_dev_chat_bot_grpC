# import os
import json
from urllib import request, parse
import env

# r_key = os.environ.get('RAKUTEN_API_KEY')
# h_key = os.environ.get('HOTPEPPER_API_KEY')
h_key = env.get_hp_key()
r_key = env.get_rak_key()

def req(url):
    with request.urlopen(url) as res:
      body = json.loads(res.read()) # レスポンスボディ
      headers = res.getheaders() # ヘッダー(dict)
      status = res.getcode() # ステータスコード
      return body

def url_gen(base_url, param_dict):
    out = base_url + '?'
    # param_dict = 
    for param in param_dict.keys():
        out += param + '=' + param_dict[param] + '&'
    out = out[:-1]
    return out

# 予算の例
def budget():
    url = 'http://webservice.recruit.co.jp/hotpepper/budget/v1/?key=' + h_key + '&format=json'
    return req(url)

# 大カテゴリの例
def get_l_cat():
    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?format=json&applicationId=' + r_key + '&categoryType=large'
    return req(url)

# baseurl = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'

# parameters = {
#             'key' : h_key,  #APIを利用するために割り当てられたキーを設定します。
#             'format' : 'json'
# }

# print(url_gen(baseurl, parameters))
