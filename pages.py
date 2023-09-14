from Packages import (AnimatedToggle,MyMessageBox,
    MyCustomContextMenu,MyQTreeWidget, QObject ,
    pyqtSignal
    )

from PyQt5 import QtCore, QtGui, QtWidgets
# from mainClass import JumiaPay
import pyperclip , typing 
from datetime import datetime
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

class Vendors():
    We = 'WE'
    Etisalat = 'Etisalat'
    # Orange = 'Orange'
    Noor = 'Noor'
    All = [We,Etisalat,Noor]#,Orange



class Page1(QObject):
    msg = MyMessageBox()
    def __init__(self,parent:QObject) -> None:
        super().__init__()
<<<<<<< HEAD
        self.ExportRange = {'AreaCode':0,'PhoneNumber':1,'HasUnpaidInvoices':2,'ResponseMessage':3 ,'price':4,}
=======
        self.ExportRange = {'AreaCode':0,'PhoneNumber':1,'HasUnpaidInvoices':2,'ServerMsg':3 ,'Price':4,'TimeScraping':5}
>>>>>>> c342788500481e81e86cb799eca7ff25e02ad0a5
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(parent)
        self.frame_4 = QtWidgets.QFrame(parent)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(3)
        self.frame_3 = QtWidgets.QFrame(self.frame_4)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.exportNamelabel = QtWidgets.QLabel(self.frame_3)
        self.exportNamelabel.setText('Export Sheet Name')
        self.exportNamelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_3.addWidget(self.exportNamelabel)
        self.lineEditExportName = QtWidgets.QLineEdit(self.frame_3)
        self.lineEditExportName.setPlaceholderText("Enter Name That will Export")
        self.horizontalLayout_3.addWidget(self.lineEditExportName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 5)
        self.horizontalLayout_3.setStretch(2, 2)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(self.frame_4)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setSpacing(10)
        self.toolButton = QtWidgets.QToolButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setText('Start')
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.toolButton_2 = QtWidgets.QToolButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setText("Stop")
        self.horizontalLayout_2.addWidget(self.toolButton_2)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame = QtWidgets.QFrame(self.frame_4)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.trecounterFrame = QtWidgets.QFrame(self.frame)
        self.counterlabel = QtWidgets.QLabel(self.trecounterFrame)
        self.counterlabel.setText("Counter: 0")
        self.treeWidget = MyQTreeWidget(self.frame,counterLabel=self.counterlabel)
<<<<<<< HEAD
        self.treeWidget.setColumns(['AreaCode','PhoneNumber','HasUnpaidInvoices','ResponseMessage','price'])
=======
        self.treeWidget.setColumns(['AreaCode','PhoneNumber','HasUnpaidInvoices','ServerMsg','Price','TimeScraping'])
