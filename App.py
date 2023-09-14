from pages import Page1,Page2
from MyPyQt5 import (

                MyQMainWindow , 
                QSideMenuEnteredLeaved , 
                QIcon , 
                QSize ,
                MyThread ,
                pyqtSignal ,
                QShortcut ,
                QKeySequence ,
                MyMessageBox

                    )
import openpyxl
import pandas , numpy
from mainClass import BaseJumia , requests
import time , os , typing , threading
from styles import Styles


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


class Window (MyQMainWindow):
    threads:typing.List[MyThread] = []
    msg = MyMessageBox()
    def __init__(self,name:str) -> None:
        self.Name = name
        super().__init__()

    def SetupUi(self):
        self.setWindowTitle(self.Name)
        self.dataframe = pandas.DataFrame()
        self.dataframeList:typing.List[pandas.DataFrame] = []
        self.setFrameLess()
        self.resize(650,500)
        self.setStyleSheet(Styles().main)
        self.setAppIcon('Data\Icons\icons8-j-48.ico')
        self.Menu = QSideMenuEnteredLeaved(
            parent = self.mainWidget ,
            Title = f"Welcome {self.Name if self.Name != 'K7Hesham' else 'Admin'}" ,
            ButtonsCount = 2 ,
            PagesCount = 2 ,
            ToggleCount = 0 ,
            ButtonsFixedHight = 50 ,
            ButtonsFrameFixedwidthMini = 50 , 
            ButtonsFrameFixedwidth = 120 ,
            ExitButtonIconPath = "Data\Icons\\reject.png" ,
            MaxButtonIconPath = "Data\Icons\maximize.png",
            Mini_MaxButtonIconPath = "Data\Icons\minimize.png",
            MiniButtonIconPath = "Data\Icons\delete.png",

        )

        self.DashBoardBtn = self.Menu.getButton(0)
        self.DashBoardBtn.setTexts(entred=' DashBoard',leaved='')
        self.DashBoardBtn.setIcon(QIcon('Data\Icons\dashboard.png'))
        self.DashBoardBtn.setIconSize(QSize(30,30))
        self.SettingBtn = self.Menu.getButton(1)
        self.SettingBtn.setIcon(QIcon('Data\Icons\setting.png'))
        self.SettingBtn.setIconSize(QSize(30,30))
        self.SettingBtn.setTexts(entred=' Setting',leaved='')
        self.DashBoard = Page1(self.Menu.getPage(0))
        self.Setting = Page2(self.Menu.getPage(1))
        self.Setting.ExportRangeSignal.connect(self.DashBoard.setExportRange)
        self.Menu.connect_Button_Page(btn = self.DashBoardBtn ,pageIndex = 0)
        self.Menu.connect_Button_Page(btn = self.SettingBtn ,pageIndex = 1)
        self.jumia = BaseJumia(
            vendor = self.Setting.vendorComboBox.currentText() ,
            timeout = 5
            )
        self.Setting.vendorComboBox.currentTextChanged.connect(self.setVendor)
        # self.threadstart = threading.Thread(target=self.start)
        self.DashBoard.toolButton.clicked.connect(self.runThread)
        self.DashBoard.toolButton_2.clicked.connect(self.kill)
        self.darkMode(False)
        self.clear = QShortcut(QKeySequence("ctrl+r"),self)
        self.clear.activated.connect(lambda: self.updateWaitingDF(signal={} , clear=True))
        return super().SetupUi()
    
    def setVendor(self):
        self.jumia = BaseJumia(
            vendor = self.Setting.vendorComboBox.currentText() ,
            timeout = 5
            )

    def kill(self):
        for thread in self.threads :
            thread.kill(msg=None)
        self.Menu.MainLabel.setText(f"Stopped")
        self.msg.showInfo("Stopped Successfully")

    def updateWaitingDF(self,signal:dict ,clear:bool=False):
        if clear == False :
            self.dataframeList[signal['index']] = signal["dataframe"]
            self.dataframe = pandas.concat(self.dataframeList)
            self.DashBoard.updateWaiting(len(self.dataframe))
        if clear == True :
            self.dataframe = pandas.DataFrame()
            self.DashBoard.updateWaiting(length = 0)
            self.dataframeList.clear()

    def reshapeExelData(self,excelfile,sheetname):
        wb = openpyxl.load_workbook(excelfile)
        try :
            ws = wb[sheetname]
        except Exception as e :
            self.msg.showWarning(f"Sheet Name Not Found \n Error in : {e}")
        df = pandas.DataFrame(ws.values)
        df.dropna(inplace=True)
        df[df.columns[0]].apply(str)
        df[df.columns[1]].apply(str)
        df = df[1:]
        self.dataframe = df
        self.DashBoard.updateWaiting(length=len(df))
        # self.updateWaitingDF(signal=dict(index=))
        
    def darkMode(self,dark:bool=True):
        if dark == False :
            self.Menu.TopFrame.setStyleSheet(Styles.Backgrounds.Orange)
            self.Menu.ButtonsFrame.setStyleSheet(Styles.Backgrounds.Orange)
        elif dark == True :
            self.Menu.TopFrame.setStyleSheet(Styles.Backgrounds.DarkOrange)
            self.Menu.ButtonsFrame.setStyleSheet(Styles.Backgrounds.DarkOrange)


    def runThread(self):
        # self.threadstart = threading.Thread(target=self.start)
        self.Menu.MainLabel.setText("Starting ...")
        fileDir = self.Setting.lineEditDirectory.text()
        if fileDir !=  "" and os.path.isfile(fileDir):
            sheetname = 'Sheet1' if self.Setting.lineEditSheetName.text() == '' else self.Setting.lineEditSheetName.text() 
            # self.threadData = threading.Thread(target=self.reshapeExelData , args=(fileDir,sheetname,))
            # self.threadData.start()
            self.reshapeExelData(excelfile = fileDir, sheetname = sheetname)
            self.start()
            # if not self.threadstart.is_alive():
            #     self.threadstart.start()
        elif fileDir ==  "":
            if self.dataframe.empty :
                self.msg.showCritical(f'No Phones In Waiting')
            else :
                self.start()
                # if not self.threadstart.is_alive():
                #     self.threadstart.start()
                # self.WorkingThread.setDataFrame(self.dataframe)
                # self.WorkingThread.start(MyThread.Priority.InheritPriority)

    def start(self):
        # self.threadData.join()
        self.dataframeList =  self.splitDataFrame(self.dataframe,self.Setting.threadsCount.value())
        for index in range(len(self.dataframeList)):
            # print(type(self.dataframeList[index]))
            Thread = WorkingThread()
            Thread.setMainClass(self)
            Thread.setJumiaObj(self.jumia)
            Thread.setDataFrame(self.dataframeList[index])
            Thread.setIndex(index)#self.dataframeList.index(df)
            Thread.msg.connect(self.msg.showInfo)
            Thread.statues.connect(self.Menu.MainLabel.setText)
            Thread.Lead.connect(self.DashBoard.treeWidget.appendDataAsDict)
            Thread.WaitingSignal.connect(self.DashBoard.updateWaiting)
            Thread.DataFrameSignal.connect(self.updateWaitingDF)
            # Thread.setDataFrame(self.dataframe)
            self.threads.append(Thread)
            Thread.start(MyThread.Priority.InheritPriority)



    def splitDataFrame(self,df:pandas.DataFrame,nArray):
        return  numpy.array_split(df,nArray)


