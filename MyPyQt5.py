import typing , sys
import pandas , sqlite3
from PyQt5.QtCore import (QCoreApplication, QEasingCurve, QPoint, QPointF, QEvent ,
                          QPropertyAnimation , QRectF, QObject ,
                          QSequentialAnimationGroup , QSize, Qt, pyqtProperty,
                          pyqtSignal, pyqtSlot , QThread )
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import  NoSuchElementException
from MyPyQt5 import QThread,QObject,pyqtSignal
import typing , time , sqlite3 , os
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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

class MyQTreeWidget(QTreeWidget,QWidget):
    onLengthChanged = pyqtSignal(int)
    childChanged = pyqtSignal(int)
    _CHILD_COUNT = 0
    _ROW_INDEX = 0
    def __init__(self, parent: typing.Optional[QWidget],counterLabel:typing.Optional[QLabel]) -> None:
        super().__init__(parent)
        self.counterLabel = counterLabel
        self.ColumnNames = []
        if counterLabel != None : 
            self.onLengthChanged.connect(self.CounterLabel)
        
    def extract_data_to_DataFrame(self,range_of:range=None)-> pandas.DataFrame:
        self.COLUMN_NAMES = [self.headerItem().text(i) for i in (range(self.columnCount()) if range_of == None else range_of)]
        self.df = pandas.DataFrame(columns=self.COLUMN_NAMES)
        for col_index in (range(self.columnCount()) if range_of == None else range_of) :
            col_vals = []
            for row_index in range(self.topLevelItemCount()):
                text = self.topLevelItem(row_index).text(col_index)
                col_vals.append(text)
                for ch_index in range(self.topLevelItem(row_index).childCount()):
                    chtext = self.topLevelItem(row_index).child(ch_index).text(col_index)
                    col_vals.append(chtext)
            self.df[self.COLUMN_NAMES[col_index]] = col_vals
        return self.df

    def getCustomDataFrame(self,values:dict)-> pandas.DataFrame:
        re = []
        df = self.extract_data_to_DataFrame()
        for key , value in values.items():
            if value != None :
                re.append(key)
        return df[re] 

    def extract_data_to_list(self,index_of_column)->list:
        return self.extract_data_to_DataFrame()[self.COLUMN_NAMES[index_of_column]].to_list()
    
    def extract_data_to_string(self,index_of_column)->str:
        return self.extract_data_to_DataFrame()[self.COLUMN_NAMES[index_of_column]].to_string(index=False)

    def extract_columns(self,lista)->str:
        return self.extract_data_to_DataFrame()[[self.COLUMN_NAMES[i] for i in lista]].to_string(index=False)

    def appendDataAsList(self,items:typing.Optional[list],childs:typing.Optional[list]=None,Icon:str=None)-> None:
        #print(items)
        item_ = QTreeWidgetItem(self)
        item_.setIcon(0,QIcon(Icon)) if Icon != None else None
        for i in range(self.columnCount()):
            self.topLevelItem(self._ROW_INDEX).setText(i,items[i])
        if childs != None:
            childindex = 0
            if type(childs[0]) is list :
                for child in childs:
                    child_ = QTreeWidgetItem(item_)
                    for i in range(self.columnCount()):
                        item = self.topLevelItem(self._ROW_INDEX)
                        item.child(childindex).setText(i, child[i])
                    self.childChanged.emit(item.childCount())
                    self._CHILD_COUNT+=1
                    childindex += 1
            else:
                child_ = QTreeWidgetItem(item_)
                for i in range(self.columnCount()):
                    item = self.topLevelItem(self._ROW_INDEX)
                    item.child(childindex).setText(i, childs[i])
                self._CHILD_COUNT+=1
                self.childChanged.emit(item.childCount())
        self._ROW_INDEX += 1
        self.onLengthChanged.emit(self._ROW_INDEX)
        

    #################
    def appendDataAsDict(self,items:typing.Optional[dict],Icon:str=None)-> None:
        print(items)
        item_ = QTreeWidgetItem(self)
        item_.setIcon(0,QIcon(Icon)) if Icon != None else None
        for column in self.ColumnNames:
            self.topLevelItem(self._ROW_INDEX).setText(self.ColumnNames.index(column),str(items[column]))
        self._ROW_INDEX += 1
        self.onLengthChanged.emit(self._ROW_INDEX)

    
    @pyqtProperty(int)
    def length(self):
        return self._ROW_INDEX
    
    
    def CounterLabel(self):
        self.counterLabel.setText(f"Count : {self._ROW_INDEX}")
        
    def setColumns(self, columns: list) -> None:
        for column in columns:
            self.ColumnNames.append(column)
            self.headerItem().setText(columns.index(column),str(column))

    def takeTopLevelItem(self, index: int) -> QTreeWidgetItem:
        """
        To Delete Row From Widget 
        """
        self._ROW_INDEX -= 1
        self.onLengthChanged.emit(self._ROW_INDEX)
        if self.topLevelItem(index).childCount() >= 1:
            self._CHILD_COUNT = self._CHILD_COUNT - self.topLevelItem(index).childCount()
        return super().takeTopLevelItem(index)

    def childrenCount(self)-> int:
        """
        To get Children Count in All widget
        """
        count = 0
        for row in range(self._ROW_INDEX):
            count = count + self.topLevelItem(row).childCount()
        return count

    def clear(self) -> None:
        """
        To Clear TreeWidget
        """
        self._ROW_INDEX = 0
        self._CHILD_COUNT = 0
        self.onLengthChanged.emit(self._ROW_INDEX)
        return super().clear()

    
class AnimatedToggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
        parent=None,
        bar_color=Qt.gray,
        checked_color="#00B0FF",#c21919 
        handle_color=Qt.white,
        pulse_unchecked_color="#44999999",
        pulse_checked_color="#4400B0EE"
        ):
        super().__init__(parent)

        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation = QBrush(QColor(pulse_checked_color))

        # Setup the rest of the widget.
        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self._pulse_radius = 0

        self.animation = QPropertyAnimation(self, b"handle_position", self)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim = QPropertyAnimation(self, b"pulse_radius", self)
        self.pulse_anim.setDuration(350)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)

    def checkedColor(self):
        return self._handle_checked_brush

    def setCheckedColor(self,color:typing.Optional[str]):
        self._bar_checked_brush = QBrush(QColor(color).lighter())
        self._handle_checked_brush = QBrush(QColor(color))


    def sizeHint(self):
        return QSize(58, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)
    def setup_animation(self, value):
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.pulse_anim.state() == QPropertyAnimation.Running:
            p.setBrush(
                self._pulse_checked_animation if
                self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()),
                          self._pulse_radius, self._pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    @pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()



class MyQFrame(QFrame):
    Enterd = pyqtSignal()
    Leaved = pyqtSignal()

    def __init__(self, parent: typing.Optional[QWidget] = ...,Draggable:typing.Optional[bool]=False) -> None:
        super().__init__(parent)
        self.oldPos = self.pos()
        self.__draggable = Draggable

    def enterEvent(self, a0: QEvent) -> None:
        self.Enterd.emit()
        return super().enterEvent(a0)
        
    def leaveEvent(self, a0: QEvent) -> None:
        self.Leaved.emit()
        return super().leaveEvent(a0)
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.__draggable:
            delta = QPoint (event.globalPos() - self.oldPos)
            self.parent().parent().move(self.parent().parent().x() + delta.x(), self.parent().parent().y() + delta.y())
            self.oldPos = event.globalPos()

            
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
    
