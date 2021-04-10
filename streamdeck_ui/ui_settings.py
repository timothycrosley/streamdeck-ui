# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import * # type: ignore
from PySide2.QtGui import * # type: ignore
from PySide2.QtWidgets import * # type: ignore

from  . import resources_rc

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.setWindowModality(Qt.ApplicationModal)
        SettingsDialog.resize(510, 144)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SettingsDialog.sizePolicy().hasHeightForWidth())
        SettingsDialog.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/icons/icons/gear.png", QSize(), QIcon.Normal, QIcon.Off)
        SettingsDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, -1, -1, -1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(30)
        self.formLayout.setVerticalSpacing(6)
        self.label = QLabel(SettingsDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_streamdeck = QLabel(SettingsDialog)
        self.label_streamdeck.setObjectName(u"label_streamdeck")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_streamdeck)

        self.label_brightness = QLabel(SettingsDialog)
        self.label_brightness.setObjectName(u"label_brightness")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_brightness)

        self.brightness = QSlider(SettingsDialog)
        self.brightness.setObjectName(u"brightness")
        self.brightness.setOrientation(Qt.Horizontal)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.brightness)

        self.label_dim = QLabel(SettingsDialog)
        self.label_dim.setObjectName(u"label_dim")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_dim)

        self.dim = QComboBox(SettingsDialog)
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.addItem("")
        self.dim.setObjectName(u"dim")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.dim)


        self.verticalLayout_2.addLayout(self.formLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Stream Deck Settings", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"Stream Deck:", None))
        self.label_streamdeck.setText("")
        self.label_brightness.setText(QCoreApplication.translate("SettingsDialog", u"Brightness:", None))
        self.label_dim.setText(QCoreApplication.translate("SettingsDialog", u"Auto dim after:", None))
        self.dim.setItemText(0, QCoreApplication.translate("SettingsDialog", u"Never", None))
        self.dim.setItemText(1, QCoreApplication.translate("SettingsDialog", u"1 minute", None))
        self.dim.setItemText(2, QCoreApplication.translate("SettingsDialog", u"2 minutes", None))
        self.dim.setItemText(3, QCoreApplication.translate("SettingsDialog", u"3 minutes", None))
        self.dim.setItemText(4, QCoreApplication.translate("SettingsDialog", u"4 minutes", None))
        self.dim.setItemText(5, QCoreApplication.translate("SettingsDialog", u"5 minutes", None))
        self.dim.setItemText(6, QCoreApplication.translate("SettingsDialog", u"10 minutes", None))
        self.dim.setItemText(7, QCoreApplication.translate("SettingsDialog", u"15 minutes", None))
        self.dim.setItemText(8, QCoreApplication.translate("SettingsDialog", u"30 minutes", None))
        self.dim.setItemText(9, QCoreApplication.translate("SettingsDialog", u"1 hour", None))
        self.dim.setItemText(10, QCoreApplication.translate("SettingsDialog", u"2 hours", None))
        self.dim.setItemText(11, QCoreApplication.translate("SettingsDialog", u"4 hours", None))
        self.dim.setItemText(12, QCoreApplication.translate("SettingsDialog", u"8 hours", None))

        self.dim.setCurrentText(QCoreApplication.translate("SettingsDialog", u"Never", None))
    # retranslateUi

