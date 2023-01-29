
from PyQt5 import QtCore, QtGui, QtWidgets
from MyPyQt5 import MyThread , MyMessageBox, MyQTreeWidget ,MyCustomContextMenu ,pyqtSignal
import datetime , openpyxl,typing,pandas,time
from mainClass import JumiaPay



class Ui_MainWindow(object):
    msg = MyMessageBox()
    def setupUi(self, MainWindow):
        MainWindow.resize(670, 554)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 20, 331, 21))
        self.lineEdit.setReadOnly(True)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(530, 62, 120, 22))
        self.comboBox.addItems(JumiaPay.Vendors.All)
        self.comboBox.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.treeWidget = MyQTreeWidget(self.centralwidget,counterLabel=self.label_4)
        self.treeWidget.setGeometry(QtCore.QRect(10, 150, 651, 361))
        self.treeWidget.setColumns(['AreaCode','PhoneNumber','HasUnpaidInvoices','Price'])
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.contextMenu)
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(540, 20, 81, 21))
        self.toolButton.clicked.connect(self.dialog)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 60, 171, 21))
        self.lineEdit_3.setPlaceholderText("Defult: Sheet1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 60, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setGeometry(QtCore.QRect(230, 520, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(260, 100, 165, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 100, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setFlat(False)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 100, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        # Thread Part 
        self.Thread = Thread()
        self.Thread.setMainClass(self)
        self.Thread.Lead.connect(self.treeWidget.appendDataAsDict)
        self.Thread.statues.connect(self.label_5.setText)
        self.Thread.msg.connect(self.msg.showInfo)
        self.pushButton.clicked.connect(self.Thread.start)
        self.pushButton_2.clicked.connect(self.Thread.kill)


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "File"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.label_3.setText(_translate("MainWindow", "Sheet Name"))
        self.label_2.setText(_translate("MainWindow", "Vendor"))
        self.label_4.setText(_translate("MainWindow", "Count : 0"))
        self.label_5.setText(_translate("MainWindow", "Status"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.setText(_translate("MainWindow", "Stop"))

    def contextMenu(self):
        menu = MyCustomContextMenu([
        "Delete Row" , # 3
        "Export All To Excel", # 4
        "Clear Results", # 10
        ])
        menu.multiConnect(functions=[
            lambda: self.delete() , # 3
            lambda: self.export(f"Hour{datetime.datetime.now().hour}Minute{datetime.datetime.now().minute}") , # 4  {datetime.datetime.now().date()} | 
            lambda: self.treeWidget.clear() , # 10
        ])
        menu.show()


    def delete(self):
        try:
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(self.treeWidget.currentItem()))
        except:
            self.msg.showWarning(text="No Item Selected please Select one !")


    def export(self,name:typing.Optional[str]):
        if self.treeWidget._ROW_INDEX > 0 :
            self.treeWidget.extract_data_to_DataFrame().to_excel(f"Data/Exports/{name}[{datetime.datetime.now().date()}].xlsx",index=False)
            self.msg.showInfo(text=f"Exported Succecfully to 'Data/Exports/{name}[{datetime.datetime.now().date()}].xlsx'")
        else :
            self.msg.showWarning(text="No Data In App Please Try Again Later")


    def dialog(self):
        file_filter = 'Data File (*.xlsx *.csv);; Excel File (*.xlsx *.xls)'
        dir = QtWidgets.QFileDialog.getOpenFileName(
            caption='Select a data file',
            filter=file_filter,
            )[0]
        self.lineEdit.setText(dir)
    
    def reshapeExelData(self,excelfile,sheetname):
        wb = openpyxl.load_workbook(excelfile)
        ws = wb[sheetname]
        df = pandas.DataFrame(ws.values)
        response = []
        for row in df.index:
            res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
            response.append(res)
        return response[1:]



class Thread(MyThread):
    Lead = pyqtSignal(dict)

    def setMainClass(self, mainClass:Ui_MainWindow):
        self.mainClass = mainClass


    def run(self) -> None:
        if self.mainClass.lineEdit.text() != "" :
            self.statues.emit("Starting")
            listOfPhones =  self.mainClass.reshapeExelData(
                excelfile = self.mainClass.lineEdit.text() , 
                sheetname = "Sheet1" if self.mainClass.lineEdit_3.text() == "" or self.mainClass.lineEdit_3.text() == " " else self.mainClass.lineEdit_3.text()
            )
            listOfPhones = list(set(listOfPhones))
            self.totalNumbers = len(listOfPhones)
            self.Jumia = JumiaPay(self.mainClass.comboBox.currentText())
            self.Jumia.Lead.connect(self.Lead.emit)
            for AreaCode,PhoneNumber in listOfPhones:
                t1 = time.time()
                print(AreaCode,PhoneNumber)
                self.statues.emit(f"Searching in {AreaCode}:{PhoneNumber}")
                self.Jumia.sendRequest(
                    AreaCode = AreaCode,
                    PhoneNumber = PhoneNumber ,
                    userAgent = self.Jumia.Flags.RandomUserAgent, 
                )
                self.msleep(100)
                t2 = time.time()
            self.statues.emit("Ending")
            self.msg.emit(f"\n {round(t2-t1,ndigits=4)} Is Total time for make {self.totalNumbers} number \nنورتنا يا رجولة متجيش تانى بقاا ^_-")
    
    






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
