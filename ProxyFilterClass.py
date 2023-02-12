import threading as thr
import numpy as np
import requests 
from bs4 import BeautifulSoup 

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
        

