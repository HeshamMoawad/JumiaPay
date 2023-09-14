
# import requests
# from bs4 import BeautifulSoup as soup
# import threading as thr
# import time , os
# import json,requests , random 
# import numpy as np
# from requests.exceptions import ConnectionError , ReadTimeout 
# # import requests
# # from bs4 import BeautifulSoup
# import numpy
# import concurrent.futures


# # url = 'https://www.socks-proxy.net/'
# # response = requests.get(url)
# # bsobj = soup(response.content)
# # proxies= set()
# # for ip in bsobj.findAll('table')[0].findAll('tbody')[0].findAll('tr'):
# #   cols = ip.findChildren(recursive = False)
# #   cols = [element.text.strip() for element in cols]
# #   #print(cols)
# #   proxy = ':'.join([cols[0],cols[1]])
# #   proxy = 'socks4://'+proxy
# #   proxies.add(proxy)
# #   print(proxy)
# ##################################################################
# # class ProxyFilterAPI(object): # From  https://free-proxy-list.net/ 
# #     Yes = 'yes'
# #     No = 'no'
# #     class ProxyFlags():
# #         RandomProxy = 'RandomProxy'
# #         NoProxy = 'NoProxy'

# #     def __init__(self) -> None:
# #         self.Threads = []  # List Of Threads that is Working
# #         self.Errors = []  # Errors in https request 
# #         self.ProxiesList = [] # Good Proxies
# #         self.start = 0
# #         self.end = 0
# #         self.phoneslist = []
# #         self.index = 0


# #     def getFreshProxyList(self)->list:
# #         ProxyList = []
# #         url = 'https://www.socks-proxy.net/'
# #         response = requests.get(url)
# #         bsobj = soup(response.content,'html.parser')
# #         for ip in bsobj.findAll('table')[0].findAll('tbody')[0].findAll('tr'):
# #             cols = ip.findChildren(recursive = False)
# #             cols = [element.text.strip() for element in cols]
# #             #print(cols)
# #             proxy = ':'.join([cols[0],cols[1]])
# #             proxy = 'socks4://'+proxy
# #             ProxyList.append(proxy)
# #         print(len(ProxyList))
# #         return ProxyList

# #     def setPhones(self,phones):
# #         self.phoneslist = phones


# #     def threadingRequstFilter(self,ip_portLists):
# #         for iplist in ip_portLists:
# #             task = thr.Thread(target = self.testProxy,args = (iplist,))
# #             self.Threads.append(task)
# #             task.start()

# #     def wait(self)-> None:
# #         for task in self.Threads:
# #             if task.is_alive() :
# #                 task.join()

# #     def autoAPI(self,wait:bool= True):
# #         self.ProxiesList = []
# #         firstlist = self.getFreshProxyList()
# #         self.threadingRequstFilter(firstlist)
# #         if wait == True :
# #             self.wait()
# #         print(f"phones = {len(self.phoneslist)} maxindex = {self.index}")
# #         with open('proxies.txt','w+') as file :
# #             file.writelines(self.ProxiesList)
# #         return self.ProxiesList
        
            

# ###################################################################


# os.system('cls')
# print("-"*20)



# class JumiaThread(object):

#     url = "https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman"

#     header = {
#             'accept': 'application/json, text/plain, */*' ,
#             'accept-encoding': 'gzip, deflate, br' ,
#             'accept-language': 'en' ,
#             'content-length': '890' ,
#             'content-type': 'application/json;charset=UTF-8' ,
#             'origin': 'https://pay.jumia.com.eg' ,
#             'referer': 'https://pay.jumia.com.eg/services/internet-bills' ,
#             'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' ,
#             }

#     payloadsfile = open("json\payloads.json","r")

#     Payloads = json.load(payloadsfile)

#     def __init__(self,Phones:list,vendor='WE') -> None:
#         self.PhonesList = Phones
#         self.ProxiesList = self.getFreshProxyList()
#         self.Payload = self.Payloads[vendor]
#         self.Threads = []
#         self.ThreadsCount = 300
#         self.PhonesSuccess = []


#     def getFreshProxyList(self)->list:
#         ProxyList = []
#         url = 'https://www.socks-proxy.net/'
#         response = requests.get(url)
#         bsobj = soup(response.content,'html.parser')
#         for ip in bsobj.findAll('table')[0].findAll('tbody')[0].findAll('tr'):
#             cols = ip.findChildren(recursive = False)
#             cols = [element.text.strip() for element in cols]
#             proxy = ':'.join([cols[0],cols[1]])
#             proxy = 'socks4://'+proxy
#             ProxyList.append(proxy)
#         print(len(ProxyList))
#         self.ProxiesList = ProxyList
#         return ProxyList
    
        
#     def tryProxy(self):
#         while self.PhonesList != [] :
#             print("\nMain While Loop ------\n")
#             for phone in self.PhonesList :
#                 proxies = self.getProxies()
#                 print(f"{len(proxies)}-> {phone} <-")
#                 self.getPhoneResponse(phone,proxies)

