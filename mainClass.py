# from requests.sessions import default_headers
from requests import Response
import pandas as pd
from Packages import (
    QObject , 
    pyqtSignal ,
    DateOperations ,
    Generator ,
    DataBase
)
import random,typing ,sqlite3,json,requests,openpyxl,datetime,pandas
from ProxyFilterClass import ProxyFilterAPI
import time

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

####################################################

class DataBaseConnection(DataBase):
    def __init__(self, vendor,relativepath: str = "Data\Database.db") -> None:
        super().__init__(relativepath)
        self.vendor = vendor

#-------------------------------------------------------------------
    def addCustomer(self,**kwargs):
        self.addToDataAsDict(
            table = self.vendor ,
            **kwargs
            )
        
#--------------------------------------------------------------------        
    def reshapeExelData(self,excelfile,sheetname):
        wb = openpyxl.load_workbook(excelfile)
        ws = wb[sheetname]
        df = pd.DataFrame(ws.values)
        response = []
        for row in df.index:
            res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
            response.append(res)
        return response[1:]

###############################################################

class LeadObjectFirst(object):
    def __init__(self,Response:dict) -> None:
        self.Response = Response
        self.Data = DataBaseConnection('Data\DataBase.db')
        self.Date = DateOperations() 
        self.DateScraping = self.Date.getCurrentDate()
        self.goNext = True
        self.statusOfResponse = Response["code"]  # "SUCCESS"
        try:
            self.Price = Response["response"]["elements"][0]["label"].split("EGP")[0].split(" ")[-2]
        except Exception as e :
            try:
                self.Price = Response["response"]["elements"][0]["label"]
                print(f"error in and fixed  {e} with response {self.Price}")
            except Exception as e :
                print(f"error in {e} with response {self.Response}")
                self.Price = "can't get Price"
        self.ServerMsg = Response["response"]["elements"][0]["label"]
        self.AreaCode = Response['AreaCode']
        self.PhoneNumber = Response['PhoneNumber']
        self.HasUnpaidInvoices = 'يوجد فاتورة' 
        self.TimeScraping = str(round(Response['TimeScraping'],ndigits =2)) # Response['TimeScraping'] 
        

    def __str__(self) -> str:
        return str(self.dictOfObject)
        
    @property
    def dictOfObject(self)->dict:
        return self.__dict__

############################################

class LeadObjectSec(object):
    def __init__(self,Response:dict) -> None:
        self.Response = Response
        self.Data = DataBaseConnection('Data\DataBase.db')
        self.Date = DateOperations() 
        self.DateScraping = self.Date.getCurrentDate()
        self.goNext = True
        self.statusOfResponse = Response["code"]  # "SUCCESS"
        self.Price = str(Response["response"]['payment_details'][0]['raw_value'])
        self.ServerMsg = 'Redirect Page' #Response["response"]["elements"][0]["label"]
        self.AreaCode = Response['AreaCode']
        self.PhoneNumber = Response['PhoneNumber']
        self.HasUnpaidInvoices = 'يوجد فاتورة' 
        self.TimeScraping = str(round(Response['TimeScraping'],ndigits =2)) # Response['TimeScraping'] 

    def __str__(self) -> str:
        return str(self.dictOfObject)
        
    @property
    def dictOfObject(self)->dict:
        return self.__dict__

############################################

class LeadObjectNoClient(object):
    def __init__(self,Response:dict) -> None:
        self.Response = Response
        self.Data = DataBaseConnection('Data\DataBase.db')
        self.Date = DateOperations() 
        self.DateScraping = self.Date.getCurrentDate()
        self.goNext = True
        self.statusOfResponse = Response["code"]  # "INVALID_FIELDS"
        self.Price = str(None)
        self.ServerMsg = Response['response'] #Response["response"]["elements"][0]["label"]
        self.AreaCode = Response['AreaCode']
        self.PhoneNumber = Response['PhoneNumber']
        self.HasUnpaidInvoices = 'لايوجد'
        self.TimeScraping = str(round(Response['TimeScraping'],ndigits =2)) # Response['TimeScraping'] 

    def __str__(self) -> str:
        return str(self.dictOfObject)
        
    @property
    def dictOfObject(self)->dict:
        return self.__dict__