## --------------- New Class to Convert CustomContextMenu
class MyCustomContextMenu(QObject):

    def __init__(self,Actions_arg:typing.List[str]) -> None:
        super().__init__()
        self.Menu = QMenu()
        self.Actions = self.convert(Actions_arg)


    def convert(self,Actions_arg:typing.List[str])-> typing.List[QAction]:
        """Adding Actions to contextmenu and returns it into List[QAction]"""
        result = []
        for action in Actions_arg:
            Action = self.Menu.addAction(action)
            result.append(Action)
        return result

    def connect(self ,index_of_Action:int,func)-> None  :
        """Adding Actions to contextmenu and returns it into List[QAction]"""
        self.Actions[index_of_Action].triggered.connect(func)

    def connectShortcut(self ,index_of_Action:int,shortcut)-> None  :
        self.Actions[index_of_Action].setShortcut(shortcut)
        
    def multiConnect(self,functions:typing.List[typing.Callable] , range_of:typing.Optional[range]=None):
        for Action in (range(len(self.Actions)) if range_of == None else range_of):
            self.Actions[Action].triggered.connect(functions[Action])


    def show(self):
        cur = QCursor()
        self.Menu.exec_(cur.pos())




## ------------ QMainWindow custom widget
class MyQMainWindow(QMainWindow):
    App = QApplication(sys.argv)
    Leaved = pyqtSignal()
    Entered = pyqtSignal()
    ShowSignal = pyqtSignal()
    MessageBox = MyMessageBox()
    msg = MyMessageBox()
    
    
    def __init__(self) -> None:
        super().__init__()
        self.mainWidget = QWidget(self)
        self.SetupUi()

    def leaveEvent(self, a0:QEvent) -> None: 
        """Method that will running if your mouse Leaved From Widget """
        self.Leaved.emit()
        return super().leaveEvent(a0)

    def enterEvent(self, a0:QEvent) -> None:
        """Method that will running if your mouse Entered Into Widget """
        self.Entered.emit()
        return super().enterEvent(a0)
    
    def setFrameLess(self):
        """to set your window without frame"""
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

    def SetupUi(self):
        """the method that will run Automaticly with calling class"""
        self.setCentralWidget(self.mainWidget)
        self.show()
        sys.exit(self.App.exec_())

    def setAppIcon(self,relativePath:str):
        """To set Icon For Your App"""
        app_icon = QIcon()
        app_icon.addFile(relativePath, QSize(16,16))
        app_icon.addFile(relativePath, QSize(24,24))
        app_icon.addFile(relativePath, QSize(32,32))
        app_icon.addFile(relativePath, QSize(48,48))
        app_icon.addFile(relativePath, QSize(256,256))
        self.App.setWindowIcon(app_icon)
    
## ---------------------- Validation some texts 

class Validation(object):
    class Numbers(object):
        def __init__(self,phone:str) -> None:
            self.__phone = phone
        def __len__(self):
            return len(self.__phone)
        def setPhone(self,phone:str)-> None :
            self.__phone = phone
        @property 
        def phone(self) -> str :
            return self.__phone
        @property
        def length(self):
            return len(self.__phone)
        def saudiNumberCountryCode(self) -> str:
            if self.length > 13 : # +9660557888738
                return self.__phone[:4]+self.__phone[6:]
            elif self.length > 12 and "+" in self.__phone: # +966557888738
                return self.__phone
            elif self.length > 12 and "+" not in self.__phone: # 9660557888738
                return self.__phone
            elif self.length > 11 and "+" not in self.__phone : # 966557888738
                return "+" + self.__phone
            elif self.length > 9 : # 0557888738
                return "+966" + self.__phone[1:]
            elif self.length > 8 : # 557888738
                return "+966" + self.__phone

    class Telegram(object):
        def channelNameOrLinkToHandle(self,text:str)->str:
            """This Method takes TelegramLink or TelegramHandle and Returns into Handle 
            examples :
                ex: Input -> https://t.me/examplelink  return -> @examplelink
                ex: Input -> @examplelink return -> @examplelink
            """
            if "@" in text:
                return text
            elif "https://t.me/"in text :
                return text.replace("https://t.me/","@")



## ---------------------- Used For some simple Batabase Actions 

