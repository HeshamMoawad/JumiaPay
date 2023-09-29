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





class JumiaPayOld(QObject):
    Lead = pyqtSignal(dict)
    msg = pyqtSignal(str)
    stop = pyqtSignal(bool)

    DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    
    def __init__(self,vendor:str) -> None:
        self.vendor = vendor
        self.URLs = {
            'WE': "internet.postpaid.wehome@aman",
            'Etisalat': "internet.postpaid.etisalat@aman",
            'Orange': "internet.bill.orangedsl@fawry",
            'Noor': "internet.bill.nooradsl@fawry"
        }
        self.Headers = {
            'WE': {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en',
                'content-length': '890',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://pay.jumia.com.eg',
                'referer': 'https://pay.jumia.com.eg/services/internet-bills',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.117 Mobile Safari/537.36',
            },

            'Etisalat': {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en',
                'content-length': '655',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://pay.jumia.com.eg',
                'referer': 'https://pay.jumia.com.eg/services/internet-bills',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            },

            'Orange': {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en',
                'content-length': '890',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://pay.jumia.com.eg',
                'referer': 'https://pay.jumia.com.eg/services/internet-bills',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            },

            'Noor': {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en',
                'content-length': '888',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://pay.jumia.com.eg',
                'referer': 'https://pay.jumia.com.eg/services/internet-bills',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }
        }
        payloadsfile = open("json\payloads.json", "r")
        self.Payloads = json.load(payloadsfile)        
        self.Proxies = []
        self.Errors = []
        # ------------- Prapares ----------------
        self.header = self.Headers[self.vendor]
        self.payload = self.Payloads[self.vendor]
        # ------------- Database Connections ------------------
        super().__init__()


    def sendRequest(self,AreaCode:str,PhoneNumber:str,proxy:typing.Optional[dict]=None,userAgent:typing.Optional[str]=None) -> Response:
        if len(AreaCode) == 1 :
            AreaCode = f'0{AreaCode}'

        session = requests.Session()
        session.proxies = proxy if proxy != None else {}
        # UserAgent Logic Method 
        if userAgent != None :
            if userAgent == self.Flags.RandomUserAgent:
                userAgent = random.choice(self.UserAgentList) 
            else :
                userAgent = userAgent
        else :
            userAgent = self.DEFAULT_USER_AGENT

        # Proxy Logic Method 
        if proxy != None :
            if proxy == self.Flags.RandomProxy :
                proxy = self.getRandomProxy()
            else:
                proxy = proxy
        else :
            proxy = {}
        print(proxy)
        self.header['user-agent'] = userAgent
        session.headers = self.header
        session.proxies = proxy
        t1 = time.time()
        response = session.post(
            url = self.URLs[self.vendor],
            json = self.reshapePayload(
                AreaCode = AreaCode ,
                PhoneNumber = PhoneNumber ,
            ) ,
        )
        t2 = time.time()
        if response.status_code == 429 :
            self.msg.emit(f'خدنا بان يا اخوياااا -_-')
            self.stop.emit(True)
        try:
            response = response.json()
            con = True
        except Exception as e :
            con = False

        if con:
            response['PhoneNumber'] = PhoneNumber
            response['AreaCode'] = AreaCode
            response['TimeScraping'] = t2-t1

            self.solveResponse(
                response = response ,
                )
                

    def setProxies(self,Proxies):
        self.Proxies = Proxies
        
    def getRandomProxy(self):
        print(len(self.Proxies))
        return str(self.Proxies[random.randint(0,len(self.Proxies)-2)])

    def reshapePayload(self,AreaCode:str,PhoneNumber:str):
        payload = self.payload
        # EG_+2035242441  # "EG_+20402917386"
        payload['payload']['phone_number'] = f"EG_+20{AreaCode}{PhoneNumber}"
        return payload

    def solveResponse(self,AreaCode:str,PhoneNumber:str,response,time)-> dict:
        print("-"*20)
        if response.status_code == 429 :
            self.msg.emit(f'خدنا بان يا اخوياااااا -_-')
            self.stop.emit(True)
        else:
            try:
                response = response.json()
                con = True
            except Exception as e :
                con = False
            Lead = {}
            if con:
                if response['code'] == self.ResponseStatus.Success :
                    if len(response['response']) == self.ResponseLength.Normal:
                        # First Response (Normal)
                        Lead['statusOfResponse'] = response["code"]  # "SUCCESS"
                        Lead['Price'] = response["response"]["elements"][0]["label"].split("EGP")[0].split(" ")[-2] 
                        Lead['Server Message'] = response["response"]["elements"][0]["label"]
                        Lead['AreaCode'] = AreaCode #response["response"]["payload"]["phone_number"].split('+2')[-1][:2]
                        Lead['PhoneNumber'] = PhoneNumber #response["response"]["payload"]["phone_number"].split('+2')[-1][2:]
                        Lead['HasUnpaidInvoices'] = 'يوجد فاتورة'

                    elif len(response['response']) == self.ResponseLength.Second :
                        # Second Response 
                        Lead['statusOfResponse'] = response["code"] # "SUCCESS"
                        Lead['Price'] = str(response["response"]['payment_details'][0]['raw_value'])
                        Lead['Server Message'] = 'Redirect Page'
                        Lead['AreaCode'] = AreaCode #response["response"]['order_details'][1]['raw_value'].split("+20")[-1][:2]
                        Lead['PhoneNumber'] = PhoneNumber #response["response"]['order_details'][1]['raw_value'].split("+20")[-1][2:]
                        Lead['HasUnpaidInvoices'] = 'يوجد فاتورة'

                elif response['code'] == self.ResponseStatus.Faild :
                    # ClientNotFound
                    Lead['statusOfResponse'] = response['code']  # 'INVALID_FIELDS'
                    Lead['Price'] = str(None)
                    Lead['Server Message'] = response['response']
                    Lead['AreaCode'] = AreaCode
                    Lead['PhoneNumber'] = PhoneNumber 
                    Lead['HasUnpaidInvoices'] = 'لايوجد'

                Lead['DateScraping'] = f"{datetime.datetime.now().date()} |{datetime.datetime.now().hour}:{datetime.datetime.now().minute}"
                Lead['TimeScraping'] = str(round(time,ndigits =2))
                self.Data.addCustomer(
                    vendor = self.vendor ,
                    **Lead
                )
                self.Lead.emit(Lead)
            else:
                Lead['Price'] = str(None) #response["response"]["elements"][0]["label"].split("EGP")[0].split(" ")[-2] 
                Lead['AreaCode'] = AreaCode #response["response"]["payload"]["phone_number"].split('+2')[-1][:2]
                Lead['PhoneNumber'] = PhoneNumber #response["response"]["payload"]["phone_number"].split('+2')[-1][2:]
                Lead['Server Message'] = '' ########
                Lead['HasUnpaidInvoices'] = 'لايوجد فاتورة'
                self.Lead.emit(Lead)



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



    def sendRequest(self, AreaCode :str , PhoneNumber:str)-> NewResponse:
        return self.post(
            timeout = 20 ,
            json = self.getPayload(
                AreaCode = AreaCode , 
                PhoneNumber = PhoneNumber ,
            ) , 
            AreaCode =  AreaCode, 
            PhoneNumber = PhoneNumber,
        )

    def getAccount(self,AreaCode :str , PhoneNumber:str):
        ...