>>>>>>> c342788500481e81e86cb799eca7ff25e02ad0a5
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.menu)
        self.treeWidget.setColumnWidth(0,70)
        self.treeWidget.setColumnWidth(1,100)
        self.treeWidget.setColumnWidth(2,130)
        self.treeWidget.setColumnWidth(3,130)
        self.treeWidget.setColumnWidth(4,40)
        self.treeWidget.setColumnWidth(5,80)
        self.verticalLayout.addWidget(self.treeWidget)
        self.trecounterFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.trecounterFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.trecounterFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.addWidget(self.counterlabel, 0, QtCore.Qt.AlignHCenter)
        self.waitinglabel = QtWidgets.QLabel(self.trecounterFrame)
        self.waitinglabel.setText("Waiting : 0")
        self.horizontalLayout.addWidget(self.waitinglabel, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.trecounterFrame)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 6)
        self.verticalLayout_3.addWidget(self.frame_4)

    def updateWaiting(self,length:int):
        self.waitinglabel.setText(f"Waiting : {length}")


    def menu (self):
        menu = MyCustomContextMenu(
            Actions_arg=[
                "Copy AreaCode", 
                "Copy Number", 
                "Delete Row", 
                "Export To Excel", 
                "Clear Data" ,
            ])
        menu.multiConnect(functions=[
            lambda: self.copy(0) ,
            lambda: self.copy(1) ,
            lambda: self.delete() ,
            lambda : self.export(self.lineEditExportName.text(),self.ExportRange),
            lambda : self.treeWidget.clear()
        ])
        menu.show()


    def copy(self , index:int):
        try :
            pyperclip.copy(self.treeWidget.currentItem().text(index))
        except :
            self.msg.showWarning(text="No Item Selected please Select one !")

    def delete(self):
        try:
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(self.treeWidget.currentItem()))
        except:
            self.msg.showWarning(text="No Item Selected please Select one !")

    def export(self,name:typing.Optional[str],values:dict):
        if name == '' or name == ' ':
            name = f"Hour{datetime.now().hour}Minute{datetime.now().minute}"
        if self.treeWidget._ROW_INDEX > 0 :
            self.treeWidget.getCustomDataFrame(values).to_excel(f"Data/Exports/{name}[{datetime.now().date()}].xlsx",index=False)
            self.msg.showInfo(text=f"Exported Succecfully to 'Data/Exports/{name}[{datetime.now().date()}].xlsx'")
        else :
            self.msg.showWarning(text="No Data In App Please Try Again Later")
    
    def setExportRange(self,values:dict):
        self.ExportRange = values