#     def getProxies(self):
#         if self.ProxiesList == []:
#             return self.getFreshProxyList()
#         else:
#             return self.ProxiesList

#     def payload(self,phone):
#         payload = self.Payload
#         payload['payload']['phone_number'] = f"EG_+20{phone}"
#         return payload

#     def getPhoneResponse(self,phone,proxies):
#         for proxy in  proxies :
#             try:
#                 response = requests.post(self.url,proxies={"http": proxy, "https": proxy},headers=self.header,json=self.payload(phone),timeout=4)
#                 if response.status_code == 200 :
#                     print(f"{proxy}-{phone}-{response}-{response.json()}-successful\n")
#                     self.PhonesList.remove(phone)
#                     self.PhonesSuccess.append(phone)
#                     self.ProxiesList.append(proxy)
#                     break
#                 elif response.status_code == 400 :
#                     print(f"{proxy}-{phone}-{response}-{response.json()}-successful ")
#                     self.ProxiesList.append(proxy)
#                     self.PhonesList.remove(phone)
#                     self.PhonesSuccess.append(phone)
#                     break
#             except ConnectionError :
#                 pass
#             except ReadTimeout :
#                 pass
#             except Exception as e :
#                 print(e)
#                 pass
        

numbers = """402443513
552639347
0224734212
473308950
502550140
402443114
402141884
553415117
402143833
473282745
483421555
553677582
553382765
403273650
403270849
482912387
402443513
482915595
403273261
552639347
0224734212
473308950
502550140
""".splitlines()



# t1 = time.time()

# threads = []
# threadsCount = 100
# apis = []

# print(f"{threadsCount} Threads | {len(phonesList)} Phone")
# def multithreads(phones__):
#     api = JumiaThread(phones__)
#     apis.append(api)
#     api.tryProxy()
    

# phones_____ = np.array_split(phonesList,threadsCount)

# # for  phones in  phones_____ :
# #     thread = thr.Thread(target=multithreads,args=(list(phones),))
# #     threads.append(thread)
# #     thread.start()

# # for thread in threads:
# #     if thread.is_alive() :
# #         thread.join()

    

# t2 = time.time()

# successlists = []

# lists = [api.PhonesSuccess for api in apis]

# for phone in lists: successlists.append(phone)

# success = []

# for i in successlists : success += i

# print(f"Total time to make total {len(phonesList)} success {len(success)} is {t2-t1} Sec")
# print(success)



import requests
from bs4 import BeautifulSoup
import json , random , time , numpy
import concurrent.futures


payloadsfile = open("json\payloads.json","r")
Payloads = json.load(payloadsfile)
payload = Payloads["WE"]

t1 = time.time()

def getFreshProxyList()->list:
    ProxyList = []
    url = 'https://www.socks-proxy.net/'
    response = requests.get(url)
    bsobj = BeautifulSoup(response.content,'html.parser')
    for ip in bsobj.findAll('table')[0].findAll('tbody')[0].findAll('tr'):
        cols = ip.findChildren(recursive = False)
        cols = [element.text.strip() for element in cols]
        proxy = ':'.join([cols[0],cols[1]])
        proxy = 'socks4://'+proxy
        ProxyList.append(proxy)
    return ProxyList


results = getFreshProxyList()
# Create proxies final list
# print(results)
final =[]
finalnumbers = []
# with open('proxies.txt','r') as file :
#     proxies = file.readlines()
#     file.close()

proxies = ["socks4://178.48.68.61:4145" , "socks4://203.210.210.99:5678" , "socks4://92.119.74.251:5678" , "socks4://37.228.65.107:51032" ,"socks4://185.186.39.79:5678" ,"socks4://124.109.44.126:4145","socks4://189.201.187.3:4145","socks4://1.9.167.36:60489","socks4://81.83.1.89:4153" , "socks4://187.44.211.118:4153" ,"socks4://122.129.112.209:4145" ,"socks4://103.169.130.52:5678" ,"socks4://213.222.34.200:4145" , "socks4://190.14.224.244:3629" , "socks4://202.179.184.44:5430" , "socks4://203.210.235.91:5678" , "socks4://167.71.241.136:33299" ,"socks4://186.1.182.194:4153" , "socks4://202.158.49.138:39172" , "socks4://177.22.33.33:4153" , "socks4://188.6.164.138:5678" , "socks4://45.65.65.18:4145" , "socks4://72.249.209.140:5678" , "socks4://79.106.246.174:4145" , "socks4://180.191.255.117:5678" , "socks4://103.233.154.18:4145" , "socks4://177.6.18.130:4153" , "socks4://202.21.113.86:4153" , "socks4://103.134.239.210:5678" , "socks4://103.140.35.11:4145" , "socks4://202.21.116.210:4153" , "socks4://201.159.103.97:31337" , "socks4://45.220.1.31:1080" , "socks4://200.0.247.86:4153" , "socks4://169.239.236.101:10801" , "socks4://179.159.134.228:4153" , "socks4://181.205.36.210:5678" , "socks4://202.131.246.250:5678" , "socks4://103.87.86.146:4153" , "socks4://167.99.151.120:5564" , "socks4://103.165.37.245:4145" , "socks4://103.26.209.206:11080" , "socks4://78.186.98.148:1080" ,"socks4://202.141.242.3:55544" , "socks4://190.216.56.1:4153" , "socks4://103.158.49.85:1088" , "socks4://213.6.244.178:4153" , "socks4://121.200.62.246:4153" , "socks4://212.200.118.254:4153" , "socks4://202.138.242.6:38373" , "socks4://200.116.198.140:37092" , "socks4://191.97.2.198:5678" , "socks4://188.212.41.158:4153" , "socks4://131.221.182.14:4153" , "socks4://27.74.243.242:5678" , "socks4://177.87.223.194:49233" , "socks4://47.243.95.228:10080" , "socks4://149.3.27.4:5678" , "socks4://36.89.218.67:1080" , "socks4://177.10.202.221:1080" , "socks4://181.48.83.114:4153" , "socks4://197.232.21.22:58253" , "socks4://149.3.27.4:5678" ]

