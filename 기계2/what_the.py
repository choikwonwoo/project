import sys
import qrcode
from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from pyzbar.pyzbar import decode
from PIL import Image
import csv
form_calss = uic.loadUiType('/Users/Assistant_1/anaconda3/Lib/site-packages/PyQt5/uic/tesrt1.ui')[0]
class CalWindow(QDialog):
    def __init__(self,parent):
        super(CalWindow, self).__init__(parent)
        self.a= uic.loadUi("C:\\Users\\Assistant_1\\anaconda3\\Lib\\site-packages\\PyQt5\\uic\\cal1.ui",self)
        self.calWindowSet()
        self.a.show()
    
    def calWindowSet(self):
 
        self.textEdit.setText(mainwindow.won)
        self.money = ""
        self.pushButton.clicked.connect(self.keyPadnum1)
        self.pushButton_2.clicked.connect(self.keyPadnum2)
        self.pushButton_3.clicked.connect(self.keyPadnum3)
        self.pushButton_4.clicked.connect(self.keyPadnum4)
        self.pushButton_5.clicked.connect(self.keyPadnum5)
        self.pushButton_6.clicked.connect(self.keyPadnum6)
        self.pushButton_7.clicked.connect(self.keyPadnum7)
        self.pushButton_8.clicked.connect(self.keyPadnum8)
        self.pushButton_9.clicked.connect(self.keyPadnum9)
        self.pushButton_10.clicked.connect(self.keyPadnum10)
        self.pushButton_11.clicked.connect(self.moneyCal)
        self.pushButton_12.clicked.connect(self.eraseMoney)
    
    def moneyCal(self):

        intMoney = int(self.money)
        resultMoney = intMoney - mainwindow.saveTotalPrice 
        self.textEdit_3.setText(str(resultMoney)+"원")

        if resultMoney <= 0:
            self.showCashError()
        else:
            self.completePayment()
        
    def completePayment(self):
        msgBox = QMessageBox(self)
        msgBox.question(self,'결제완료',"결제가 완료되었습니다.",QMessageBox.Yes)

        self.a.close()
        del self.a
        mainwindow.hardReset()
        
    

    def showCashError(self):
        msgBox = QMessageBox(self)
        msgBox.question(self,'결제실패',"금액이 부족합니다. 다시 결제해 주세요",QMessageBox.Yes)
        self.textEdit_3.setText("0")
        self.money = ""
        self.textEdit_2.setText(self.money)

    def eraseMoney(self):
        self.money = ""    
        self.textEdit_2.setText(self.money)
    def keyPadnum1(self):
        self.money= self.money + "1"
        self.textEdit_2.setText(self.money)
    def keyPadnum2(self):
        self.money= self.money + "2"
        self.textEdit_2.setText(self.money)
    def keyPadnum3(self):
        self.money= self.money + "3"
        self.textEdit_2.setText(self.money)
    def keyPadnum4(self):
        self.money= self.money + "4"
        self.textEdit_2.setText(self.money)
    def keyPadnum5(self):
        self.money= self.money + "5"
        self.textEdit_2.setText(self.money)
    def keyPadnum6(self):
        self.money= self.money + "6"
        self.textEdit_2.setText(self.money)
    def keyPadnum7(self):
        self.money= self.money + "7"
        self.textEdit_2.setText(self.money)
    def keyPadnum8(self):
        self.money= self.money + "8"
        self.textEdit_2.setText(self.money)
    def keyPadnum9(self):
        self.money= self.money + "9"
        self.textEdit_2.setText(self.money)
    def keyPadnum10(self):
        self.money= self.money + "0"
        self.textEdit_2.setText(self.money)





class MainWindow(QMainWindow,form_calss):
    def __init__(self):
        super().__init__()
        self.Total_Price =0
        self.subject = 0
        self.setupUi(self)
        
        self.pushButton_5.clicked.connect(self.read_QR)
        self.pushButton_3.clicked.connect(self.opencall)


        
    def make_QR(self):#QR코드 실시간 인식이 들어가면 됨......
        img1 = qrcode.make('''1:5:2:2:6:2:3:10:2:1:5:2:2:6:2:3:10:2:1:5:2:2:6:2:3:10:2:1:5:2:2:6:2:3:10:2''')
        img1.save('qr_test.png')

    def read_QR(self):
        self.make_QR()
        img = Image.open('qr_test.png')
        result = decode(img)
        allData=[x.data.decode("utf-8").split(":") for x in result][0]

        self.name = [allData[x] for x in range(len(allData)) if (x % 3) == 0]
        self.count = [allData[x] for x in range(len(allData)) if ((x + 1) % 3) == 0]
        self.price = [allData[x] for x in range(len(allData)) if ((x + 2) % 3) == 0]
        self.decoding()
        self.subject = len(self.name)
        self.tableWidget.setRowCount(self.subject)
        
        allsubjectData = [self.name , self.price, self.count]

        for i in range(self.subject):
            for j in range(3):
                item = QTableWidgetItem(allsubjectData[j][i])
                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                self.tableWidget.setItem(i, j, item)
        for i in range(len(self.price)):
            self.Total_Price =  self.Total_Price + int(self.price[i]) * int(self.count[i])
        print(self.Total_Price)
        self.won = str(self.Total_Price)
        self.won +="원"
        self.textEdit.setText(self.won)
        self.saveTotalPrice =self.Total_Price

        print(self.name)
        print(self.price)
        print(len(self.name))
        # self.makeBill()
        self.reset()
        

    def reset(self):
        self.Total_Price = 0
        self.subject = 0
        self.name.clear()
        self.price.clear()
        self.count.clear()

    def hardReset(self):
        self.reset()
        mainwindow.textEdit.setText("")
        mainwindow.tableWidget.setRowCount(0)
        

    def opencall(self):
        CalWindow(self)
    
    def makeBill(self):
        firstTag = ['상품명','가격','수량']
        img = Image.open("qr_test.png")
        with open('billtest.csv','w', newline='') as f:
            billList =[0 for i in range(len(self.name))]
            writer =csv.writer(f)
            writer.writerow(firstTag)
            for i in range(len(self.name)):
                billList[i] = [self.name[i],self.price[i],self.count[i]] 
                writer.writerow(billList[i])
            writer.writerow(img)
            f.close()
    
    
    def decoding(self):
        for i in range(len(self.name)):
            self.price[i] = str(int(self.price[i]) * 100)
            if self.name[i] == "1":
                self.name[i]="감자"
            elif self.name[i] == "2":
                self.name[i] = "고구마"
            elif self.name[i] == "3":
                self.name[i] = "과자"
            elif self.name[i] == "2":
                self.name[i]="고구마"
        

        

        # billList =[0 for i in range(len(self.name))]
        # file = open('billtest.txt','w')
        # file.write('상품명 가격 수량\n')
        # for i in range(len(self.name)):            
        #     billList[i] = [self.name[i],self.price[i],self.count[i]]
        #     print(billList)
        #     file.write((str(billList[i])).strip('[]')+'\n')
        # file.close()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()

