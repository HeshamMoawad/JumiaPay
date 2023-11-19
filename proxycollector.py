import threading as thr
import numpy as np
import requests , random , typing
from bs4 import BeautifulSoup
from PyQt5.QtCore import  QThread , pyqtSignal
from JumiaPay import JumiaPay
from qmodels import MyTableModel


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
def row(row)->dict:
    areacode = str(int(float(row[0])))
    if not (2 >= len(areacode) > 0 ):
        areacode = f"0{areacode}"
    return {
        'AreaCode' : areacode ,
        'PhoneNumber' : str(int(float(row[1]))),
    }


class Worker(QThread):
    def __init__(self , max:int ,sharingdata , vendor  , model:MyTableModel , proxycollector:'ProxyCollector', timeout :int = 5 ) -> None:
        super().__init__()
        self.sharingdata = sharingdata
        self.model = model
        self.max = max
        self.Threads:typing.List[thr.Thread] = []  # List Of Threads that is Working
        self.Errors = []  # Errors in https request 
        self.__stop = False
        self.proxycollector = proxycollector
        self.jumia = JumiaPay(vendor)
        self.timeout = timeout

    def run(self) -> None:
        self.autoAPI(True)

    def testProxy(self):
        while not self.sharingdata.empty  and not self.__stop :
            research = True
            rowdata = row(self.sharingdata.get_row())
            while research and not self.__stop  :
                try :
                    resault = self.jumia.getAccount(**rowdata,proxy=self.proxycollector.getProxy(), timeout=self.timeout)
                    print(resault)
                    self.model.addrow(resault)
                    research = False
                except Exception as e : 
                    # print(e)
                    ...

    def threadingRequstFilter(self):
        for _ in range(self.max):
            task = thr.Thread(target = self.testProxy)
            self.Threads.append(task)
            task.start()

    def wait(self)-> None:
        for task in self.Threads:
            if task.is_alive() :
                task.join()
        self.Threads.clear()

    def autoAPI(self,wait:bool= True):
        self.Threads.clear()
        self.threadingRequstFilter()
        if wait == True :
            self.wait()

    def stop(self):
        self.__stop = True

    def start(self, priority: QThread.Priority = ...) -> None:
        if not self.Threads :
            self.__stop = False
            return super().start(priority)
        
    def setVendor(self,vendor:str):
        self.jumia = JumiaPay(vendor)

    


class ProxyCollector(QThread): # From  https://free-proxy-list.net/ 
    status = pyqtSignal(str)
    filled = pyqtSignal()

    Yes = 'yes'
    No = 'no'
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    class Source:
        S1 = 's1'
        S2 = 's2'
        S3 = 's3'
        S4 = 's4'

    def __init__(self , waiting:int ,source:Source) -> None:
        super().__init__()
        self.ProxiesList = [] # Good Proxies
        self.__stop = False
        self.__proxiesIndex = 0
        self.waiting = waiting
        self.source = source

        
    def run(self) -> None:
        while True :
            self.fill()
            self.filled.emit()
            self.sleep(self.waiting)

    def getProxy(self)-> dict :
        try :
            ip_port = self.ProxiesList[self.__proxiesIndex]
            self.__proxiesIndex = int(self.__proxiesIndex+1) if self.__proxiesIndex <= len(self.ProxiesList)-2 else 0
            return self.__getProxyDict(ip_port=ip_port)
        except Exception as e :
            print(f"Error from getting proxy ==> {e}")
            return self.__getProxyDict(ip_port=random.choice(self.ProxiesList))
        
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
        if ExportToTXT == True :
            with open("Proxies.txt",'w+')as file :
                file.writelines([ip_port+"\n" for ip_port in ProxyList])
                file.close()
        return ProxyList
        
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

    def fill(self): 
        if self.source == self.Source.S1 :
            firstlist =  self.getFreshProxyList(self.Yes) #+ self.getFreshProxyList_2() + self.getFreshProxyList_5() + self.getFreshProxyList_6()
        elif self.source == self.Source.S2 :
            firstlist =  self.getFreshProxyList_2() #+ self.getFreshProxyList_5() + self.getFreshProxyList_6()
        elif self.source == self.Source.S3 :
            firstlist =  self.getFreshProxyList_5() #+ self.getFreshProxyList_6()
        elif self.source == self.Source.S4 :
            firstlist =  self.getFreshProxyList_6()
        else :
            firstlist = self.getFreshProxyList(self.Yes) + self.getFreshProxyList_2() + self.getFreshProxyList_5() + self.getFreshProxyList_6()
        # firstlist = ... #self.getFreshProxyList(self.Yes) + self.getFreshProxyList_2() + self.getFreshProxyList_5() + self.getFreshProxyList_6()
        self.ProxiesList.clear()
        self.ProxiesList += firstlist
        print(f"Get in {self.source} --> {len(self.ProxiesList)}")

