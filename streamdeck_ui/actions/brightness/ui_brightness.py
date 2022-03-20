# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'brightness.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Brightness(object):
    def setupUi(self, Brightness):
        if not Brightness.objectName():
            Brightness.setObjectName(u"Brightness")
        Brightness.resize(313, 325)
        self.verticalLayout = QVBoxLayout(Brightness)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(Brightness)
        self.label.setObjectName(u"label")

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dial = QDial(Brightness)
        self.dial.setObjectName(u"dial")
        self.dial.setMaximumSize(QSize(64, 64))
        self.dial.setMinimum(-100)
        self.dial.setMaximum(100)
        self.dial.setSingleStep(1)
        self.dial.setWrapping(False)
        self.dial.setNotchTarget(10.000000000000000)
        self.dial.setNotchesVisible(True)

        self.horizontalLayout.addWidget(self.dial)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.amount = QLabel(Brightness)
        self.amount.setObjectName(u"amount")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amount.sizePolicy().hasHeightForWidth())
        self.amount.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.amount)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.label_2 = QLabel(Brightness)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setTextFormat(Qt.PlainText)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label_2)

        self.verticalLayout_4.setStretch(3, 2)

        self.verticalLayout.addLayout(self.verticalLayout_4)


        self.retranslateUi(Brightness)

        QMetaObject.connectSlotsByName(Brightness)
    # setupUi

    def retranslateUi(self, Brightness):
        Brightness.setWindowTitle(QCoreApplication.translate("Brightness", u"Form", None))
        self.label.setText(QCoreApplication.translate("Brightness", u"Change brightness:", None))
        self.amount.setText(QCoreApplication.translate("Brightness", u"0", None))
        self.label_2.setText(QCoreApplication.translate("Brightness", u"Use the brigtness action to increase or decrease the Stream Deck brightness.", None))
    # retranslateUi

