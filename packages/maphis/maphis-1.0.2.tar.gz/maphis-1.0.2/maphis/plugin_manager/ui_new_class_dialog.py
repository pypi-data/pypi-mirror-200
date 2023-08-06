# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_class_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide6.QtWidgets import *


class Ui_NewClassDialog(object):
    def setupUi(self, NewClassDialog):
        if not NewClassDialog.objectName():
            NewClassDialog.setObjectName(u"NewClassDialog")
        NewClassDialog.resize(525, 378)
        self.formLayout = QFormLayout(NewClassDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.lblName = QLabel(NewClassDialog)
        self.lblName.setObjectName(u"lblName")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblName)

        self.txtName = QLineEdit(NewClassDialog)
        self.txtName.setObjectName(u"txtName")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txtName)

        self.lblDescription = QLabel(NewClassDialog)
        self.lblDescription.setObjectName(u"lblDescription")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblDescription)

        self.txtDescription = QLineEdit(NewClassDialog)
        self.txtDescription.setObjectName(u"txtDescription")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.txtDescription)

        self.lblKey = QLabel(NewClassDialog)
        self.lblKey.setObjectName(u"lblKey")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lblKey)

        self.txtKey = QLineEdit(NewClassDialog)
        self.txtKey.setObjectName(u"txtKey")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.txtKey)

        self.tableMethods = QTableWidget(NewClassDialog)
        self.tableMethods.setObjectName(u"tableMethods")
        self.tableMethods.setAlternatingRowColors(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.tableMethods)

        self.lblMethods = QLabel(NewClassDialog)
        self.lblMethods.setObjectName(u"lblMethods")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lblMethods)

        self.buttonBox = QDialogButtonBox(NewClassDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.buttonBox)


        self.retranslateUi(NewClassDialog)

        QMetaObject.connectSlotsByName(NewClassDialog)
    # setupUi

    def retranslateUi(self, NewClassDialog):
        NewClassDialog.setWindowTitle(QCoreApplication.translate("NewClassDialog", u"Form", None))
        self.lblName.setText(QCoreApplication.translate("NewClassDialog", u"Name:", None))
        self.lblDescription.setText(QCoreApplication.translate("NewClassDialog", u"Description:", None))
        self.lblKey.setText(QCoreApplication.translate("NewClassDialog", u"Key:", None))
        self.lblMethods.setText(QCoreApplication.translate("NewClassDialog", u"Methods to include:", None))
    # retranslateUi