class Page2(QObject):
    msg = MyMessageBox()
    ExportRangeSignal = pyqtSignal(dict)
    def __init__(self,parent) -> None:
        super().__init__()
        # self.ExportRange = {'AreaCode':0,'PhoneNumber':1,'HasUnpaidInvoices':2,'Server Message':3 ,'Price':4,'TimeScraping':5}
        self.verticalLayout = QtWidgets.QVBoxLayout(parent)
        self.frame = QtWidgets.QFrame(parent)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setContentsMargins(0, 0, 9, 9)
        self.verticalLayout_4.setSpacing(20)
        self.settingGroupBox = QtWidgets.QGroupBox(self.frame)
        self.settingGroupBox.setTitle('Setting')
        self.VertSetting = QtWidgets.QVBoxLayout(self.settingGroupBox)
        self.VertSetting.setContentsMargins(3, 3, 3, 3)
        self.dirFrame = QtWidgets.QFrame(self.settingGroupBox)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.dirFrame)
        self.directorylabel = QtWidgets.QLabel(self.dirFrame)
        self.directorylabel.setText('File Directory')
        self.horizontalLayout_15.addWidget(self.directorylabel, 0, QtCore.Qt.AlignHCenter)
        self.lineEditDirectory = QtWidgets.QLineEdit(self.dirFrame)
        self.lineEditDirectory.setPlaceholderText("File Directory Here ")
        self.lineEditDirectory.setReadOnly(True)
        self.horizontalLayout_15.addWidget(self.lineEditDirectory)
        self.toolButton = QtWidgets.QToolButton(self.dirFrame)
        self.toolButton.setIcon(QtGui.QIcon('Data\Icons\icons8-export-excel-96.png'))
        self.toolButton.setIconSize(QtCore.QSize(25,25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setAutoRaise(True)
        self.toolButton.clicked.connect(self.getFileDir)
        self.horizontalLayout_15.addWidget(self.toolButton)
        self.horizontalLayout_15.setStretch(0, 1)
        self.horizontalLayout_15.setStretch(1, 3)
        self.horizontalLayout_15.setStretch(2, 1)
        self.VertSetting.addWidget(self.dirFrame)
        self.sheetNameFrame = QtWidgets.QFrame(self.settingGroupBox)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.sheetNameFrame)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.sheetNamelabel = QtWidgets.QLabel(self.sheetNameFrame)
        self.sheetNamelabel.setText("Sheet Name")
        self.horizontalLayout_17.addWidget(self.sheetNamelabel, 0, QtCore.Qt.AlignHCenter)
        self.lineEditSheetName = QtWidgets.QLineEdit(self.sheetNameFrame)
        self.lineEditSheetName.setPlaceholderText('Defualt : Sheet1')
        self.horizontalLayout_17.addWidget(self.lineEditSheetName)
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem)
        self.horizontalLayout_17.setStretch(0, 2)
        self.horizontalLayout_17.setStretch(1, 3)
        self.VertSetting.addWidget(self.sheetNameFrame)
        self.secFrame = QtWidgets.QFrame(self.settingGroupBox)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.secFrame)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.timeRequestFrame = QtWidgets.QFrame(self.secFrame)
        self.timeRequestlabel = QtWidgets.QLabel(self.timeRequestFrame)
        self.timeRequestlabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.timeRequestlabel.setText('Threads Count')
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.timeRequestFrame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.addWidget(self.timeRequestlabel)#, 0, QtCore.Qt.AlignHCenter
        self.threadsCount = QtWidgets.QSpinBox(self.timeRequestlabel)
        self.threadsCount.setMinimum(1)
        self.threadsCount.setMaximum(100)
        self.threadsCount.setValue(100)
        self.horizontalLayout_2.addWidget(self.threadsCount)
        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 2)
        self.horizontalLayout_16.addWidget(self.timeRequestFrame) ######################
        self.vendorFrame = QtWidgets.QFrame(self.secFrame)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.vendorFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.vendorlabel = QtWidgets.QLabel(self.vendorFrame)
        self.vendorlabel.setText('Vendor')
        self.horizontalLayout.addWidget(self.vendorlabel, 0, QtCore.Qt.AlignHCenter)
        self.vendorComboBox = QtWidgets.QComboBox(self.vendorFrame)
        # self.vendorComboBox.currentTextChanged.connect(self.setve)
        self.vendorComboBox.addItems(Vendors.All)
        self.horizontalLayout.addWidget(self.vendorComboBox)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 4)
        self.horizontalLayout_16.addWidget(self.vendorFrame)
        self.VertSetting.addWidget(self.secFrame)
        self.randomFrame = QtWidgets.QFrame(self.settingGroupBox)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.randomFrame)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QtWidgets.QFrame(self.randomFrame)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.randproxylabel = QtWidgets.QLabel(self.frame_4)
        self.randproxylabel.setText('Random Proxy')
        self.horizontalLayout_3.addWidget(self.randproxylabel, 0, QtCore.Qt.AlignHCenter)
        self.proxytoggle = AnimatedToggle(self.frame_4)
        self.proxytoggle.setCheckedColor(Styles.Colors.DarkOrangeToggle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.proxytoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_3.addWidget(self.proxytoggle)
        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 2)
        self.horizontalLayout_10.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.randomFrame)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.randUseragentlabel = QtWidgets.QLabel(self.frame_5)
        self.randUseragentlabel.setText('Random User-Agent')
        self.horizontalLayout_4.addWidget(self.randUseragentlabel, 0, QtCore.Qt.AlignHCenter)
        self.randUseragenttoggle = AnimatedToggle(self.frame_5)
        self.randUseragenttoggle.setCheckedColor(Styles.Colors.DarkOrangeToggle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.randUseragenttoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_4.addWidget(self.randUseragenttoggle)
        self.horizontalLayout_4.setStretch(0, 3)
        self.horizontalLayout_4.setStretch(1, 2)
        self.horizontalLayout_10.addWidget(self.frame_5)
        self.VertSetting.addWidget(self.randomFrame)
        self.verticalLayout_4.addWidget(self.settingGroupBox)
        self.optionGroupbox = QtWidgets.QGroupBox(self.frame)
        self.optionGroupbox.setTitle("Export Options")
        self.VertExportOption = QtWidgets.QVBoxLayout(self.optionGroupbox)
        self.VertExportOption.setContentsMargins(3, 3, 3, 3)
        self.opFirstFrame = QtWidgets.QFrame(self.optionGroupbox)
        self.opFirstFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.opFirstFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.opFirstFrame)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.areaCodeFrame = QtWidgets.QFrame(self.opFirstFrame)
        self.areaCodeFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.areaCodeFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.areaCodeFrame)
        self.areCodelabel = QtWidgets.QLabel(self.areaCodeFrame)
        self.areCodelabel.setText('AreaCode')
        self.horizontalLayout_6.addWidget(self.areCodelabel, 0, QtCore.Qt.AlignHCenter)
        self.areaCodetoggle = AnimatedToggle(self.areaCodeFrame)
        self.areaCodetoggle.setCheckedColor(Styles.Colors.DarkOrangeToggle)
        self.areaCodetoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.areaCodetoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_6.addWidget(self.areaCodetoggle)
        self.horizontalLayout_6.setStretch(0, 3)
        self.horizontalLayout_6.setStretch(1, 2)
        self.horizontalLayout_12.addWidget(self.areaCodeFrame)
        self.phoneFrame = QtWidgets.QFrame(self.opFirstFrame)
        self.phoneFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.phoneFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.phoneFrame)
        self.phonelabel = QtWidgets.QLabel(self.phoneFrame)
        self.phonelabel.setText('PhoneNumber')
        self.horizontalLayout_7.addWidget(self.phonelabel, 0, QtCore.Qt.AlignHCenter)
        self.phonetoggle = AnimatedToggle(self.phoneFrame)
        self.phonetoggle.setCheckedColor(Styles.Colors.DarkOrangeToggle)
        self.phonetoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.phonetoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_7.addWidget(self.phonetoggle)
        self.horizontalLayout_7.setStretch(0, 3)
        self.horizontalLayout_7.setStretch(1, 2)
        self.horizontalLayout_12.addWidget(self.phoneFrame)
        self.VertExportOption.addWidget(self.opFirstFrame)
        self.opSecFrame = QtWidgets.QFrame(self.optionGroupbox)
        self.opSecFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.opSecFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.opSecFrame)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.hasInvoFrame = QtWidgets.QFrame(self.opSecFrame)
        self.hasInvoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hasInvoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.hasInvoFrame)
        self.hasInvolabel = QtWidgets.QLabel(self.hasInvoFrame)
        self.hasInvolabel.setText('HasUnpaidInvoices') 
        self.hasInvolabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_5.addWidget(self.hasInvolabel)
        self.hasInvotoggle = AnimatedToggle(self.hasInvoFrame)
        self.hasInvotoggle.setCheckedColor(Styles.Colors.DarkOrangeToggle)
        self.hasInvotoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.hasInvotoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_5.addWidget(self.hasInvotoggle)
        self.horizontalLayout_5.setStretch(0, 3)
        self.horizontalLayout_5.setStretch(1, 2)
        self.horizontalLayout_13.addWidget(self.hasInvoFrame)
        self.serverMsgFrame = QtWidgets.QFrame(self.opSecFrame)
        self.serverMsgFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.serverMsgFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.serverMsgFrame)
        self.serverMsglabel = QtWidgets.QLabel(self.serverMsgFrame)
        self.serverMsglabel.setText("ServerMsg")
        self.horizontalLayout_11.addWidget(self.serverMsglabel, 0, QtCore.Qt.AlignHCenter)
        self.serverMsgtoggle = AnimatedToggle(self.serverMsgFrame)
        self.serverMsgtoggle.setCheckedColor(Styles.Colors.DarkOrangeToggle)
        self.serverMsgtoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.serverMsgtoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_11.addWidget(self.serverMsgtoggle)
        self.horizontalLayout_11.setStretch(0, 3)
        self.horizontalLayout_11.setStretch(1, 2)
        self.horizontalLayout_13.addWidget(self.serverMsgFrame)
        self.VertExportOption.addWidget(self.opSecFrame)
        self.opThirdFrame = QtWidgets.QFrame(self.optionGroupbox)
        self.opThirdFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.opThirdFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.opThirdFrame)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.PriceFrame = QtWidgets.QFrame(self.opThirdFrame)
        self.PriceFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.PriceFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.PriceFrame)
        self.pricelabel = QtWidgets.QLabel(self.PriceFrame)
        self.pricelabel.setText('Price')
        self.horizontalLayout_8.addWidget(self.pricelabel, 0, QtCore.Qt.AlignHCenter)
        self.pricetoggle = AnimatedToggle(self.PriceFrame)
        self.pricetoggle.setCheckedColor(Styles.Colors.DarkOrangeToggle)
        self.pricetoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.pricetoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_8.addWidget(self.pricetoggle)
        self.horizontalLayout_8.setStretch(0, 3)
        self.horizontalLayout_8.setStretch(1, 2)
        self.horizontalLayout_14.addWidget(self.PriceFrame)
        self.timeScrapingFrame = QtWidgets.QFrame(self.opThirdFrame)
        self.timeScrapingFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.timeScrapingFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.timeScrapingFrame)
        self.timeScrapinglabel = QtWidgets.QLabel(self.timeScrapingFrame)
        self.timeScrapinglabel.setText('TimeScraping')
        self.horizontalLayout_9.addWidget(self.timeScrapinglabel, 0, QtCore.Qt.AlignHCenter)
        self.timeScrapingtoggle = AnimatedToggle(self.timeScrapingFrame)
        self.timeScrapingtoggle.setCheckedColor(Styles.Colors.DarkOrangeToggle)
        self.timeScrapingtoggle.stateChanged.connect(self.exportrange)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.timeScrapingtoggle.setSizePolicy(sizePolicy)
        self.horizontalLayout_9.addWidget(self.timeScrapingtoggle)
        self.horizontalLayout_9.setStretch(0, 3)
        self.horizontalLayout_9.setStretch(1, 2)
        self.horizontalLayout_14.addWidget(self.timeScrapingFrame)
        self.VertExportOption.addWidget(self.opThirdFrame)
        self.optionGroupbox.setFixedHeight(210)
        self.verticalLayout_4.addWidget(self.optionGroupbox)
        self.verticalLayout_4.setStretch(0,3)
        self.verticalLayout_4.setStretch(1,1)
        self.verticalLayout.addWidget(self.frame)
        self.timeScrapingtoggle.setChecked(True)
        self.pricetoggle.setChecked(True)
        self.serverMsgtoggle.setChecked(True)
        self.hasInvotoggle.setChecked(True)
        self.phonetoggle.setChecked(True)
        self.areaCodetoggle.setChecked(True)



    def exportrange(self): # ['AreaCode','PhoneNumber','HasUnpaidInvoices','ResponseMessage','price']
        result = {}
        result['AreaCode'] = 0 if self.areaCodetoggle.isChecked() else None
        result['PhoneNumber'] = 1  if self.phonetoggle.isChecked() else None
        result['HasUnpaidInvoices'] = 2 if self.hasInvotoggle.isChecked() else None
<<<<<<< HEAD
        result['ResponseMessage'] = 3  if self.serverMsgtoggle.isChecked() else None
        result['price'] = 4  if self.pricetoggle.isChecked() else None
=======
        result['ServerMsg'] = 3  if self.serverMsgtoggle.isChecked() else None
        result['Price'] = 4  if self.pricetoggle.isChecked() else None
        result['TimeScraping'] = 5  if self.timeScrapingtoggle.isChecked() else None
>>>>>>> c342788500481e81e86cb799eca7ff25e02ad0a5
        self.ExportRangeSignal.emit(result)

    def getFileDir(self):
        file_filter = 'Data File (*.xlsx *.csv);; Excel File (*.xlsx *.xls)'
        dir = QtWidgets.QFileDialog.getOpenFileName(
            caption='Select a data file',
            filter=file_filter,
            )[0]
        self.lineEditDirectory.clear()
        self.lineEditDirectory.setText(dir)



