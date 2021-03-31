import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5 import uic
# import serial
# import qrcode
import queue

item_dict = {'1':'DDD', '2': 'A'}

uiadresss = uic.loadUiType('minsoo.ui')[0]
Temps = []
Data = []
rawBarcode = ''

print(q)
class Thread1(QThread):
    qtSignal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
    def run(self):
        while 1:
            # ser = serial.Serial('/dev/ttyUSB0', 9600)
            # rawBarcode = str(ser.read(6))
            # rawBarcode = rawBarcode.replace("b","").replace("'","")
            # print(rawBarcode)
            rawBarcode("1:20:1")
            Make_Temp(rawBarcode)

    def Make_Temp(self, rawBarcode):
        data = rawBarcode.split(':')

        name = item_dict.get(data[0])
        price = str(int(data[1]) * 100)
        num = data[2]
        
        self.qtSignal.emit((name,price,num))
        ## 이벤트 발생!!!!!!!!!!

class CalWindow(QDialog):
    
    def __init__(self, parent):

        super(CalWindow, self).__init__(parent)


        self.a = uic.loadUi("C:\\Users\\Assistant_1\\anaconda3\\Lib\\site-packages\\PyQt5\\uic\\minsoo2.ui", self)
        self.QR_image()
        self.a.show()
        self.pushButton.clicked.connect(self.exit)

    def QR_image(self):
        self.lbl = QLabel(self)
        self.lbl.move(150, -150)
        self.lbl.resize(400, 400)
        pixmap = QPixmap("qr_test.png")
        pixmap = pixmap.scaledToWidth(100)
        self.lbl.setPixmap(QPixmap(pixmap))
        self.resize(400, 400)

    def exit(self):
        self.a.close()


class Main_Window(QMainWindow, uiadresss):

    def __init__(self):
        super().__init__()
        self.x = Thread1()
        self.x.qtSignal.connect(nowPrice)
        self.x.start()
        self.setupUi(self)

    
        self.Make_Temp()

        
        
        self.pushButton.clicked.connect(self.newWindow)

    def del_botton(self):
        button = self.sender()
        if button:
            row = self.tableWidget.indexAt(button.pos()).row()
            del Temps[row]
            del self.name[row]
            del self.price[row]
            del self.count[row]
            self.tableWidget.removeRow(row)
            self.nowPrice()

    def plus(self):

        self.item = QPushButton("del")
        self.item.clicked.connect(self.del_botton)
        self.tableWidget.setRowCount(len(Temps))
        self.tableWidget.setCellWidget(len(Temps) - 1, 3, self.item)

        self.item1 = QPushButton("+")
        self.item2 = QPushButton("-")

        self.item1.clicked.connect(self.countPlus)
        self.item2.clicked.connect(self.countMinus)
        self.tableWidget.setCellWidget(len(Temps) - 1, 4, self.item1)
        self.tableWidget.setCellWidget(len(Temps) - 1, 5, self.item2)

    def countPlus(self):
        button = self.sender()
        if button:
            row = self.tableWidget.indexAt(button.pos()).row()
            self.count[row] = str(int(self.count[row]) + 1)
            item = QTableWidgetItem(self.count[row])
            self.tableWidget.setItem(row, 2, item)
            self.nowPrice()

    def countMinus(self):
        button = self.sender()
        if button:
            row = self.tableWidget.indexAt(button.pos()).row()
            if int(self.count[row]) != 1:
                self.count[row] = str(int(self.count[row]) - 1)
                item = QTableWidgetItem(self.count[row])
                self.tableWidget.setItem(row, 2, item)
                self.nowPrice()
            else:
                pass

    def listMaker(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subject = len(self.name)

        allsubjectData = [self.name1, self.price1, self.count]

        for i in range(self.subject):
            for j in range(3):
                item = QTableWidgetItem(allsubjectData[j][i])
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.tableWidget.setItem(i, j, item)


    

    @pyqtSlot(tuple)
    def nowPrice(self, data):
        print(data)
        totalPrice = 0
        for i in range(len(self.price)):
            totalPrice += int(self.price1[i]) * int(self.count[i])
        self.textEdit.setText(str(totalPrice) + '원')

    def newWindow(self):
        sumString = ""
        for i in range(len(self.name)):
            sumString += self.name[i] + ':' + self.price[i] + ':' + self.count[i]
            if i != int(len(self.name)) - 1:
                sumString += ':'

        # img1 = qrcode.make(sumString)
        # img1.save('qr_test.png') 
        CalWindow(self)

    # def main(self):
    #     while 1:
    #         ser = serial.Serial('/dev/ttyUSB0', 9600)
    #         line = ser.read(6)
    #         print(line)
    #         self.Make_Temp(line)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Main_Window()

    mainwindow.show()
    #mainwindow.show()

    

    app.exec_()