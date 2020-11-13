import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sip
import PyQt5.sip
import random
life = 0
class Ui_EditMine(QWidget):
    def __init__(self):
        super(Ui_EditMine, self).__init__()
        self.originalNumber()
        self.ingame = 0

    def originalNumber(self):
        self.col = 16
        self.row = 16
        self.labels = list()
        self.start0 = 0
        self.mines = 40
        self.alreadyShow = 0 #已经开启的方格数量
        
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setFixedSize(500, 80)#固定窗体大小
        Form.move(400, 200)
        Form.setWindowIcon(QIcon(''))#设置窗体图标

        self.gridLayoutWidget = QtWidgets.QWidget(Form)#设置布局
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 80, 700, 700))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(2)
        
        self.inputRow = QtWidgets.QSpinBox(Form)
        self.inputRow.setObjectName("inputRow")
        self.inputRow.setGeometry(20, 30, 40, 20)
        
        self.inputCol = QtWidgets.QSpinBox(Form)
        self.inputCol.setObjectName("inputCol")
        self.inputCol.setGeometry(80, 30, 40, 20)
        
        self.inputMine = QtWidgets.QSpinBox(Form)
        self.inputMine.setObjectName("inputMine")
        self.inputMine.setGeometry(140, 30, 40, 20)
        
        self.startButton = QtWidgets.QPushButton(Form)
        self.startButton.setObjectName("startButton")
        self.startButton.setGeometry(200, 30, 40, 20)
        
        self.info = QtWidgets.QLabel(Form)
        self.info.setObjectName("info")
        self.info.setGeometry(250, 15, 200, 40)
        
        
        #一些文字信息的显示
        self.retranslateUi(Form)
        
        Form.show()
        
        self.startButton.clicked.connect(lambda:self.loadGame())
        

        
    
    def loadGame(self):
        if self.inputCol.value() < 1 or self.inputRow.value() < 1 or self.inputMine.value() < 1\
           or self.inputMine.value() > self.inputCol.value() * self.inputRow.value():#设置有问题
            self.col = 16
            self.row = 16
            self.mines = 40
        else:
            self.col = self.inputCol.value()
            self.row = self.inputRow.value()
            self.mines = self.inputMine.value()
        if self.ingame == 1:
            self.remove()
            self.originalNumber()
        _translate = QtCore.QCoreApplication.translate
        self.ingame = 1#游戏状态
        global life
        life = 1#开始时生命为1
        width = 500
        if 40 + 40 * self.col > width:
            width = 40 + 40 * self.col
        Form.setFixedSize(width, 100 + self.row * 40)#固定窗体大小
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 80, 40 * self.col, 40 * self.row))#设置雷区的布局
        
        
        self.initRandom()#生成雷区
        self.initNum()#生成每个格子周围的地雷数量
        for i in range(0, self.row):#初始化二维数组
            self.labels.append([])
            for j in range(0, self.col):
                label = pointOne(i, j, 0, "")
                # 绑定雷区点击事件
                label.rightClicked.connect(self.changePoint)
                label.leftClicked.connect(self.changeMine)
                label.setFrameShape(QFrame.Box)
                label.setStyleSheet("border-width: 1px;border-style:solid;color:balck;")
                label.setFont(QFont("Roman times", 15, QFont.Bold))
                label.setText("")
                self.labels[i].append(label)
                self.gridLayout.addWidget(label, i, j)

        information = "当前游戏为" + str(self.row) + " * " + str(self.col) + "雷区\n共有" + str(self.mines) + "个地雷"
        self.info.setText(_translate("Form", information))
        self.startButton.setText("重来")
        
    
    def remove(self):#清除雷区，用来重新进行游戏
        for row in range(self.row):
            for col in range(self.col):
                self.gridLayout.removeWidget(self.labels[row][col])
                sip.delete(self.labels[row][col])
        self.labels = list()
        
    def initRandom(self):#生成随机雷区
        self.map = [[0] * self.col for row in range(self.row)]
        mapall = random.sample(range(0, self.row * self.col), self.mines)
        for i in range(self.mines):
            self.map[mapall[i] // self.col][mapall[i] % self.col] = 1
    
    def initNum(self):#生成每个格子周围的地雷数量
        self.num = [[0] * self.col for row in range(self.row)]
        kx = [0, 0, 1, -1, 1, 1, -1, -1]
        ky = [1, -1, 0, 0, 1, -1, 1, -1]
        for i in range(self.row):
            for j in range(self.col):
                for k in range(8):#每个格子周围有8个格子
                    if self.map[i][j] == 1:#这个格子就是地雷的话设置数量为-1
                        self.num[i][j] = -1
                        continue
                    else:
                        xi = i + kx[k]
                        yi = j + ky[k]
                        if -1 < xi < self.row and -1 < yi < self.col and self.map[xi][yi] == 1:
                            self.num[i][j] += 1
                            
    def changeMine(self, i, j):#左键点击事件
        if self.labels[i][j].status == 1 or self.labels[i][j].status == 2:
            return
        if self.labels[i][j].status == 3:
            self.labels[i][j].status = 0
        _translate = QtCore.QCoreApplication.translate
        if self.num[i][j] != -1:
            xi = [1, -1, 0, 0]
            yi = [0, 0, 1, -1]
            vis = [[0] * self.col for row in range(self.row)]
            self.DFS(i, j, xi, yi, vis)
            if self.gameIsWin():
                self.winGame()
        else:
            information = "你玩扫雷的样子像极了蔡虚坤\n游戏失败！"
            self.info.setText(information)
            self.showGame()
    
    def changePoint(self, i, j):#右键点击
        if self.labels[i][j].status == 1 or life == 0:
            return
        _translate = QtCore.QCoreApplication.translate
        if self.labels[i][j].status == 2:
            self.labels[i][j].setStyleSheet("color:black;")
            self.labels[i][j].setFont(QFont("Roman times", 15, QFont.Bold))
            self.labels[i][j].setText("??")
            self.labels[i][j].status = 3
        elif self.labels[i][j].status == 0:
            self.labels[i][j].status = 2
            self.labels[i][j].setStyleSheet("color:red;")
            self.labels[i][j].setFont(QFont("华文楷体", 15, QFont.Bold))
            self.labels[i][j].setText("危")
        elif self.labels[i][j].status == 3:
            self.labels[i][j].setStyleSheet("color:black;")
            self.labels[i][j].setFont(QFont("Roman times", 15, QFont.Bold))
            self.labels[i][j].setText("")
            self.labels[i][j].status = 0

    def showPointNumber(self, i, j):
        if self.num[i][j] == 1:
            self.labels[i][j].setStyleSheet("color:blue;")
        elif self.num[i][j] == 2:
            self.labels[i][j].setStyleSheet("color:brown;")
        elif self.num[i][j] == 3:
            self.labels[i][j].setStyleSheet("color:#660099;")
        elif self.num[i][j] == 4:
            self.labels[i][j].setStyleSheet("color:purple;")
        elif self.num[i][j] == 5:
            self.labels[i][j].setStyleSheet("color:orange;")
        elif self.num[i][j] == 6:
            self.labels[i][j].setStyleSheet("color:pink;")
        elif self.num[i][j] == 7:
            self.labels[i][j].setStyleSheet("color:#00aa00;")
        elif self.num[i][j] == 8:
            self.labels[i][j].setStyleSheet("color:black;")
        elif self.num[i][j] == 0:
            self.labels[i][j].setStyleSheet("color:white;")
        self.labels[i][j].setFont(QFont("Roman times", 15, QFont.Bold))
        self.labels[i][j].setText(str(self.num[i][j]))
        self.labels[i][j].status = 1
        self.alreadyShow += 1
        if self.gameIsWin():
            self.winGame()

    def winGame(self):
        information = "您是祖国未来的接班人！\n游戏胜利！"
        self.info.setText(information)
        self.showGame()

    def gameIsWin(self):
        return self.alreadyShow == self.row * self.col - self.mines and life

    def showGame(self):#游戏结束时候的展示雷区
        global life
        life = 0
        for row in range(self.row):
            for col in range(self.col):
                if self.num[row][col] != -1:
                    if self.labels[row][col].status != 1:
                        self.showPointNumber(row, col)
                else:
                    if self.labels[row][col].status != 2:
                        self.labels[row][col].setStyleSheet("color:red;")
                    else:
                        self.labels[row][col].setStyleSheet("color:green;")
                    self.labels[row][col].setFont(QFont("Roman times", 15, QFont.Bold))
                    self.labels[row][col].setText("雷")
        
    def retranslateUi(self, Form):#游戏开始前的提示文字
        _translate = QtCore.QCoreApplication.translate
        #设置窗体标题
        Form.setWindowTitle(_translate("Form", "你想要怎样的雷区呢？"))
        self.startButton.setText(_translate("Form", "开始"))
        self.info.setText(_translate("Form", "请设置雷区大小\n默认为16*16, 40个雷"))

    def DFS(self, x, y, xi, yi, vis):
        vis[x][y] = 1
        if self.num[x][y] == -1:
            return
        if self.num[x][y] != 0:
            if self.labels[x][y].status == 0:
                self.showPointNumber(x, y)
                return
        if self.num[x][y] == 0:
            self.showPointNumber(x, y)
        for i in range(4):
            xp = x + xi[i]
            yp = y + yi[i]
            if -1 < xp < self.row and -1 < yp < self.col and self.labels[xp][yp].status == 0 and self.num[xp][yp] != -1 and vis[xp][yp] == 0:
                self.DFS(xp, yp, xi, yi, vis)

class pointOne(QtWidgets.QLabel):
    leftClicked = pyqtSignal(int, int)
    rightClicked = pyqtSignal(int, int)
    def __init__(self, i, j, num, parent=None):
        super (pointOne, self).__init__ (parent)
        self.num = num
        self.i = i
        self.j = j
        self.leftAndRightClicked = False
        self.status = 0  # 0、1、2、3代表没挖开、挖开、旗子、疑问
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.leftClicked.emit(self.i, self.j)
        if QMouseEvent.button() == Qt.RightButton:
            self.rightClicked.emit(self.i, self.j)


if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_EditMine()
    ui.setupUi(Form)
    sys.exit(app.exec_())