def getpayload(phone):
    p = payload
    p['payload']['phone_number'] = f"EG_+20{phone}"
    return p




def test(data:list):
    data.reverse()
    for proxy in data :
        proxy =  proxy
        # proxy = ["socks4://178.48.68.61:4145" , "socks4://203.210.210.99:5678" , "socks4://92.119.74.251:5678" , "socks4://37.228.65.107:51032" ,"socks4://185.186.39.79:5678" ,"socks4://124.109.44.126:4145","socks4://189.201.187.3:4145","socks4://1.9.167.36:60489","socks4://81.83.1.89:4153" , "socks4://187.44.211.118:4153" ,"socks4://122.129.112.209:4145" ,"socks4://103.169.130.52:5678" ,"socks4://213.222.34.200:4145" , "socks4://190.14.224.244:3629" , "socks4://202.179.184.44:5430" , "socks4://203.210.235.91:5678" , "socks4://167.71.241.136:33299" ,"socks4://186.1.182.194:4153" , "socks4://202.158.49.138:39172" , "socks4://177.22.33.33:4153" , "socks4://188.6.164.138:5678" , "socks4://45.65.65.18:4145" , "socks4://72.249.209.140:5678" , "socks4://79.106.246.174:4145" , "socks4://180.191.255.117:5678" , "socks4://103.233.154.18:4145" , "socks4://177.6.18.130:4153" , "socks4://202.21.113.86:4153" , "socks4://103.134.239.210:5678" , "socks4://103.140.35.11:4145" , "socks4://202.21.116.210:4153" , "socks4://201.159.103.97:31337" , "socks4://45.220.1.31:1080" , "socks4://200.0.247.86:4153" , "socks4://169.239.236.101:10801" , "socks4://179.159.134.228:4153" , "socks4://181.205.36.210:5678" , "socks4://202.131.246.250:5678" , "socks4://103.87.86.146:4153" , "socks4://167.99.151.120:5564" , "socks4://103.165.37.245:4145" , "socks4://103.26.209.206:11080" , "socks4://78.186.98.148:1080" ,"socks4://202.141.242.3:55544" , "socks4://190.216.56.1:4153" , "socks4://103.158.49.85:1088" , "socks4://213.6.244.178:4153" , "socks4://121.200.62.246:4153" , "socks4://212.200.118.254:4153" , "socks4://202.138.242.6:38373" , "socks4://200.116.198.140:37092" , "socks4://191.97.2.198:5678" , "socks4://188.212.41.158:4153" , "socks4://131.221.182.14:4153" , "socks4://27.74.243.242:5678" , "socks4://177.87.223.194:49233" , "socks4://47.243.95.228:10080" , "socks4://149.3.27.4:5678" , "socks4://36.89.218.67:1080" , "socks4://177.10.202.221:1080" , "socks4://181.48.83.114:4153" , "socks4://197.232.21.22:58253" , "socks4://149.3.27.4:5678" ]                              
        try:
            num = '402443513' #data['num']
            res = requests.post('https://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman', json=getpayload(num), proxies={'http' : proxy , 'https' : proxy}, timeout=5)
            final.append(proxy)
            finalnumbers.append({num:res.json()})
            print(f"{proxy} - succecss {res.json()}")
            # numbers.remove(num)
            
        except Exception as e:
            # results.remove(proxy)
            print(f"{proxy} notworking ... ")
            pass
        

# while numbers != [] :
#     print(f"------ ***********@ {len(numbers)} @*********** -------")
#     arr = numpy.array_split(results)
    
#     # test multiple proxies concurrently
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(test, numbers)

#     # to print the number of proxies
#     print(f"\n{final}-{len(final)}\n")
#     print(f"\n{finalnumbers}-{len(finalnumbers)}\n")
#     final.clear()
#     finalnumbers.clear()
#     results = getFreshProxyList()

test(proxies)
print(("-"*30) + f"{final}\n")
with open("filteredproxies.txt",'w+') as file :
    file.writelines(final)
    file.close()
    print("saved successfully")

print(f"{time.time()-t1} total time")

# save the working proxies to a file
# numpy.save('file.npy', final)



