from pages import Page1,Page2
from MyPyQt5 import (MyQMainWindow , 
                    QSideMenuEnteredLeaved , 
                    QIcon , 
                    QSize ,
                    MyThread ,
                    pyqtSignal ,
                    QShortcut ,
                    QKeySequence
                    
                    )
import openpyxl
import pandas
from mainClass import JumiaPay
import time


class Window (MyQMainWindow):


    def SetupUi(self):
        self.dataframe = pandas.DataFrame()
        self.setFrameLess()
        self.resize(650,500)
        self.setStyleSheet("font:14px;")
        self.Menu = QSideMenuEnteredLeaved(
            parent = self.mainWidget ,
            ButtonsCount = 2 ,
            PagesCount = 2 ,
            ToggleCount = 1 ,
            ButtonsFixedHight = 50 ,
            ButtonsFrameFixedwidthMini = 50 , 
            ButtonsFrameFixedwidth = 130 ,
            ExitButtonIconPath = "Data\Icons\\reject.png" ,
            MaxButtonIconPath = "Data\Icons\maximize.png",
            Mini_MaxButtonIconPath = "Data\Icons\minimize.png",
            MiniButtonIconPath = "Data\Icons\delete.png",

        )
        self.DarkMode = self.Menu.setToggleText(0,"Dark Mode")
        self.DashBoardBtn = self.Menu.getButton(0)
        self.DashBoardBtn.setTexts(entred='DashBoard',leaved='')
        self.DashBoardBtn.setIcon(QIcon('Data\Icons\dashboard.png'))
        self.DashBoardBtn.setIconSize(QSize(30,30))
        self.SettingBtn = self.Menu.getButton(1)
        self.SettingBtn.setIcon(QIcon('Data\Icons\setting.png'))
        self.SettingBtn.setIconSize(QSize(30,30))
        self.SettingBtn.setTexts(entred='Setting',leaved='')
        self.DashBoard = Page1(self.Menu.getPage(0))
        self.DashBoard
        self.Setting = Page2(self.Menu.getPage(1))
        self.Setting.ExportRangeSignal.connect(self.DashBoard.setExportRange)
        self.Menu.connect_Button_Page(
            btn = self.DashBoardBtn ,
            pageIndex = 0
        )
        self.Menu.connect_Button_Page(
            btn = self.SettingBtn ,
            pageIndex = 1
        )
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
        df = df[1:]
        self.updateWaitingDF(df)

    
    # def logicDirMethod(self):
    #     result = {}
    #     result['go'] = True
    #     if self.Setting.lineEditDirectory.text() !=  "" :
    #         try:
    #             fileDir = self.Setting.lineEditDirectory.text()
    #             sheetname = 'Sheet1' if self.Setting.lineEditSheetName.text() == '' else self.Setting.lineEditSheetName.text() 
    #             self.reshapeExelData(
    #                     excelfile = fileDir, 
    #                     sheetname = sheetname
    #                 )
    #             result["go"] = True
    #             result['Dataframe'] = self.dataframe
    #         except Exception as e :
    #             print(e)
    #             result["go"] = False 
    #             result['Dataframe'] = self.dataframe
    #             self.msg.showWarning(f'File Directory Not Found Or Sheet Name Not Exist\nPlease Make Sure you Entered currect sheet name ')


    #     elif self.Setting.lineEditDirectory.text() ==  "" :

    #         if self.dataframe.empty :
    #             self.msg.showInfo(f'No Phones In Waiting')
    #             result["go"] = False 
    #             result['Dataframe'] = self.dataframe

    #         else :
    #             result["go"] = True
    #             result['Dataframe'] = self.dataframe
    #     self.Setting.lineEditDirectory.clear()
    #     return result


class WorkingThread(MyThread):
    Lead = pyqtSignal(dict)
    WaitingSignal = pyqtSignal(int)
    DataFrame = pyqtSignal(pandas.DataFrame)

    def setMainClass(self,mainclass:Window):
        self.MainClass = mainclass


    def run(self) -> None:
        go = self.logicDirMethod() #self.MainClass.logicDirMethod()
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












w = Window()
w.show()






