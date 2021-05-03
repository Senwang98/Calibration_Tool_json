# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1350, 895)
        MainWindow.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.show_pic1 = QtWidgets.QLabel(self.centralwidget)
        self.show_pic1.setGeometry(QtCore.QRect(20, 20, 384, 384))
        self.show_pic1.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.show_pic1.setAutoFillBackground(False)
        self.show_pic1.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.show_pic1.setText("")
        self.show_pic1.setScaledContents(True)
        self.show_pic1.setObjectName("show_pic1")
        self.show_pic1.setStyleSheet(''' 
                                        QLabel{
                                        text-align: center; background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                        border-radius: 10px; padding: 6px; height: 14px; border-style: outset; font: 14px;}
                                        ''')

        self.show_pic2 = QtWidgets.QLabel(self.centralwidget)
        self.show_pic2.setGeometry(QtCore.QRect(424, 20, 384, 384))
        self.show_pic2.setMouseTracking(True)
        self.show_pic2.setAutoFillBackground(False)
        self.show_pic2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.show_pic2.setText("")
        self.show_pic2.setScaledContents(True)
        self.show_pic2.setObjectName("show_pic2")
        self.show_pic2.setStyleSheet(''' 
                                        QLabel{
                                        text-align: center; background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                        border-radius: 10px; padding: 6px; height: 14px; border-style: outset; font: 14px;}
                                        ''')

        self.show_pic3 = QtWidgets.QLabel(self.centralwidget)
        self.show_pic3.setGeometry(QtCore.QRect(20, 420, 788, 384))
        self.show_pic3.setMouseTracking(True)
        self.show_pic3.setAutoFillBackground(False)
        self.show_pic3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.show_pic3.setText("")
        self.show_pic3.setScaledContents(True)
        self.show_pic3.setObjectName("show_pic3")
        self.show_pic3.setStyleSheet(''' 
                                        QLabel{
                                        text-align: center; background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                        border-radius: 10px; padding: 6px; height: 14px; border-style: outset; font: 12px;}
                                        ''')

        self.process_bar = QtWidgets.QSlider(self.centralwidget)
        self.process_bar.setGeometry(QtCore.QRect(20, 835, 271, 22))
        self.process_bar.setMouseTracking(False)
        self.process_bar.setTabletTracking(False)
        self.process_bar.setOrientation(QtCore.Qt.Horizontal)
        self.process_bar.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.process_bar.setTickInterval(10)
        self.process_bar.setObjectName("process_bar")

        self.label_process = QtWidgets.QLabel(self.centralwidget)
        self.label_process.setGeometry(QtCore.QRect(300, 835, 101, 16))
        self.label_process.setObjectName("label_process")

        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(380, 825, 70, 40))
        self.btn_open.setCheckable(True)
        self.btn_open.setObjectName("btn_open")
        self.btn_open.setStyleSheet(''' 
                                       QPushButton{
                                       text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                       border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
    
                                       QPushButton:pressed{
                                       text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                       border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                       ''')

        self.btn_display_pause = QtWidgets.QPushButton(self.centralwidget)
        self.btn_display_pause.setGeometry(QtCore.QRect(460, 825, 70, 40))
        self.btn_display_pause.setObjectName("btn_display_pause")
        self.btn_display_pause.setStyleSheet(''' 
                                               QPushButton{
                                               text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                               border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}

                                               QPushButton:pressed{
                                               text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                               border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                               ''')
        self.btn_change = QtWidgets.QPushButton(self.centralwidget)
        self.btn_change.setGeometry(QtCore.QRect(540, 825, 70, 40))
        self.btn_change.setObjectName("btn_change")
        self.btn_change.setStyleSheet(''' 
                                        QPushButton{
                                        text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        
                                        QPushButton:pressed{
                                        text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        ''')

        self.btn_start_record = QtWidgets.QPushButton(self.centralwidget)
        self.btn_start_record.setGeometry(QtCore.QRect(620, 825, 70, 40))
        self.btn_start_record.setObjectName("btn_start_record")
        self.btn_start_record.setStyleSheet(''' 
                                               QPushButton{
                                               text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                               border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}

                                               QPushButton:pressed{
                                               text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                               border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                               ''')

        self.btn_end_record = QtWidgets.QPushButton(self.centralwidget)
        self.btn_end_record.setGeometry(QtCore.QRect(700, 825, 70, 40))
        self.btn_end_record.setObjectName("btn_end_record")
        self.btn_end_record.setStyleSheet(''' 
                                               QPushButton{
                                               text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                               border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}

                                               QPushButton:pressed{
                                               text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                               border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                               ''')

        self.btn_verify = QtWidgets.QPushButton(self.centralwidget)
        self.btn_verify.setGeometry(QtCore.QRect(780, 825, 70, 40))
        self.btn_verify.setObjectName("btn_finish")
        self.btn_verify.setStyleSheet(''' 
                                        QPushButton{
                                        text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        
                                        QPushButton:pressed{
                                        text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        ''')

        self.btn_action = QtWidgets.QPushButton(self.centralwidget)
        self.btn_action.setGeometry(QtCore.QRect(860, 825, 70, 40))
        self.btn_action.setObjectName("btn_action")
        self.btn_action.setStyleSheet(''' 
                                        QPushButton{
                                        text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        
                                        QPushButton:pressed{
                                        text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        ''')

        self.btn_lock = QtWidgets.QPushButton(self.centralwidget)
        self.btn_lock.setGeometry(QtCore.QRect(940, 825, 70, 40))
        self.btn_lock.setObjectName("btn_lock")
        self.btn_lock.setStyleSheet(''' 
                                        QPushButton{
                                        text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        
                                        QPushButton:pressed{
                                        text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        ''')

        self.btn_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(1020, 825, 70, 40))
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setStyleSheet(''' 
                                        QPushButton{
                                        text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        
                                        QPushButton:pressed{
                                        text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                        border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                        ''')

        self.btn_skeleton = QtWidgets.QPushButton(self.centralwidget)
        self.btn_skeleton.setGeometry(QtCore.QRect(1100, 825, 70, 40))
        self.btn_skeleton.setObjectName("btn_skeleton")
        self.btn_skeleton.setStyleSheet(''' 
                                            QPushButton{
                                            text-align : center;background-color: light gary;font: bold;border-color: gray; border-width: 1px; 
                                            border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                            
                                            QPushButton:pressed{
                                            text-align : center;background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                            border-radius: 15px; padding: 6px; height : 14px; border-style: outset; font : 12px;}
                                            ''')

        self.start_label = QtWidgets.QLabel(self.centralwidget)
        self.start_label.setGeometry(QtCore.QRect(1195, 815, 50, 22))
        self.start_label.setObjectName("start_label")

        self.start_information = QtWidgets.QLabel(self.centralwidget)
        self.start_information.setGeometry(QtCore.QRect(1190, 840, 50, 30))
        self.start_information.setMouseTracking(True)
        self.start_information.setAutoFillBackground(False)
        self.start_information.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.start_information.setText("")
        self.start_information.setScaledContents(True)
        self.start_information.setObjectName("start_information")
        self.start_information.setStyleSheet(''' 
                                                QLabel{
                                                text-align: center; background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                                border-radius: 10px; padding: 6px; height: 14px; border-style: outset; font: 12px;}
                                                ''')

        self.end_label = QtWidgets.QLabel(self.centralwidget)
        self.end_label.setGeometry(QtCore.QRect(1275, 815, 50, 22))
        self.end_label.setObjectName("end_label")

        self.end_information = QtWidgets.QLabel(self.centralwidget)
        self.end_information.setGeometry(QtCore.QRect(1270, 840, 50, 30))
        self.end_information.setMouseTracking(True)
        self.end_information.setAutoFillBackground(False)
        self.end_information.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.end_information.setText("")
        self.end_information.setScaledContents(True)
        self.end_information.setObjectName("end_information")
        self.end_information.setStyleSheet(''' 
                                                        QLabel{
                                                        text-align: center; background-color: white; font: bold; border-color: gray; border-width: 1px; 
                                                        border-radius: 10px; padding: 6px; height: 14px; border-style: outset; font: 12px;}
                                                        ''')

        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(828, 20, 132, 780))
        self.table.setStyleSheet("")
        self.table.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.table.setAlternatingRowColors(False)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setCascadingSectionResizes(False)
        # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setStyleSheet(
            "background-color: white; border-radius: 5px;border-color: gray; border-width: 1px;font: bold;border-style: outset;")

        self.table2 = QtWidgets.QTableWidget(self.centralwidget)
        self.table2.setGeometry(QtCore.QRect(980, 20, 350, 780))
        self.table2.setStyleSheet("")
        self.table2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.table2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.table2.setAlternatingRowColors(False)
        self.table2.setObjectName("table2")
        self.table2.setColumnCount(0)
        self.table2.setRowCount(0)
        self.table2.horizontalHeader().setVisible(True)
        self.table2.horizontalHeader().setCascadingSectionResizes(False)
        # self.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table2.setStyleSheet(
            "background-color: white; border-radius: 5px;border-color: gray; border-width: 1px;font: bold;border-style: outset;")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "标定工具"))
        self.btn_open.setText(_translate("MainWindow", "打开"))
        self.btn_open.setShortcut(_translate("MainWindow", "O"))
        self.btn_display_pause.setText(_translate("MainWindow", "播放/暂停"))
        # self.btn_display_pause.setShortcut(_translate("MainWindow", "Space"))
        self.btn_change.setText(_translate("MainWindow", "切换"))
        self.btn_change.setShortcut(_translate("MainWindow", "C"))
        self.label_process.setText(_translate("MainWindow", "0 / NA"))
        self.start_label.setText(_translate("MainWindow", "开始帧："))
        self.end_label.setText(_translate("MainWindow", "结束帧："))
        self.btn_start_record.setText(_translate("MainWindow", "记录开始"))
        self.btn_start_record.setShortcut(_translate("MainWindow", "S"))
        self.btn_end_record.setText(_translate("MainWindow", "记录结束"))
        self.btn_end_record.setShortcut(_translate("MainWindow", "E"))
        self.btn_verify.setText(_translate("MainWindow", "验证"))
        self.btn_action.setText(_translate("MainWindow", "记录动作"))
        self.btn_action.setShortcut(_translate("MainWindow", "F"))
        self.btn_lock.setText(_translate("MainWindow", "锁定/解锁"))
        self.btn_lock.setShortcut(_translate("MainWindow", "L"))
        self.btn_save.setText(_translate("MainWindow", "保存"))
        self.btn_skeleton.setText(_translate("MainWindow", "骨架"))
