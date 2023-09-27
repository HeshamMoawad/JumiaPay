# Producer : K7 Team
# Hamada - Hesham

from PyQt5.QtCore import (
    QObject ,
    Qt , 
    pyqtSignal, 
    pyqtSlot , 
    QThread , 
    QTime ,
    QAbstractTableModel ,
    QModelIndex ,
)
from PyQt5.QtSql import QSqlDatabase , QSqlQuery 
from PyQt5 import QtCore, QtNetwork
import typing , pandas 
from PyQt5.QtWidgets import (
    QMessageBox ,
    QWidget ,
    QLabel ,
)
from PyQt5.QtGui import QMovie
from datetime import datetime


#### Messages class
class MyMessageBox(QMessageBox):
    INFO = QMessageBox.Icon.Information
    WARNING = QMessageBox.Icon.Warning
    CRITICAL = QMessageBox.Icon.Critical

    def showWarning(self,text:typing.Optional[str]="Warning",title:typing.Optional[str]="Warning"):
        self.setIcon(self.WARNING)
        self.setWindowTitle(title)
        self.setText(text)
        self.exec_()

    def showInfo(self,text:typing.Optional[str]="Info",title:typing.Optional[str]="Information"):
        self.setIcon(self.INFO)
        self.setWindowTitle(title)
        self.setText(text)
        self.exec_()

    def showCritical(self,text:typing.Optional[str]="Critical",title:typing.Optional[str]="Critical"):
        self.setIcon(self.CRITICAL)
        self.setWindowTitle(title)
        self.setText(text)
        self.exec_()        

    def showAsk(self,text:typing.Optional[str]="Critical",title:typing.Optional[str]="Ask"):
        self.setIcon(self.Icon.Question)
        self.setWindowTitle(title)
        self.setText(text)
        self.setStandardButtons(self.StandardButton.Ok | self.StandardButton.Cancel)
        return self.exec_()
        

#### Internet Checker
class Checking(QObject):
    status = pyqtSignal(str)
    msg = MyMessageBox() 
    LeadSignal = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.internetConnected = False
    
    def isConnect(self)->bool:
        network_manager = QtNetwork.QNetworkAccessManager()
        reply = network_manager.get(QtNetwork.QNetworkRequest(QtCore.QUrl('https://www.google.com')))
        loop = QtCore.QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
        if reply.error() == QtNetwork.QNetworkReply.NetworkError.NoError:
            return True
        else:
            return False


#### ModelView
class MyTableModel(QAbstractTableModel):
    lengthChanged = pyqtSignal(int)
    message = pyqtSignal(str)
    def __init__(self, columns:typing.List[str]):
        super().__init__()
        self._data = pandas.DataFrame(columns=columns) 

    @property
    def columns(self):
        return self._data.columns

    def rowCount(self,parent: QModelIndex = ...):
        return len(self._data)

    def columnCount(self,parent: QModelIndex = ... ):
        return len(self._data.columns)


    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data.loc[index.row()][index.column()])
        return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal and section < len(self._data.columns):
                return self._data.columns[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None


    def dataframe(self)->pandas.DataFrame:
        return self._data

    def clear(self):
        self.beginResetModel()
        self._data = pandas.DataFrame(columns=self._data.columns)
        self.lengthChanged.emit(self.rowCount())
        self.endResetModel()
        

    def updateDataFrame(self,df:pandas.DataFrame):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data) + len(df))
        self._data = pandas.concat([self._data,df])
        self.lengthChanged.emit(self.rowCount())
        self.endInsertRows()


    def addrow(self, row):
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
        self._data.loc[len(self._data)] = row
        self.lengthChanged.emit(self.rowCount())
        self.endInsertRows()

    def export(self):
        try :
            name = f"Export-{datetime.now().date()}-({self.rowCount()}).xlsx"
            self._data.to_excel(name,index=False)
            self.message.emit(f"Exported Successfully as {name}")
        except :
            self.message.emit("Can't Export sheet ")

#### Sharing Dataframe
class SharingDataFrame(QObject):
    lengthChanged = pyqtSignal(int)

    def __init__(self, columns:typing.List[str] ,parent: typing.Optional['QObject'] = ...) -> None:
        super().__init__(parent)
        self.__data = pandas.DataFrame(columns=columns)

    @property
    def empty(self):
        return self.__data.empty

    def __len__(self):
        return len(self.__data)

    def rowCount(self):
        return len(self.__data)

    def add_Row(self,row:list):
        self.__data.loc[self.rowCount()] = row
        self.lengthChanged.emit(self.rowCount())
        
    def data(self)-> pandas.DataFrame:
        return self.__data

    def setData(self,data:pandas.DataFrame):
        data = data[data.columns[:2]]
        data.columns = self.__data.columns
        self.__data = data
        self.lengthChanged.emit(self.rowCount())

    def clear(self):
        self.__data = pandas.DataFrame(columns=self.__data.columns)
        self.lengthChanged.emit(self.rowCount())

    def get_row(self):
        frow = self.__data.iloc[0]
        self.__data = self.__data.iloc[1:, :]
        self.lengthChanged.emit(self.rowCount())
        return frow


#### Loading Widget
class GifWidget(QWidget):
    def __init__(self ,parent:QWidget=None, gifPath:str = "Data\Icons\icons8-loading-infinity.gif"):
        super().__init__(parent)
        self.movie = QMovie(gifPath)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMovie(self.movie)
        self.label.setScaledContents(False)

    def hide(self) -> None:
        self.movie.stop()
        return super().hide()

    def show(self) -> None:
        self.movie.start()
        return super().show()
    

#### Database class managment
class QDataBase():
    def __init__(self, db_path ):
        self.db_path = db_path
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_path)

    def check_user_exists(self, handle):
        if not self.db.open():
            return False
        query = QSqlQuery(self.db)
        query.prepare(f"SELECT * FROM Leads WHERE handle =:handle")
        query.bindValue(":handle", handle)
        query.exec_()
        result = query.first()
        self.db.close()
        if result:
            return True
        else:
            return False

    def add_user(self, TableName:str='Leads' , **kwargs):
        columns = self.get_column_names(TableName)
        if not self.db.isOpen() and not self.db.open():
            return
        query = QSqlQuery(self.db)
        query.prepare(f"""INSERT INTO {TableName} {str(tuple(columns)).replace("'","")} VALUES {tuple([(kwargs.get(column,"NULL") ) for column in columns ])} ;""")
        query.exec_()
        self.db.close()

    def get_column_names(self,tableName):
        column_names = []
        if not self.db.open():
            return column_names
        query = QSqlQuery()
        query.exec_(f"PRAGMA table_info({tableName});" )
        while query.next():
            column_names.append(query.value(1))
        self.db.close()
        return column_names

