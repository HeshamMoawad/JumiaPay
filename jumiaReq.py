import requests as req
import json
# from ProxyFilterClass import ProxyFilterAPI



url = "http://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman"

# # proxy = {'http': 'http://173.244.200.156:64631', 'https': 'https://173.244.200.156:64631'}
# proxy = {
#     'http': 'http://41.33.47.147:1981', 
#     'https': 'https://41.33.47.147:1981'
#     }


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en',
    'content-length': '890',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': '_gcl_au=1.1.1770403842.1674681967; userLanguage=en_EG; _fbp=fb.2.1674681967920.197242572; _ga=GA1.3.1606906537.1674681968; jpay_app_tmx_session_id=62f641fc-6566-472a-95ae-14c2022999c3; _gid=GA1.3.1389614948.1674779779; __cf_bm=k4lbN_qWTVFM2HahnaS0i0Kqp3A1Nx6YH0ZruAjGl0U-1674779780-0-AZKIvzfbCFSgqrzGILmtAr5rlakQyQr1LQR8NM2aCwAVM9Evc5R0eNKdLnkKcTDwivubwCf5OxRaK8IhIRDFSO7MXxjszic0YFTeujzHFzBb2Cb38uVzk6YN0wXXq1K0nxLaZ6Q7Q3VJvnWDOYgqvFQA5E+Eot3VCQjlStnh5YrwF1b+FiYoysacvDBO5SswGw==; _gat_UA-60910804-8=1',
    'origin': 'https://pay.jumia.com.eg',
    'referer': 'https://pay.jumia.com.eg/services/internet-bills',
    # 'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest':'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.117 Mobile Safari/537.36',
    # 'x-device-id': 'device-hash',
    # 'x-device-version': 'Web',
}

file = open("json\payloads.json",'r')
jsondata = json.load(file)['WE']
print("-----")
print(type(jsondata))
print("-----")


s = req.Session()
# s.proxies = proxy
s.headers = headers
res = s.post(
    url = url, 
    json = jsondata,
    

)

print(res.status_code)

response = res.json()



# "StatusOfResponse"	TEXT,
# "AreaCode"	TEXT,
# "PhoneNumber"	TEXT,
# "HasUnpaidInvoices"	TEXT,
# "Price"	TEXT




# First Response (Normal)
statusOfResponse = response["code"]  # "SUCCESS"
Price = response["response"]["elements"][0]["label"].split("EGP")[0].split(" ")[-2] 
AreaCode = response["response"]["payload"]["phone_number"].split('+2')[-1][:2]
PhoneNumber = response["response"]["payload"]["phone_number"].split('+2')[-1][2:]
HasUnpaidInvoices = str(True)




# Second Response 
statusOfResponse = response["code"] # "SUCCESS"
Price = str(response["response"]['payment_details'][0]['raw_value'])
AreaCode = response["response"]['order_details'][1]['raw_value'].split("+20")[-1][:2]
PhoneNumber = response["response"]['order_details'][1]['raw_value'].split("+20")[-1][2:]
HasUnpaidInvoices = str(True)



# ClientNotFound
statusOfResponse = response['code']  # 'INVALID_FIELDS'
Price = str(None)
AreaCode = AreaCode
PhoneNumber = PhoneNumber 
HasUnpaidInvoices = str(False)


URLs = {
    'WE':"https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman" ,
    'Etisalat' : "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.etisalat@aman" ,
    'Orange' : "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.bill.orangedsl@fawry" ,
    'Noor' : "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.bill.nooradsl@fawry"
}

headers = {
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





WEURL = "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman"
WEheader = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en',
    'content-length': '890',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://pay.jumia.com.eg',
    'referer': 'https://pay.jumia.com.eg/services/internet-bills',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.117 Mobile Safari/537.36',
}
EtisalatURL = "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.etisalat@aman"
Etisalatheader = {
    'accept': 'application/json, text/plain, */*' ,
    'accept-encoding': 'gzip, deflate, br' ,
    'accept-language': 'en' ,
    'content-length': '655' ,
    'content-type': 'application/json;charset=UTF-8' ,
    'origin': 'https://pay.jumia.com.eg' ,
    'referer': 'https://pay.jumia.com.eg/services/internet-bills' ,
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
}
OrangeURL = "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.bill.orangedsl@fawry"
Orangeheader = {
    'accept': 'application/json, text/plain, */*' ,
    'accept-encoding': 'gzip, deflate, br' ,
    'accept-language': 'en' ,
    'content-length': '890' ,
    'content-type': 'application/json;charset=UTF-8' ,
    'origin': 'https://pay.jumia.com.eg' ,
    'referer': 'https://pay.jumia.com.eg/services/internet-bills' ,
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
}
NoorURL = "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.bill.nooradsl@fawry"
Noorheader = {
    'accept': 'application/json, text/plain, */*' ,
    'accept-encoding': 'gzip, deflate, br' ,
    'accept-language': 'en' ,
    'content-length': '888' ,
    'content-type': 'application/json;charset=UTF-8' ,
    'origin': 'https://pay.jumia.com.eg' ,
    'referer': 'https://pay.jumia.com.eg/services/internet-bills' , 
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
}
