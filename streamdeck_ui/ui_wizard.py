# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'wizard.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Wizard(object):
    def setupUi(self, Wizard):
        if not Wizard.objectName():
            Wizard.setObjectName(u"Wizard")
        Wizard.resize(679, 406)
        self.wizardPage1 = QWizardPage()
        self.wizardPage1.setObjectName(u"wizardPage1")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wizardPage1.sizePolicy().hasHeightForWidth())
        self.wizardPage1.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.wizardPage1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.label = QLabel(self.wizardPage1)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_3 = QLabel(self.wizardPage1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.radioButton = QRadioButton(self.wizardPage1)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setChecked(True)

        self.verticalLayout_4.addWidget(self.radioButton)

        self.radioButton_2 = QRadioButton(self.wizardPage1)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_4.addWidget(self.radioButton_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton_5 = QRadioButton(self.wizardPage1)
        self.radioButton_5.setObjectName(u"radioButton_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.radioButton_5.sizePolicy().hasHeightForWidth())
        self.radioButton_5.setSizePolicy(sizePolicy1)

        self.horizontalLayout_4.addWidget(self.radioButton_5)

        self.spinBox = QSpinBox(self.wizardPage1)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(10000)
        self.spinBox.setSingleStep(100)

        self.horizontalLayout_4.addWidget(self.spinBox)

        self.label_4 = QLabel(self.wizardPage1)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.radioButton_3 = QRadioButton(self.wizardPage1)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout_4.addWidget(self.radioButton_3)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 7)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        Wizard.addPage(self.wizardPage1)
        self.wizardPage2 = QWizardPage()
        self.wizardPage2.setObjectName(u"wizardPage2")
        self.verticalLayout_6 = QVBoxLayout(self.wizardPage2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.label_2 = QLabel(self.wizardPage2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.label_5 = QLabel(self.wizardPage2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.treeWidget = QTreeWidget(self.wizardPage2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setHeaderHidden(True)

        self.horizontalLayout_6.addWidget(self.treeWidget)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 7)

        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.verticalLayout_6.addLayout(self.verticalLayout_3)

        Wizard.addPage(self.wizardPage2)
        self.wizardPage = QWizardPage()
        self.wizardPage.setObjectName(u"wizardPage")
        self.verticalLayout_7 = QVBoxLayout(self.wizardPage)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(6, 6, 6, 6)
        self.label_6 = QLabel(self.wizardPage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_6)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.label_7 = QLabel(self.wizardPage)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.widget = QWidget(self.wizardPage)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(20, 20))

        self.horizontalLayout_8.addWidget(self.widget)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 7)

        self.verticalLayout_5.addLayout(self.horizontalLayout_8)


        self.verticalLayout_7.addLayout(self.verticalLayout_5)

        Wizard.addPage(self.wizardPage)
        QWidget.setTabOrder(self.radioButton, self.radioButton_2)
        QWidget.setTabOrder(self.radioButton_2, self.radioButton_5)
        QWidget.setTabOrder(self.radioButton_5, self.radioButton_3)
        QWidget.setTabOrder(self.radioButton_3, self.treeWidget)

        self.retranslateUi(Wizard)

        QMetaObject.connectSlotsByName(Wizard)
    # setupUi

    def retranslateUi(self, Wizard):
        Wizard.setWindowTitle(QCoreApplication.translate("Wizard", u"Wizard", None))
        self.label.setText(QCoreApplication.translate("Wizard", u"Start an action", None))
        self.label_3.setText(QCoreApplication.translate("Wizard", u"Step 1 of 3", None))
        self.radioButton.setText(QCoreApplication.translate("Wizard", u"button is pressed", None))
        self.radioButton_2.setText(QCoreApplication.translate("Wizard", u"button is released", None))
        self.radioButton_5.setText(QCoreApplication.translate("Wizard", u"button is held for", None))
        self.label_4.setText(QCoreApplication.translate("Wizard", u"milliseconds", None))
        self.radioButton_3.setText(QCoreApplication.translate("Wizard", u"after previous action", None))
        self.label_2.setText(QCoreApplication.translate("Wizard", u"Select an action", None))
        self.label_5.setText(QCoreApplication.translate("Wizard", u"Step 2 of 3", None))
        self.label_6.setText(QCoreApplication.translate("Wizard", u"Configure the action", None))
        self.label_7.setText(QCoreApplication.translate("Wizard", u"Step 3 of 3", None))
    # retranslateUi

