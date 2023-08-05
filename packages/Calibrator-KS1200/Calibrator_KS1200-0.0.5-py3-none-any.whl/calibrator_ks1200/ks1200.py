from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QInputDialog, QApplication
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sqlite3
import traceback
import os
import sys
from sys import platform
from Exchange_data_str_bu7 import *
from Exchange_data_str_itm import *
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
" тестирую автоматичиескую версионку сборки"
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget_main = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget_main.setGeometry(QtCore.QRect(9, 9, 981, 581))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget_main.sizePolicy().hasHeightForWidth())
        self.stackedWidget_main.setSizePolicy(sizePolicy)
        self.stackedWidget_main.setObjectName("stackedWidget_main")
        self.Logo = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Logo.sizePolicy().hasHeightForWidth())
        self.Logo.setSizePolicy(sizePolicy)
        self.Logo.setObjectName("Logo")
        self.label_logo = QtWidgets.QLabel(self.Logo)
        self.label_logo.setEnabled(True)
        self.label_logo.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_logo.sizePolicy().hasHeightForWidth())
        self.label_logo.setSizePolicy(sizePolicy)
        self.label_logo.setStyleSheet("background-color: rgb(243, 242, 242);")
        self.label_logo.setText("")
        self.label_logo.setPixmap(QtGui.QPixmap("Logo_etalon.png"))
        self.label_logo.setObjectName("label_logo")
        self.tab_logo = self.stackedWidget_main.addWidget(self.Logo)
        self.Settings = QtWidgets.QWidget()
        self.Settings.setObjectName("Settings")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Settings)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_settings = QtWidgets.QVBoxLayout()
        self.verticalLayout_settings.setObjectName("verticalLayout_settings")
        self.label_device_nubmer = QtWidgets.QLabel(self.Settings)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_device_nubmer.setFont(font)
        self.label_device_nubmer.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_device_nubmer.setObjectName("label_device_nubmer")
        self.verticalLayout_settings.addWidget(self.label_device_nubmer)
        self.lineEdit_device_number = QtWidgets.QLineEdit(self.Settings)
        self.lineEdit_device_number.setFont(font)
        self.lineEdit_device_number.setObjectName("lineEdit_device_number")
        self.lineEdit_device_number.textEdited.connect(self.device_number_changed)
        self.verticalLayout_settings.addWidget(self.lineEdit_device_number)
        self.label_device_name = QtWidgets.QLabel(self.Settings)
        self.label_device_name.setFont(font)
        self.label_device_name.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_device_name.setObjectName("label_device_name")
        self.verticalLayout_settings.addWidget(self.label_device_name)
        self.lineEdit_device_name = QtWidgets.QLineEdit(self.Settings)
        self.lineEdit_device_name.setFont(font)
        self.lineEdit_device_name.setObjectName("lineEdit_device_name")
        self.lineEdit_device_name.textEdited.connect(self.device_name_changed)
        self.verticalLayout_settings.addWidget(self.lineEdit_device_name)
        self.label_device_next_veryfing_date = QtWidgets.QLabel(self.Settings)
        self.label_device_next_veryfing_date.setFont(font)
        self.label_device_next_veryfing_date.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_device_next_veryfing_date.setObjectName("label_device_next_veryfing_date")
        self.verticalLayout_settings.addWidget(self.label_device_next_veryfing_date)
        self.lineEdit_device_next_veryfing_date = QtWidgets.QLineEdit(self.Settings)
        self.lineEdit_device_next_veryfing_date.setFont(font)
        self.lineEdit_device_next_veryfing_date.setObjectName("lineEdit_device_next_veryfing_date")
        self.lineEdit_device_next_veryfing_date.textEdited.connect(self.device_next_veryfing_date_changed)
        self.verticalLayout_settings.addWidget(self.lineEdit_device_next_veryfing_date)
        self.label_devic_veryfing_date = QtWidgets.QLabel(self.Settings)
        self.label_devic_veryfing_date.setFont(font)
        self.label_devic_veryfing_date.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_devic_veryfing_date.setObjectName("label_devic_veryfing_date")
        self.verticalLayout_settings.addWidget(self.label_devic_veryfing_date)
        self.lineEdit_device_produce_date = QtWidgets.QLineEdit(self.Settings)
        self.lineEdit_device_produce_date.setFont(font)
        self.lineEdit_device_produce_date.setObjectName("lineEdit_device_produce_date")
        self.lineEdit_device_produce_date.textEdited.connect(self.device_produce_date_changed)
        self.verticalLayout_settings.addWidget(self.lineEdit_device_produce_date)
        self.label_device_produce_date = QtWidgets.QLabel(self.Settings)
        self.label_device_produce_date.setFont(font)
        self.label_device_produce_date.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_device_produce_date.setObjectName("label_device_produce_date")
        self.verticalLayout_settings.addWidget(self.label_device_produce_date)
        self.lineEdit_device_veryfing_date = QtWidgets.QLineEdit(self.Settings)
        self.lineEdit_device_veryfing_date.setFont(font)
        self.lineEdit_device_veryfing_date.setObjectName("lineEdit_device_veryfing_date")
        self.lineEdit_device_veryfing_date.textEdited.connect(self.device_veryfing_date_changed)
        self.verticalLayout_settings.addWidget(self.lineEdit_device_veryfing_date)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_settings.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_settings)
        
        self.verticalLayout_buttons = QtWidgets.QVBoxLayout()
        self.verticalLayout_buttons.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_buttons.setSpacing(6)
        self.verticalLayout_buttons.setObjectName("verticalLayout_buttons")
        self.pushButton_settings_ISH = QtWidgets.QPushButton(self.Settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_settings_ISH.sizePolicy().hasHeightForWidth())
        self.pushButton_settings_ISH.setSizePolicy(sizePolicy)
        self.pushButton_settings_ISH.setSizeIncrement(QtCore.QSize(0, 0))
        self.pushButton_settings_ISH.setBaseSize(QtCore.QSize(0, 0))
        self.pushButton_settings_ISH.setFont(font)
        self.pushButton_settings_ISH.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_settings_ISH.setObjectName("pushButton_settings_ISH")
        self.pushButton_settings_ISH.clicked.connect(self.open_settings_ISH)
        self.verticalLayout_buttons.addWidget(self.pushButton_settings_ISH)
        self.pushButton_settings_date = QtWidgets.QPushButton(self.Settings)
        sizePolicy.setHeightForWidth(self.pushButton_settings_date.sizePolicy().hasHeightForWidth())
        self.pushButton_settings_date.setSizePolicy(sizePolicy)
        self.pushButton_settings_date.setFont(font)
        self.pushButton_settings_date.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_settings_date.setObjectName("pushButton_settings_date")
        self.verticalLayout_buttons.addWidget(self.pushButton_settings_date)
        self.pushButton_settings_printer = QtWidgets.QPushButton(self.Settings)
        sizePolicy.setHeightForWidth(self.pushButton_settings_printer.sizePolicy().hasHeightForWidth())
        self.pushButton_settings_printer.setSizePolicy(sizePolicy)
        self.pushButton_settings_printer.setFont(font)
        self.pushButton_settings_printer.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_settings_printer.setObjectName("pushButton_settings_printer")
        self.verticalLayout_buttons.addWidget(self.pushButton_settings_printer)
        self.pushButton_settings_connections = QtWidgets.QPushButton(self.Settings)
        sizePolicy.setHeightForWidth(self.pushButton_settings_connections.sizePolicy().hasHeightForWidth())
        self.pushButton_settings_connections.setSizePolicy(sizePolicy)
        self.pushButton_settings_connections.setFont(font)
        self.pushButton_settings_connections.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_settings_connections.setObjectName("pushButton_settings_connections")
        self.verticalLayout_buttons.addWidget(self.pushButton_settings_connections)
        self.pushButton_settings_verifying = QtWidgets.QPushButton(self.Settings)
        sizePolicy.setHeightForWidth(self.pushButton_settings_verifying.sizePolicy().hasHeightForWidth())
        self.pushButton_settings_verifying.setSizePolicy(sizePolicy)
        self.pushButton_settings_verifying.setFont(font)
        self.pushButton_settings_verifying.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_settings_verifying.setObjectName("pushButton_settings_verifying")
        self.verticalLayout_buttons.addWidget(self.pushButton_settings_verifying)
        self.pushButton_settings_device = QtWidgets.QPushButton(self.Settings)
        self.pushButton_settings_device.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_settings_device.sizePolicy().hasHeightForWidth())
        self.pushButton_settings_device.setSizePolicy(sizePolicy)
        self.pushButton_settings_device.setFont(font)
        self.pushButton_settings_device.setMouseTracking(False)
        self.pushButton_settings_device.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_settings_device.setObjectName("pushButton_settings_device")
        self.verticalLayout_buttons.addWidget(self.pushButton_settings_device)
        self.pushButton_settings_system_update = QtWidgets.QPushButton(self.Settings)
        self.pushButton_settings_system_update.setEnabled(True)
        sizePolicy.setHeightForWidth(self.pushButton_settings_system_update.sizePolicy().hasHeightForWidth())
        self.pushButton_settings_system_update.setSizePolicy(sizePolicy)
        self.pushButton_settings_system_update.setFont(font)
        self.pushButton_settings_system_update.setMouseTracking(False)
        self.pushButton_settings_system_update.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_settings_system_update.setObjectName("pushButton_settings_system_update")
        self.verticalLayout_buttons.addWidget(self.pushButton_settings_system_update)
        self.horizontalLayout.addLayout(self.verticalLayout_buttons)
        self.tab_settings = self.stackedWidget_main.addWidget(self.Settings)
        #   -----------------------------------------------------------------
        #   вкладка Настройка ИСХ
        #   -----------------------------------------------------------------
        self.Settings_ISH = QtWidgets.QWidget()
        self.Settings_ISH.setObjectName("Settings_ISH")

        #   Таблица эталонных датчиков
   
        self.tableWidget_settings_ISH = QtWidgets.QTableWidget(self.Settings_ISH)
        self.tableWidget_settings_ISH.setGeometry(QtCore.QRect(0, 0, 971, 541))
        self.tableWidget_settings_ISH.setObjectName("tableWidget_settings_ISH")
        columnWidths = [50, 80, 321]
        self.tableWidget_settings_ISH.setColumnCount(len(columnWidths))
        rowCount = self.db_query('SELECT COUNT(*) FROM ish_data')[0][0]
        self.tableWidget_settings_ISH.setRowCount(rowCount)
        for column in range(len(columnWidths)):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            self.tableWidget_settings_ISH.setHorizontalHeaderItem(column, item)
            self.tableWidget_settings_ISH.setColumnWidth(column, columnWidths[column])
        self.tableWidget_settings_ISH.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        sensor_ish_data=self.db_query('SELECT ish_data_sensor FROM ish_data')
        for row in range(rowCount):
            font.setPointSize(16)
            item = QtWidgets.QTableWidgetItem() # Создаём строки таблицы ИСХ
            item.setFont(font)
            item.setText(str(row+1))
            self.tableWidget_settings_ISH.setVerticalHeaderItem(row, item)
            self.tableWidget_settings_ISH.setRowHeight (row, 41)
            font.setPointSize(14)
            sensor=self.db_query('SELECT * FROM sensors WHERE sensor_id='+str(sensor_ish_data[row][0]))
            item = QtWidgets.QTableWidgetItem(str(sensor[0][1]))
            item.setFont(font)
            item.setFlags(Qt.ItemFlag.ItemIsSelectable)
            self.tableWidget_settings_ISH.setItem(row, 0, item) # Записываем в таблцу ИСХ название датчика
            item = QtWidgets.QTableWidgetItem(sensor[0][4])
            item.setFont(font)
            item.setFlags(Qt.ItemFlag.ItemIsSelectable)
            self.tableWidget_settings_ISH.setItem(row, 1, item) # Записываем в таблицу ИСХ тип датчика
            match str(sensor[0][4]):
                case "ЭТС":
                    sensor_type="ets"
                case "ППО":
                    sensor_type="ppo"
                case "ПРО":
                    sensor_type="pro"
                case _:
                    sensor_type="error"
            coef_set = self.db_query('SELECT option_value FROM options WHERE option_name="coef_set_ish_'+sensor_type+'"')
            group_name = "self.groupBox_coef_set_ish_"+sensor_type+"_"+str(row)
            exec(group_name+" = QtWidgets.QGroupBox(self.Settings_ISH)")
            exec(group_name+".setGeometry(QtCore.QRect(0, 0, "+str((coef_set[0][0].count(',')+1)*40)+", 40))")
            exec(group_name+".setTitle('')")
            exec(group_name+".setObjectName('"+group_name[5:]+"')")            
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(Qt.ItemFlag.ItemIsSelectable)
            self.tableWidget_settings_ISH.setItem(row, 2, item)
            self.tableWidget_settings_ISH.setCellWidget(row, 2, eval(group_name))
            i = 0
            for coef in coef_set[0][0].split(","):
                button_name = "self.pushButton_"+sensor[0][4]+"_"+coef+"_"+str(row)
                exec(button_name+" = QtWidgets.QPushButton("+group_name+")")
                exec(button_name+".setFont(font)")
                exec(button_name+".setGeometry(QtCore.QRect("+str(i*40)+", 0, 40, 40))")
                i+=1
                exec(button_name+".setObjectName('"+button_name[5:]+"')")
                exec(button_name+".setText('"+coef+"')")
                coef_val = self.db_query("SELECT ish_data_"+coef+" FROM ish_data WHERE ish_data_sensor="+str(sensor_ish_data[row][0]))
                exec(button_name+".clicked.connect(self.coef_edit)")
                if coef_val[0][0] is not None and coef_val[0][0] != 0:
                    exec(button_name+".setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(38, 0, 255);')")
 
            # brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
            # brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
            # brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
            # brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
            # item.setBackground(brush)

        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget_settings_ISH.setItem(0, 1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.tableWidget_settings_ISH.setItem(1, 1, item)
        # item = QtWidgets.QTableWidgetItem()
        # brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        # brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        # item.setBackground(brush)
        # brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        # brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        # item.setForeground(brush)
        # self.tableWidget_settings_ISH.setItem(3, 1, item)
        # self.tableWidget_settings_ISH.horizontalHeader().setVisible(False)
        # self.tableWidget_settings_ISH.horizontalHeader().setStretchLastSection(False)
        
        self.pushButton_ish_back = QtWidgets.QPushButton(self.Settings_ISH)
        self.pushButton_ish_back.setGeometry(QtCore.QRect(414, 550, 141, 31))
        self.pushButton_ish_back.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_ish_back.setObjectName("pushButton_back")
        self.pushButton_ish_back.clicked.connect(lambda :self.stackedWidget_main.setCurrentIndex(1))
        self.tab_settings_ish = self.stackedWidget_main.addWidget(self.Settings_ISH)


        #   -----------------------------------------------------------------
        #   вкладка Датчики
        #   -----------------------------------------------------------------
        self.Sensors = QtWidgets.QWidget()
        self.Sensors.setObjectName("Sensors")

        #   Таблица датчиков
   
        self.tableWidget_sensors = QtWidgets.QTableWidget(self.Sensors)
        self.tableWidget_sensors.setGeometry(QtCore.QRect(0, 0, 971, 541))
        self.tableWidget_sensors.setObjectName("tableWidget_sensors")
        columnWidths = [50, 178, 78, 98, 100, 130]
        columnCount = len(columnWidths)
        self.tableWidget_sensors.setColumnCount(columnCount)
        rowCount = self.db_query('SELECT COUNT(*) FROM sensors')[0][0]
        self.tableWidget_sensors.setRowCount(rowCount)
        for column in range(columnCount):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            self.tableWidget_sensors.setHorizontalHeaderItem(column, item)
            self.tableWidget_sensors.setColumnWidth(column, columnWidths[column])
        self.tableWidget_sensors.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        sensor=self.db_query('SELECT * FROM sensors')
        for row in range(rowCount):
            font.setPointSize(16)
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            item.setText(str(row+1))
            self.tableWidget_sensors.setVerticalHeaderItem(row, item)
            font.setPointSize(14)
            for column in range (columnCount):
                item = QtWidgets.QTableWidgetItem(str(sensor[row][column+1]))
                item.setFont(font)
                item.setFlags(Qt.ItemFlag.ItemIsSelectable)
                self.tableWidget_sensors.setItem(row, column, item)
        self.pushButton_sensors_back = QtWidgets.QPushButton(self.Sensors)
        self.pushButton_sensors_back.setGeometry(QtCore.QRect(414, 550, 141, 31))
        self.pushButton_sensors_back.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_sensors_back.setObjectName("pushButton_sensors_back")
        self.pushButton_sensors_back.clicked.connect(lambda :self.stackedWidget_main.setCurrentIndex(1))
        self.pushButton_sensor_add = QtWidgets.QPushButton(self.Sensors)
        self.pushButton_sensor_add.setGeometry(QtCore.QRect(50, 550, 141, 31))
        self.pushButton_sensor_add.setObjectName("pushButton_sensor_add")
        self.pushButton_sensor_add.clicked.connect(lambda: self.add_sensor_to_list(-1))
        self.tableWidget_sensors.cellClicked.connect(self.add_sensor_to_list)
        self.tab_sensors = self.stackedWidget_main.addWidget(self.Sensors)
        #   -----------------------------------------------------------------
        #                       вкладка РУЧНОЕ ИЗМЕРЕНИЕ
        #   -----------------------------------------------------------------
        self.Manual = QtWidgets.QWidget()
        self.Manual.setObjectName("Manual")
        self.pushButton_manual_start_stop = QtWidgets.QPushButton(self.Manual)
        self.pushButton_manual_start_stop.setGeometry(QtCore.QRect(60, 530, 191, 51))
        self.pushButton_manual_start_stop.clicked.connect(self.manual_start_stop)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_manual_start_stop.setFont(font)
        self.pushButton_manual_start_stop.setStyleSheet("background-color: rgb(31, 100, 10); color: rgb(255, 255, 255);")
        self.pushButton_manual_start_stop.setObjectName("pushButton_manual_start_stop")
        self.groupBox_manual_path = QtWidgets.QGroupBox(self.Manual)
        self.groupBox_manual_path.setGeometry(QtCore.QRect(350, 530, 571, 51))
        self.groupBox_manual_path.setTitle("")
        self.groupBox_manual_path.setObjectName("groupBox_manual_path")
        self.pushButton_manual_channels_settings = QtWidgets.QPushButton(self.groupBox_manual_path)
        self.pushButton_manual_channels_settings.setGeometry(QtCore.QRect(0, 0, 191, 51))
        font.setPointSize(10)
        self.pushButton_manual_channels_settings.setFont(font)
        self.pushButton_manual_channels_settings.setObjectName("pushButton_manual_channels_settings")
        self.pushButton_manual_channels_settings.clicked.connect(lambda :self.stackedWidget_Manual.setCurrentIndex(0))
        self.pushButton_manual_measuring = QtWidgets.QPushButton(self.groupBox_manual_path)
        self.pushButton_manual_measuring.setGeometry(QtCore.QRect(190, 0, 191, 51))
        self.pushButton_manual_measuring.setFont(font)
        self.pushButton_manual_measuring.setObjectName("pushButton_manual_measuring")
        self.pushButton_manual_measuring.clicked.connect(lambda :self.stackedWidget_Manual.setCurrentIndex(1))
        self.pushButton_manual_result = QtWidgets.QPushButton(self.groupBox_manual_path)
        self.pushButton_manual_result.setGeometry(QtCore.QRect(380, 0, 191, 51))
        self.pushButton_manual_result.setFont(font)
        self.pushButton_manual_result.setObjectName("pushButton_manual_result")
        self.pushButton_manual_result.clicked.connect(lambda :self.stackedWidget_Manual.setCurrentIndex(2))
        
        self.stackedWidget_Manual = QtWidgets.QStackedWidget(self.Manual)
        self.stackedWidget_Manual.setGeometry(QtCore.QRect(0, 0, 971, 521))
        self.stackedWidget_Manual.setObjectName("stackedWidget_Manual")
        self.channels_settings = QtWidgets.QWidget()
        self.channels_settings.setObjectName("channels_settings")

        #   -----------------------------------------------------------------
        #   Таблица уставок
        #   -----------------------------------------------------------------

        self.tableWidget_ustavka = QtWidgets.QTableWidget(self.channels_settings)
        self.tableWidget_ustavka.setGeometry(QtCore.QRect(0, 0, 141, 521))
        self.tableWidget_ustavka.setObjectName("tableWidget_ustavka")
        self.tableWidget_ustavka.setColumnCount(2)
        self.tableWidget_ustavka.setRowCount(1)
        for column in range(2):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_ustavka.setHorizontalHeaderItem(column, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget_ustavka.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tableWidget_ustavka.setItem(0, 1, item)
        self.tableWidget_ustavka.horizontalHeader().setDefaultSectionSize(60)
        self.tableWidget_ustavka.cellClicked.connect(self.add_ustavka_to_tab)

        #   -----------------------------------------------------------------
        #   Таблица каналов
        #   -----------------------------------------------------------------

        self.tableWidget_channels_settings = QtWidgets.QTableWidget(self.channels_settings)
        self.tableWidget_channels_settings.setGeometry(QtCore.QRect(140, 0, 831, 521))
        self.tableWidget_channels_settings.setObjectName("tableWidget_channels_settings")
        self.tableWidget_channels_settings.cellClicked.connect(self.add_sensor_to_tab)
        columnWidths = [50, 178, 78, 98, 100, 130]
        columnCount = len(columnWidths)
        rowCount = 8
        self.tableWidget_channels_settings.setColumnCount(columnCount)
        self.tableWidget_channels_settings.setRowCount(rowCount)
        font.setPointSize(13)
        for row in range(rowCount):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            self.tableWidget_channels_settings.setVerticalHeaderItem(row, item)
            for column in range(columnCount):
                if row == 0:
                    item = QtWidgets.QTableWidgetItem()
                    item.setFont(font)
                    self.tableWidget_channels_settings.setHorizontalHeaderItem(column, item)
                    self.tableWidget_channels_settings.setColumnWidth(column, columnWidths[column])
                if column == 0:
                    item = QtWidgets.QTableWidgetItem("+")
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter)
                    item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                else:
                    item = QtWidgets.QTableWidgetItem("")
                    item.setFlags(Qt.ItemFlag.NoItemFlags)
                font.setPointSize(14)
                item.setFont(font)
                self.tableWidget_channels_settings.setItem(row, column, item)
        self.tableWidget_channels_settings.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget_channels_settings.horizontalHeader().setDefaultSectionSize(116)
        self.stackedWidget_Manual.addWidget(self.channels_settings)

        #   -----------------------------------------------------------------
        #   Раздел Измерение
        #   -----------------------------------------------------------------

        self.measuring = QtWidgets.QWidget()
        self.measuring.setObjectName("measuring")
        self.tableWidget_progress_bar = QtWidgets.QTableWidget(self.measuring)
        self.tableWidget_progress_bar.setGeometry(QtCore.QRect(0, 0, 921, 21))
        self.tableWidget_progress_bar.setObjectName("tableWidget_progress_bar")
        self.tableWidget_progress_bar.setColumnCount(0)
        self.tableWidget_progress_bar.setRowCount(1)
        self.tableWidget_progress_bar.verticalHeader().hide()
        self.tableWidget_progress_bar.horizontalHeader().hide()
        self.tableWidget_progress_bar.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_progress_bar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableWidget_progress_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_progress_bar.setVerticalHeaderItem(0, item)

        #   -----------------------------------------------------------------
        #   Переключатель график\таблица
        #   -----------------------------------------------------------------

        self.measuring_view = QtWidgets.QStackedWidget(self.measuring)
        self.measuring_view.setGeometry(QtCore.QRect(0, 30, 981, 491))
        self.measuring_view.setObjectName("measuring_view")
        self.graph = QtWidgets.QWidget()
        self.graph.setObjectName("graph")
        self.groupBox_channels_buttons = QtWidgets.QGroupBox(self.graph)
        self.groupBox_channels_buttons.setGeometry(QtCore.QRect(0, 0, 110, 441))
        # self.groupBox_channels_buttons.setStyleSheet('border-style: none')
        self.groupBox_channels_buttons.setObjectName("groupBox_channels_buttons")
        font = QtGui.QFont()
        self.color_buttons = ["24, 181, 59", "130, 109, 255", "84, 114, 47", "242, 80, 80",
                        "0, 255, 0", "224, 192, 79", "43, 209, 199", "60, 84, 119", "0, 0, 255"]
        for i in range (9):
            exec(f"self.pushButton_{str(i+1)} = QtWidgets.QPushButton(self.groupBox_channels_buttons)")
            exec(f"self.pushButton_{str(i+1)}.setGeometry(QtCore.QRect(0, "+str(i*50)+", 41, 41))")
            font.setPointSize(20)
            exec("self.pushButton_"+str(i+1)+".setFont(font)")
            if i != 8: exec("self.pushButton_"+str(i+1)+".setEnabled(False)")
            exec("self.pushButton_"+str(i+1)+".setCheckable(True)")
            exec("self.pushButton_"+str(i+1)+".setStyleSheet('color: rgb(255, 255, 255); background-color: rgb("+self.color_buttons[i]+")')")
            exec("self.pushButton_"+str(i+1)+".setObjectName('pushButton_"+str(i+1)+"')")
            exec("self.pushButton_"+str(i+1)+".clicked.connect(self.graph_btn_toggle)")
            exec("self.label_temp_of_chan_"+str(i+1)+"= QtWidgets.QLabel(self.groupBox_channels_buttons)")
            exec("self.label_temp_of_chan_"+str(i+1)+".setObjectName('label_temp_of_chan_"+str(i+1)+"')")
            exec("self.label_temp_of_chan_"+str(i+1)+".setGeometry(QtCore.QRect(45, "+str(i*50)+", 65, 41))")
            font.setPointSize(14)
            exec("self.label_temp_of_chan_"+str(i+1)+".setFont(font)")
        self.pushButton_9.setChecked(True)
        self.graphWidget = pg.PlotWidget(self.graph, axisItems={'bottom': pg.DateAxisItem()}) # pg.DateAxisItem(utcOffset=0)
        self.graphWidget.setGeometry(QtCore.QRect(110, 0, 811, 491))
        self.graphWidget.setObjectName("graphWidget")
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True)
        self.groupBox_navigate_buttons = QtWidgets.QGroupBox(self.graph)
        self.groupBox_navigate_buttons.setGeometry(QtCore.QRect(930, 0, 41, 441))
        self.groupBox_navigate_buttons.setObjectName("groupBox_navigate_buttons")
        buttons = ["move_graph_left", "move_graph_right", "move_graph_up", "move_graph_down", "scale_vertical_up", "scale_vertical_down", "scale_horizontal_up", "scale_horizontal_down", "scale_auto"]
        font = QtGui.QFont()
        font.setPointSize(12)
        for i in range(len(buttons)):
            exec("self.pushButton_"+buttons[i]+" = QtWidgets.QPushButton(self.groupBox_navigate_buttons)")
            exec("self.pushButton_"+buttons[i]+".setGeometry(QtCore.QRect(0, "+str(i*50)+", 41, 41))")
            exec("self.pushButton_"+buttons[i]+".setFont(font)")
            # self.pushButton_left.setStyleSheet("")
            exec("self.pushButton_"+buttons[i]+".setObjectName('pushButton_"+buttons[i]+"')")
            exec("self.pushButton_"+buttons[i]+".clicked.connect(self."+buttons[i]+")")

        self.pushButton_view_table = QtWidgets.QPushButton(self.graph)
        self.pushButton_view_table.setGeometry(QtCore.QRect(930, 450, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_view_table.setFont(font)
        self.pushButton_view_table.setStyleSheet("")
        self.pushButton_view_table.setObjectName("pushButton_view_table")
        self.pushButton_view_table.clicked.connect(lambda :self.measuring_view.setCurrentIndex(1))
        self.measuring_view.addWidget(self.graph)

        #   -----------------------------------------------------------------
        #   Таблица показаний в ходе ручного измерения.
        #   -----------------------------------------------------------------

        self.table = QtWidgets.QWidget()
        self.table.setObjectName("table")
        self.tableWidget = QtWidgets.QTableWidget(self.table)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 921, 491))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(7)
        for row in range(7):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(row, item)
        for col in range(8):
            item = QtWidgets.QTableWidgetItem(str(col))
            self.tableWidget.setItem(0, col, item)
            for row in range(6):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(row+1, col, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(92)
        
        self.pushButton_view_graph = QtWidgets.QPushButton(self.table)
        self.pushButton_view_graph.setGeometry(QtCore.QRect(930, 450, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_view_graph.setFont(font)
        self.pushButton_view_graph.setStyleSheet("")
        self.pushButton_view_graph.setObjectName("pushButton_view_graph")
        self.pushButton_view_graph.clicked.connect(lambda :self.measuring_view.setCurrentIndex(0))
        self.measuring_view.addWidget(self.table)
        self.stackedWidget_Manual.addWidget(self.measuring)
        self.tab_manual = self.stackedWidget_main.addWidget(self.Manual)

        #   -----------------------------------------------------------------
        #   Раздел Результат
        #   -----------------------------------------------------------------

        self.manual_result = QtWidgets.QWidget()
        self.manual_result.setObjectName("manual_result")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.manual_result)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 971, 521))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_manual_result = QtWidgets.QGroupBox(self.horizontalLayoutWidget_3)
        self.groupBox_manual_result.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_manual_result.setTitle("")
        self.groupBox_manual_result.setObjectName("groupBox_manual_result")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_manual_result)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_manual_model = QtWidgets.QLineEdit(self.groupBox_manual_result)
        self.lineEdit_manual_model.setObjectName("lineEdit_model")
        self.gridLayout_3.addWidget(self.lineEdit_manual_model, 6, 1, 1, 1)
        self.label_manual_number = QtWidgets.QLabel(self.groupBox_manual_result)
        self.label_manual_number.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_manual_number.setObjectName("label_manual_number")
        self.gridLayout_3.addWidget(self.label_manual_number, 7, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(454, 402, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 8, 0, 1, 2)
        self.label_manual_fio = QtWidgets.QLabel(self.groupBox_manual_result)
        self.label_manual_fio.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_manual_fio.setObjectName("label_manual_fio")
        self.gridLayout_3.addWidget(self.label_manual_fio, 3, 0, 1, 1)
        self.label_manual_model = QtWidgets.QLabel(self.groupBox_manual_result)
        self.label_manual_model.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_manual_model.setObjectName("label_manual_model")
        self.gridLayout_3.addWidget(self.label_manual_model, 6, 0, 1, 1)
        self.label_manual_megaommetr = QtWidgets.QLabel(self.groupBox_manual_result)
        self.label_manual_megaommetr.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_manual_megaommetr.setObjectName("label_manual_megaommetr")
        self.gridLayout_3.addWidget(self.label_manual_megaommetr, 5, 0, 1, 1)
        self.label_manual_customer = QtWidgets.QLabel(self.groupBox_manual_result)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_manual_customer.setFont(font)
        self.label_manual_customer.setStyleSheet("")
        self.label_manual_customer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_manual_customer.setObjectName("label_manual_customer")
        self.gridLayout_3.addWidget(self.label_manual_customer, 0, 0, 1, 2)
        self.lineEdit_manual_customer = QtWidgets.QLineEdit(self.groupBox_manual_result)
        self.lineEdit_manual_customer.setObjectName("lineEdit_manual_customer")
        self.gridLayout_3.addWidget(self.lineEdit_manual_customer, 2, 0, 1, 2)
        self.lineEdit_manual_operators_name = QtWidgets.QLineEdit(self.groupBox_manual_result)
        self.lineEdit_manual_operators_name.setObjectName("lineEdit_manual_operators_name")
        self.gridLayout_3.addWidget(self.lineEdit_manual_operators_name, 4, 0, 1, 2)
        self.lineEdit_manual_number = QtWidgets.QLineEdit(self.groupBox_manual_result)
        self.lineEdit_manual_number.setObjectName("lineEdit_manual_number")
        self.gridLayout_3.addWidget(self.lineEdit_manual_number, 7, 1, 1, 1)
        self.label_manual_customer_2 = QtWidgets.QLabel(self.groupBox_manual_result)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_manual_customer_2.setFont(font)
        self.label_manual_customer_2.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_manual_customer_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_manual_customer_2.setObjectName("label_manual_customer_2")
        self.gridLayout_3.addWidget(self.label_manual_customer_2, 1, 0, 1, 2)
        self.horizontalLayout_3.addWidget(self.groupBox_manual_result)
        self.groupBox_manual_measuring_conditions = QtWidgets.QGroupBox(self.horizontalLayoutWidget_3)
        self.groupBox_manual_measuring_conditions.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_manual_measuring_conditions.setTitle("")
        self.groupBox_manual_measuring_conditions.setObjectName("groupBox_manual_measuring_conditions")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_manual_measuring_conditions)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_manual_t_atm = QtWidgets.QLabel(self.groupBox_manual_measuring_conditions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_manual_t_atm.sizePolicy().hasHeightForWidth())
        self.label_manual_t_atm.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_manual_t_atm.setFont(font)
        self.label_manual_t_atm.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_manual_t_atm.setObjectName("label_manual_t_atm")
        self.gridLayout_4.addWidget(self.label_manual_t_atm, 1, 0, 1, 1)
        self.lineEdit_manual_temp = QtWidgets.QLineEdit(self.groupBox_manual_measuring_conditions)
        self.lineEdit_manual_temp.setText("")
        self.lineEdit_manual_temp.setObjectName("lineEdit_manual_temp")
        self.gridLayout_4.addWidget(self.lineEdit_manual_temp, 1, 1, 1, 1)
        self.label_manual_p_atm = QtWidgets.QLabel(self.groupBox_manual_measuring_conditions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_manual_p_atm.sizePolicy().hasHeightForWidth())
        self.label_manual_p_atm.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_manual_p_atm.setFont(font)
        self.label_manual_p_atm.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_manual_p_atm.setObjectName("label_manual_p_atm")
        self.gridLayout_4.addWidget(self.label_manual_p_atm, 2, 0, 1, 1)
        self.lineEdit_manual_pressure = QtWidgets.QLineEdit(self.groupBox_manual_measuring_conditions)
        self.lineEdit_manual_pressure.setText("")
        self.lineEdit_manual_pressure.setObjectName("lineEdit_manual_pressure")
        self.gridLayout_4.addWidget(self.lineEdit_manual_pressure, 2, 1, 1, 1)
        self.label_manual_hydro = QtWidgets.QLabel(self.groupBox_manual_measuring_conditions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_manual_hydro.sizePolicy().hasHeightForWidth())
        self.label_manual_hydro.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_manual_hydro.setFont(font)
        self.label_manual_hydro.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_manual_hydro.setObjectName("label_manual_hydro")
        self.gridLayout_4.addWidget(self.label_manual_hydro, 4, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_4.addItem(spacerItem4, 5, 0, 1, 2)
        self.lineEdit_manual_hydro = QtWidgets.QLineEdit(self.groupBox_manual_measuring_conditions)
        self.lineEdit_manual_hydro.setText("")
        self.lineEdit_manual_hydro.setObjectName("lineEdit_manual_hydro")
        self.gridLayout_4.addWidget(self.lineEdit_manual_hydro, 4, 1, 1, 1)
        self.label_manual_article_name = QtWidgets.QLabel(self.groupBox_manual_measuring_conditions)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_manual_article_name.setFont(font)
        self.label_manual_article_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_manual_article_name.setObjectName("label_manual_article_name")
        self.gridLayout_4.addWidget(self.label_manual_article_name, 0, 0, 1, 2)
        self.horizontalLayout_3.addWidget(self.groupBox_manual_measuring_conditions)
        self.pushButton_save_protocol = QtWidgets.QPushButton(self.groupBox_manual_measuring_conditions)
        self.pushButton_save_protocol.setGeometry(QtCore.QRect(100, 170, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_save_protocol.setFont(font)
        self.pushButton_save_protocol.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(96, 121, 255);")
        self.pushButton_save_protocol.setObjectName("pushButton_save_protocol")
        self.pushButton_save_protocol.clicked.connect(self.save_manual_protocol)
        self.gridLayout_4.addWidget(self.pushButton_save_protocol)
        self.stackedWidget_Manual.addWidget(self.manual_result)

        #   -----------------------------------------------------------------
        #                       вкладка АВТОМАТИЧЕСКОЕ ИЗМЕРЕНИЕ
        #   -----------------------------------------------------------------

        self.Auto = QtWidgets.QWidget()
        self.Auto.setObjectName("Auto")
        self.groupBox_bottom_buttons = QtWidgets.QGroupBox(self.Auto)
        self.groupBox_bottom_buttons.setGeometry(QtCore.QRect(30, 490, 901, 51))
        self.groupBox_bottom_buttons.setObjectName("groupBox_bottom_buttons")
        self.pushButton_measuring_type = QtWidgets.QPushButton(self.groupBox_bottom_buttons)
        self.pushButton_measuring_type.setGeometry(QtCore.QRect(0, 0, 180, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_measuring_type.setFont(font)
        self.pushButton_measuring_type.setStyleSheet("color: rgb(154, 154, 154);")
        self.pushButton_measuring_type.setObjectName("pushButton_measuring_type")
        self.pushButton_measuring_type.clicked.connect(lambda :self.stackedWidget_auto_measuring_modes.setCurrentIndex(0))
        self.pushButton_tpoints_sensors = QtWidgets.QPushButton(self.groupBox_bottom_buttons)
        self.pushButton_tpoints_sensors.setGeometry(QtCore.QRect(180, 0, 180, 51))
        self.pushButton_tpoints_sensors.setFont(font)
        self.pushButton_tpoints_sensors.setStyleSheet("color: rgb(154, 154, 154);")
        self.pushButton_tpoints_sensors.setObjectName("pushButton_tpoints_sensors")
        self.pushButton_tpoints_sensors.clicked.connect(lambda :self.stackedWidget_auto_measuring_modes.setCurrentIndex(1))
        self.pushButton_measuring_settings = QtWidgets.QPushButton(self.groupBox_bottom_buttons)
        self.pushButton_measuring_settings.setGeometry(QtCore.QRect(360, 0, 180, 51))
        self.pushButton_measuring_settings.setFont(font)
        self.pushButton_measuring_settings.setStyleSheet("color: rgb(154, 154, 154);")
        self.pushButton_measuring_settings.setObjectName("pushButton_measuring_settings")
        self.pushButton_measuring_settings.clicked.connect(lambda :self.stackedWidget_auto_measuring_modes.setCurrentIndex(2))
        self.pushButton_start_stop_manual = QtWidgets.QPushButton(self.groupBox_bottom_buttons)
        self.pushButton_start_stop_manual.setGeometry(QtCore.QRect(540, 0, 180, 51))
        self.pushButton_start_stop_manual.setFont(font)
        self.pushButton_start_stop_manual.setStyleSheet("color: rgb(154, 154, 154);")
        self.pushButton_start_stop_manual.setObjectName("pushButton_start_stop_manual")
        self.pushButton_start_stop_manual.clicked.connect(lambda :self.stackedWidget_auto_measuring_modes.setCurrentIndex(3))
        self.pushButton_protocol = QtWidgets.QPushButton(self.groupBox_bottom_buttons)
        self.pushButton_protocol.setGeometry(QtCore.QRect(720, 0, 180, 51))
        self.pushButton_protocol.setFont(font)
        self.pushButton_protocol.setStyleSheet("color: rgb(154, 154, 154);")
        self.pushButton_protocol.setObjectName("pushButton_protocol")
        self.pushButton_protocol.clicked.connect(lambda :self.stackedWidget_auto_measuring_modes.setCurrentIndex(4))

        self.stackedWidget_auto_measuring_modes = QtWidgets.QStackedWidget(self.Auto)
        self.stackedWidget_auto_measuring_modes.setGeometry(QtCore.QRect(-1, -1, 971, 481))
        self.stackedWidget_auto_measuring_modes.setObjectName("stackedWidget_auto_measuring_modes")
        self.measuring_type = QtWidgets.QWidget()
        self.measuring_type.setObjectName("measuring_type")
        self.pushButton_veryfication_TS = QtWidgets.QPushButton(self.measuring_type)
        self.pushButton_veryfication_TS.setGeometry(QtCore.QRect(520, 160, 341, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_veryfication_TS.setFont(font)
        self.pushButton_veryfication_TS.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_veryfication_TS.setObjectName("pushButton_veryfication_TS")
        self.pushButton_graduation_TS = QtWidgets.QPushButton(self.measuring_type)
        self.pushButton_graduation_TS.setGeometry(QtCore.QRect(520, 270, 341, 71))
        self.pushButton_graduation_TS.setFont(font)
        self.pushButton_graduation_TS.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_graduation_TS.setObjectName("pushButton_graduation_TS")
        self.pushButton_calibration_TP = QtWidgets.QPushButton(self.measuring_type)
        self.pushButton_calibration_TP.setGeometry(QtCore.QRect(100, 270, 341, 71))
        self.pushButton_calibration_TP.setFont(font)
        self.pushButton_calibration_TP.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_calibration_TP.setObjectName("pushButton_calibration_TP")
        self.pushButton_veryfication_TP = QtWidgets.QPushButton(self.measuring_type)
        self.pushButton_veryfication_TP.setGeometry(QtCore.QRect(100, 160, 341, 71))
        self.pushButton_veryfication_TP.setFont(font)
        self.pushButton_veryfication_TP.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_veryfication_TP.setObjectName("pushButton_veryfication_TP")
        self.pushButton_veryfication_TP.clicked.connect(lambda :self.stackedWidget_measuring_types_tables.setCurrentIndex(0))
        self.stackedWidget_auto_measuring_modes.addWidget(self.measuring_type)
        self.tpoints_sensors = QtWidgets.QWidget()
        self.tpoints_sensors.setObjectName("tpoints_sensors")
        self.stackedWidget_measuring_types_tables = QtWidgets.QStackedWidget(self.tpoints_sensors)
        self.stackedWidget_measuring_types_tables.setGeometry(QtCore.QRect(60, 0, 911, 481))
        self.stackedWidget_measuring_types_tables.setObjectName("stackedWidget_measuring_types_tables")

        #   -----------------------------------------------------------------
        #   Раздел измерения термопар в автоматическом режиме.
        #   -----------------------------------------------------------------
        
        self.TP = QtWidgets.QWidget()
        self.TP.setObjectName("TP")
        self.tableWidget_TP = QtWidgets.QTableWidget(self.TP)
        self.tableWidget_TP.setGeometry(QtCore.QRect(0, 0, 911, 481))
        self.tableWidget_TP.setObjectName("tableWidget_TP")
        self.tableWidget_TP.setColumnCount(9)
        self.tableWidget_TP.setRowCount(8)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        item.setFont(font)
        font.setPointSize(16)
        for row in range(8):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            self.tableWidget_TP.setVerticalHeaderItem(row, item)
        for col in range(9):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_TP.setHorizontalHeaderItem(col, item)
        for row in range (8):
            for col in range(2):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFont(font)
                self.tableWidget_TP.setItem(row, col, item)
        self.tableWidget_TP.horizontalHeader().setDefaultSectionSize(150)
        self.stackedWidget_measuring_types_tables.addWidget(self.TP)

        #   -----------------------------------------------------------------
        #   Раздел поверки термоспоротивлений в автоматическом режиме.
        #   -----------------------------------------------------------------

        self.TS_veryfications = QtWidgets.QWidget()
        self.TS_veryfications.setObjectName("TS_veryfications")
        self.tableWidget_TS_veryfications = QtWidgets.QTableWidget(self.TS_veryfications)
        self.tableWidget_TS_veryfications.setGeometry(QtCore.QRect(0, 0, 911, 481))
        self.tableWidget_TS_veryfications.setObjectName("tableWidget_TS_veryfications")
        self.tableWidget_TS_veryfications.setColumnCount(10)
        self.tableWidget_TS_veryfications.setRowCount(8)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        item.setFont(font)
        font.setPointSize(16)
        for row in range(8):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            self.tableWidget_TS_veryfications.setVerticalHeaderItem(row, item)
        for col in range(10):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_TS_veryfications.setHorizontalHeaderItem(col, item)
        for row in range (8):
            for col in range(2):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFont(font)
                self.tableWidget_TS_veryfications.setItem(row, col, item)
        self.tableWidget_TS_veryfications.horizontalHeader().setDefaultSectionSize(150)
        self.stackedWidget_measuring_types_tables.addWidget(self.TS_veryfications)

        #   -----------------------------------------------------------------
        #   Раздел градуировки термосопротивлений в автоматическом режиме.
        #   -----------------------------------------------------------------
        
        self.TS_gradiations = QtWidgets.QWidget()
        self.TS_gradiations.setObjectName("TS_gradiations")
        self.tableWidget_TS_gradiations = QtWidgets.QTableWidget(self.TS_gradiations)
        self.tableWidget_TS_gradiations.setGeometry(QtCore.QRect(0, 0, 911, 481))
        self.tableWidget_TS_gradiations.setObjectName("tableWidget_TS_gradiations")
        self.tableWidget_TS_gradiations.setColumnCount(9)
        self.tableWidget_TS_gradiations.setRowCount(8)
        font = QtGui.QFont()
        font.setPointSize(16)
        for row in range(8):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            self.tableWidget_TS_gradiations.setVerticalHeaderItem(row, item)
        for col in range(9):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_TS_gradiations.setHorizontalHeaderItem(col, item)
        for row in range(8):
            for col in range(2):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFont(font)
                self.tableWidget_TS_gradiations.setItem(row, col, item)
        self.tableWidget_TS_gradiations.horizontalHeader().setDefaultSectionSize(150)
        self.stackedWidget_measuring_types_tables.addWidget(self.TS_gradiations)


        self.tableWidget_tpoints = QtWidgets.QTableWidget(self.tpoints_sensors)
        self.tableWidget_tpoints.setGeometry(QtCore.QRect(0, 0, 61, 481))
        self.tableWidget_tpoints.setObjectName("tableWidget_tpoints")
        self.tableWidget_tpoints.setColumnCount(1)
        self.tableWidget_tpoints.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_tpoints.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        item.setForeground(brush)
        self.tableWidget_tpoints.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(16)
        item.setFont(font)
        self.tableWidget_tpoints.setItem(0, 0, item)
        self.tableWidget_tpoints.horizontalHeader().setDefaultSectionSize(50)
        self.stackedWidget_auto_measuring_modes.addWidget(self.tpoints_sensors)

        self.measuring_settings = QtWidgets.QWidget()
        self.measuring_settings.setObjectName("measuring_settings")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.measuring_settings)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 971, 481))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_measuring_data = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_measuring_data.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_measuring_data.setTitle("")
        self.groupBox_measuring_data.setObjectName("groupBox_measuring_data")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_measuring_data)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_model = QtWidgets.QLineEdit(self.groupBox_measuring_data)
        self.lineEdit_model.setObjectName("lineEdit_model")
        self.gridLayout_2.addWidget(self.lineEdit_model, 6, 1, 1, 1)
        self.label_number = QtWidgets.QLabel(self.groupBox_measuring_data)
        self.label_number.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_number.setObjectName("label_number")
        self.gridLayout_2.addWidget(self.label_number, 7, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(454, 402, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 8, 0, 1, 2)
        self.label_fio = QtWidgets.QLabel(self.groupBox_measuring_data)
        self.label_fio.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_fio.setObjectName("label_fio")
        self.gridLayout_2.addWidget(self.label_fio, 3, 0, 1, 1)
        self.label_model = QtWidgets.QLabel(self.groupBox_measuring_data)
        self.label_model.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_model.setObjectName("label_model")
        self.gridLayout_2.addWidget(self.label_model, 6, 0, 1, 1)
        self.label_megaommetr = QtWidgets.QLabel(self.groupBox_measuring_data)
        self.label_megaommetr.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_megaommetr.setObjectName("label_megaommetr")
        self.gridLayout_2.addWidget(self.label_megaommetr, 5, 0, 1, 1)
        self.label_customer = QtWidgets.QLabel(self.groupBox_measuring_data)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_customer.setFont(font)
        self.label_customer.setStyleSheet("")
        self.label_customer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_customer.setObjectName("label_customer")
        self.gridLayout_2.addWidget(self.label_customer, 0, 0, 1, 2)
        self.lineEdit_customer = QtWidgets.QLineEdit(self.groupBox_measuring_data)
        self.lineEdit_customer.setObjectName("textBrowser_customer")
        self.gridLayout_2.addWidget(self.lineEdit_customer, 2, 0, 1, 2)
        self.lineEdit_operators_name = QtWidgets.QLineEdit(self.groupBox_measuring_data)
        self.lineEdit_operators_name.setObjectName("lineEdit_operators_name")
        self.gridLayout_2.addWidget(self.lineEdit_operators_name, 4, 0, 1, 2)
        self.lineEdit_number = QtWidgets.QLineEdit(self.groupBox_measuring_data)
        self.lineEdit_number.setObjectName("lineEdit_number")
        self.gridLayout_2.addWidget(self.lineEdit_number, 7, 1, 1, 1)
        self.label_customer_2 = QtWidgets.QLabel(self.groupBox_measuring_data)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_customer_2.setFont(font)
        self.label_customer_2.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_customer_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_customer_2.setObjectName("label_customer_2")
        self.gridLayout_2.addWidget(self.label_customer_2, 1, 0, 1, 2)
        self.horizontalLayout_2.addWidget(self.groupBox_measuring_data)
        self.groupBox_measuring_conditions = QtWidgets.QGroupBox(self.horizontalLayoutWidget)
        self.groupBox_measuring_conditions.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_measuring_conditions.setTitle("")
        self.groupBox_measuring_conditions.setObjectName("groupBox_measuring_conditions")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_measuring_conditions)
        self.gridLayout.setObjectName("gridLayout")
        self.label_t_atm = QtWidgets.QLabel(self.groupBox_measuring_conditions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_t_atm.sizePolicy().hasHeightForWidth())
        self.label_t_atm.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_t_atm.setFont(font)
        self.label_t_atm.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_t_atm.setObjectName("label_t_atm")
        self.gridLayout.addWidget(self.label_t_atm, 1, 0, 1, 1)
        self.lineEdit_temp = QtWidgets.QLineEdit(self.groupBox_measuring_conditions)
        self.lineEdit_temp.setText("")
        self.lineEdit_temp.setObjectName("lineEdit_temp")
        self.gridLayout.addWidget(self.lineEdit_temp, 1, 1, 1, 1)
        self.label_p_atm = QtWidgets.QLabel(self.groupBox_measuring_conditions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_p_atm.sizePolicy().hasHeightForWidth())
        self.label_p_atm.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_p_atm.setFont(font)
        self.label_p_atm.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_p_atm.setObjectName("label_p_atm")
        self.gridLayout.addWidget(self.label_p_atm, 2, 0, 1, 1)
        self.lineEdit_pressure = QtWidgets.QLineEdit(self.groupBox_measuring_conditions)
        self.lineEdit_pressure.setText("")
        self.lineEdit_pressure.setObjectName("lineEdit_pressure")
        self.gridLayout.addWidget(self.lineEdit_pressure, 2, 1, 1, 1)
        self.label_hydro = QtWidgets.QLabel(self.groupBox_measuring_conditions)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_hydro.sizePolicy().hasHeightForWidth())
        self.label_hydro.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_hydro.setFont(font)
        self.label_hydro.setStyleSheet("color: rgb(154, 154, 154);")
        self.label_hydro.setObjectName("label_hydro")
        self.gridLayout.addWidget(self.label_hydro, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 2)
        self.lineEdit_hydro = QtWidgets.QLineEdit(self.groupBox_measuring_conditions)
        self.lineEdit_hydro.setText("")
        self.lineEdit_hydro.setObjectName("lineEdit_hydro")
        self.gridLayout.addWidget(self.lineEdit_hydro, 4, 1, 1, 1)
        self.label_article_name = QtWidgets.QLabel(self.groupBox_measuring_conditions)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_article_name.setFont(font)
        self.label_article_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_article_name.setObjectName("label_article_name")
        self.gridLayout.addWidget(self.label_article_name, 0, 0, 1, 2)
        self.horizontalLayout_2.addWidget(self.groupBox_measuring_conditions)

        self.stackedWidget_auto_measuring_modes.addWidget(self.measuring_settings)
        self.start_stop = QtWidgets.QWidget()
        self.start_stop.setObjectName("start_stop")
        self.textBrowser = QtWidgets.QTextBrowser(self.start_stop)
        self.textBrowser.setEnabled(False)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 971, 261))
        self.textBrowser.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textBrowser.setObjectName("textBrowser")
        self.progressBar = QtWidgets.QProgressBar(self.start_stop)
        self.progressBar.setGeometry(QtCore.QRect(70, 290, 861, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.pushButton_start_stop_auto = QtWidgets.QPushButton(self.start_stop)
        self.pushButton_start_stop_auto.setGeometry(QtCore.QRect(390, 370, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_start_stop_auto.setFont(font)
        self.pushButton_start_stop_auto.setStyleSheet("background-color: rgb(31, 100, 10); color: rgb(255, 255, 255);")
        self.pushButton_start_stop_auto.setObjectName("pushButton_start_stop_auto")
        self.stackedWidget_auto_measuring_modes.addWidget(self.start_stop)
        self.protocol = QtWidgets.QWidget()
        self.protocol.setObjectName("protocol")
        self.label_measuring_finished = QtWidgets.QLabel(self.protocol)
        self.label_measuring_finished.setGeometry(QtCore.QRect(370, 80, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_measuring_finished.setFont(font)
        self.label_measuring_finished.setObjectName("label_measuring_finished")
        self.pushButton_print_auto = QtWidgets.QPushButton(self.protocol)
        self.pushButton_print_auto.setGeometry(QtCore.QRect(100, 170, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_print_auto.setFont(font)
        self.pushButton_print_auto.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(96, 121, 255);")
        self.pushButton_print_auto.setObjectName("pushButton_print_auto")
        self.pushButton_preview_auto = QtWidgets.QPushButton(self.protocol)
        self.pushButton_preview_auto.setGeometry(QtCore.QRect(100, 230, 201, 41))
        self.pushButton_preview_auto.setFont(font)
        self.pushButton_preview_auto.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(96, 121, 255);")
        self.pushButton_preview_auto.setObjectName("pushButton_preview_auto")
        self.pushButton_XML_download_auto = QtWidgets.QPushButton(self.protocol)
        self.pushButton_XML_download_auto.setGeometry(QtCore.QRect(100, 290, 201, 41))
        self.pushButton_XML_download_auto.setFont(font)
        self.pushButton_XML_download_auto.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(96, 121, 255);")
        self.pushButton_XML_download_auto.setObjectName("pushButton_XML_download_auto")
        self.stackedWidget_auto_measuring_modes.addWidget(self.protocol)
        self.tab_auto = self.stackedWidget_main.addWidget(self.Auto)
        #   -----------------------------------------------------------------
        #                       вкладка АРХИВ
        #   -----------------------------------------------------------------
        self.Archive = QtWidgets.QWidget()
        self.Archive.setObjectName("Archive")
        self.listWidget_archive = QtWidgets.QListWidget(self.Archive)
        self.listWidget_archive.setGeometry(QtCore.QRect(0, 0, 811, 501))
        self.listWidget_archive.setObjectName("listWidget_archive")
        self.progressBar_memory = QtWidgets.QProgressBar(self.Archive)
        self.progressBar_memory.setGeometry(QtCore.QRect(200, 540, 771, 23))
        self.progressBar_memory.setProperty("value", 10)
        self.progressBar_memory.setObjectName("progressBar_memory")
        self.label_memory = QtWidgets.QLabel(self.Archive)
        self.label_memory.setGeometry(QtCore.QRect(10, 540, 171, 21))
        self.label_memory.setFont(font)
        self.label_memory.setObjectName("label_memory")
        self.pushButton_delete = QtWidgets.QPushButton(self.Archive)
        self.pushButton_delete.setGeometry(QtCore.QRect(830, 70, 141, 31))
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.pushButton_export = QtWidgets.QPushButton(self.Archive)
        self.pushButton_export.setGeometry(QtCore.QRect(830, 20, 141, 31))
        self.pushButton_export.setFont(font)
        self.pushButton_export.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.pushButton_export.setObjectName("pushButton_export")
        self.tab_archive = self.stackedWidget_main.addWidget(self.Archive)

        #   -----------------------------------------------------------------
        #                       Боковое меню
        #   -----------------------------------------------------------------
        self.toolButton_side_menu = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_side_menu.setEnabled(True)
        self.toolButton_side_menu.setGeometry(QtCore.QRect(991, 9, 24, 582))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_side_menu.sizePolicy().hasHeightForWidth())
        self.toolButton_side_menu.setSizePolicy(sizePolicy)
        self.toolButton_side_menu.setStyleSheet("background-color: rgb(38, 0, 51); color: rgb(255, 255, 255);")
        self.toolButton_side_menu.setObjectName("toolButton_side_menu")
        self.toolButton_side_menu.clicked.connect(self.open_side_menu)
        self.widget_side_menu = QtWidgets.QWidget(self.centralwidget)
        self.widget_side_menu.setEnabled(True)
        self.widget_side_menu.setGeometry(QtCore.QRect(824, 9, 186, 582))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_side_menu.sizePolicy().hasHeightForWidth())
        self.widget_side_menu.setSizePolicy(sizePolicy)
        self.widget_side_menu.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
        self.widget_side_menu.setStyleSheet("background-color: rgb(38, 0, 51);")
        self.widget_side_menu.setObjectName("widget_side_menu")
        self.widget_side_menu.close()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_mode_mnual = QtWidgets.QPushButton(self.widget_side_menu)
        self.pushButton_mode_mnual.setGeometry(QtCore.QRect(6, 10, 171, 41))
        self.pushButton_mode_mnual.setFont(font)
        self.pushButton_mode_mnual.setStyleSheet("background-color: rgb(74, 0, 99); color: rgb(255, 255, 255);")
        self.pushButton_mode_mnual.setObjectName("pushButton_mode_mnual")
        self.pushButton_mode_mnual.clicked.connect(self.open_mode_manual)
        self.pushButton_mode_auto = QtWidgets.QPushButton(self.widget_side_menu)
        self.pushButton_mode_auto.setGeometry(QtCore.QRect(6, 60, 171, 41))
        self.pushButton_mode_auto.setFont(font)
        self.pushButton_mode_auto.setStyleSheet("background-color: rgb(74, 0, 99); color: rgb(255, 255, 255);")
        self.pushButton_mode_auto.setObjectName("pushButton_mode_auto")
        self.pushButton_mode_auto.clicked.connect(self.open_mode_auto)
        self.pushButton_sensors = QtWidgets.QPushButton(self.widget_side_menu)
        self.pushButton_sensors.setGeometry(QtCore.QRect(6, 110, 171, 41))
        self.pushButton_sensors.setFont(font)
        self.pushButton_sensors.setStyleSheet("background-color: rgb(74, 0, 99); color: rgb(255, 255, 255);")
        self.pushButton_sensors.setObjectName("pushButton_sensors")
        self.pushButton_sensors.clicked.connect(self.open_sensors)
        self.pushButton_archive = QtWidgets.QPushButton(self.widget_side_menu)
        self.pushButton_archive.setGeometry(QtCore.QRect(6, 160, 171, 41))
        self.pushButton_archive.setFont(font)
        self.pushButton_archive.setStyleSheet("background-color: rgb(74, 0, 99); color: rgb(255, 255, 255);")
        self.pushButton_archive.setObjectName("pushButton_archive")
        self.pushButton_archive.clicked.connect(self.open_archive)
        self.pushButton_settings = QtWidgets.QPushButton(self.widget_side_menu)
        self.pushButton_settings.setGeometry(QtCore.QRect(6, 530, 171, 41))
        self.pushButton_settings.setFont(font)
        self.pushButton_settings.setStyleSheet("background-color: rgb(74, 0, 99); color: rgb(255, 255, 255);")
        self.pushButton_settings.setObjectName("pushButton_settings")
        self.pushButton_settings.clicked.connect(self.open_settings)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.stackedWidget_main.setCurrentIndex(self.tab_logo)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #   -----------------------------------------------------------------
        #                       инициализация
        #   -----------------------------------------------------------------
        
        #   ===     загрузка списка измерений в раздел Архив    ===
        count_of_measurements = self.db_query("SELECT COUNT(*) FROM measurements")[0][0]
        if count_of_measurements:
            for i in range(count_of_measurements):
                measurement = self.db_query("SELECT * FROM measurements WHERE measurement_id="+str(i+1))
                item = QtWidgets.QListWidgetItem()
                item.setText(measurement[0][3]+", "+str(measurement[0][1])+", "+str(measurement[0][2]))
                self.listWidget_archive.addItem(item)
        
        self.lineEdit_manual_customer.setText("Заказчик "+str(count_of_measurements+1))
        self.lineEdit_manual_temp.setText(self.db_query('SELECT option_value FROM options WHERE option_name="default_t"')[0][0])
        self.lineEdit_manual_pressure.setText(self.db_query('SELECT option_value FROM options WHERE option_name="default_p"')[0][0])
        self.lineEdit_manual_hydro.setText(self.db_query('SELECT option_value FROM options WHERE option_name="default_h"')[0][0])

        match platform:                 # определяем на какой платформе запускается приложение
            case "win32":               # под Win запускаемся в оконном режиме и соответвующими COM портами
                MainWindow.showNormal()
                self.portname_bu7 = 'COM1'
                self.portname_itm = 'COM5'
            case "linux":               # под Linux запускаемся в полном экране
                MainWindow.showFullScreen()
                self.portname_bu7 = '/dev/ttyS1'
                self.portname_itm = '/dev/ttyUSB0'

        self.timer_measuring = QTimer()
        self.timer_measuring.setInterval(5000)                  # Измерение раз в 5 сек.
        self.timer_measuring.timeout.connect(self.do_measuring_step)
        self.timer_ustavka = QTimer()
        self.timer_ustavka.timeout.connect(self.do_ustavka_step)
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.changeDefaultTab)
        self.timer.start()
        self.clear_data()

    def manual_start_stop(self):
        match self.pushButton_manual_start_stop.text():
            case "Старт":
                self.manual_start()
            case "Стоп":
                self.manual_stop()
            case _:
                print (self.pushButton_manual_start_stop.text())

    def manual_start(self):
        self.graph_x_points = 10
        self.stab_time = None
        self.stab_flag = False
        self.stab_prev_temp = 0
        self.clear_data()
        rowCount = self.tableWidget_ustavka.rowCount()-1 #т.к. последняя строка с "+"
        print("rowCount = ", rowCount)
        # print ("time = ", QtCore.QTime.fromString(self.tableWidget_ustavka.item(rowCount-1,1).text(), "hh:mm").msecsSinceStartOfDay())
        if rowCount > 0:                                            # если в таблице уставки есть хоть одна уставка, то обрабатываем её.
            self.ustavka_step = 0
            self.tableWidget_progress_bar.setColumnCount(rowCount)
            total_time = 0
            table_width = 921
            for row in range(rowCount): total_time += QtCore.QTime.fromString(self.tableWidget_ustavka.item(row,1).text(), "hh:mm").msecsSinceStartOfDay()
            if QtCore.QTime.fromString(self.tableWidget_ustavka.item(rowCount-1,1).text(), "hh:mm").msecsSinceStartOfDay() == 0 and total_time != 0: table_width -= 50 # если последняя строка с нулевым временем, то резервируем 50 пикселей
            for col in range(rowCount):
                time = QtCore.QTime.fromString(self.tableWidget_ustavka.item(col,1).text(), "hh:mm").msecsSinceStartOfDay()
                if time == 0:
                    if total_time == 0: cell_width = 921
                    else: cell_width = 50
                else: cell_width = int(table_width*time/total_time)
                self.tableWidget_progress_bar.setColumnWidth(col, cell_width) #if col != rowCount-1:  надо разобраться.
                progressBar_name = "self.progressBar_"+str(col)
                exec(progressBar_name+" = QtWidgets.QProgressBar()")
                exec(progressBar_name+".setObjectName('"+progressBar_name+"')")
                exec(progressBar_name+".setAlignment(Qt.AlignmentFlag.AlignHCenter)")
                exec(progressBar_name+".setStyleSheet('QProgressBar{max-height: 19px;}')") #padding: 1px;
                if time: exec(progressBar_name+".setRange(0,"+str(time)+")")
                else:
                    exec(progressBar_name+".setRange(0, 50)")
                self.tableWidget_progress_bar.setCellWidget(0, col, eval(progressBar_name))
            self.do_ustavka() # запустили нагрев на данную уставку
        else:                                                       # Иначе просто создаем один прогрессбар с максимальным значением и показываем на нем "Замер".
            self.progressBar_0 = QtWidgets.QProgressBar()
            self.progressBar_0.setObjectName("self.progressBar_0")
            self.progressBar_0.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.progressBar_0.setStyleSheet('QProgressBar{max-height: 19px;}')
            self.progressBar_0.setFormat('Замер')
            self.progressBar_0.setRange(0,100)
            self.progressBar_0.setValue(100)
            self.tableWidget_progress_bar.setColumnCount(1)
            self.tableWidget_progress_bar.setCellWidget(0, 0, self.progressBar_0)
        self.timer_measuring.start()
        result = exchange_data_itm("W,startmeas=1", self.portname_itm)
        print("Запуск измерений в ИТМ", result)
        self.pushButton_manual_start_stop.setStyleSheet("background-color: rgb(255, 0, 0); color: rgb(255, 255, 255);")
        self.pushButton_manual_start_stop.setText("Стоп")

    def clear_data(self):
        self.graphWidget.clear()                            # очистка графиков
        self.measured_data_channel = []                     # список измеренных достоверных (в режиме стабильности) данных по каналам
        self.measured_data_counter_channel = []             # список счетчиков измеренных достоверных данных текущей уствки на канал (временные данные)
        self.data_for_graph = []                            # список всех измеренных данных для графиков
        self.sensor_pen = []                                # список свойств карандашей для отображения графиков по каналам
        self.sensor_graph = []                              # указатели на графики по каналам
        self.time_of_start = QtCore.QDateTime.currentDateTime() # время начала измерений
        for i in range(9):
            self.data_for_graph.append(list())
            self.data_for_graph[i].append(list())
            self.data_for_graph[i].append(list())
            exec("self.sensor_pen.append(pg.mkPen(color=("+self.color_buttons[i]+"), width=3))")
            self.sensor_graph.append(self.graphWidget.plot(list(range(0)),list(range(0)), pen=self.sensor_pen[i]) )
            if not eval("self.pushButton_"+str(i+1)+".isChecked()"):
                self.graphWidget.removeItem(self.sensor_graph[i])
            if i == 8: break 
            self.measured_data_counter_channel.append(0)
            self.measured_data_channel.append(list())       # список содержит списки значений и времени для отображения на графике
            self.measured_data_channel[i].append(list())    # список измеренных данных на канал
            self.measured_data_channel[i].append(list())    # время, в которое сделан замер

    def manual_stop(self):
        self.tableWidget_progress_bar.setColumnCount(0)
        self.timer_measuring.stop()
        self.timer_ustavka.stop()
        result = exchange_data_itm("W,stopmeas=1", self.portname_itm)
        print("Останов измерений в ИТМ", result)
        self.pushButton_manual_start_stop.setStyleSheet("background-color: rgb(31, 100, 10); color: rgb(255, 255, 255);")
        self.pushButton_manual_start_stop.setText("Старт")

    def do_ustavka_step(self):
        exec("self.progressBar_"+str(self.ustavka_step)+".setValue("+str(self.timer_ustavka.interval())+")") # доводим текущий progressbar до 100%
        self.ustavka_step +=1
        if self.ustavka_step >= self.tableWidget_ustavka.rowCount()-1:
            self.manual_stop()
            return
        self.do_ustavka()

    def do_ustavka(self):
        time = QtCore.QTime.fromString(self.tableWidget_ustavka.item(self.ustavka_step,1).text(), "hh:mm").msecsSinceStartOfDay()
        temperature = int(self.tableWidget_ustavka.item(self.ustavka_step,0).text())
        print("W,T2="+str(temperature)+".0")
        result = exchange_data_bu7("W,Ts2="+str(temperature)+".0", self.portname_bu7)                #Запускаем нагрев на заданную температуру
        if result != "W,Ts2-OK":
            print("Нет связи с БУ7:", result)
        print("Запустили нагрев на:"+str(temperature)+" градусов")
        for row in range(8): self.measured_data_counter_channel[row] = 0
        if time:
            self.timer_ustavka.setInterval(time)
            self.timer_ustavka.setSingleShot(True)
        self.progressbar_show_heating(time)

    def do_measuring_step(self):
        result = exchange_data_bu7('R,T2', self.portname_bu7)
        current_temp = extract_val_param(result, 'T2')
        print("текущая температура: "+current_temp)
        if current_temp == 'errval':
            print('Нет связи с БУ7')
            current_temp = 10
        print("Дрейф:", abs(float(current_temp) - float(self.stab_prev_temp)))
        interval = QtCore.QDateTime.currentDateTime().toTime_t()                        # - self.time_of_start.toTime_t();
        for row in range (8):                                                           # пишем данные для графиков
            if self.tableWidget_channels_settings.item(row, 0).text() != "+":
                result = exchange_data_itm("R,valch"+str(row+1), self.portname_itm)
                val = extract_val_param(result, "valch"+str(row+1))
                if val == "errval":
                    print("Нет связи с ИТМ:", result)
                else:
                    self.data_for_graph[row][0].append(float(val))
                    self.data_for_graph[row][1].append(interval)
                    val = f"{float(val):.2f}"                                   # оставляем 2 разряда после точки
                    exec(f"self.label_temp_of_chan_{str(row+1)}.setText(str(val))")
        self.data_for_graph[8][0].append(float(current_temp))                   # заполняем список данных из нагревателя БУ7, температуру
        self.data_for_graph[8][1].append(interval)                              # и время
        self.label_temp_of_chan_9.setText(str(f"{float(current_temp):.2f}"))
        self.show_graph()

        if self.tableWidget_ustavka.rowCount()-1 > 0:
            time = QtCore.QTime.fromString(self.tableWidget_ustavka.item(self.ustavka_step,1).text(), "hh:mm").msecsSinceStartOfDay() # Время текущей уставки
            if abs(float(current_temp) - float(self.stab_prev_temp)) < 1:  # 0.1 должно быть в релизе
                if self.stab_time == None:
                    self.stab_time = QtCore.QTime.currentTime()
                else:
                    if abs(QtCore.QTime.currentTime().secsTo(self.stab_time)) >= 5: # 1800 должно быть в релизе
                        print("Стабильность достигнута.")
                        self.stab_flag = True
                        if not self.timer_ustavka.isActive() and time:
                            self.timer_ustavka.start()
                            print("Запускаем таймер текущей уставки")
                        # exec("self.progressBar_"+str(self.ustavka_step)+".setStyleSheet('')")
                        exec("self.progressBar_"+str(self.ustavka_step)+".setStyleSheet('QProgressBar{max-height: 19px;}')") #padding: 1px;
                        if time: 
                            exec("self.progressBar_"+str(self.ustavka_step)+".setValue("+str(self.timer_ustavka.interval()-self.timer_ustavka.remainingTime())+")")
                            exec("self.progressBar_"+str(self.ustavka_step)+".resetFormat()")
                        else: 
                            exec("self.progressBar_"+str(self.ustavka_step)+".setValue(50)")
                            exec("self.progressBar_"+str(self.ustavka_step)+".setFormat('Замер')")
                        for row in range(8):    # перебираем каналы в таблице датчиков, если указано, что датчик подключен - считываем данные и сохраняем в соответствующий список.
                            if self.tableWidget_channels_settings.item(row, 0).text() != "+" and self.stab_flag:
                                result = exchange_data_itm("R,valch"+str(row+1), self.portname_itm)
                                val = extract_val_param(result, "valch"+str(row+1))
                                if val == "errval":
                                    print("Нет связи с ИТМ:", result)
                                else:
                                    self.measured_data_counter_channel[row]+=1
                                    self.measured_data_channel[row][0].append(float(val))
                                    self.measured_data_channel[row][1].append(QtCore.QDateTime.currentDateTime())
                                    self.tableWidget.item(4,row).setText(str(val))
                                    print(row, list(range(len(self.measured_data_channel[row][0]))), self.measured_data_channel[row][1][self.measured_data_counter_channel[row]-1].toString("d MMM yyyy HH:mm:ss"))
                                print("Измерение канала "+str(row+1)+": ", val)
            else:
                self.stab_time = None
                self.stab_flag = False
                self.timer_ustavka.stop()
                self.stab_prev_temp = current_temp
                for row in range(8):
                    if self.measured_data_counter_channel[row]:
                        print("Очистка временных данных", self.measured_data_counter_channel[row], self.measured_data_channel[row][0],len(self.measured_0_channel[row][0]))
                        self.measured_0_channel[row][0]=self.measured_data_channel[row][0][0:len(self.measured_data_channel[row][0])-self.measured_data_counter_channel[row]]
                        self.measured_data_channel[row][1]=self.measured_data_channel[row][1][0:len(self.measured_data_channel[row][1])-self.measured_data_counter_channel[row]]
                        print(self.measured_data_channel[row][0])
                        self.measured_data_counter_channel[row] = 0
                self.progressbar_show_heating(time)
                print("Ждем стабильности")

    def show_graph(self):
        for chan in range(9):
            # data_len = len(self.data_for_graph[chan][0])
            # if data_len:
            #     if self.graph_x_points > data_len: x = data_len
            #     else: x = self.graph_x_points
            # if len(self.data_for_graph[chan][0]): self.sensor_graph[chan].setData(list(range(x)), self.data_for_graph[chan][0][-x:])
            if len(self.data_for_graph[chan][0]):
                self.sensor_graph[chan].setData(self.data_for_graph[chan][1], self.data_for_graph[chan][0])
                print (self.data_for_graph[chan][1], self.data_for_graph[chan][0])

    def graph_btn_toggle(self):
        button = QApplication.instance().sender()
        button_name = "self."+button.objectName()
        button_num = int(button_name.split("_")[1])
        if eval("self.pushButton_"+str(button_num)+".isChecked()"):
            self.graphWidget.addItem(self.sensor_graph[button_num-1])
        else:
            self.graphWidget.removeItem(self.sensor_graph[button_num-1])
    
    def move_graph_left(self):
        graph_range = self.graphWidget.viewRange()
        delta = (graph_range[0][1]-graph_range[0][0])/10
        self.graphWidget.setXRange(graph_range[0][0]-delta,graph_range[0][1]-delta, padding = 0)

    def move_graph_right(self):
        graph_range = self.graphWidget.viewRange()
        delta = (graph_range[0][1]-graph_range[0][0])/10
        self.graphWidget.setXRange(graph_range[0][0]+delta,graph_range[0][1]+delta, padding = 0)

    def move_graph_up(self):
        graph_range = self.graphWidget.viewRange()
        delta = (graph_range[1][1]-graph_range[1][0])/10
        self.graphWidget.setYRange(graph_range[1][0]-delta,graph_range[1][1]-delta, padding = 0)

    def move_graph_down(self):
        graph_range = self.graphWidget.viewRange()
        delta = (graph_range[1][1]-graph_range[1][0])/10
        self.graphWidget.setYRange(graph_range[1][0]+delta,graph_range[1][1]+delta, padding = 0)

    def scale_vertical_up(self):
        graph_range = self.graphWidget.viewRange()
        delta = (graph_range[1][1]-graph_range[1][0])/20
        self.graphWidget.setYRange(graph_range[1][0]-delta,graph_range[1][1]+delta, padding = 0)

    def scale_vertical_down(self):
        graph_range = self.graphWidget.viewRange()
        delta = (graph_range[1][1]-graph_range[1][0])/20
        self.graphWidget.setYRange(graph_range[1][0]+delta,graph_range[1][1]-delta, padding = 0)

    def scale_horizontal_up(self):
        graph_range = self.graphWidget.viewRange()
        x_range = (graph_range[0][1]-graph_range[0][0])
        delta = x_range/20
        if x_range >= 10:self.graph_x_points = int(x_range)
        print (self.graph_x_points, x_range)
        self.graphWidget.setXRange(graph_range[0][0]-delta,graph_range[0][1]+delta, padding = 0)

    def scale_horizontal_down(self):
        graph_range = self.graphWidget.viewRange()
        x_range = (graph_range[0][1]-graph_range[0][0])
        delta = x_range/20
        if x_range >= 10:self.graph_x_points = int(x_range)
        print (self.graph_x_points, x_range)
        self.graphWidget.setXRange(graph_range[0][0]+delta,graph_range[0][1]-delta, padding = 0)

    def scale_auto(self):
        self.graphWidget.enableAutoRange()

    def add_ustavka_to_tab(self, selected_row, selected_col):
        parent = QApplication.instance().sender()
        rowCount = self.tableWidget_ustavka.rowCount()
        if selected_row !=0:
            if selected_row+1 == rowCount and self.tableWidget_ustavka.item(selected_row-1,1).text() == "00:00": return
        temperature = self.tableWidget_ustavka.item(selected_row,0).text()
        time = self.tableWidget_ustavka.item(selected_row,1).text()
        Change_ustavka_dialog_inst = Change_ustavka_dialog(temperature, time, selected_row, rowCount, self)
        Change_ustavka_dialog_inst.show()
        Change_ustavka_dialog_inst.exec()

    # Добавление и удаление датчиков в общий список всех датчиков.

    def add_sensor_to_list(self, selected_row):
        parent = QApplication.instance().sender()
        rowCount = self.tableWidget_sensors.rowCount()
        Sensor_edit_dialog_inst = Sensor_edit_dialog(self, selected_row)
        Sensor_edit_dialog_inst.show()
        Sensor_edit_dialog_inst.exec()

    def progressbar_show_heating(self, time):
        exec("self.progressBar_"+str(self.ustavka_step)+".setStyleSheet('QProgressBar{color:rgb(0,0,0);} QProgressBar::chunk {background-color: rgb(255,0,0);}')")
        exec("self.progressBar_"+str(self.ustavka_step)+".setFormat('Нагрев')")
        if time: exec("self.progressBar_"+str(self.ustavka_step)+".setValue("+str(self.timer_ustavka.interval())+")")
        else: exec("self.progressBar_"+str(self.ustavka_step)+".setValue(50)")

    # Добавление и удаление датчиков в таблицу текущих измерений
    
    def add_sensor_to_tab(self, selected_row):
        parent = QApplication.instance().sender()
        item_val = self.tableWidget_channels_settings.item(selected_row,0).text()
        items = []
        if item_val != "+":
            items.append("Удалить")
        rowCount = self.db_query("SELECT COUNT(*) FROM sensors")[0][0]
        sensor = self.db_query("SELECT * FROM sensors")
        for row in range(rowCount):
            items.append(str(sensor[row][1])+", №"+str(sensor[row][2]))
        item, ok = QInputDialog.getItem(parent, 'Выбор датчика', 'Выберите датчик:', items, 0, False)

        if ok:
            if item == "Удалить":
                sensor[0]=["","+","","","","",""]
                result = exchange_data_itm("W,sen"+str(selected_row+1)+"=non", self.portname_itm)
                if result != "W,sen"+str(selected_row+1)+"-OK":
                    print(f"Не удалось записать тип датчика non:", result)
                exec("self.pushButton_"+str(selected_row+1)+".setEnabled(False)")
                exec("self.pushButton_"+str(selected_row+1)+".setChecked(False)")
            else:
                sensor_sn = item.split(", №")[1]
                sensor = self.db_query("SELECT * FROM sensors WHERE sensor_sn='"+sensor_sn+"'")
                exec("self.pushButton_"+str(selected_row+1)+".setEnabled(True)")
                exec("self.pushButton_"+str(selected_row+1)+".setChecked(True)")
            self.measured_data_channel[selected_row][0].clear()
            print (sensor[0])
            for column in range(len(sensor[0])-1):
                self.tableWidget_channels_settings.item(selected_row,column).setText(str(sensor[0][column+1]))

            # заносим данные о нем в таблицу хода измерений.

            if sensor[0][0]:
                self.tableWidget.item(1, selected_row).setText(str(sensor[0][2]))
                ish_set = self.db_query('SELECT option_value FROM options WHERE option_name="sh_set_ish"')
                if ish_set[0][0].find(sensor[0][4])>=0:
                    self.tableWidget.item(2, selected_row).setText("да")
                    match str(sensor[0][4]):
                        case "ЭТС":
                            coef_set="coef_set_ish_ets"
                            coef_set_itm = ['ish1A', 'ish1B', 'ish1C', 'ish1D', 'ish1Wal', 'ish1Rttb', 'ish1M']
                            sensor_type = 'ISH1'
                        case "ППО":
                            coef_set="coef_set_ish_ppo"
                            coef_set_itm = ['ish3tPPOZn', 'ish3tPPOAl', 'ish3tPPOCu', 'ish3uPPOZn', 'ish3uPPOAl', 'ish3uPPOCu']
                            sensor_type = 'ISH3'
                        case "ПРО":
                            coef_set="coef_set_ish_pro"
                            coef_set_itm = ['ish4tPROAl', 'ish4tPROCu', 'ish4tPROPd', 'ish4tPROPt', 'ish4uPROAl', 'ish4uPROCu', 'ish4uPROPd', 'ish4uPROPt']
                            sensor_type = 'ISH4'
                        case _:
                            coef_set="error"
                            sensor_type = 'error'
                    coef_set = self.db_query(f'SELECT option_value FROM options WHERE option_name="{coef_set}"')[0][0]
                    coef_set = coef_set.split(',')
                    print(coef_set)
                    for i in range(len(coef_set)):
                        coef_data = self.db_query(f'SELECT ish_data_{coef_set[i]} FROM ish_data WHERE ish_data_sensor="{sensor[0][0]}"')[0][0]
                        if coef_data:
                            print(coef_data)
                            result = exchange_data_itm(f"W,{coef_set_itm[i]}={str(coef_data)}", self.portname_itm)
                            print(result)
                else:
                    self.tableWidget.item(2, selected_row).setText("")
                    sensor_type = (sensor[0][4].split("(")[1])[:-1]
                print('sensor type = '+sensor_type)
                result = exchange_data_itm("W,sen"+str(selected_row+1)+"="+sensor_type, self.portname_itm)
                print(result)
                if result != "W,sen"+str(selected_row+1)+"-OK":
                    print(f"Не удалось записать тип датчика {sensor_type}:", result)
                self.tableWidget.item(3, selected_row).setText(str(sensor[0][4]))
            else:
                for row in range(6): self.tableWidget.item(row+1, selected_row).setText('')

    def save_manual_protocol(self):
        empty = True
        for chan in range (8):
            if len (self.measured_data_channel[chan]): empty = False
        if not empty:
            measurement_id = self.db_query("SELECT COUNT(*) FROM measurements")[0][0]+1
            data_tuple = (  measurement_id,
                            "m",
                            QtCore.QDateTime.currentDateTime().toString("yyyy-MM-d HH:mm:ss"),
                            self.lineEdit_manual_customer.text(),
                            self.lineEdit_manual_operators_name.text(),
                            self.lineEdit_manual_model.text(),
                            self.lineEdit_manual_number.text(),
                            self.lineEdit_manual_temp.text(),
                            self.lineEdit_manual_pressure.text(),
                            self.lineEdit_manual_hydro.text()
                            )
            self.db_query("INSERT INTO measurements (measurement_id, measurement_type, measurement_datetime, measurement_customer, measurement_operator, measurement_megaohmmeter_model, measurement_megaohmmeter_sn, measurement_t, measurement_p, measurement_h) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", "write", data_tuple)
            for chan in range (9):
                count = len (self.measured_data_channel[chan][0])
                if count:
                    if chan == 8: sensor_id = 0
                    else:
                        sensor_sn = self.tableWidget_channels_settings.item(chan,1).text()
                        sensor_id = int(self.db_query('SELECT sensor_id FROM sensors WHERE sensor_sn="'+sensor_sn+'"')[0][0])
                    measurement_data_id = self.db_query("SELECT COUNT(*) FROM measurements_data")[0][0]+1
                    for i in range(count):
                        data_tuple = (  measurement_data_id+i,
                                        measurement_id,
                                        sensor_id,
                                        self.measured_data_channel[chan][1][i].toString("yyyy-MM-d HH:mm:ss"),
                                        self.measured_data_channel[chan][0][i],
                                        0,
                                        0,
                                        0)
                        print(data_tuple)
                        self.db_query("INSERT INTO measurements_data (measurement_data_id, measurement_data_measurement, measurement_data_sensor, measurement_data_datetime, measurement_data_t, measurement_data_r, measurment_data_u, measurment_data_isolator_r) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", "write", data_tuple)

    def coef_edit(self):
        button = QApplication.instance().sender()
        button_name = "self."+button.objectName()
        par = button_name.split("_")
        coef = par[2]
        row = int(par[3])
        coef_val=self.db_query("SELECT ish_data_"+coef+" FROM ish_data WHERE ish_data_id="+str(row+1))[0][0]
        if coef_val is None:
            coef_val = 0
        else:
            coef_val = float(coef_val)

        coef_val, ok = QInputDialog.getDouble(button, 'Изменение коэффициента '+coef, 'Введите новое значение:', coef_val)

        if ok:
            self.db_query("UPDATE ish_data SET ish_data_"+coef+"="+str(coef_val)+" WHERE ish_data_id="+str(row+1), "write")
            if coef_val is not None and coef_val != 0:
                exec(button_name+".setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(38, 0, 255);')")
            else:
                exec(button_name+".setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);')")

    def db_query(self, query, action='read', data_tuple = None):
        try:
            sqlite_connection = sqlite3.connect('ks1200.db')
            cursor = sqlite_connection.cursor()
            # print("База данных создана и успешно подключена к SQLite")
            # print("результат запроса:")
            # print (query+":")
            if data_tuple: cursor.execute(query, data_tuple)
            else: cursor.execute(query)
            if action =="write": sqlite_connection.commit()
            record = cursor.fetchall()
            # print(record)
            cursor.close()
        except sqlite3.Error as error:
            print("Класс исключения: ", error.__class__)
            print("Исключение", error.args)
            print("Печать подробноcтей исключения SQLite: ")
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))
        finally:
            if (sqlite_connection):
                sqlite_connection.close()
            return record

    def device_number_changed(self, new_data):
        self.db_query("UPDATE options SET option_value='"+new_data+"' WHERE option_name='device_nubmer'", "write")

    def device_name_changed(self, new_data):
        self.db_query("UPDATE options SET option_value='"+new_data+"' WHERE option_name='device_name'", "write")

    def device_veryfing_date_changed(self, new_data):
        self.db_query("UPDATE options SET option_value='"+new_data+"' WHERE option_name='device_veryfing_date'", "write")

    def device_next_veryfing_date_changed(self, new_data):
        self.db_query("UPDATE options SET option_value='"+new_data+"' WHERE option_name='device_next_veryfing_date'", "write")

    def device_produce_date_changed(self, new_data):
        self.db_query("UPDATE options SET option_value='"+new_data+"' WHERE option_name='device_produce_date'", "write")

    def changeDefaultTab(self):
        self.stackedWidget_main.setCurrentIndex(self.tab_manual)

    def open_side_menu(self):
        if self.widget_side_menu.isVisible() == False:
                self.toolButton_side_menu.setGeometry(QtCore.QRect(800, 9, 24, 582))
                self.widget_side_menu.show()
        else:
                self.toolButton_side_menu.setGeometry(QtCore.QRect(991, 9, 24, 582))
                self.widget_side_menu.close()

    def open_settings(self):
        self.widget_side_menu.close()
        self.toolButton_side_menu.setGeometry(QtCore.QRect(991, 9, 24, 582))
        self.stackedWidget_main.setCurrentIndex(self.tab_settings)

    def open_settings_ISH(self):
        self.stackedWidget_main.setCurrentIndex(self.tab_settings_ish)

    def open_mode_manual(self):
        self.widget_side_menu.close()
        self.toolButton_side_menu.setGeometry(QtCore.QRect(991, 9, 24, 582))
        self.stackedWidget_main.setCurrentIndex(self.tab_manual)
 
    def open_mode_auto(self):
        self.widget_side_menu.close()
        self.toolButton_side_menu.setGeometry(QtCore.QRect(991, 9, 24, 582))
        self.stackedWidget_main.setCurrentIndex(self.tab_auto)

    def open_sensors(self):
        self.widget_side_menu.close()
        self.toolButton_side_menu.setGeometry(QtCore.QRect(991, 9, 24, 582))
        self.stackedWidget_main.setCurrentIndex(self.tab_sensors)

    def open_archive(self):
        self.widget_side_menu.close()
        self.toolButton_side_menu.setGeometry(QtCore.QRect(991, 9, 24, 582))
        self.stackedWidget_main.setCurrentIndex(self.tab_archive)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            if MainWindow.windowState() == Qt.WindowState.WindowFullScreen:
                MainWindow.showNormal()
            else: MainWindow.showFullScreen()
        event.accept()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KS1200"))
        self.label_device_nubmer.setText(_translate("MainWindow", "Заводской номер:"))
        self.lineEdit_device_number.setText(_translate("MainWindow", self.db_query("SELECT option_value FROM options WHERE option_name='device_nubmer'")[0][0]))
        self.label_device_name.setText(_translate("MainWindow", "Наименование прибора:"))
        self.lineEdit_device_name.setText(_translate("MainWindow", self.db_query("SELECT option_value FROM options WHERE option_name='device_name'")[0][0]))
        self.label_device_next_veryfing_date.setText(_translate("MainWindow", "Очередная поверка:"))
        self.lineEdit_device_next_veryfing_date.setText(_translate("MainWindow", self.db_query("SELECT option_value FROM options WHERE option_name='device_veryfing_date'")[0][0]))
        self.label_devic_veryfing_date.setText(_translate("MainWindow", "Дата поверки:"))
        self.lineEdit_device_produce_date.setText(_translate("MainWindow", self.db_query("SELECT option_value FROM options WHERE option_name='device_next_veryfing_date'")[0][0]))
        self.label_device_produce_date.setText(_translate("MainWindow", "Дата производства:"))
        self.lineEdit_device_veryfing_date.setText(_translate("MainWindow", self.db_query("SELECT option_value FROM options WHERE option_name='device_produce_date'")[0][0]))
        self.pushButton_settings_ISH.setText(_translate("MainWindow", "Настройки ИСХ"))
        self.pushButton_settings_date.setText(_translate("MainWindow", "Настройка даты и времени"))
        self.pushButton_settings_printer.setText(_translate("MainWindow", "Настройка принтера"))
        self.pushButton_settings_connections.setText(_translate("MainWindow", "Настройка подключений"))
        self.pushButton_settings_verifying.setText(_translate("MainWindow", "Поверка калибратора (пломбировка переключателя)"))
        self.pushButton_settings_device.setText(_translate("MainWindow", "Настройка оборудования"))
        self.pushButton_settings_system_update.setText(_translate("MainWindow", "Обновление системы"))
        item = self.tableWidget_settings_ISH.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Описание датчика"))
        item = self.tableWidget_settings_ISH.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Тип"))
        item = self.tableWidget_settings_ISH.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Коэффициенты"))
        __sortingEnabled = self.tableWidget_settings_ISH.isSortingEnabled()
        self.tableWidget_settings_ISH.setSortingEnabled(False)
        self.tableWidget_settings_ISH.setSortingEnabled(__sortingEnabled)
        items_text = ["Описание датчика", "Заводской номер", "Класс", "Тип", "Диапазон", "Дата выпуска"]
        for col in range(len(items_text)):
            item = self.tableWidget_sensors.horizontalHeaderItem(col)
            item.setText(_translate("MainWindow", items_text[col]))
        self.pushButton_ish_back.setText(_translate("MainWindow", "Назад"))
        self.pushButton_sensors_back.setText(_translate("MainWindow", "Назад"))
        self.pushButton_sensor_add.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_manual_start_stop.setText(_translate("MainWindow", "Старт"))
        self.pushButton_manual_channels_settings.setText(_translate("MainWindow", "1. Настройка"))
        self.pushButton_manual_measuring.setText(_translate("MainWindow", "2. Измерение"))
        self.pushButton_manual_result.setText(_translate("MainWindow", "3. Результат"))
        item = self.tableWidget_ustavka.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Уставка"))
        item = self.tableWidget_ustavka.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Время\n(чч:мм)"))
        __sortingEnabled = self.tableWidget_ustavka.isSortingEnabled()
        self.tableWidget_ustavka.setSortingEnabled(False)
        item = self.tableWidget_ustavka.item(0, 0)
        item.setText(_translate("MainWindow", "+"))
        self.tableWidget_ustavka.setSortingEnabled(__sortingEnabled)
        for row in range(8):
            item = self.tableWidget_channels_settings.verticalHeaderItem(row)
            item.setText(_translate("MainWindow", str(row+1)))
        items_text = ["Описание датчика", "Заводской\nномер", "Класс", "СХ", "Диапазон, °С", "Дата выпуска"]
        for col in range(len(items_text)):
            item = self.tableWidget_channels_settings.horizontalHeaderItem(col)
            item.setText(_translate("MainWindow", items_text[col]))
        self.groupBox_channels_buttons.setTitle(_translate("MainWindow", ""))
        for i in range(8):
            exec("self.pushButton_"+str(i+1)+".setText(_translate('MainWindow','"+str(i+1)+"'))")
            exec("self.label_temp_of_chan_"+str(i+1)+".setText(_translate('MainWindow','-.-'))")
        self.pushButton_9.setText(_translate('MainWindow',"БУ7"))
        self.label_temp_of_chan_9.setText(_translate('MainWindow','-.-'))
        self.groupBox_navigate_buttons.setTitle(_translate("MainWindow", ""))
        self.pushButton_move_graph_left.setText(_translate("MainWindow", "←"))
        self.pushButton_move_graph_right.setText(_translate("MainWindow", "→"))
        self.pushButton_move_graph_up.setText(_translate("MainWindow", "↑"))
        self.pushButton_move_graph_down.setText(_translate("MainWindow", "↓"))
        self.pushButton_scale_vertical_up.setText(_translate("MainWindow", "UD+"))
        self.pushButton_scale_vertical_down.setText(_translate("MainWindow", "UD-"))
        self.pushButton_scale_horizontal_up.setText(_translate("MainWindow", "LR+"))
        self.pushButton_scale_horizontal_down.setText(_translate("MainWindow", "LR-"))
        self.pushButton_scale_auto.setText(_translate("MainWindow", "Auto"))
        self.pushButton_view_table.setText(_translate("MainWindow", "Table"))
        items_text = ["Измерительный канал:", "Номер датчика:", "Эталон:", "Статическая характеристика:", "Значение:", "Текущее отклонение:", "Дрейф на минуту:"]
        for col in range(len(items_text)):
            item = self.tableWidget.verticalHeaderItem(col)
            item.setText(_translate("MainWindow", items_text[col]))        
        self.pushButton_view_graph.setText(_translate("MainWindow", "Graph"))
        self.groupBox_bottom_buttons.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton_measuring_type.setText(_translate("MainWindow", "1. Тип измерения"))
        self.pushButton_tpoints_sensors.setText(_translate("MainWindow", "2. Температурные точки\nи данные датчиков"))
        self.pushButton_measuring_settings.setText(_translate("MainWindow", "3. Параметры измерения"))
        self.pushButton_start_stop_manual.setText(_translate("MainWindow", "4. Запуск/остановка"))
        self.pushButton_protocol.setText(_translate("MainWindow", "5. Протокол"))
        self.pushButton_veryfication_TS.setText(_translate("MainWindow", "Поверка ТС"))
        self.pushButton_graduation_TS.setText(_translate("MainWindow", "Градуировка ТС"))
        self.pushButton_calibration_TP.setText(_translate("MainWindow", "Калибровка ТП"))
        self.pushButton_veryfication_TP.setText(_translate("MainWindow", "Поверка ТП"))
        __sortingEnabled = self.tableWidget_TS_veryfications.isSortingEnabled()
        self.tableWidget_TS_veryfications.setSortingEnabled(False)
        self.tableWidget_TS_veryfications.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.tableWidget_TS_gradiations.isSortingEnabled()
        self.tableWidget_TS_gradiations.setSortingEnabled(False)
        self.tableWidget_TS_gradiations.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.tableWidget_TP.isSortingEnabled()
        self.tableWidget_TP.setSortingEnabled(False)
        self.tableWidget_TP.setSortingEnabled(__sortingEnabled)
        for row in range(8):
            item = self.tableWidget.item(0, row)
            item.setText(_translate("MainWindow", str(row+1)))
            item = self.tableWidget_TS_veryfications.item(row, 0)
            item.setText(_translate("MainWindow", str(row+1)))
            item = self.tableWidget_TS_veryfications.item(row, 1)
            item.setText(_translate("MainWindow", "+"))
            item = self.tableWidget_TS_gradiations.item(row, 0)
            item.setText(_translate("MainWindow", str(row+1)))
            item = self.tableWidget_TS_gradiations.item(row, 1)
            item.setText(_translate("MainWindow", "+"))
            item = self.tableWidget_TP.item(row, 0)
            item.setText(_translate("MainWindow", str(row+1)))
            item = self.tableWidget_TP.item(row, 1)
            item.setText(_translate("MainWindow", "+"))
        items_text = ["Канал", "Тип СИ", "Заводской\nномер", "Год выпуска", "Класс\nдопуска", "Диапазон, °С", "Вид испытаний", "Замечания по\nвнешнему осмотру", "Электросопротивление\nизоляции"]
        for col in range(len(items_text)):
            item = self.tableWidget_TP.horizontalHeaderItem(col)
            item.setText(_translate("MainWindow", items_text[col]))
        items_text = ["Канал", "Тип СИ", "Заводской\nномер", "Год выпуска", "НСХ", "Класс\nдопуска", "Диапазон, °С", "Вид испытаний", "Замечания по\nвнешнему осмотру", "Электросопротивление\nизоляции"]
        for col in range(len(items_text)):
            item = self.tableWidget_TS_veryfications.horizontalHeaderItem(col)
            item.setText(_translate("MainWindow", items_text[col]))            
        items_text = ["Канал", "Тип СИ", "Заводской\nномер", "Год выпуска", "НСХ", "Класс\nдопуска", "Диапазон, °С", "Замечания по\nвнешнему осмотру", "Электросопротивление\nизоляции"]
        for col in range(len(items_text)):
            item = self.tableWidget_TS_gradiations.horizontalHeaderItem(col)
            item.setText(_translate("MainWindow", items_text[col]))  
        item = self.tableWidget_tpoints.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Темп.\nточки"))
        __sortingEnabled = self.tableWidget_tpoints.isSortingEnabled()
        self.tableWidget_tpoints.setSortingEnabled(False)
        item = self.tableWidget_tpoints.item(0, 0)
        item.setText(_translate("MainWindow", "+"))
        self.tableWidget_tpoints.setSortingEnabled(__sortingEnabled)
        self.label_number.setText(_translate("MainWindow", "номер"))
        self.label_fio.setText(_translate("MainWindow", "Ф.И.О. оператора"))
        self.label_model.setText(_translate("MainWindow", "модель"))
        self.label_megaommetr.setText(_translate("MainWindow", "Данные о мегаомметре"))
        self.label_customer.setText(_translate("MainWindow", "Данные для протокола"))
        self.label_customer_2.setText(_translate("MainWindow", "Заказчик"))
        self.label_t_atm.setText(_translate("MainWindow", "Температура окружающего воздуха. °С"))
        self.label_p_atm.setText(_translate("MainWindow", "Атмосферное давлениеб кПа"))
        self.label_hydro.setText(_translate("MainWindow", "Относительная влажность воздуха, %"))
        self.label_article_name.setText(_translate("MainWindow", "Условия поверки"))
        self.label_manual_number.setText(_translate("MainWindow", "номер"))
        self.label_manual_fio.setText(_translate("MainWindow", "Ф.И.О. оператора"))
        self.label_manual_model.setText(_translate("MainWindow", "модель"))
        self.label_manual_megaommetr.setText(_translate("MainWindow", "Данные о мегаомметре"))
        self.label_manual_customer.setText(_translate("MainWindow", "Данные для протокола"))
        self.label_manual_customer_2.setText(_translate("MainWindow", "Заказчик"))
        self.label_manual_t_atm.setText(_translate("MainWindow", "Температура окружающего воздуха. °С"))
        self.label_manual_p_atm.setText(_translate("MainWindow", "Атмосферное давлениеб кПа"))
        self.label_manual_hydro.setText(_translate("MainWindow", "Относительная влажность воздуха, %"))
        self.label_manual_article_name.setText(_translate("MainWindow", "Условия поверки"))
        self.pushButton_save_protocol.setText(_translate("MainWindow", "Сохранить"))
        self.pushButton_start_stop_auto.setText(_translate("MainWindow", "Старт"))
        self.label_measuring_finished.setText(_translate("MainWindow", "Измерения завершены"))
        self.pushButton_print_auto.setText(_translate("MainWindow", "Печать"))
        self.pushButton_preview_auto.setText(_translate("MainWindow", "Просмотр"))
        self.pushButton_XML_download_auto.setText(_translate("MainWindow", "Выгрузить XML"))
        self.label_memory.setText(_translate("MainWindow", "Внутренняя память"))
        self.pushButton_delete.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_export.setText(_translate("MainWindow", "Экспорт"))
        self.toolButton_side_menu.setText(_translate("MainWindow", "М"))
        self.pushButton_mode_mnual.setText(_translate("MainWindow", "Ручной режим"))
        self.pushButton_mode_auto.setText(_translate("MainWindow", "Авто-режим"))
        self.pushButton_sensors.setText(_translate("MainWindow", "Датчики"))
        self.pushButton_archive.setText(_translate("MainWindow", "Архив"))
        self.pushButton_settings.setText(_translate("MainWindow", "Настройка"))

class Change_ustavka_dialog(QDialog):
    def __init__(self, temperature, time, selected_row, rowCount, MainWindow):
        QDialog.__init__(self)
        self.setupUi(self)
        result = exchange_data_bu7('R,Tmin2,Tmax2', MainWindow.portname_bu7)
        min = extract_val_param(result, 'Tmin2')[:extract_val_param(result, 'Tmin2').find('.')]
        if min == 'errval':
            print('Нет связи с БУ7')
            min = 50
        max = extract_val_param(result, 'Tmax2')[:extract_val_param(result, 'Tmax2').find('.')]
        if max == 'errval':
            print('Нет связи с БУ7')
            max = 1300
        if selected_row > 0:
            min = MainWindow.tableWidget_ustavka.item(selected_row-1,0).text()
        if selected_row < rowCount - 2:
            max = MainWindow.tableWidget_ustavka.item(selected_row+1,0).text()
            self.timeEdit.setMinimumTime(QtCore.QTime.fromString("00:01", "hh:mm"))
        if temperature == "+":
            self.pushButton_delete.setEnabled(False)
            time = "00:00"
            temperature = min
        self.spinBox.setRange(int(min),int(max))
        self.spinBox.setValue(int(temperature))
        self.timeEdit.setTime(QtCore.QTime.fromString(time, "hh:mm"))
        self.MainWindow = MainWindow
        self.buttonBox.accepted.connect(lambda: self.accept_data(temperature, time, selected_row, rowCount))
        self.buttonBox.rejected.connect(self.reject_data)
        self.pushButton_delete.clicked.connect(lambda: self.delete_data(selected_row))

    def accept_data(self, temperature, time, selected_row, rowCount):
        if selected_row+1 == rowCount:
            self.MainWindow.tableWidget_ustavka.insertRow(selected_row)
            item = QtWidgets.QTableWidgetItem()
            self.MainWindow.tableWidget_ustavka.setItem(selected_row, 0, item)
            item = QtWidgets.QTableWidgetItem()
            self.MainWindow.tableWidget_ustavka.setItem(selected_row, 1, item)

        self.MainWindow.tableWidget_ustavka.item(selected_row,0).setText(str(self.spinBox.value()))
        self.MainWindow.tableWidget_ustavka.item(selected_row,1).setText(self.timeEdit.time().toString("hh:mm"))
        self.close()

    def reject_data(self):
        self.close()

    def delete_data(self, selected_row):
        self.MainWindow.tableWidget_ustavka.removeRow(selected_row)
        self.MainWindow.tableWidget_ustavka.selectionModel().clearCurrentIndex()
        self.close()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setModal(True)
        Dialog.resize(362, 106)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_temperature = QtWidgets.QLabel(Dialog)
        self.label_temperature.setObjectName("label_temperature")
        self.horizontalLayout.addWidget(self.label_temperature)
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_time = QtWidgets.QLabel(Dialog)
        self.label_time.setObjectName("label_time")
        self.horizontalLayout.addWidget(self.label_time)
        self.timeEdit = QtWidgets.QTimeEdit(Dialog)
        self.timeEdit.setObjectName("timeEdit")
        self.horizontalLayout.addWidget(self.timeEdit)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setGeometry(QtCore.QRect(141, 15, 191, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton_delete = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_delete.setGeometry(QtCore.QRect(10, 15, 101, 31))
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_time.setText(_translate("Dialog", "Время (Ч:ММ):"))
        self.label_temperature.setText(_translate("Dialog", "Температура, °С:"))
        # self.groupBox.setTitle(_translate("Dialog", "GroupBox"))
        self.pushButton_delete.setText(_translate("Dialog", "Удалить"))

class Sensor_edit_dialog(QDialog):
    def __init__(self, MainWindow, selected_row):
        QDialog.__init__(self)
        self.setupUi(self)
        self.MainWindow = MainWindow
        print(selected_row)
        all_types = ['sh_set_ish','sh_set_nsh_tp','sh_set_nsh_tr']
        types = []
        for sh in all_types:
            for i in MainWindow.db_query("SELECT option_value FROM options WHERE option_name='"+sh+"'")[0][0].split(','):
                types.append(i)
        self.comboBox_sensor_type.addItems(types)
        classes = []
        for i in MainWindow.db_query("SELECT option_value FROM options WHERE option_name='sensors_classes'")[0][0].split(','):
            classes.append(i)
        self.comboBox_sensor_class.addItems(classes)
        if selected_row >= 0:
            sensor_sn = MainWindow.tableWidget_sensors.item(selected_row,1).text()
            sensor = MainWindow.db_query("SELECT * FROM sensors WHERE sensor_sn='"+sensor_sn+"'")
            self.lineEdit_sensor_name.setText(str(sensor[0][1]))
            self.lineEdit_sensor_sn.setText(str(sensor[0][2]))
            self.dateEdit_sensor_year_of_issue.setDate(QDate.fromString(sensor[0][6],'yyyy-MM-dd'))
            self.comboBox_sensor_type.setCurrentIndex(types.index(sensor[0][4]))
            self.comboBox_sensor_class.setCurrentIndex(classes.index(sensor[0][3]))
            self.lineEdit_sensor_t_range.setText(sensor[0][5])
            sensor_id = int(sensor[0][0])
        else:
            sensor_id = int(MainWindow.db_query("SELECT option_value FROM options WHERE option_name='counter_of_sensors'")[0][0])+1
        self.buttonBox.accepted.connect(lambda: self.accept_data(selected_row, sensor_id))
        self.buttonBox.rejected.connect(self.reject_data)
        self.pushButton_sensor_delete.clicked.connect(lambda: self.delete_data(selected_row, sensor_id))

    def accept_data(self, selected_row, sensor_id):
        data_tuple = (  sensor_id,
                        self.lineEdit_sensor_name.text(),
                        self.lineEdit_sensor_sn.text(),
                        self.comboBox_sensor_class.currentText(),
                        self.comboBox_sensor_type.currentText(),
                        self.lineEdit_sensor_t_range.text(),
                        self.dateEdit_sensor_year_of_issue.date().toString('yyyy-MM-dd'),
                        )
        if selected_row >= 0:
            MainWindow.db_query("UPDATE sensors SET sensor_id = ?, sensor_name = ?, sensor_sn = ?, sensor_class = ?, sensor_type = ?, sensor_t_range = ?, sensor_year_of_issue = ? WHERE sensor_id ='" + str(sensor_id)+"';", "write", data_tuple)
        else:
            MainWindow.db_query("INSERT INTO sensors (sensor_id, sensor_name, sensor_sn, sensor_class, sensor_type, sensor_t_range, sensor_year_of_issue) VALUES (?, ?, ?, ?, ?, ?, ?);", "write", data_tuple)
            MainWindow.db_query('UPDATE options SET option_value = ' + str(sensor_id) + ' WHERE option_name = "counter_of_sensors"', 'write')
            # Если добавлен датчик ИСХ, то добаввляем строку в таблицу коэффициентов.
            if self.comboBox_sensor_type.currentText() == "ЭТС" or self.comboBox_sensor_type.currentText() == "ППО" or self.comboBox_sensor_type.currentText() == "ПРО":
                ish_data_id = int(MainWindow.db_query("SELECT option_value FROM options WHERE option_name='counter_of_sensors_ish'")[0][0])+1
                MainWindow.db_query('UPDATE options SET option_value = ' + str(ish_data_id) + ' WHERE option_name = "counter_of_sensors_ish"', 'write')
                data_tuple_ish = ( ish_data_id, sensor_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                MainWindow.db_query("INSERT INTO ish_data (ish_data_id, ish_data_sensor, ish_data_A, ish_data_B, ish_data_C, ish_data_D, ish_data_W, ish_data_Rttb, ish_data_M, ish_data_tZn, ish_data_tAl, ish_data_tCu, ish_data_eZn, ish_data_eAl, ish_data_eCu, ish_data_tPd, ish_data_tPt, ish_data_ePd, ish_data_ePt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", "write", data_tuple_ish)
            selected_row = MainWindow.tableWidget_sensors.rowCount()
            MainWindow.tableWidget_sensors.insertRow(selected_row)
            font = QtGui.QFont()
            font.setPointSize(14)
            item = QtWidgets.QTableWidgetItem()
            item.setFont(font)
            item.setText(str(selected_row+1))
            MainWindow.tableWidget_sensors.setVerticalHeaderItem(selected_row, item)
            for col in range(6):
                item = QtWidgets.QTableWidgetItem()
                item.setFont(font)
                item.setFlags(Qt.ItemFlag.ItemIsSelectable)
                MainWindow.tableWidget_sensors.setItem(selected_row, col, item)
        for col in range(len(data_tuple)-1):
            MainWindow.tableWidget_sensors.item(selected_row,col).setText(data_tuple[col+1])
        self.close()

    def reject_data(self):
        self.close()

    def delete_data(self, selected_row, sensor_id):
        MainWindow.tableWidget_sensors.removeRow(selected_row)
        MainWindow.tableWidget_sensors.selectionModel().clearCurrentIndex()
        MainWindow.db_query("DELETE from sensors WHERE sensor_id ='" + str(sensor_id)+"';","write")
        if self.comboBox_sensor_type.currentText() == "ЭТС" or self.comboBox_sensor_type.currentText() == "ППО" or self.comboBox_sensor_type.currentText() == "ПРО":
            MainWindow.db_query("DELETE from ish_data WHERE ish_data_sensor ='" + str(sensor_id)+"';","write")
        self.close()

    def setupUi(self, Dialog_sensor_edit):
        Dialog_sensor_edit.setObjectName("Dialog_sensor_edit")
        Dialog_sensor_edit.resize(531, 162)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog_sensor_edit.setFont(font)
        self.label_sensor_name = QtWidgets.QLabel(Dialog_sensor_edit)
        self.label_sensor_name.setGeometry(QtCore.QRect(10, 20, 141, 16))
        self.label_sensor_name.setFont(font)
        self.label_sensor_name.setObjectName("label_sensor_name")
        self.label_sensor_sn = QtWidgets.QLabel(Dialog_sensor_edit)
        self.label_sensor_sn.setGeometry(QtCore.QRect(10, 50, 131, 16))
        self.label_sensor_sn.setFont(font)
        self.label_sensor_sn.setObjectName("label_sensor_sn")
        self.label_sensor_class = QtWidgets.QLabel(Dialog_sensor_edit)
        self.label_sensor_class.setGeometry(QtCore.QRect(180, 80, 51, 16))
        self.label_sensor_class.setFont(font)
        self.label_sensor_class.setObjectName("label_sensor_class")
        self.label_sensor_type = QtWidgets.QLabel(Dialog_sensor_edit)
        self.label_sensor_type.setGeometry(QtCore.QRect(10, 80, 41, 16))
        self.label_sensor_type.setFont(font)
        self.label_sensor_type.setObjectName("label_sensor_type")
        self.label_sensor_t_range = QtWidgets.QLabel(Dialog_sensor_edit)
        self.label_sensor_t_range.setGeometry(QtCore.QRect(350, 80, 81, 16))
        self.label_sensor_t_range.setFont(font)
        self.label_sensor_t_range.setObjectName("label_sensor_t_range")
        self.lineEdit_sensor_name = QtWidgets.QLineEdit(Dialog_sensor_edit)
        self.lineEdit_sensor_name.setGeometry(QtCore.QRect(150, 20, 371, 21))
        self.lineEdit_sensor_name.setFont(font)
        self.lineEdit_sensor_name.setText("")
        self.lineEdit_sensor_name.setObjectName("lineEdit_sensor_name")
        self.lineEdit_sensor_sn = QtWidgets.QLineEdit(Dialog_sensor_edit)
        self.lineEdit_sensor_sn.setGeometry(QtCore.QRect(150, 50, 131, 21))
        self.lineEdit_sensor_sn.setFont(font)
        self.lineEdit_sensor_sn.setText("")
        self.lineEdit_sensor_sn.setObjectName("lineEdit_sensor_sn")
        self.comboBox_sensor_class = QtWidgets.QComboBox(Dialog_sensor_edit)
        self.comboBox_sensor_class.setGeometry(QtCore.QRect(240, 80, 69, 22))
        self.comboBox_sensor_class.setObjectName("comboBox_sensor_class")
        self.comboBox_sensor_type = QtWidgets.QComboBox(Dialog_sensor_edit)
        self.comboBox_sensor_type.setGeometry(QtCore.QRect(50, 80, 81, 22))
        self.comboBox_sensor_type.setObjectName("comboBox_sensor_type")
        self.lineEdit_sensor_t_range = QtWidgets.QLineEdit(Dialog_sensor_edit)
        self.lineEdit_sensor_t_range.setGeometry(QtCore.QRect(430, 80, 91, 21))
        self.lineEdit_sensor_t_range.setFont(font)
        self.lineEdit_sensor_t_range.setText("")
        self.lineEdit_sensor_t_range.setObjectName("lineEdit_sensor_t_range")
        self.label_sensor_year_of_issue = QtWidgets.QLabel(Dialog_sensor_edit)
        self.label_sensor_year_of_issue.setGeometry(QtCore.QRect(300, 50, 111, 16))
        self.label_sensor_year_of_issue.setFont(font)
        self.label_sensor_year_of_issue.setObjectName("label_sensor_year_of_issue")
        self.dateEdit_sensor_year_of_issue = QtWidgets.QDateEdit(Dialog_sensor_edit)
        self.dateEdit_sensor_year_of_issue.setGeometry(QtCore.QRect(410, 50, 110, 22))
        self.dateEdit_sensor_year_of_issue.setFont(font)
        self.dateEdit_sensor_year_of_issue.setObjectName("dateEdit_sensor_year_of_issue")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_sensor_edit)
        self.buttonBox.setGeometry(QtCore.QRect(340, 120, 171, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton_sensor_delete = QtWidgets.QPushButton(Dialog_sensor_edit)
        self.pushButton_sensor_delete.setGeometry(QtCore.QRect(20, 120, 81, 31))
        self.pushButton_sensor_delete.setObjectName("pushButton_sensor_delete")

        self.retranslateUi(Dialog_sensor_edit)
        self.buttonBox.accepted.connect(Dialog_sensor_edit.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog_sensor_edit.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog_sensor_edit)

    def retranslateUi(self, Dialog_sensor_edit):
        _translate = QtCore.QCoreApplication.translate
        Dialog_sensor_edit.setWindowTitle(_translate("Dialog_sensor_edit", "Редактирование датчика"))
        self.label_sensor_name.setText(_translate("Dialog_sensor_edit", "Название датчика:"))
        self.label_sensor_sn.setText(_translate("Dialog_sensor_edit", "Заводской номер:"))
        self.label_sensor_class.setText(_translate("Dialog_sensor_edit", "Класс:"))
        self.label_sensor_type.setText(_translate("Dialog_sensor_edit", "Тип:"))
        self.label_sensor_t_range.setText(_translate("Dialog_sensor_edit", "Диапазон:"))
        self.label_sensor_year_of_issue.setText(_translate("Dialog_sensor_edit", "Дата выпуска:"))
        self.pushButton_sensor_delete.setText(_translate("Dialog_sensor_edit", "Удалить"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
