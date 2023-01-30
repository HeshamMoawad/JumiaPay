import threading as thr
import numpy as np
import requests 
from bs4 import BeautifulSoup 


class ProxyFilterAPI(object): # From  https://free-proxy-list.net/ 
    Yes = 'yes'
    No = 'no'

    def __init__(self) -> None:
        self.Threads = []  # List Of Threads that is Working
        self.Errors = []  # Errors in https request 
        self.ProxiesList = [] # Good Proxies

    def getFreshProxyList(
        self,
        httpsFilter:str ,
        ExportToTXT:bool= False ,
        ):
        ProxyList = []
        response = requests.get(url = 'https://free-proxy-list.net/')
        self.soup = BeautifulSoup(response.text,'html.parser')
        table = self.soup.find("tbody")
        rows = table.find_all("tr")
        for row in rows :
            row = row.find_all('td')
            ip = row[0].text
            port = row[1].text
            https = row[6].text
            #print(f"{ip}:{port} --> https:{https}")
            if https == httpsFilter :
                ip_port = f"{ip}:{port}"
                ProxyList.append(ip_port)
        if ExportToTXT == True :
            with open("Proxies.txt",'w+')as file :
                file.writelines([ip_port+"\n" for ip_port in ProxyList])
                file.close()
        return ProxyList


    def testProxy(self,ip_port):
        proxy = {'http':ip_port,'https':ip_port}
        try:
            response = requests.get(url = "http://httpbin.org/ip",proxies= proxy ,timeout = 5)
            self.ProxiesList.append(ip_port)
        except Exception as e :
            self.Errors.append(e)


    def threadingRequstFilter(self,ip_portLists):
        for iplist in ip_portLists:
            task = thr.Thread(target = self.testProxy,args = (iplist,))
            self.Threads.append(task)
            task.start()

    def wait(self)-> None:
        for task in self.Threads:
            if task.is_alive() :
                task.join()

    def autoAPI(self,wait:bool= True):
        firstlist = self.getFreshProxyList(httpsFilter=self.Yes)
        self.threadingRequstFilter(firstlist)
        if wait == True :
            self.wait()
        return self.ProxiesList
        

        

# if __name__ == "__main__":
#     proxy = Proxy()
#     proxy.run("127.0.0.1", 3000)


# import requests , json ,typing
# from bs4 import BeautifulSoup 

# url = "http://pay.jumia.com.eg/api/v3/utilities/service-form-type/internet.postpaid.wehome@aman"#'http://www.httpbin.org/ip'

# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'en',
#     'content-length': '890',
#     'content-type': 'application/json;charset=UTF-8',
#     'cookie': '_gcl_au=1.1.1770403842.1674681967; userLanguage=en_EG; _fbp=fb.2.1674681967920.197242572; _ga=GA1.3.1606906537.1674681968; jpay_app_tmx_session_id=62f641fc-6566-472a-95ae-14c2022999c3; _gid=GA1.3.1389614948.1674779779; __cf_bm=k4lbN_qWTVFM2HahnaS0i0Kqp3A1Nx6YH0ZruAjGl0U-1674779780-0-AZKIvzfbCFSgqrzGILmtAr5rlakQyQr1LQR8NM2aCwAVM9Evc5R0eNKdLnkKcTDwivubwCf5OxRaK8IhIRDFSO7MXxjszic0YFTeujzHFzBb2Cb38uVzk6YN0wXXq1K0nxLaZ6Q7Q3VJvnWDOYgqvFQA5E+Eot3VCQjlStnh5YrwF1b+FiYoysacvDBO5SswGw==; _gat_UA-60910804-8=1',
#     'origin': 'https://pay.jumia.com.eg',
#     'referer': 'https://pay.jumia.com.eg/services/internet-bills',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.117 Mobile Safari/537.36',
# }

# proxy = {
#     'http':  '135.181.14.45:5959',
#     'https': '135.181.14.45:5959',
# }



# file = open("payload.json",'r')
# jsondata = json.load(file)
# print("-----")
# print(type(jsondata))
# print("-----")


# r = requests.post(
#     url,
#     proxies=proxy,
#     headers= headers ,
#     json = jsondata 
#     )  
# print('   Tor IP:', r.json())
# print("-----"*20)

# r = requests.post(
#     url,
#     headers = headers ,
#     json = jsondata ,
#     )
# print('direct IP:', r.json())

# ---------------------------------------
# class FreshProxy():  # From  https://free-proxy-list.net/ 
#     Yes = 'yes'
#     No = 'no'

#     def __init__(self) -> None:
#         self.ProxyList = []

#     def getFreshProxyList(
#         self,
#         httpsFilter:str ,
#         ExportToTXT:bool= False ,
#         ):
#         response = requests.get(url = 'https://free-proxy-list.net/')
#         self.soup = BeautifulSoup(response.text,'html.parser')
#         table = self.soup.find("tbody")
#         rows = table.find_all("tr")
#         for row in rows :
#             row = row.find_all('td')
#             ip = row[0].text
#             port = row[1].text
#             https = row[6].text
#             print(f"{ip}:{port} --> https:{https}")
#             if https == httpsFilter :
#                 ip_port = f"{ip}:{port}"
#                 self.ProxyList.append(ip_port)
#         if ExportToTXT == True :
#             with open("Proxies.txt",'w+')as file :
#                 file.writelines([ip_port+"\n" for ip_port in self.ProxyList])
#                 file.close()

#         return self.ProxyList



# pr = FreshProxy()
# l = pr.getFreshProxyList(httpsFilter = pr.Yes,ExportToTXT=True)

# print(l)







# print(response.text)




# from vpn.controller import VPNServer

# # Instantiates the object, takes the same args as env vars.
# vpn_server = VPNServer()  # Defaults to console logging. Pass 'log="file"' for file logging.

# vpn_server.create_vpn_server()  # Create a VPN Server, login information will be saved to a JSON file.

# # Re-configure an existing VPN Server (not required, unless the configuration steps have been interrupted)
# # vpn_server.reconfigure_vpn()

# # Test an existing VPN Server (not required, as a test is run right after creation anyway)
# # vpn_server.test_vpn()

# vpn_server.delete_vpn_server()  # Deletes the VPN Server removing the AWS resources acquired during creation.



# import winreg

# def getProxy():
#     proxy = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings")
#     server, type = winreg.QueryValueEx(proxy, "ProxyServer")
#     enabled, type = winreg.QueryValueEx(proxy, "ProxyEnable")
#     if enabled:
#         return server
#     return None



# print(getProxy())

# from urllib import request as urlrequest

# proxy_host = '127.0.0.1:9050'    # host and port of your proxy
# url = 'http://www.httpbin.org/ip'

# req = urlrequest.Request(url)
# req.set_proxy(proxy_host, 'http')

# response = urlrequest.urlopen(req)
# print(response.read().decode('utf8'))


# print(urlrequest.getproxies())

