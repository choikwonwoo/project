import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5 import uic
import serial
import qrcode
import queue


uiadresss = uic.loadUiType('minsoo.ui')[0]
Temps = []
Data = []
rawBarcode = ''
q = queue.Queue()
print(q)
class Thread1(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
    def run(self):
        while 1:
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            rawBarcode = str(ser.read(6))
            rawBarcode = rawBarcode.replace("b","").replace("'","")
            print(rawBarcode)
            q.put(rawBarcode)
            print(q)
            # mainwindow.Make_Temp()        

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
        x = Thread1()
        x.start()
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


    def Make_Temp(self):
        
        rawBarcode =q.get()
        if rawBarcode in Temps:
            print("```")
        else:
            Temps.append(rawBarcode)
            print(Temps)
            self.plus()
        # Temps.append('1:20:1')
        # self.plus()

        self.name = [0 for i in range(len(Temps))]
        self.name1 = [0 for i in range(len(Temps))]
        self.price = [0 for i in range(len(Temps))]
        self.price1 = [0 for i in range(len(Temps))]
        self.count = [0 for i in range(len(Temps))]

        print(Temps)
        Data = [0 for i in range(len(Temps))]
        for i in range(len(Temps)):
            Data[i] = Temps[i].split(':')

        print(Data)
        for i in range(len(Data)):
            self.name[i] = Data[i][0]
            self.price[i] = Data[i][1]
            self.count[i] = Data[i][2]

        print(self.name)
        print(self.price)
        print(self.count)

        for i in range(len(self.name)):
            if self.name[i] == "1":
                self.name1[i] = 'DDD'
            elif self.name[i] == "2":
                self.name1[i] = 'D'
            elif self.name[i] == "3":
                self.name1[i] = 'A'
            elif self.name[i] == "4":
                self.name1[i] = 'C'
            elif self.name[i] == "5":
                self.name1[i] = 'Q'
            elif self.name[i] == "6":
                self.name1[i] = 'W'
            elif self.name[i] == "7":
                self.name1[i] = 'E'
            elif self.name[i] == "8":
                self.name1[i] = 'R'
            elif self.name[i] == "9":
                self.name1[i] = 'T'
            elif self.name[i] == "10":
                self.name1[i] = 'Y'
            elif self.name[i] == "11":
                self.name1[i] = 'U'
            elif self.name[i] == "12":
                self.name1[i] = 'I'
            elif self.name[i] == "13":
                self.name1[i] = 'O'

            self.price1[i] = str(int(self.price[i]) * 100)
            self.nowPrice()
            self.listMaker()
            print(self.price)
            print(self.name)
            print(self.count)


    def nowPrice(self):
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

        img1 = qrcode.make(sumString)
        img1.save('qr_test.png')
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