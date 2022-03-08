# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'obs.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ObsWidget(object):
    def setupUi(self, ObsWidget):
        if not ObsWidget.objectName():
            ObsWidget.setObjectName(u"ObsWidget")
        ObsWidget.resize(414, 287)
        self.verticalLayout = QVBoxLayout(ObsWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(6)
        self.label = QLabel(ObsWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.scene = QLineEdit(ObsWidget)
        self.scene.setObjectName(u"scene")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.scene)

        self.label_2 = QLabel(ObsWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setTextFormat(Qt.MarkdownText)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2.setWordWrap(True)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.label_2)

        self.label_3 = QLabel(ObsWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.lineEdit = QLineEdit(ObsWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit)


        self.verticalLayout.addLayout(self.formLayout)


        self.retranslateUi(ObsWidget)

        QMetaObject.connectSlotsByName(ObsWidget)
    # setupUi

    def retranslateUi(self, ObsWidget):
        ObsWidget.setWindowTitle(QCoreApplication.translate("ObsWidget", u"Form", None))
        self.label.setText(QCoreApplication.translate("ObsWidget", u"Scene:", None))
        self.label_2.setText(QCoreApplication.translate("ObsWidget", u"Use the **OBS Scene** action to switch to an OBS scene. This action requires the websocket addin to be installed in OBS.", None))
        self.label_3.setText(QCoreApplication.translate("ObsWidget", u"Password (optional):", None))
    # retranslateUi

