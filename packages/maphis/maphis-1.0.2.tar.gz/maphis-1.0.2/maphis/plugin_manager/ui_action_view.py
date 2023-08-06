# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'action_view.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_ActionView(object):
    def setupUi(self, ActionView):
        if not ActionView.objectName():
            ActionView.setObjectName(u"ActionView")
        ActionView.resize(533, 458)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ActionView.sizePolicy().hasHeightForWidth())
        ActionView.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ActionView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cmbActions = QComboBox(ActionView)
        self.cmbActions.setObjectName(u"cmbActions")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cmbActions.sizePolicy().hasHeightForWidth())
        self.cmbActions.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.cmbActions)

        self.actionInfoLayout = QVBoxLayout()
        self.actionInfoLayout.setObjectName(u"actionInfoLayout")

        self.verticalLayout.addLayout(self.actionInfoLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btnApply = QToolButton(ActionView)
        self.btnApply.setObjectName(u"btnApply")
        sizePolicy.setHeightForWidth(self.btnApply.sizePolicy().hasHeightForWidth())
        self.btnApply.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.btnApply)

        self.bntApplyAll = QToolButton(ActionView)
        self.bntApplyAll.setObjectName(u"bntApplyAll")
        sizePolicy.setHeightForWidth(self.bntApplyAll.sizePolicy().hasHeightForWidth())
        self.bntApplyAll.setSizePolicy(sizePolicy)
        self.bntApplyAll.setPopupMode(QToolButton.MenuButtonPopup)
        self.bntApplyAll.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_2.addWidget(self.bntApplyAll)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ActionView)

        QMetaObject.connectSlotsByName(ActionView)
    # setupUi

    def retranslateUi(self, ActionView):
        ActionView.setWindowTitle(QCoreApplication.translate("ActionView", u"Form", None))
        self.btnApply.setText(QCoreApplication.translate("ActionView", u"Apply to selected", None))
        self.bntApplyAll.setText(QCoreApplication.translate("ActionView", u"Apply to all", None))
    # retranslateUi

