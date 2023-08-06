# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'action_info_view.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QPlainTextEdit, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_ActionInfoView(object):
    def setupUi(self, ActionInfoView):
        if not ActionInfoView.objectName():
            ActionInfoView.setObjectName(u"ActionInfoView")
        ActionInfoView.resize(400, 487)
        self.verticalLayout = QVBoxLayout(ActionInfoView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.grpDescription = QGroupBox(ActionInfoView)
        self.grpDescription.setObjectName(u"grpDescription")
        self.horizontalLayout = QHBoxLayout(self.grpDescription)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.txtDescription = QPlainTextEdit(self.grpDescription)
        self.txtDescription.setObjectName(u"txtDescription")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtDescription.sizePolicy().hasHeightForWidth())
        self.txtDescription.setSizePolicy(sizePolicy)
        self.txtDescription.setReadOnly(True)

        self.horizontalLayout.addWidget(self.txtDescription)


        self.verticalLayout.addWidget(self.grpDescription)

        self.grpComputes = QGroupBox(ActionInfoView)
        self.grpComputes.setObjectName(u"grpComputes")
        self.horizontalLayout_2 = QHBoxLayout(self.grpComputes)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableComputes = QTableWidget(self.grpComputes)
        self.tableComputes.setObjectName(u"tableComputes")
        sizePolicy.setHeightForWidth(self.tableComputes.sizePolicy().hasHeightForWidth())
        self.tableComputes.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.tableComputes)


        self.verticalLayout.addWidget(self.grpComputes)

        self.grpUserParameters = QGroupBox(ActionInfoView)
        self.grpUserParameters.setObjectName(u"grpUserParameters")
        self.horizontalLayout_3 = QHBoxLayout(self.grpUserParameters)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tableUserParameters = QTableWidget(self.grpUserParameters)
        self.tableUserParameters.setObjectName(u"tableUserParameters")
        sizePolicy.setHeightForWidth(self.tableUserParameters.sizePolicy().hasHeightForWidth())
        self.tableUserParameters.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.tableUserParameters)


        self.verticalLayout.addWidget(self.grpUserParameters)


        self.retranslateUi(ActionInfoView)

        QMetaObject.connectSlotsByName(ActionInfoView)
    # setupUi

    def retranslateUi(self, ActionInfoView):
        ActionInfoView.setWindowTitle(QCoreApplication.translate("ActionInfoView", u"Form", None))
        self.grpDescription.setTitle(QCoreApplication.translate("ActionInfoView", u"Description", None))
        self.grpComputes.setTitle(QCoreApplication.translate("ActionInfoView", u"Computes", None))
        self.grpUserParameters.setTitle(QCoreApplication.translate("ActionInfoView", u"User parameters", None))
    # retranslateUi

