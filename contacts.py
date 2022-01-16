import sqlite3
from PySide6.QtCore import * 
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtUiTools import QUiLoader


class Main_win(QMainWindow):
    def __init__(self):
        super().__init__()
        loader=QUiLoader()
        self.app=loader.load("contacts.ui")
        self.app.show()
        self.connect_to_db=sqlite3.connect("contacts.db")
        self.cur=self.connect_to_db.cursor()
        self.read_db()
        self.app.Dark_mode.clicked.connect(self.Dmode)
        self.app.Light_mode.clicked.connect(self.UnDmode)
        self.app.ADD.clicked.connect(self.add)
        self.app.DELETE.clicked.connect(self.delete)
        self.app.DELETE_ALL.clicked.connect(self.deleteall)
        self.id=0
        self.cur.execute("SELECT * FROM person")
        result=self.cur.fetchall()
        self.id=len(result)
        
    def read_db(self):
        self.cur.execute("SELECT * FROM person")
        result=self.cur.fetchall()
        for item in result:
            lab=QLabel()
            lab.setText(F"{item[1]} {item[2]}\n{item[3]}\n{item[4]}")
            self.app.verticalLayout.addWidget(lab)
    
    def Dmode(self):
        self.app.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.app.ADD.setStyleSheet("background-color: rgb(76, 76, 76);")
        self.app.DELETE.setStyleSheet("background-color: rgb(76, 76, 76);")
        self.app.DELETE_ALL.setStyleSheet("background-color: rgb(76, 76, 76);")
        self.app.scrollArea.setStyleSheet("background-color: rgb(76, 76, 76);")
        self.app.mode.setStyleSheet("background-color: rgb(76, 76, 76);")

    def UnDmode(self):
        self.app.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.app.ADD.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.app.DELETE.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.app.DELETE_ALL.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.app.scrollArea.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.app.mode.setStyleSheet("background-color: rgb(240, 240, 240);")

    def add(self):
        name=self.app.lineEdit_1.text()
        fullname=self.app.lineEdit_2.text()
        number=self.app.lineEdit_3.text()
        email=self.app.lineEdit_4.text()
        self.id+=1
        if name=="":
           mas=QMessageBox()
           mas.setText("enter name:: ")
           mas.exec()
           return
           
        self.cur.execute(f"INSERT INTO person VALUES({self.id},'{name}','{fullname}','{number}','{email}');")
        self.connect_to_db.commit()
        lab=QLabel()
        lab.setText(F"{name} {fullname}\n{number}\n{email}")
        self.app.verticalLayout.addWidget(lab)


    def delete(self):
        number=self.app.lineEdit_3.text()
        if number=="":
           mas=QMessageBox()
           mas.setText("enter number:: ")
           mas.exec()
           return
        self.cur.execute(f"DELETE FROM person WHERE number = \'{number}\';")
        self.connect_to_db.commit()
        for i in range(self.app.verticalLayout.count()):
            self.app.verticalLayout.itemAt(i).widget().deleteLater()
        self.read_db()

    def deleteall(self):
        self.cur.execute("DELETE FROM person;")
        self.connect_to_db.commit()
        for i in range(self.app.verticalLayout.count()):
            self.app.verticalLayout.itemAt(i).widget().deleteLater()
    

my_app=QApplication()
mwin=Main_win()
my_app.exec()