class DataBase():
    def __init__(self,relativepath:str = "Data\Database.db") -> None:
        self.con = sqlite3.connect(relativepath)
        self.cur = self.con.cursor()


    def exist(self,column,val):
        """
        Check if this Value is exist or not \n
        1- If value is exist that will return -> True \n
        2- If value is not exist that will return -> False

        """
        self.cur.execute(f"""SELECT * FROM data WHERE {column} = '{val}'; """)
        return True if self.cur.fetchall() != [] else False
    
    
    def add_to_db(self,table:str,**kwargs):
        """
        Adding values to Database :-\n
        example : \n
        'if you want to add number to (PhoneNumber)column in (userdata) table in DB'\n
        add_to_db(\n
            table = userdata ,\n
            PhoneNumber = value , # number that you want to add
        )
        """
        try:
            self.cur.execute(f"""
            INSERT INTO {table} {str(tuple(kwargs.keys())).replace("'","")}
            VALUES {tuple(kwargs.values())}; 
            """)
            self.con.commit()
        except Exception as e:
            print(f"\n{e} \nError in Database \n")

    def close(self):
        """Closing DataBase"""
        return self.con.close()

## -------------------------- Used for make some console methods
class JavaScriptCodeHandler(object):

    def __init__(self,driver:WebDriver) -> None:
        self.driver = driver
    
    def jscode(self,command):
        """
        Method to send commands to webdriver console\n example:\n
        1- 'if you want to define variable to console'\n
        jscode("var num = 1")\n
        2- 'if you want to get value from console function'\n
        return jscode("return value")\n
         """
        return self.driver.execute_script(command)
    

    def WaitingElement(self,timeout:int,val:str,by:str=By.XPATH)->typing.Optional[WebElement]:
        """Waiting Element to be located and return it with WebElemnt instance"""
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time :
                print("TimedOut and Breaked")
                break
            try:
                result = self.driver.find_element(by,val)
                break
            except NoSuchElementException :
                QThread.msleep(100)
        return result
    
    def WaitingElements(self,timeout:int,val:str,by:str=By.XPATH)->typing.Optional[typing.List[WebElement]]:
        """Waiting Elements to be located and return its with List[WebElemnt] instance"""
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time :
                print("TimedOut and Breaked")
                break
            try:
                result = self.driver.find_elements(by,val)
                break
            except NoSuchElementException :
                QThread.msleep(100)
        return result
            
    def WaitingMethod(self,timeout:int,func):
        """Waiting Method to be done and return value from Method with same instance"""
        end_time = time.time() + timeout
        while True:
            if time.time() > end_time :
                print("TimedOut and Breaked")
                break
            try:
                result = func()
            except Exception as e :
                pass
        return result

    
##----------------- Base Class to start webdriver , scraping with some Options 

class BaseScrapingClassQt5(QObject):
    LeadSignal = pyqtSignal(list)
    PersntageSignal = pyqtSignal(int)
    def __init__(
            self,
            url:str ,
            loginElementXpath:str ,
            headless:bool = False ,
            darkMode:bool = False ,
            userProfile:str="Guest", 
            ) -> None:
        
        option = Options()
        option.headless = True if  headless == True else False
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.add_argument('--disable-logging')
        option.add_argument('--force-dark-mode') if darkMode == True else None
        option.add_argument(f"user-data-dir={os.getcwd()}\\Profiles\\{userProfile}")
        self.driver = Chrome(ChromeDriverManager().install(),options=option)
        self.js = JavaScriptCodeHandler(self.driver)
        self.driver.maximize_window()
        self.driver.get(url)
        self.leadCount = 0
        self.js.WaitingElement(600,loginElementXpath)
        QThread.sleep(3)
        super().__init__()

    def exit(self):
        """To exit webdriver"""
        self.driver.quit()

    def wait_elm(self,val:str,by:str=By.XPATH,timeout:int=5)->WebElement:
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        arg = (by,val)
        return self.wait.until(EC.presence_of_element_located(arg))

    def wait_elms(self,val:str,by:str=By.XPATH,timeout:int=30)->typing.List[WebElement]:
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        arg = (by,val)
        elments = self.wait.until(EC.presence_of_all_elements_located(arg))
        return elments

    def NormalScroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

