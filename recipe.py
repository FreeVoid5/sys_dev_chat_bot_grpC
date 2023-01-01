import requests
import json
import env
import time
import pandas as pd
from req import req

res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=')
key = env.get_rak_key()

def get_l_cat():
    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?format=json&applicationId=' + key + '&categoryType=large'
    return req(url) 


res = get_l_cat()
for i in range(len(res['result']['large'])):
    time.sleep(0.05)
    print(res['result']['large'][i]['categoryId'],res['result']['large'][i]['categoryName'])

def get_m_cat():
    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?format=json&applicationId=' + key + '&categoryType=medium'
    return req(url)

res = get_m_cat()
#print(res['result']['medium'][0])
for i in range(len(res['result']['medium'])):
    time.sleep(0.05)
    print(res['result']['medium'][i]['categoryId'],res['result']['medium'][i]['categoryName'])

def get_s_cat():
    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?format=json&applicationId=' + key + '&categoryType=small'
    return req(url)

res = get_s_cat()
print(res['result']['small'][0])
for i in range(len(res['result']['small'])):
    time.sleep(0.05)
    print(res['result']['small'][i]['categoryId'],res['result']['small'][i]['categoryName'])

