# Producer : K7 Team
# Hamada - Hesham

from configparser import ConfigParser
import pandas as pd 
from tasks import  QThread , pyqtSignal , typing 
import os


# Constants
COLUMNS = ['AreaCode','PhoneNumber']
TABEL_MODEL_COLUMNS = COLUMNS + ["Server Message","New AreaCode","New PhoneNumber"]




class ExcelReader(QThread):
    # Define Signals
    onReadExcel = pyqtSignal(pd.DataFrame)
    onFaildRead = pyqtSignal(str)

    def __init__(self, excelPath:str = '') -> None:
        super().__init__()
        self.excelPath = excelPath

    def setExcelPath(self , excelPath:str):
        self.excelPath = excelPath

    # Read Excel Method
    def loadExel(self)-> pd.DataFrame :
        if os.path.isfile(self.excelPath):
            try :
                data = pd.read_excel(self.excelPath)
                self.onReadExcel.emit(data)
            except Exception as e :
                self.onFaildRead.emit(str(e))
        else :
            self.onFaildRead.emit("File Dos Not Exist or Path Not Found !!")

    # Method that Run When QThread Started
    def run(self) -> None:
        self.loadExel()
        
    def start(self) -> None:
        if not self.isRunning():
            return super().start(self.Priority.HighPriority)
    
    def stop(self):
        if self.isRunning(self):
            self.terminate()
            self.wait()

    def delete(self):
        self.stop()
        self.deleteLater()


 
class SettingReader ():
    
    def __init__(self,path) -> None:
        self.start(path)

    def start(self,path):    
        self.config = ConfigParser()
        self.config.read(path)

    def getDomain(self):
        return self.config.get('DOMAIN', 'domain')

    def getSerialNumber(self):
        return self.config.get('SerialNumber', 'SerialNumber')

 
 
  
########################################################################################      
# class Excel ()  : 
#     def ExcelRead(code, Num):
#         result = []
#         if len(str(code)) == 1:
#             code = "0" + str(code)
#             result.append(str(str(code) + str(Num)))
#             print(result)
#             return result
#         elif len(str(code)) == 2 :
#             result.append(str(code + str(Num)))
#             print(result)
#             return result    
#         else :
#             return result
    
#     resultdata = ExcelRead('4', 114655556)
    
#     data = pd.DataFrame({"Num": resultdata})
#     data.to_excel("data.xlsx", index=False)


       

 
    





