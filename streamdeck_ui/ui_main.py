# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(844, 625)
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.device_list = QComboBox(self.centralwidget)
        self.device_list.setObjectName(u"device_list")
        self.device_list.setMinimumSize(QSize(400, 0))

        self.horizontalLayout_3.addWidget(self.device_list)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_4)

        self.brightness = QSlider(self.centralwidget)
        self.brightness.setObjectName(u"brightness")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.brightness.sizePolicy().hasHeightForWidth())
        self.brightness.setSizePolicy(sizePolicy1)
        self.brightness.setMinimumSize(QSize(200, 0))
        self.brightness.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.brightness)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 20, -1, -1)
        self.pages = QTabWidget(self.centralwidget)
        self.pages.setObjectName(u"pages")
        self.pages.setAutoFillBackground(False)
        self.pages.setStyleSheet(u"b")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.gridLayout_2 = QGridLayout(self.page_1)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.pages.addTab(self.page_1, "")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_3 = QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pages.addTab(self.page_2, "")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_11 = QGridLayout(self.page_3)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.pages.addTab(self.page_3, "")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_10 = QGridLayout(self.page_4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.pages.addTab(self.page_4, "")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_9 = QGridLayout(self.page_5)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.pages.addTab(self.page_5, "")
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.gridLayout_8 = QGridLayout(self.page_6)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.pages.addTab(self.page_6, "")
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.gridLayout_7 = QGridLayout(self.page_7)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.pages.addTab(self.page_7, "")
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.gridLayout_6 = QGridLayout(self.page_8)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.pages.addTab(self.page_8, "")
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.gridLayout_5 = QGridLayout(self.page_9)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.pages.addTab(self.page_9, "")
        self.tab_10 = QWidget()
        self.tab_10.setObjectName(u"tab_10")
        self.gridLayout_4 = QGridLayout(self.tab_10)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pages.addTab(self.tab_10, "")

        self.horizontalLayout.addWidget(self.pages)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(250, 0))
        self.groupBox.setMaximumSize(QSize(250, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.imageButton = QPushButton(self.groupBox)
        self.imageButton.setObjectName(u"imageButton")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.imageButton)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.text = QLineEdit(self.groupBox)
        self.text.setObjectName(u"text")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.text)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.command = QLineEdit(self.groupBox)
        self.command.setObjectName(u"command")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.command)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.keys = QLineEdit(self.groupBox)
        self.keys.setObjectName(u"keys")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.keys)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_6)

        self.write = QPlainTextEdit(self.groupBox)
        self.write.setObjectName(u"write")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.write)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_8)

        self.switch_page = QSpinBox(self.groupBox)
        self.switch_page.setObjectName(u"switch_page")
        self.switch_page.setMinimum(0)
        self.switch_page.setMaximum(10)
        self.switch_page.setValue(0)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.switch_page)

        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_7)

        self.change_brightness = QSpinBox(self.groupBox)
        self.change_brightness.setObjectName(u"change_brightness")
        self.change_brightness.setMinimum(-99)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.change_brightness)


        self.verticalLayout_3.addLayout(self.formLayout)


        self.horizontalLayout.addWidget(self.groupBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 844, 27))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Stream Deck UI", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Brightness:", None))
        self.pages.setTabText(self.pages.indexOf(self.page_1), QCoreApplication.translate("MainWindow", u"Page 1", None))
        self.pages.setTabText(self.pages.indexOf(self.page_2), QCoreApplication.translate("MainWindow", u"2", None))
        self.pages.setTabText(self.pages.indexOf(self.page_3), QCoreApplication.translate("MainWindow", u"3", None))
        self.pages.setTabText(self.pages.indexOf(self.page_4), QCoreApplication.translate("MainWindow", u"4", None))
        self.pages.setTabText(self.pages.indexOf(self.page_5), QCoreApplication.translate("MainWindow", u"5", None))
        self.pages.setTabText(self.pages.indexOf(self.page_6), QCoreApplication.translate("MainWindow", u"6", None))
        self.pages.setTabText(self.pages.indexOf(self.page_7), QCoreApplication.translate("MainWindow", u"7", None))
        self.pages.setTabText(self.pages.indexOf(self.page_8), QCoreApplication.translate("MainWindow", u"8", None))
        self.pages.setTabText(self.pages.indexOf(self.page_9), QCoreApplication.translate("MainWindow", u"9", None))
        self.pages.setTabText(self.pages.indexOf(self.tab_10), QCoreApplication.translate("MainWindow", u"10", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Configure Button", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Image:", None))
        self.imageButton.setText(QCoreApplication.translate("MainWindow", u"Choose", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Text:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Command:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Press Keys:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Write Text:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Switch Page:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Brightness +/-:", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

