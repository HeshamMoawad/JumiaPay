import threading as thr
import numpy as np
import requests , random
from bs4 import BeautifulSoup
from PyQt5.QtCore import  QThread , pyqtSignal

from concurrent.futures import ThreadPoolExecutor
import multiprocessing

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

class ProxyCollector(QThread): # From  https://free-proxy-list.net/ 
    status = pyqtSignal(str)
    filled = pyqtSignal()

    Yes = 'yes'
    No = 'no'
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    

    def __init__(self) -> None:
        super().__init__()
        self.Threads = []  # List Of Threads that is Working
        self.Errors = []  # Errors in https request 
        self.tempProxiesList = []
        self.ProxiesList = [] # Good Proxies
        self.__stop = False
        self.__proxiesIndex = 0
        
    def run(self) -> None:
        while not self.__stop :
            self.autoAPI(True)
            print(f"Length of Proxies is -> {len(self.tempProxiesList)}")
            self.filled.emit()
            self.sleep(20)

    def getProxy(self)-> dict :
        try :
            ip_port = self.tempProxiesList[self.__proxiesIndex]
            self.__proxiesIndex = int(self.__proxiesIndex+1) if self.__proxiesIndex <= len(self.tempProxiesList)-2 else 0
            return self.__getProxyDict(ip_port=ip_port)
        except Exception as e :
            return self.__getProxyDict(ip_port=random.choice(self.tempProxiesList))
    
    def __getProxyDict(self,ip_port):
        return {'http':ip_port,'https':ip_port}

    def getFreshProxyList(
        self,
        httpsFilter:str ,
        ExportToTXT:bool= False ,
        ):
        ProxyList = []
        breaked = True
        while breaked :
            try:
                response = requests.get(url = 'https://free-proxy-list.net/')
                breaked = False
            except Exception as e: ...
        soup = BeautifulSoup(response.text,'html.parser')
        table = soup.find("tbody")
        rows = table.find_all("tr")
        for row in rows :
            row = row.find_all('td')
            ip = row[0].text
            port = row[1].text
            https = row[6].text
            if https == httpsFilter :
                ip_port = f"{ip}:{port}"
                ProxyList.append(ip_port)
        # if ExportToTXT == True :
        #     with open("Proxies.txt",'w+')as file :
        #         file.writelines([ip_port+"\n" for ip_port in ProxyList])
        #         file.close()
        return ProxyList

    def testProxy(self,ip_port_list:list):
        for ip_port in ip_port_list :
            print(ip_port)
            try:
                response = requests.get(url = "http://httpbin.org/ip",proxies= self.__getProxyDict(ip_port) ,timeout = 6)
                self.ProxiesList.append(ip_port)
            except Exception as e :
                self.Errors.append(e)


    def threadingRequstFilter(self,ip_portLists):
        # with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor :
        #     self.futures = [executor.submit(self.testProxy, ip_port) for ip_port in ip_portLists]
        # for f in self.futures :
        #     result = f.result()
        #     print(result)
        array_of_lists = np.array_split(ip_portLists,200)
        for iplist in array_of_lists:
            task = thr.Thread(target = self.testProxy,args = (iplist,))
            self.Threads.append(task)
            task.start()

    def wait(self)-> None:
        for task in self.Threads:
            if task.is_alive() :
                task.join()

    def autoAPI(self,wait:bool= True):
        self.ProxiesList.clear()
        self.Threads.clear()
        firstlist =  self.getFreshProxyList(self.Yes) + self.getFreshProxyList_2() + self.getFreshProxyList_6()
        self.threadingRequstFilter(firstlist)
        if wait == True :
            self.wait()
        self.tempProxiesList = self.ProxiesList.copy()
        return self.tempProxiesList
        
    def getFreshProxyList_2(self):
        ProxyList = []
        breaked = True
        while breaked :
            try:
                response = requests.get(url = 'https://www.sslproxies.org/' )
                breaked = False
            except Exception as e: ...
        soup = BeautifulSoup(response.text,'html.parser')
        table = soup.find("tbody")
        rows = table.find_all("tr")
        for row in rows :
            row = row.find_all('td')
            ip = row[0].text
            port = row[1].text
            https = row[6].text
        # if https == self.Yes :
            ip_port = f"{ip}:{port}"
            ProxyList.append(ip_port)
        return ProxyList
    
    def getFreshProxyList_3(self): # no
        ProxyList = []
        breaked = True
        while breaked :
            try:
                response = requests.get(url = 'https://www.us-proxy.org/')
                breaked = False
            except Exception as e: ...
        soup = BeautifulSoup(response.text,'html.parser')
        table = soup.find("tbody")
        rows = table.find_all("tr")
        for row in rows :
            row = row.find_all('td')
            ip = row[0].text
            port = row[1].text
            https = row[6].text
        if https == self.Yes :
            ip_port = f"{ip}:{port}"
            ProxyList.append(ip_port)
        return ProxyList

    def getFreshProxyList_4(self): # no
        ProxyList = []
        breaked = True
        while breaked :
            try:
                response = requests.get(url = 'https://free-proxy-list.net/anonymous-proxy.html')
                breaked = False
            except Exception as e: ...
        soup = BeautifulSoup(response.text,'html.parser')
        table = soup.find("tbody")
        rows = table.find_all("tr")
        for row in rows :
            row = row.find_all('td')
            ip = row[0].text
            port = row[1].text
            https = row[6].text
        if https == self.Yes :
            ip_port = f"{ip}:{port}"
            ProxyList.append(ip_port)
        return ProxyList

    def getFreshProxyList_5(self):
        breaked = True
        while breaked :
            try:
                response = requests.get(url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=https')
                breaked = False
            except Exception as e: ...
        return [ip_port for ip_port in response.text.splitlines()]

    def getFreshProxyList_6(self):
        breaked = True
        while breaked :
            try:
                response = requests.get(url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http')
                breaked = False
            except Exception as e: ...
        return [f"{ip_port}" for ip_port in response.text.splitlines()]