########################################################################

class MyQToolButton(QToolButton):
    Enterd = pyqtSignal()
    Leaved = pyqtSignal()
    __leavedString = ''
    __entredString = ''
    margin = 0

    def __init__(self, parent: typing.Optional[QWidget] = ... , Duration:int=250) -> None:
        super().__init__(parent)
        self.Animation = QPropertyAnimation(self,b"Margin",self)
        self.Animation.setDuration(Duration)
        self.Animation.setStartValue(0)
        self.Animation.setEndValue(5)

    def enterEvent(self, a0: QEvent) -> None:
        self.Enterd.emit()
        self.setText(self.__entredString)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.Animation.setDirection(self.Animation.Direction.Forward)
        self.Animation.start()
        return super().enterEvent(a0)

        
    def leaveEvent(self, a0: QEvent) -> None:
        self.Leaved.emit()
        self.setText(self.__leavedString)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.Animation.setDirection(self.Animation.Direction.Backward)
        self.Animation.start()
        
        return super().leaveEvent(a0)

    def setTexts(self,leaved:str,entred:str):
        self.__leavedString = leaved
        self.__entredString = entred

    def setMiniWidthHeight(self,miniWidth,miniHeight):
        self.miniWidth = miniWidth
        self.miniHeight = miniHeight

    def setMaxWidthHeight(self,maxWidth,maxHeight):
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight

    @pyqtProperty(int)
    def Margin(self):
        return self.margin

    @Margin.setter
    def Margin(self,margin):
        self.margin = margin
        style = f"""margin:{margin}px;"""
        stylesheet = self.styleSheet() + style
        self.setStyleSheet(stylesheet)




##################################################################################

