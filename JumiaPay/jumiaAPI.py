from PyQt5.QtCore import QObject , pyqtSignal
import random,typing ,json,requests,datetime
import time
from .RequestsCore import Requests , NewResponse
from urllib3.exceptions import InsecureRequestWarning
import requests
from .generator import Generator
from .jumiaCore import (
    LeadObjectFirst ,
    LeadObjectSec ,
    LeadObjectNoClient ,
    LeadObjectUndefined ,
    Vendors ,
    ResponseStatus ,
    ResponseLength ,
    Flags ,
    ContentLength
)
from .exceptions import IPAddressBanned
####################################################

# MIT License

# Copyright (c) 2023 HeshamMoawad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Contact Me
# GitHub : github.com/HeshamMoawad
# Gmail : HeshamMoawad120120@gmail.com
# Whatsapp : +201111141853

class JumiaPay(Requests):

    def __init__(self,vendor:str=Vendors.We) -> None:
        self.gen = Generator()
        self.vendor = vendor
        self.URLs = {
            'WE': "internet.postpaid.wehome@aman",
            'Etisalat': "internet.postpaid.etisalat@aman",
            'Orange': "internet.bill.orangedsl@fawry",
            'Noor': "internet.bill.nooradsl@fawry"
        }
        self.Errors = []
        # ------------- Prapares ----------------
        self.payload:dict = json.load(open("json\payloads.json", "r"))[self.vendor]
        # Suppress only the single warning from urllib3 needed.
        super().__init__(
            "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/"+self.URLs[self.vendor],  {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://pay.jumia.com.eg',
                'referer': 'https://pay.jumia.com.eg/services/internet-bills',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.117 Mobile Safari/537.36',
            })
        self.updateHeaders(ContentLength.All[self.vendor])
    
    def getPayload(self,AreaCode:str,PhoneNumber:str):
        payload = self.payload.copy()
        # EG_+2035242441  # "EG_+20402917386"
        payload['payload']['phone_number'] = f"EG_+20{AreaCode}{PhoneNumber}"
        return payload

    def sendRequest(self, AreaCode :str , PhoneNumber:str ,proxy=None, userAgent=None )-> NewResponse:
        self.updateHeaders({'user-agent':userAgent}) if userAgent != None else None
        return self.post(
            timeout = 15 ,
            json = self.getPayload(
                AreaCode = AreaCode , 
                PhoneNumber = PhoneNumber ,
            ) , 
            proxies=proxy ,
            AreaCode =  AreaCode, 
            PhoneNumber = PhoneNumber,
        )

    def getAccount(self, AreaCode :str, PhoneNumber:str, proxy=None)-> list:
        response = self.sendRequest(AreaCode,PhoneNumber,proxy,self.gen.getRandomUserAgent())
        jsonData = response.json() if response.status_code != 429 else {}
        if response.status_code == 200 :
            if 'elements' in jsonData['response'].keys() :
                serverMsg = jsonData['response']['elements'][0]['label']
            elif 'payment_details' in jsonData['response'].keys():
                serverMsg = jsonData['response']['payment_details'][-1]['value']
            else :
                serverMsg = str(jsonData['response'])
        elif response.status_code == 400 :
            if jsonData['code'] == "FAILED" or jsonData['code'] == "INVALID_FIELDS" or jsonData['code'] == "INVALID_REQUEST"  :
                serverMsg = str(jsonData['response'])
            else :
                serverMsg = str(jsonData)
        elif response.status_code == 429 :
            raise IPAddressBanned
            serverMsg = "IP Address Have Banned"
        else :
            serverMsg = response.text
        return [response.AreaCode,response.PhoneNumber,serverMsg]








