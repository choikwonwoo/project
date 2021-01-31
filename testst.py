import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import cv2
from pyzbar import pyzbar
import qrcode
import threading

uiadresss =uic.loadUiType('minsoo.ui')[0]
Temps = []
Data = []
class CalWindow(QDialog):
    def __init__(self,parent):
        super(CalWindow, self).__init__(parent)
        self.a= uic.loadUi("C:\\Users\\Assistant_1\\anaconda3\\Lib\\site-packages\\PyQt5\\uic\\minsoo2.ui",self)
        self.QR_image()
        self.a.show()
        self.pushButton.clicked.connect(self.exit)

    def QR_image(self):
        self.lbl =QLabel(self)
        self.lbl.move(150,-150)
        self.lbl.resize(400,400)
        pixmap = QPixmap("qr_test.png")
        pixmap = pixmap.scaledToWidth(100)
        self.lbl.setPixmap(QPixmap(pixmap))
        self.resize(400,400)
        

    def exit(self):
        self.a.close()

class Main_Window(QMainWindow,uiadresss):

    def __init__(self):
        super().__init__()
        
        
        self.setupUi(self)
        
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
           


    def plus(self):
        
        self.item = QPushButton("del")
        self.item.clicked.connect(self.del_botton)
        self.tableWidget.setRowCount(len(Temps))
        self.tableWidget.setCellWidget(len(Temps)-1,3,self.item)

        self.item1 = QPushButton("+")
        self.item2 = QPushButton("-")
        

        self.item1.clicked.connect(self.countPlus)
        self.item2.clicked.connect(self.countMinus)
        self.tableWidget.setCellWidget(len(Temps)-1,4,self.item1)
        self.tableWidget.setCellWidget(len(Temps)-1,5,self.item2)
        
        
        

    def countPlus(self):
        button = self.sender()
        if button:
            row = self.tableWidget.indexAt(button.pos()).row() 
            self.count[row] = str(int(self.count[row]) +1)
            item = QTableWidgetItem(self.count[row])
            self.tableWidget.setItem(row, 2, item)
            self.nowPrice()


    def countMinus(self):
        button = self.sender()
        if button:
            row = self.tableWidget.indexAt(button.pos()).row()
            if int(self.count[row]) != 1:
                self.count[row] = str(int(self.count[row]) -1)
                item = QTableWidgetItem(self.count[row])
                self.tableWidget.setItem(row, 2, item)
                self.nowPrice()
            else:
                pass
            

 

    def listMaker(self):    
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subject = len(self.name)
       
        
        allsubjectData = [self.name1 , self.price1, self.count]

        for i in range(self.subject):
            for j in range(3):
                item = QTableWidgetItem(allsubjectData[j][i])
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.tableWidget.setItem(i, j, item)
    

    def read_barcodes(self,frame):
        barcodes = pyzbar.decode(self.frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            # 1
            self.barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # 2
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.frame, self.barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            self.Make_Temp(self.barcode_info)
        return self.frame

    def Make_Temp(self,barcode_info):
        
        if self.barcode_info in Temps:
            print("```")
        else:
            Temps.append(self.barcode_info)
            self.plus()

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
                self.name1[i] = '감자'
            elif self.name[i] == "2":
                self.name1[i] = '고구마'
            elif self.name[i] == "3":
                self.name1[i] = '과자'
            elif self.name[i] == "4":
                self.name1[i] = '음료'
            elif self.name[i] == "5":
                self.name1[i] = '물'
            elif self.name[i] == "6":
                self.name1[i] = '라면'
            elif self.name[i] == "7":
                self.name1[i] = '우유'
            elif self.name[i] == "8":
                self.name1[i] = '치즈'
            elif self.name[i] == "9":
                self.name1[i] = '아이스크림'
            elif self.name[i] == "10":
                self.name1[i] = '버섯'
            elif self.name[i] == "11":
                self.name1[i] = '냉동식품'
            elif self.name[i] == "12":
                self.name1[i] = '생활용품'
            elif self.name[i] == "13":
                self.name1[i] = '전자제품'

            self.price1[i] = str(int(self.price[i])*100)
            self.nowPrice()
            self.listMaker()
            print(self.price)
            print(self.name)
            print(self.count)



    def nowPrice(self):
        totalPrice = 0
        for i in range(len(self.price)):
            totalPrice += int(self.price1[i])*int(self.count[i])
        self.textEdit.setText(str(totalPrice)+'원')
 

    def newWindow(self):
        sumString = ""
        for i in range(len(self.name)):
            sumString += self.name[i] +':'+ self.price[i] +':'+ self.count[i]
            if i != int(len(self.name))-1:
                sumString += ':'

        img1 = qrcode.make(sumString)
        img1.save('qr_test.png')
        CalWindow(self)
        

    def main(self):
    #1
        
        camera = cv2.VideoCapture(0)
        ret, self.frame = camera.read()
    #2
        while ret:
            ret, self.frame = camera.read()
            self.frame = self.read_barcodes(self.frame)
            cv2.imshow('Barcode/QR code reader', self.frame)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break

    #3
        camera.release()
        cv2.destroyAllWindows()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Main_Window()
    t =threading.Thread(target =mainwindow.show())
    t.start()
    mainwindow.main()

    app.exec_()