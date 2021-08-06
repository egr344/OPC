import logging
import time
from opcua import Client
from threading import Thread
from PyQt5 import QtWidgets, QtCore
from window import Ui_MainWindow
import sys


class ParamWriter(Thread):
    # Конструктор класса. sensorsAndServer - список узлов и серверов, listLcdNumber - словарь где ключ это номер узла, а значени список lcd экранов для этого узла
    def __init__(self, sensorsAndServer, dictLcdNumber):
        Thread.__init__(self)
        self.sensorsAndServer = sensorsAndServer
        self.stopMark = False
        self.dictLcdNumber = dictLcdNumber

# Функция меняет значения марекра остановки
    def stop(self):
        self.stopMark = True

# функция передает значения температуры и вреимени с сервера на lcd дисплеи
    def run(self):
        dict_node = self.get_dict_node()
        while not self.stopMark:
            for sensor in self.dictLcdNumber.keys():
                self.dictLcdNumber[sensor][0].display(
                    dict_node[sensor]["Tempreture"].get_value())
                self.dictLcdNumber[sensor][1].display(
                    dict_node[sensor]["Time"].get_value())
            time.sleep(0.1)

# Возвращает словрь в котором каждому узлу соответсвтует словарь с наименованием значения и самим значением
    def get_dict_node(self):
        dict = {}
        for i in range(1, len(self.sensorsAndServer), 1):
            dict[i] = {}
            for param in self.sensorsAndServer[i].get_variables():
                if(param.get_description().to_string() == "Tempreture"):
                    dict[i].update({"Tempreture": param})
                elif(param.get_description().to_string() == "Time"):
                    dict[i].update({"Time": param})
        return dict


class mywindow(QtWidgets.QMainWindow):
    # Конструктор класса. В нем задаются взаимосвязи кнопок и функций
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connectFlag = False
        self.ui.pushButtonConnect.clicked.connect(self.connect_click)
        self.ui.pushButton_3.clicked.connect(self.set_velocity_force_sen_1)
        self.ui.pushButton.clicked.connect(self.set_velocity_force_sen_2)
        self.ui.pushButton_2.clicked.connect(self.set_velocity_force_sen_3)
        self.ui.pushButton_5.clicked.connect(self.exit_program)

    # функция запускает соединение с сервером
    def connect_click(self):
        if(not self.connectFlag):
            logging.basicConfig(
                level=logging.WARN)
            self.client = Client("opc.tcp://localhost:4840")
            try:
                self.client.connect()
                self.connectFlag = True
                self.sensorsAndServer = self.client.get_root_node().get_children()[
                    0].get_children()
                self.pm = ParamWriter(self.sensorsAndServer, {
                    1: [self.ui.lcdNumberTempSen1, self.ui.lcdNumberTimeSen1],
                    2: [self.ui.lcdNumberTempSen2, self.ui.lcdNumberTimeSen2],
                    3: [self.ui.lcdNumberTempSen3, self.ui.lcdNumberTimeSen3]})
                self.pm.start()
                self.ui.statusbar.showMessage("Соединение установлено")
                self.ui.pushButtonConnect.setText("Disconnect")
            except ConnectionRefusedError:
                self.ui.statusbar.showMessage("Сервер не отвечает")
        else:
            self.connectFlag = False
            self.pm.stop()
            time.sleep(0.05)
            self.client.disconnect()
            self.ui.statusbar.showMessage("Соединение разорвано")
            self.ui.pushButtonConnect.setText("Connect")

# Записывает значения скорости и силы на сервер для первого сенсора
    def set_velocity_force_sen_1(self):
        if(self.connectFlag and self.ui.lineEdit.hasAcceptableInput() and
           self.ui.lineEdit_4.hasAcceptableInput()):
            for param in self.sensorsAndServer[1].get_variables():
                if(param.get_description().to_string() == "Velocity"):
                    param.set_value(self.ui.lineEdit.text())
                elif(param.get_description().to_string() == "Force"):
                    param.set_value(self.ui.lineEdit_4.text())
            self.ui.statusbar.showMessage("Параметры установлены")
        else:
            self.ui.statusbar.showMessage(
                "Параметры введены неверно или отсутствует подключение к серверу")

# Записывает значения скорости и силы на сервер для второго сенсора
    def set_velocity_force_sen_2(self):
        if(self.connectFlag and self.ui.lineEdit_2.hasAcceptableInput() and
           self.ui.lineEdit_5.hasAcceptableInput()):
            for param in self.sensorsAndServer[2].get_variables():
                if(param.get_description().to_string() == "Velocity"):
                    param.set_value(self.ui.lineEdit_2.text())
                elif(param.get_description().to_string() == "Force"):
                    param.set_value(self.ui.lineEdit_5.text())
            self.ui.statusbar.showMessage("Параметры установлены")
        else:
            self.ui.statusbar.showMessage(
                "Параметры введены неверно или отсутствует подключение к серверу")

# Записывает значения скорости и силы на сервер для третьего сенсора
    def set_velocity_force_sen_3(self):
        if(self.connectFlag and self.ui.lineEdit_3.hasAcceptableInput() and
           self.ui.lineEdit_6.hasAcceptableInput()):
            for param in self.sensorsAndServer[3].get_variables():
                if(param.get_description().to_string() == "Velocity"):
                    param.set_value(self.ui.lineEdit_3.text())
                elif(param.get_description().to_string() == "Force"):
                    param.set_value(self.ui.lineEdit_6.text())
            self.ui.statusbar.showMessage("Параметры установлены")
        else:
            self.ui.statusbar.showMessage(
                "Параметры введены неверно или отсутствует подключение к серверу")

# Корректно завершает работу программы
    def exit_program(self):
        if (not self.connectFlag):
            QtCore.QCoreApplication.instance().quit()
        else:
            self.connect_click()
            QtCore.QCoreApplication.instance().quit()


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