############################################

class LeadObjectUndefined(object):
    def __init__(self,Response:dict) -> None:
        self.Response = Response
        self.Data = DataBaseConnection('Data\DataBase.db')
        self.Date = DateOperations() 
        self.DateScraping = self.Date.getCurrentDate()
        self.goNext = True
        self.statusOfResponse = f'Undefined-{Response}'  # "INVALID_FIELDS"
        self.Price = str(None)
        self.ServerMsg = Response["response"] if 'response' in Response.keys() else "Undefined Message"   #Response["response"]["elements"][0]["label"]
        self.AreaCode = Response['AreaCode']
        self.PhoneNumber = Response['PhoneNumber']
        self.HasUnpaidInvoices = "Undefined"
        self.TimeScraping = str(round(Response['TimeScraping'],ndigits =2)) # Response['TimeScraping'] 

    def __str__(self) -> str:
        return str(self.dictOfObject)
        
    @property
    def dictOfObject(self)->dict:
        return self.__dict__

###############################################################



class JumiaPay(QObject):
    Lead = pyqtSignal(dict)
    msg = pyqtSignal(str)
    stop = pyqtSignal(bool)

    DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    
    class ResponseStatus():
        Success = 'SUCCESS'
        INVALID_FIELDS = 'INVALID_FIELDS'
        Faild = 'FAILED'

    class ResponseLength():
        Normal = 6
        Second = 5

    class Flags():
        RandomUserAgent = 'RandomUserAgent'
        RandomProxy = 'RandomProxy'

    class Vendors():
        We = 'WE'
        Etisalat = 'Etisalat'
        Orange = 'Orange'
        Noor = 'Noor'
        All = [We,Etisalat,Orange,Noor]

    def __init__(self,vendor:str) -> None:
        self.vendor = vendor
        self.URLs = {
        'WE':"https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman" ,
        'Etisalat' : "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.etisalat@aman" ,
        'Orange' : "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.bill.orangedsl@fawry" ,
        'Noor' : "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.bill.nooradsl@fawry"
        }
        self.Headers = {
        'WE':{
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
                'accept': 'application/json, text/plain, */*' ,
                'accept-encoding': 'gzip, deflate, br' ,
                'accept-language': 'en' ,
                'content-length': '655' ,
                'content-type': 'application/json;charset=UTF-8' ,
                'origin': 'https://pay.jumia.com.eg' ,
                'referer': 'https://pay.jumia.com.eg/services/internet-bills' ,
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
            } ,

        'Orange' : {
                'accept': 'application/json, text/plain, */*' ,
                'accept-encoding': 'gzip, deflate, br' ,
                'accept-language': 'en' ,
                'content-length': '890' ,
                'content-type': 'application/json;charset=UTF-8' ,
                'origin': 'https://pay.jumia.com.eg' ,
                'referer': 'https://pay.jumia.com.eg/services/internet-bills' ,
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
            },
        
        'Noor' : {
                'accept': 'application/json, text/plain, */*' ,
                'accept-encoding': 'gzip, deflate, br' ,
                'accept-language': 'en' ,
                'content-length': '888' ,
                'content-type': 'application/json;charset=UTF-8' ,
                'origin': 'https://pay.jumia.com.eg' ,
                'referer': 'https://pay.jumia.com.eg/services/internet-bills' , 
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
            }
        }
        payloadsfile = open("json\payloads.json","r")
        self.Payloads = json.load(payloadsfile)
        self.generator = Generator()
        self.Proxies = []
        self.Errors = []
        # ------------- Prapares ----------------
        self.header = self.Headers[self.vendor]
        self.payload = self.Payloads[self.vendor]
        # ------------- Database Connections ------------------
        self.Data = DataBaseConnection(vendor)
        self.ProxyAPI = ProxyFilterAPI()

        super().__init__()


    def convertDataframeToPhonesList(self,df:pandas.DataFrame)->list:
        response = []
        for row in range(0,len(df)):
            res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
            if f"{df.iloc[row]}" != 'None' :
                response.append(res)
        return response


    def sendRequest(self,AreaCode:str,PhoneNumber:str,proxy:typing.Optional[dict]=None,userAgent:typing.Optional[str]=None) -> Response:
        if len(AreaCode) == 1 :
            AreaCode = f'0{AreaCode}'

        session = requests.Session()
        session.proxies = proxy if proxy != None else {}
        # UserAgent Logic Method 
        if userAgent != None :
            if userAgent == self.Flags.RandomUserAgent:
                userAgent = self.generator.getRandomUserAgent() #self.getRandomUserAgent()
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
        payload['payload']['phone_number'] = f"EG_+20{AreaCode}{PhoneNumber}" # EG_+2035242441  # "EG_+20402917386"
        return payload


    def solveResponse(self,response:dict)-> dict:
        print("-"*20)
        print(response)
        if response['code'] == self.ResponseStatus.Success :
            if len(response['response']) == self.ResponseLength.Normal:
                Lead = LeadObjectFirst(response)
                print(f"First-{Lead.dictOfObject}")
                self.Lead.emit(Lead.dictOfObject)
                self.Data.addCustomer(**Lead.dictOfObject)
            elif len(response['response']) == self.ResponseLength.Second :
                Lead = LeadObjectSec(response)
                print(f"Sec-{Lead.dictOfObject}")
                self.Lead.emit(Lead.dictOfObject)
                self.Data.addCustomer(**Lead.dictOfObject)
        elif response['code'] == self.ResponseStatus.INVALID_FIELDS :
            if len(response) == 7 :
                Lead = LeadObjectNoClient(response)
                print(f"NoClient-{Lead.dictOfObject}")
                self.Lead.emit(Lead.dictOfObject)
                self.Data.addCustomer(**Lead.dictOfObject)
            else :
                Lead = LeadObjectUndefined(response)
                print(f"Undefined 'INVALID_FIELDS' ({len(Lead.Response)})- {Lead.Response}")
                try:
                    with open(f'Data\Errors\\{Lead.AreaCode+Lead.PhoneNumber}.txt','w+') as file :
                        file.write(f"Undefined 'INVALID_FIELDS' ({len(Lead.Response)})- {Lead.Response}")
                        file.close()
                except Exception as e :
                    print(e)
                self.Lead.emit(Lead.dictOfObject)
                self.Data.addCustomer(**Lead.dictOfObject)
        elif response['code'] == self.ResponseStatus.Faild :
            Lead = LeadObjectUndefined(response)
            print(f"Undefined '{self.ResponseStatus.Faild}' ({len(Lead.Response)})- {Lead.Response}")
            try:
                with open(f'Data\Errors\\{Lead.AreaCode+Lead.PhoneNumber}.txt','w+') as file :
                    file.write(f"Undefined '{self.ResponseStatus.Faild}' ({len(Lead.Response)})- {Lead.Response}")
                    file.close()
            except Exception as e :
                print(e)
            self.Lead.emit(Lead.dictOfObject)
            self.Data.addCustomer(**Lead.dictOfObject)
        else :
            Lead = LeadObjectUndefined(response)
            print(f"Global Undefined ({len(Lead.Response)}) - {Lead.Response}")
            try:
                with open(f'Data\Errors\\{Lead.AreaCode+Lead.PhoneNumber}.txt','w+') as file :
                    file.write(f"Global Undefined ({len(Lead.Response)}) - {Lead.Response}")
                    file.close()
            except Exception as e :
                print(e)
            self.Lead.emit(Lead.dictOfObject)
            self.Data.addCustomer(**Lead.dictOfObject)





