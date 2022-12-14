import requests
import json
import env
import pandas as pd
from req import req

res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=')

key = env.get_hp_key()

