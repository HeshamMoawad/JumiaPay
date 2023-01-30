from requests import Response
import pandas as pd
import threading as thr 
from MyPyQt5 import QObject , pyqtSignal
import random,typing ,re,sqlite3,json,requests,openpyxl,datetime






url = 'https://httpbin.org/ip' #"https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman"

header = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en',
                'content-length': '890',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://pay.jumia.com.eg',
                'referer': 'https://pay.jumia.com.eg/services/internet-bills',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.117 Mobile Safari/537.36',
            }

proxy = {
    'http':'http://127.0.0.1:3000',
    'https':'https://127.0.0.1:3000'

}

# payloadsfile = open("json\payloads.json","r")
# Payloads = json.load(payloadsfile)


session = requests.Session()
session.proxies = proxy 
response = session.get(
    url = url ,

)


print(response.status_code)
print(response.text)



