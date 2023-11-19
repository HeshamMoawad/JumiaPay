# Producer : K7 Team
# Hamada - Hesham

from PyQt5.QtCore import  QObject, QThread
from qmodels import (
    QThread ,
    QObject ,
    Checking ,
    pyqtSignal ,
    typing ,
    SharingDataFrame
)
from proxycollector import ProxyCollector
from JumiaPay import JumiaPay
import requests , json

def row(row)->dict:
    areacode = str(int(float(row[0])))
    if not (2 >= len(areacode) > 0 ):
        areacode = f"0{areacode}"
    return {
        'AreaCode' : areacode ,
        'PhoneNumber' : str(int(float(row[1]))),
    }


class Task(QThread):
    result = pyqtSignal(list)
    def __init__(self ,parent:'TasksContainer',sharingdata:SharingDataFrame,vendor:str,proxiesCollector:ProxyCollector, **kwargs) -> None:
        super().__init__()
        self.setParent(parent)
        self.sharingdata = sharingdata
        self.proxiesCollector = proxiesCollector
        self.checker = parent.checker
        self.__stop = False 
        self.__vendor = vendor
    
    def parent(self)-> 'TasksContainer' : return super().parent()

    def run(self) -> None: 
        self.jumia = JumiaPay(self.__vendor)
        while not self.sharingdata.empty and not self.__stop  :
            while not self.sharingdata.empty and not self.__stop  :
                self.searchFor()
                if self.sharingdata.empty :
                    self.__stop = True
                    

    def searchFor(self):
        research = True
        rowdata = row(self.sharingdata.get_row())
        while research :
            try :
                resault = self.jumia.getAccount(**rowdata,proxy=self.proxiesCollector.getProxy())
                print(resault)
                self.result.emit(resault)
                research = False
            except Exception as e : 
                #print(e)
                ...



    def __str__(self) -> str:
        return f"JumiaPayWorker(isRunning : {self.isRunning()})"
        
    def start(self) -> None:
        if not self.isRunning():
            return super().start(self.Priority.HighPriority)
    
    def stop(self):
        # if self.isRunning():
        self.__stop = True
        self.terminate()
        # self.wait()

    def delete(self):
        self.stop()
        # self.wait()
        self.deleteLater()

        
class TasksContainer(QObject):
    status = pyqtSignal(str)
    msg = pyqtSignal(str)
    result = pyqtSignal(list)


    def __init__(self,sharingdata:SharingDataFrame,proxyCollector:ProxyCollector,vendor:str,**kwargs) -> None:
        super().__init__()
        self.__tasks:typing.List[Task]= []
        self.sharingdata = sharingdata
        self.checker = Checking()
        self.proxyCollector = proxyCollector
        self.setVendor(vendor)

    @property
    def tasks(self)->typing.List[Task]:
        return self.__tasks
    
    def start(self,max:int):
        if not self.sharingdata.empty:
            if self.checker.isConnect():
                if self.sharingdata.rowCount() < max :
                    max = self.sharingdata.rowCount()
                for _ in range(max):
                    print(f"Running {_}")
                    task = Task(self , self.sharingdata, self.__vendor ,self.proxyCollector)
                    task.finished.connect(lambda : self.status.emit("OFF "))
                    task.result.connect(self.result.emit)
                    self.__tasks.append(task)
                    task.start()
                self.status.emit("ON ")
            else :
                self.msg.emit("No Internet Connection !!")
        else :
            self.msg.emit("No Data in Wating !")


    def stop(self):
        for task in self.__tasks : task.delete()
        self.__tasks.clear()       
        self.status.emit("OFF ")

    def isRunning(self):
        return True if len(self.__tasks) > 0 else False

    def setVendor(self,vendor:str):
        self.__vendor = vendor
        print(vendor)