class QSideMenuEnteredLeaved(QWidget):

    Buttons:typing.List[MyQToolButton] = []
    Pages:typing.List[QWidget] = []
    Toggles:typing.List[AnimatedToggle] = []
    ToggleLabels:typing.List[QLabel] = []

    def __init__(
            self,
            parent:QWidget,
            Title:str = "" ,
            ButtonsCount:int = 2,
            PagesCount:int = 2 ,
            ToggleCount:int = 2 ,
            ButtonsSpacing:int = 3 ,
            Duration:int = 400 ,
            DefultIconPath:str = None ,
            ClickIconPath:str = None ,  
            StretchMenuForStacked:tuple=(1,5) ,
            StretchTopForBottomFrame:tuple = (1,6),
            ButtonsFrameFixedwidth:int=None,
            ButtonsFrameFixedwidthMini:int=30,
            TopFrameFixedHight:int= 40,
            ExitButtonIconPath:str=None ,
            ButtonsFixedHight:int=None , 
            MaxButtonIconPath:str = None ,
            Mini_MaxButtonIconPath:str = None ,
            MiniButtonIconPath:str = None,
            **kwargs,

        ) -> None:
        super().__init__(parent)
        self.ButtonsFrameFixedwidthMini = ButtonsFrameFixedwidthMini
        self.DefultIconPath = DefultIconPath
        self.ClickIconPath = ClickIconPath
        self.verticalLayout = QVBoxLayout(parent)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.TopFrame = MyQFrame(parent,Draggable=True)
        self.TopFrame.setFixedHeight(TopFrameFixedHight) if TopFrameFixedHight != None else None
        self.horizontalLayout_2 = QHBoxLayout(self.TopFrame)
        self.MainLabel = QLabel(self.TopFrame)
        self.MainLabel.setText(Title)
        self.horizontalLayout_2.addWidget(self.MainLabel, 4 ,Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignCenter)
        self.MiniButton = QPushButton(self.TopFrame)
        self.MiniButton.setFlat(True)
        self.MiniButton.setFixedSize(QSize(20,20))
        self.MiniButton.setIcon(QIcon(MiniButtonIconPath)) if MiniButtonIconPath != None else None
        self.horizontalLayout_2.addWidget(self.MiniButton, 0,Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignCenter)
        self.MiniButton.clicked.connect(parent.parent().showMinimized)
        self.MaxButton = QPushButton(self.TopFrame)
        self.MaxButton.setFlat(True)
        self.MaxButton.setFixedSize(QSize(20,20))
        self.MaxButton.setIcon(QIcon(MaxButtonIconPath)) if MaxButtonIconPath != None else None
        self.MaxButton.clicked.connect(lambda : self.max_mini(self.parent().parent(),MaxButtonIconPath,Mini_MaxButtonIconPath,ButtonsFrameFixedwidth))
        self.horizontalLayout_2.addWidget(self.MaxButton, 0,Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignCenter)
        self.ExitButton = QPushButton(self.TopFrame)        
        self.ExitButton.setFlat(True)
        self.ExitButton.setFixedSize(QSize(20,20))
        self.ExitButton.setIconSize(QSize(20,20))
        self.ExitButton.setIcon(QIcon(ExitButtonIconPath)) if ExitButtonIconPath != None else None
        self.ExitButton.clicked.connect(parent.close)
        self.ExitButton.clicked.connect(QCoreApplication.instance().quit)        
        self.horizontalLayout_2.addWidget(self.ExitButton, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout_2.setContentsMargins(5,5,6,5)
        self.verticalLayout.addWidget(self.TopFrame)
        self.BottomFrame = MyQFrame(parent)
        self.horizontalLayout = QHBoxLayout(self.BottomFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.ButtonsFrame = MyQFrame(self.BottomFrame)
        self.ButtonsFrame.setFixedWidth(ButtonsFrameFixedwidth) if ButtonsFrameFixedwidth != None else None
        self.verticalLayout_2 = QVBoxLayout(self.ButtonsFrame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(ButtonsSpacing)
        self.MaxButton.setStyleSheet(Styles.PushButton.Normal)
        self.ExitButton.setStyleSheet(Styles.PushButton.Normal)
        self.MiniButton.setStyleSheet(Styles.PushButton.Normal)
        for index in range(ButtonsCount) :
            Button = MyQToolButton(self.ButtonsFrame)
            Button.setTexts(f'{index}',f"Button {index}") 
            Button.setAutoRaise(True)
            Button.setStyleSheet(Styles.Button)
            #Button.setCheckable(True)
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
            sizePolicy.setHeightForWidth(Button.sizePolicy().hasHeightForWidth())
            Button.setFixedHeight(ButtonsFixedHight) if ButtonsFixedHight != None else None
            Button.setSizePolicy(sizePolicy)
            if index == ButtonsCount - 1 :
                self.verticalLayout_2.addWidget(Button ,1, Qt.AlignmentFlag.AlignTop)
            else :
                self.verticalLayout_2.addWidget(Button ,0, Qt.AlignmentFlag.AlignTop)
            self.Buttons.append(Button)
 
        for i in range(ToggleCount):
            ToggleLabel = QLabel(self.ButtonsFrame)
            self.verticalLayout_2.addWidget(ToggleLabel,0,Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
            self.ToggleLabels.append(ToggleLabel)
            Toggle = AnimatedToggle(self.ButtonsFrame)
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            Toggle.setSizePolicy(sizePolicy)
            self.verticalLayout_2.addWidget(Toggle,0,Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)
            self.Toggles.append(Toggle)
            Toggle.hide()
            ToggleLabel.hide()

        self.horizontalLayout.addWidget(self.ButtonsFrame)
        self.stackedWidget = QStackedWidget(self.BottomFrame)
        for Page in range(PagesCount):
            Page = QWidget()
            self.stackedWidget.addWidget(Page)
            self.Pages.append(Page)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.horizontalLayout.setStretch(0 , StretchMenuForStacked[0])
        self.horizontalLayout.setStretch(1, StretchMenuForStacked[1])
        self.verticalLayout.addWidget(self.BottomFrame)
        self.verticalLayout.setStretch(0 ,StretchTopForBottomFrame[0])
        self.verticalLayout.setStretch(1 , StretchTopForBottomFrame[1])
        self.MAXWIDTH = self.ButtonsFrame.width()
        self.NORMALWIDTH = self.MAXWIDTH
        self.Animation = QPropertyAnimation(self,b"Width",self)
        self.Animation.setDuration(Duration)
        self.ButtonsFrame.Enterd.connect(self.entered)
        self.ButtonsFrame.Leaved.connect(self.leaved)
        self.ButtonsFrame.setFixedWidth(self.ButtonsFrameFixedwidthMini)

        self.setCurrentPage(0)
    
    @pyqtProperty(int)
    def Width(self):
        return self.ButtonsFrame.width()
    
    @Width.setter
    def Width(self,val):
        self.ButtonsFrame.setFixedWidth(val)
        
    def leaved(self)-> None:
        self.Animation.setStartValue(self.ButtonsFrameFixedwidthMini)
        self.Animation.setEndValue(self.MAXWIDTH)
        self.Animation.setDirection(self.Animation.Direction.Backward)
        self.Animation.start()
        for tog in self.Toggles:
            tog.hide()
        for lbl in self.ToggleLabels:
            lbl.hide()

    def entered(self):
        self.Animation.setStartValue(self.ButtonsFrameFixedwidthMini)
        self.Animation.setEndValue(self.MAXWIDTH)
        self.Animation.setDirection(self.Animation.Direction.Forward)
        self.Animation.start()
        for tog in self.Toggles:
            tog.show()
        for lbl in self.ToggleLabels:
            lbl.show()


    @pyqtSlot(int,str)
    def setButtonText(self,index:int,text:str)-> None:
        self.getButton(index).setText(text)

    @pyqtSlot(int,str)
    def setButtonIcon(self,index:int,IconPath:str)-> None:
        self.getButton(index).setIcon(QIcon(IconPath))
        
    def Connections(self,index:int,func):
        self.getButton(index).clicked.connect(func)

    def getButton(self,index:int)-> MyQToolButton :
        return self.Buttons[index]

    def getPage(self,index:int)-> QWidget:
        return self.Pages[index]

    def getToggle(self,index:int)-> AnimatedToggle :
        return self.Toggles[index]

    def getToggleLabel(self,index:int) -> QLabel:
        return self.ToggleLabels[index]

    @pyqtSlot(int)
    def setCurrentPage(self,index:int):
        self.stackedWidget.setCurrentIndex(index)

    def max_mini(self , parent:QMainWindow , path1:str , path2:str , Fixedwidth):
        if parent.isMaximized():
            parent.showNormal()
            self.MaxButton.setIcon(QIcon(path1))
            self.MAXWIDTH = self.NORMALWIDTH
        else :
            parent.showMaximized()
            self.MaxButton.setIcon(QIcon(path2))
            self.MAXWIDTH = Fixedwidth + 150 if Fixedwidth is int else 200


    def setToggleText(self,index:int,text:str=None) -> AnimatedToggle:
        self.ToggleLabels[index].setText(text) if text != None else None
        return self.Toggles[index]

    def connect_Button_Page(self,btn:MyQToolButton,pageIndex:int):
        btn.clicked.connect(lambda : self.setCurrentPage(pageIndex))
        


## ------------- Custom Thread class
class MyThread(QThread):

    statues = pyqtSignal(str)
    msg = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        
    def kill(self,msg:str=None):
        """Method to kill Thread when it Running"""
        if self.isRunning():
            self.terminate()
            self.wait()
        if msg != None :
            self.msg.emit(msg)
        self.statues.emit("Stopped")

    def start(self, priority: 'QThread.Priority' = ...) -> None:
        """Method to start Thread when it NotRunning"""
        if self.isRunning():
            pass
        else:
            return super().start(priority)

###################################################
