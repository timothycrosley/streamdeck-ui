# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'button.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpinBox, QTextEdit, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_ButtonForm(object):
    def setupUi(self, ButtonForm):
        if not ButtonForm.objectName():
            ButtonForm.setObjectName(u"ButtonForm")
        ButtonForm.resize(568, 778)
        self.formLayout = QFormLayout(ButtonForm)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(ButtonForm)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add_image = QPushButton(ButtonForm)
        self.add_image.setObjectName(u"add_image")

        self.horizontalLayout_2.addWidget(self.add_image)

        self.remove_image = QPushButton(ButtonForm)
        self.remove_image.setObjectName(u"remove_image")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_image.sizePolicy().hasHeightForWidth())
        self.remove_image.setSizePolicy(sizePolicy)
        self.remove_image.setMaximumSize(QSize(30, 16777215))
        icon = QIcon()
        icon.addFile(u":/icons/icons/cross.png", QSize(), QIcon.Normal, QIcon.Off)
        self.remove_image.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.remove_image)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_9 = QLabel(ButtonForm)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.background_color = QPushButton(ButtonForm)
        self.background_color.setObjectName(u"background_color")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.background_color.sizePolicy().hasHeightForWidth())
        self.background_color.setSizePolicy(sizePolicy1)
        self.background_color.setMaximumSize(QSize(16777215, 16777215))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette.setBrush(QPalette.Active, QPalette.Light, brush1)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush1)
        brush2 = QBrush(QColor(127, 127, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush2)
        brush3 = QBrush(QColor(170, 170, 170, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush1)
        brush4 = QBrush(QColor(255, 255, 220, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush5 = QBrush(QColor(0, 0, 0, 128))
        brush5.setStyle(Qt.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush5)
#endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush5)
#endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush5)
#endif
        self.background_color.setPalette(palette)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.background_color)

        self.label_2 = QLabel(ButtonForm)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.text = QTextEdit(ButtonForm)
        self.text.setObjectName(u"text")

        self.horizontalLayout_3.addWidget(self.text)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.text_v_align = QPushButton(ButtonForm)
        self.text_v_align.setObjectName(u"text_v_align")
        self.text_v_align.setMinimumSize(QSize(40, 30))
        self.text_v_align.setMaximumSize(QSize(30, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/vertical-align.png", QSize(), QIcon.Normal, QIcon.Off)
        self.text_v_align.setIcon(icon1)

        self.verticalLayout_4.addWidget(self.text_v_align)

        self.text_h_align = QPushButton(ButtonForm)
        self.text_h_align.setObjectName(u"text_h_align")
        self.text_h_align.setMinimumSize(QSize(40, 30))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/horizontal-align.png", QSize(), QIcon.Normal, QIcon.Off)
        self.text_h_align.setIcon(icon2)

        self.verticalLayout_4.addWidget(self.text_h_align)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_4 = QLabel(ButtonForm)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.text_font = QComboBox(ButtonForm)
        self.text_font.setObjectName(u"text_font")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.text_font.sizePolicy().hasHeightForWidth())
        self.text_font.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.text_font)

        self.text_font_style = QComboBox(ButtonForm)
        self.text_font_style.setObjectName(u"text_font_style")

        self.horizontalLayout.addWidget(self.text_font_style)

        self.text_font_size = QSpinBox(ButtonForm)
        self.text_font_size.setObjectName(u"text_font_size")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.text_font_size.sizePolicy().hasHeightForWidth())
        self.text_font_size.setSizePolicy(sizePolicy3)
        self.text_font_size.setMinimum(12)
        self.text_font_size.setMaximum(72)

        self.horizontalLayout.addWidget(self.text_font_size)

        self.text_color = QPushButton(ButtonForm)
        self.text_color.setObjectName(u"text_color")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.text_color.sizePolicy().hasHeightForWidth())
        self.text_color.setSizePolicy(sizePolicy4)
        self.text_color.setMaximumSize(QSize(16777215, 16777215))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Light, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Midlight, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Dark, brush2)
        palette1.setBrush(QPalette.Active, QPalette.Mid, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush)
        palette1.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Active, QPalette.AlternateBase, brush1)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipBase, brush4)
        palette1.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush5)
#endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Light, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Midlight, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Dark, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.Mid, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush4)
        palette1.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush5)
#endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Light, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Midlight, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Dark, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Mid, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette1.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush5)
#endif
        self.text_color.setPalette(palette1)

        self.horizontalLayout.addWidget(self.text_color)

        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 1)

        self.formLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_3 = QLabel(ButtonForm)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_3)

        self.command = QLineEdit(ButtonForm)
        self.command.setObjectName(u"command")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.command)

        self.label_5 = QLabel(ButtonForm)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_5)

        self.keys = QLineEdit(ButtonForm)
        self.keys.setObjectName(u"keys")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.keys)

        self.label_8 = QLabel(ButtonForm)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_8)

        self.switch_page = QSpinBox(ButtonForm)
        self.switch_page.setObjectName(u"switch_page")
        self.switch_page.setMinimum(0)
        self.switch_page.setMaximum(999999999)
        self.switch_page.setValue(0)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.switch_page)

        self.label_10 = QLabel(ButtonForm)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_10)

        self.switch_state = QSpinBox(ButtonForm)
        self.switch_state.setObjectName(u"switch_state")
        self.switch_state.setMaximum(999999999)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.switch_state)

        self.label_7 = QLabel(ButtonForm)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.label_7)

        self.change_brightness = QSpinBox(ButtonForm)
        self.change_brightness.setObjectName(u"change_brightness")
        self.change_brightness.setMinimum(-99)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.change_brightness)

        self.label_6 = QLabel(ButtonForm)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_6)

        self.write = QPlainTextEdit(ButtonForm)
        self.write.setObjectName(u"write")

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.write)


        self.retranslateUi(ButtonForm)

        QMetaObject.connectSlotsByName(ButtonForm)
    # setupUi

    def retranslateUi(self, ButtonForm):
        ButtonForm.setWindowTitle(QCoreApplication.translate("ButtonForm", u"Form", None))
        self.label.setText(QCoreApplication.translate("ButtonForm", u"Image:", None))
        self.add_image.setText(QCoreApplication.translate("ButtonForm", u"Image...", None))
#if QT_CONFIG(tooltip)
        self.remove_image.setToolTip(QCoreApplication.translate("ButtonForm", u"Remove the image from the button", None))
#endif // QT_CONFIG(tooltip)
        self.remove_image.setText("")
        self.label_9.setText(QCoreApplication.translate("ButtonForm", u"Background", None))
#if QT_CONFIG(tooltip)
        self.background_color.setToolTip(QCoreApplication.translate("ButtonForm", u"Text Color", None))
#endif // QT_CONFIG(tooltip)
        self.background_color.setText("")
        self.label_2.setText(QCoreApplication.translate("ButtonForm", u"Label:", None))
#if QT_CONFIG(tooltip)
        self.text_v_align.setToolTip(QCoreApplication.translate("ButtonForm", u"Text vertical alignment", None))
#endif // QT_CONFIG(tooltip)
        self.text_v_align.setText("")
#if QT_CONFIG(tooltip)
        self.text_h_align.setToolTip(QCoreApplication.translate("ButtonForm", u"Text horizontal alignment", None))
#endif // QT_CONFIG(tooltip)
        self.text_h_align.setText("")
        self.label_4.setText(QCoreApplication.translate("ButtonForm", u"Label Font:", None))
#if QT_CONFIG(tooltip)
        self.text_font.setToolTip(QCoreApplication.translate("ButtonForm", u"Text Font style", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.text_font_style.setToolTip(QCoreApplication.translate("ButtonForm", u"Text Font", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.text_font_size.setToolTip(QCoreApplication.translate("ButtonForm", u"Text Font size", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.text_color.setToolTip(QCoreApplication.translate("ButtonForm", u"Text Color", None))
#endif // QT_CONFIG(tooltip)
        self.text_color.setText("")
        self.label_3.setText(QCoreApplication.translate("ButtonForm", u"Command:", None))
        self.label_5.setText(QCoreApplication.translate("ButtonForm", u"Press Keys:", None))
        self.label_8.setText(QCoreApplication.translate("ButtonForm", u"Switch Page:", None))
        self.label_10.setText(QCoreApplication.translate("ButtonForm", u"Switch state", None))
        self.label_7.setText(QCoreApplication.translate("ButtonForm", u"Brightness +/-:", None))
        self.label_6.setText(QCoreApplication.translate("ButtonForm", u"Write Text:", None))
    # retranslateUi

