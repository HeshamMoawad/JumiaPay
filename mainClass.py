# from requests.sessions import default_headers
from requests import Response
import pandas as pd
import threading as thr 
from MyPyQt5 import QObject , pyqtSignal
import random,typing ,re,sqlite3,json,requests,openpyxl 


####################################################

class DataBaseConnection(object):
    def __init__(self) -> None:
        self.con = sqlite3.connect("Data\Database.db")
        self.cur = self.con.cursor()
#--------------------------------------------------------------------
    def exist(self,table,value:dict) ->bool :
        if len(value) > 1 :
            add = f"AND {value.keys()[1]} = '{value.values()[1]}'"
        else :
            add = ""
        self.cur.execute(f"""SELECT * FROM {table} WHERE {value.keys()[0]} = '{value.values()[0]}' {add}; """)
        return True if self.cur.fetchall() != [] else False
    
#-------------------------------------------------------------------
    def addCustomer(self,vendor,**kwargs):
        try:
            self.cur.execute(f"""
            INSERT INTO {vendor} {str(tuple(kwargs.keys())).replace("'","")}
            VALUES {tuple(kwargs.values())}; 
            """)
            self.con.commit()
        except Exception as e:
            print(f"\n{e} \nError in addCustomer \n")

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



class JumiaPay(QObject):
    Lead = pyqtSignal(dict)
    
    DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    class ResponseStatus():
        Success = 'SUCCESS'
        Faild = 'INVALID_FIELDS'

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
        useragentfile = open("user-agents.txt",'r')
        self.UserAgentList =  useragentfile.readlines()
        # ------------- Prapares ----------------
        self.header = self.Headers[self.vendor]
        self.payload = self.Payloads[self.vendor]
        # ------------- Database Connections ------------------
        self.Data = DataBaseConnection()
    

        super().__init__()

    

    def sendRequest(self,AreaCode:str,PhoneNumber:str,proxy:typing.Optional[dict]=None,userAgent:typing.Optional[str]=None) -> Response:
        session = requests.Session()
        session.proxies = proxy if proxy != None else {}
        # UserAgent Logic Method
        if userAgent != None :
            if userAgent == self.Flags.RandomUserAgent:
                userAgent = self.getRandomUserAgent()
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
        self.header['user-agent']= userAgent
        print(self.header)
        session.headers = self.header
        session.proxies = proxy
        response = session.post(
            url = self.URLs[self.vendor],
            json = self.reshapePayload(
                AreaCode = AreaCode ,
                PhoneNumber = PhoneNumber ,
            ) ,
        )
        self.solveResponse(response)
        
        

    def getRandomUserAgent(self) -> str :
        return str(self.UserAgentList[random.randint(0,len(self.UserAgentList))]).replace("\n","")
        
        
    def getRandomProxy(self):
        pass

    def reshapePayload(self,AreaCode:str,PhoneNumber:str):
        payload = self.payload
        payload['payload']['phone_number'] = f"EG_+20{AreaCode}{PhoneNumber}" # EG_+2035242441  # "EG_+20402917386"
        return payload


    def solveResponse(self,AreaCode:str,PhoneNumber:str,response:Response)-> dict:
        response = response.json()
        Lead = {}
        if response['code'] == self.ResponseStatus.Success :
            if len(response['response']) == self.ResponseLength.Normal:
                # First Response (Normal)
                Lead['statusOfResponse'] = response["code"]  # "SUCCESS"
                Lead['Price'] = response["response"]["elements"][0]["label"].split("EGP")[0].split(" ")[-2] 
                Lead['AreaCode'] = response["response"]["payload"]["phone_number"].split('+2')[-1][:2]
                Lead['PhoneNumber'] = response["response"]["payload"]["phone_number"].split('+2')[-1][2:]
                Lead['HasUnpaidInvoices'] = str(True)

            elif len(response['response']) == self.ResponseLength.Second :
                # Second Response 
                Lead['statusOfResponse'] = response["code"] # "SUCCESS"
                Lead['Price'] = str(response["response"]['payment_details'][0]['raw_value'])
                Lead['AreaCode'] = response["response"]['order_details'][1]['raw_value'].split("+20")[-1][:2]
                Lead['PhoneNumber'] = response["response"]['order_details'][1]['raw_value'].split("+20")[-1][2:]
                Lead['HasUnpaidInvoices'] = str(True)

        elif response['code'] == self.ResponseStatus.Faild :
            # ClientNotFound
            Lead['statusOfResponse'] = response['code']  # 'INVALID_FIELDS'
            Lead['Price'] = str(None)
            Lead['AreaCode'] = AreaCode
            Lead['PhoneNumber'] = PhoneNumber 
            Lead['HasUnpaidInvoices'] = str(False)
        if not self.Data.exist(self.vendor,**{'PhoneNumber':Lead['PhoneNumber'],'AreaCode':Lead['AreaCode']}):
            self.Data.addCustomer(
                vendor = self.vendor ,
                **Lead
            )
        self.Lead.emit(Lead)
        return Lead

















