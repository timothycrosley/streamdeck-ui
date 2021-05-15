# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from . import resources_rc


class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.setWindowModality(Qt.ApplicationModal)
        SettingsDialog.resize(452, 156)
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
        self.dim.setObjectName(u"dim")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.dim)

        # Feedback Enable Disable

        self.button_feedback = QLabel(SettingsDialog)
        self.button_feedback.setObjectName(u"label_button_feedback")
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.button_feedback)
        self.buttonfeedback = QComboBox(SettingsDialog)
        self.buttonfeedback.setObjectName(u"button_feedback")
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.buttonfeedback)

        # Custom Image For Feedback Section

        self.imagelabel = QLabel(SettingsDialog)
        self.imagelabel.setObjectName(u"label")
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.imagelabel)
        self.horizontalLayout_2 = QHBoxLayout(SettingsDialog)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.imageButton = QPushButton(SettingsDialog)
        self.imageButton.setObjectName(u"imageButton")
        self.horizontalLayout_2.addWidget(self.imageButton)
        self.removeButton = QPushButton(SettingsDialog)
        self.removeButton.setObjectName(u"removeButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.removeButton.sizePolicy().hasHeightForWidth())
        self.removeButton.setSizePolicy(sizePolicy2)
        self.removeButton.setMaximumSize(QSize(30, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/cross.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeButton.setIcon(icon1)
        self.horizontalLayout_2.addWidget(self.removeButton)
        self.formLayout.setLayout(5, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.buttonBox = QDialogButtonBox(SettingsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept)
        self.buttonBox.rejected.connect(SettingsDialog.reject)

        QMetaObject.connectSlotsByName(SettingsDialog)

    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(
            QCoreApplication.translate("SettingsDialog", u"Stream Deck Settings", None)
        )
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"Stream Deck:", None))
        self.label_streamdeck.setText("")
        self.label_brightness.setText(
            QCoreApplication.translate("SettingsDialog", u"Brightness:", None)
        )
        self.label_dim.setText(
            QCoreApplication.translate("SettingsDialog", u"Auto dim after:", None)
        )
        self.button_feedback.setText(
            QCoreApplication.translate("SettingsDialog", u"Button Feedback Enabled:", None)
        )
        self.imagelabel.setText(
            QCoreApplication.translate("SettingsDialog", u"Feedback Custom Image:", None)
        )
        self.imageButton.setText(
            QCoreApplication.translate("SettingsDialog", u"Select Image:", None)
        )
        self.dim.setCurrentText("")

    # retranslateUi
