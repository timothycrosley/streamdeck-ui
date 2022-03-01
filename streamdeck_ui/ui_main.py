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

from  . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(974, 550)
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionDocs = QAction(MainWindow)
        self.actionDocs.setObjectName(u"actionDocs")
        self.actionGithub = QAction(MainWindow)
        self.actionGithub.setObjectName(u"actionGithub")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAutoFillBackground(False)
        self.horizontalLayout_7 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(9, -1, -1, 3)
        self.leftwidget = QWidget(self.centralwidget)
        self.leftwidget.setObjectName(u"leftwidget")
        self.verticalLayout_2 = QVBoxLayout(self.leftwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.deviceSettings_horizontalLayout = QHBoxLayout()
        self.deviceSettings_horizontalLayout.setObjectName(u"deviceSettings_horizontalLayout")
        self.deviceSettings_horizontalLayout.setContentsMargins(0, 0, 0, 6)
        self.device_list = QComboBox(self.leftwidget)
        self.device_list.setObjectName(u"device_list")
        self.device_list.setMinimumSize(QSize(400, 0))

        self.deviceSettings_horizontalLayout.addWidget(self.device_list)

        self.settingsButton = QPushButton(self.leftwidget)
        self.settingsButton.setObjectName(u"settingsButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingsButton.sizePolicy().hasHeightForWidth())
        self.settingsButton.setSizePolicy(sizePolicy)
        self.settingsButton.setMinimumSize(QSize(0, 0))
        self.settingsButton.setMaximumSize(QSize(30, 16777215))
        icon = QIcon()
        icon.addFile(u":/icons/icons/gear.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsButton.setIcon(icon)

        self.deviceSettings_horizontalLayout.addWidget(self.settingsButton)

        self.cpu_usage = QProgressBar(self.leftwidget)
        self.cpu_usage.setObjectName(u"cpu_usage")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cpu_usage.sizePolicy().hasHeightForWidth())
        self.cpu_usage.setSizePolicy(sizePolicy1)
        self.cpu_usage.setMaximumSize(QSize(25, 25))
        self.cpu_usage.setMaximum(130)
        self.cpu_usage.setValue(0)
        self.cpu_usage.setOrientation(Qt.Vertical)

        self.deviceSettings_horizontalLayout.addWidget(self.cpu_usage)


        self.verticalLayout_2.addLayout(self.deviceSettings_horizontalLayout)

        self.pages = QTabWidget(self.leftwidget)
        self.pages.setObjectName(u"pages")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pages.sizePolicy().hasHeightForWidth())
        self.pages.setSizePolicy(sizePolicy2)
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

        self.verticalLayout_2.addWidget(self.pages)

        self.verticalLayout_2.setStretch(1, 1)

        self.horizontalLayout_7.addWidget(self.leftwidget)

        self.rightwidget = QWidget(self.centralwidget)
        self.rightwidget.setObjectName(u"rightwidget")
        self.rightwidget.setMinimumSize(QSize(300, 0))
        self.verticalLayout_4 = QVBoxLayout(self.rightwidget)
        self.verticalLayout_4.setSpacing(8)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 0, 0, 0)
        self.horizontalsplitter = QSplitter(self.rightwidget)
        self.horizontalsplitter.setObjectName(u"horizontalsplitter")
        self.horizontalsplitter.setFrameShape(QFrame.NoFrame)
        self.horizontalsplitter.setOrientation(Qt.Vertical)
        self.horizontalsplitter.setHandleWidth(10)
        self.topwidget = QWidget(self.horizontalsplitter)
        self.topwidget.setObjectName(u"topwidget")
        self.verticalLayout_5 = QVBoxLayout(self.topwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.widget_6 = QWidget(self.topwidget)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout = QHBoxLayout(self.widget_6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 6)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.text = QPlainTextEdit(self.widget_6)
        self.text.setObjectName(u"text")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.text.sizePolicy().hasHeightForWidth())
        self.text.setSizePolicy(sizePolicy3)
        self.text.setMaximumSize(QSize(200, 16777215))
        self.text.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.text.setCursorWidth(1)

        self.horizontalLayout_2.addWidget(self.text)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, -1, 10, -1)
        self.textButton = QPushButton(self.widget_6)
        self.textButton.setObjectName(u"textButton")
        self.textButton.setMaximumSize(QSize(30, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/up.png", QSize(), QIcon.Normal, QIcon.Off)
        self.textButton.setIcon(icon1)

        self.verticalLayout.addWidget(self.textButton)

        self.text_horizontal_button = QPushButton(self.widget_6)
        self.text_horizontal_button.setObjectName(u"text_horizontal_button")
        self.text_horizontal_button.setMaximumSize(QSize(30, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/edit-alignment-center.png", QSize(), QIcon.Normal, QIcon.Off)
        self.text_horizontal_button.setIcon(icon2)

        self.verticalLayout.addWidget(self.text_horizontal_button)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, 10, -1)
        self.image_label = QLabel(self.widget_6)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.image_label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.imageButton = QPushButton(self.widget_6)
        self.imageButton.setObjectName(u"imageButton")
        self.imageButton.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_3.addWidget(self.imageButton)

        self.removeButton = QPushButton(self.widget_6)
        self.removeButton.setObjectName(u"removeButton")
        self.removeButton.setMaximumSize(QSize(30, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/cross.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeButton.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.removeButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(2, 1)

        self.horizontalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_5.addWidget(self.widget_6)

        self.line = QFrame(self.topwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line)

        self.frame = QFrame(self.topwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 8, 0, 0)
        self.verticalsplitter = QSplitter(self.frame)
        self.verticalsplitter.setObjectName(u"verticalsplitter")
        self.verticalsplitter.setOrientation(Qt.Horizontal)
        self.verticalsplitter.setHandleWidth(12)
        self.topleftwidget = QWidget(self.verticalsplitter)
        self.topleftwidget.setObjectName(u"topleftwidget")
        self.verticalLayout_8 = QVBoxLayout(self.topleftwidget)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.topleftwidget)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.action_up_button = QPushButton(self.topleftwidget)
        self.action_up_button.setObjectName(u"action_up_button")
        self.action_up_button.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.action_up_button)

        self.action_down_button = QPushButton(self.topleftwidget)
        self.action_down_button.setObjectName(u"action_down_button")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/down.png", QSize(), QIcon.Normal, QIcon.Off)
        self.action_down_button.setIcon(icon4)

        self.horizontalLayout_4.addWidget(self.action_down_button)

        self.remove_action_button = QPushButton(self.topleftwidget)
        self.remove_action_button.setObjectName(u"remove_action_button")
        self.remove_action_button.setMinimumSize(QSize(0, 0))
        self.remove_action_button.setMaximumSize(QSize(30, 16777215))
        self.remove_action_button.setIcon(icon3)

        self.horizontalLayout_4.addWidget(self.remove_action_button)


        self.verticalLayout_8.addLayout(self.horizontalLayout_4)

        self.treeWidget_2 = QTreeWidget(self.topleftwidget)
        self.treeWidget_2.setObjectName(u"treeWidget_2")
        self.treeWidget_2.setIndentation(0)
        self.treeWidget_2.header().setVisible(True)

        self.verticalLayout_8.addWidget(self.treeWidget_2)

        self.verticalsplitter.addWidget(self.topleftwidget)
        self.toprightwidget = QWidget(self.verticalsplitter)
        self.toprightwidget.setObjectName(u"toprightwidget")
        self.verticalLayout_9 = QVBoxLayout(self.toprightwidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.label = QLabel(self.toprightwidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setFont(font)

        self.horizontalLayout_5.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.add_action_button = QPushButton(self.toprightwidget)
        self.add_action_button.setObjectName(u"add_action_button")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add_action_button.setIcon(icon5)

        self.horizontalLayout_5.addWidget(self.add_action_button)


        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        self.treeWidget = QTreeWidget(self.toprightwidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setEnabled(True)
        self.treeWidget.setAlternatingRowColors(False)
        self.treeWidget.setIconSize(QSize(32, 32))
        self.treeWidget.setTextElideMode(Qt.ElideLeft)
        self.treeWidget.setIndentation(40)
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setUniformRowHeights(False)
        self.treeWidget.header().setVisible(False)

        self.verticalLayout_9.addWidget(self.treeWidget)

        self.verticalsplitter.addWidget(self.toprightwidget)

        self.horizontalLayout_8.addWidget(self.verticalsplitter)


        self.verticalLayout_5.addWidget(self.frame)

        self.verticalLayout_5.setStretch(2, 1)
        self.horizontalsplitter.addWidget(self.topwidget)
        self.bottomwidget = QWidget(self.horizontalsplitter)
        self.bottomwidget.setObjectName(u"bottomwidget")
        self.verticalLayout_7 = QVBoxLayout(self.bottomwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.actionlabel = QLabel(self.bottomwidget)
        self.actionlabel.setObjectName(u"actionlabel")
        self.actionlabel.setFont(font)

        self.verticalLayout_7.addWidget(self.actionlabel)

        self.actionwidget = QWidget(self.bottomwidget)
        self.actionwidget.setObjectName(u"actionwidget")
        self.verticalLayout_6 = QVBoxLayout(self.actionwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.helpwidget = QWidget(self.actionwidget)
        self.helpwidget.setObjectName(u"helpwidget")
        self.verticalLayout_10 = QVBoxLayout(self.helpwidget)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_3 = QLabel(self.helpwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_3.setWordWrap(True)

        self.verticalLayout_10.addWidget(self.label_3)


        self.verticalLayout_6.addWidget(self.helpwidget)


        self.verticalLayout_7.addWidget(self.actionwidget)

        self.verticalLayout_7.setStretch(1, 1)
        self.horizontalsplitter.addWidget(self.bottomwidget)

        self.verticalLayout_4.addWidget(self.horizontalsplitter)

        self.verticalLayout_4.setStretch(0, 1)

        self.horizontalLayout_7.addWidget(self.rightwidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 974, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.device_list, self.settingsButton)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionDocs)
        self.menuHelp.addAction(self.actionGithub)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Stream Deck UI", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionDocs.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionGithub.setText(QCoreApplication.translate("MainWindow", u"Github", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About...", None))
        self.settingsButton.setText("")
        self.cpu_usage.setFormat("")
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
        self.text.setDocumentTitle("")
        self.text.setPlainText("")
        self.text.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type label here", None))
        self.textButton.setText("")
        self.text_horizontal_button.setText("")
        self.image_label.setText("")
        self.imageButton.setText(QCoreApplication.translate("MainWindow", u" Select image... ", None))
        self.removeButton.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Actions:", None))
        self.action_up_button.setText("")
        self.action_down_button.setText("")
        self.remove_action_button.setText("")
        ___qtreewidgetitem = self.treeWidget_2.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Configuration", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Action", None));
        self.label.setText(QCoreApplication.translate("MainWindow", u"Add a new action:", None))
        self.add_action_button.setText("")
        ___qtreewidgetitem1 = self.treeWidget.headerItem()
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"1", None));
        self.actionlabel.setText(QCoreApplication.translate("MainWindow", u"Configure action:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Ubuntu'; font-weight:600;\">Help<br /></span><span style=\" font-family:'Ubuntu';\"><br />1. Select the Stream Deck button to configure<br />2. Select an action from the list of available actions</span><span style=\" font-family:'Ubuntu'; font-weight:600;\"><br /></span><span style=\" font-family:'Ubuntu';\">3. Configure the action here<br />4. Click the </span><span style=\" font-family:'Ubuntu'; font-weight:600;\">+</span><span style=\" font-family:'Ubuntu';\"> sign next to Add new action</span></p>\n"
"<p style=\"-qt-paragraph-type"
                        ":empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Ubuntu'; font-weight:600;\"><br /></p></body></html>", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

