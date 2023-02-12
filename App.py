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

                    )
import openpyxl
import pandas
from mainClass import JumiaPay 
import time
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
    def __init__(self,name:str) -> None:
        self.Name = name
        super().__init__()

    def SetupUi(self):
        self.setWindowTitle(self.Name)
        self.dataframe = pandas.DataFrame()
        self.setFrameLess()
        self.resize(650,500)
        self.setStyleSheet(Styles().main)
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
        # Thread Part ------
        self.WorkingThread = WorkingThread()
        self.WorkingThread.setMainClass(self)
        self.WorkingThread.msg.connect(self.msg.showInfo)
        self.WorkingThread.statues.connect(self.Menu.MainLabel.setText)
        self.WorkingThread.Lead.connect(self.DashBoard.treeWidget.appendDataAsDict)
        self.WorkingThread.WaitingSignal.connect(self.DashBoard.updateWaiting)
        self.WorkingThread.DataFrame.connect(self.updateWaitingDF)
        self.DashBoard.toolButton.clicked.connect(self.WorkingThread.start)
        self.DashBoard.toolButton_2.clicked.connect(lambda : self.WorkingThread.kill('Stopped Succesfully'))
        self.darkMode(False)
        self.clear = QShortcut(QKeySequence("ctrl+r"),self)
        self.clear.activated.connect(lambda: self.updateWaitingDF(df=pandas.DataFrame() , clear=True))

        return super().SetupUi()



    def updateWaitingDF(self,df:pandas.DataFrame ,clear:bool=False):
        self.dataframe = df
        self.DashBoard.updateWaiting(len(df))
        if clear == True :
            self.dataframe = pandas.DataFrame()
            self.DashBoard.updateWaiting(0)

    def reshapeExelData(self,excelfile,sheetname):
        wb = openpyxl.load_workbook(excelfile)
        ws = wb[sheetname]
        df = pandas.DataFrame(ws.values)
        df.dropna(inplace=True)
        df[df.columns[0]].apply(str)
        df[df.columns[1]].apply(str)
        df = df[1:]
        self.updateWaitingDF(df)

    def darkMode(self,dark:bool=True):
        if dark == False :
            self.Menu.TopFrame.setStyleSheet(Styles.Backgrounds.Orange)
            self.Menu.ButtonsFrame.setStyleSheet(Styles.Backgrounds.Orange)
            # self.mainWidget.setStyleSheet(Styles.Backgrounds.DarkOrange)
        elif dark == True :
            self.Menu.TopFrame.setStyleSheet(Styles.Backgrounds.DarkOrange)
            self.Menu.ButtonsFrame.setStyleSheet(Styles.Backgrounds.DarkOrange)



    
class WorkingThread(MyThread):
    Lead = pyqtSignal(dict)
    WaitingSignal = pyqtSignal(int)
    DataFrame = pyqtSignal(pandas.DataFrame)

    def setMainClass(self,mainclass:Window):
        self.MainClass = mainclass

    def run(self) -> None:
        try:
            go = self.logicDirMethod()
            print(go)
            if go['go'] :
                useproxies = self.MainClass.Setting.proxytoggle.isChecked()
                useuseragent = self.MainClass.Setting.randUseragenttoggle.isChecked()
                self.stop = False
                self.statues.emit("Starting")
                self.Jumia = JumiaPay(self.MainClass.Setting.vendorComboBox.currentText())
                phonelist = self.Jumia.convertDataframeToPhonesList(go['Dataframe'])
                totalnumbers = len(phonelist)
                self.Jumia.Lead.connect(self.Lead.emit)
                self.Jumia.msg.connect(self.msg.emit)
                self.Jumia.stop.connect(self.stopping)
                t1 = time.time()
                if useproxies :
                    Proxies = self.Jumia.ProxyAPI.autoAPI()
                    self.Jumia.setProxies(Proxies = Proxies)
                loops = 0
                waiting = totalnumbers
                sleeping = self.MainClass.Setting.timeRequestspinbox.value()
                dataframe = go['Dataframe']
                for AreaCode , PhoneNumber in phonelist :
                    if self.stop == True:
                        self.statues.emit(f"Stopped for Banned")
                        self.msg.emit("خدنا باان يا اخوياا -_- ")
                        break
                    if loops == 10 and useproxies:
                        Proxies = self.Jumia.ProxyAPI.autoAPI()
                        self.Jumia.setProxies(Proxies = Proxies)
                        loops = 0
                    print(AreaCode,PhoneNumber)
                    self.statues.emit(f"will sleeping for {sleeping}")
                    self.sleep(sleeping)
                    self.statues.emit(f"Request for +2{AreaCode}{PhoneNumber}")
                    try:
                        self.Jumia.sendRequest(
                            AreaCode = AreaCode,
                            PhoneNumber = PhoneNumber ,
                            userAgent = self.Jumia.Flags.RandomUserAgent if useuseragent else None, 
                            proxy = self.Jumia.Flags.RandomProxy if useproxies else None,
                        )
                    except Exception as e :
                        self.Jumia.Errors.append(f"{AreaCode+PhoneNumber} -> {e}")
                    waiting -= 1
                    self.WaitingSignal.emit(waiting)
                    dataframe = dataframe[1:]
                    self.DataFrame.emit(dataframe)
                    loops =+ 1
                with open("Errors.txt",'w+') as file :
                    file.writelines(self.Jumia.Errors)
                t2 = time.time()
                self.statues.emit("Ending")
                self.msg.emit(f"\n {round(t2-t1,ndigits=2)} Is Total time for make {totalnumbers} number \nنورتنا يا رجولة متجيش تانى بقاا ^_-")
        except Exception as e :
            self.msg.emit(f"Error in {e}\nPlease Contact Hesham")
    def stopping(self,stop:bool):
        self.stop = stop
        
    def logicDirMethod(self):
        result = {}
        result['go'] = True
        
        if self.MainClass.Setting.lineEditDirectory.text() !=  "" :
            try:
                fileDir = self.MainClass.Setting.lineEditDirectory.text()
                sheetname = 'Sheet1' if self.MainClass.Setting.lineEditSheetName.text() == '' else self.Setting.lineEditSheetName.text() 
                self.MainClass.reshapeExelData(excelfile = fileDir, sheetname = sheetname)
                result["go"] = True
                result['Dataframe'] = self.MainClass.dataframe
            except Exception as e :
                print(e)
                result["go"] = False 
                result['Dataframe'] = self.MainClass.dataframe
                self.msg.emit(f'File Directory Not Found Or Sheet Name Not Exist\nPlease Make Sure you Entered currect sheet name ')

        elif self.MainClass.Setting.lineEditDirectory.text() ==  "" :

            if self.MainClass.dataframe.empty :

                self.msg.emit(f'No Phones In Waiting')
                result["go"] = False 
                result['Dataframe'] = self.MainClass.dataframe

            else :
                result["go"] = True
                result['Dataframe'] = self.MainClass.dataframe

        self.MainClass.Setting.lineEditDirectory.clear()
        return result