class WorkingThread(MyThread):
    Lead = pyqtSignal(dict)
    WaitingSignal = pyqtSignal(int)
    DataFrameSignal = pyqtSignal(dict)

    def setMainClass(self,mainclass:Window):
        self.MainClass = mainclass

    def run(self) -> None:
        print(self.DataFrame)
        while not self.DataFrame.empty:
            try :

                proxyList = self.JumiaObj.getFreshProxyList()
                print("getFreshProxyList")
                con = True
            except Exception as e :
                print(e)
                con = False
            if con :
                print("Start")
                if self.__index%2 :
                    proxyList.reverse()
                for proxy in proxyList :
                    print(proxy.requestShape)
                    if self.DataFrame.empty :
                        break
                    try :
                        lead = self.JumiaObj.sendRequest(
                                AreaCode = self.DataFrame.iloc[0][0],
                                PhoneNumber = self.DataFrame.iloc[0][1],
                                proxy = proxy.requestShape ,
                            )
                        print(f"\n{lead.status_code} - {lead.type}\n")
                        self.Lead.emit(lead.__dict__)
                        self.next()
                    except Exception as e :
                        pass
                        # print(f"\t[+]\t Error With Proxy {e} - {e}")

        self.statues.emit("Ended")
    def stopping(self,stop:bool):
        self.stop = stop
        
    def setJumiaObj(self, jumia:BaseJumia):
        self.JumiaObj = jumia

    def setDataFrame(self,df:pandas.DataFrame):
        self.DataFrame = df

    def setIndex(self,index):
        self.__index = index

    def next(self):
        self.DataFrame = self.DataFrame[1:]
        self.DataFrame.reset_index()
        self.DataFrameSignal.emit(
            dict(dataframe=self.DataFrame , index=self.__index)
            )
        


