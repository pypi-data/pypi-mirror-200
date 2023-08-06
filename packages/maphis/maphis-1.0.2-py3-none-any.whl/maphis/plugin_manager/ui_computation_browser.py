# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'computation_browser.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ComputationBrowser(object):
    def setupUi(self, ComputationBrowser):
        if not ComputationBrowser.objectName():
            ComputationBrowser.setObjectName(u"ComputationBrowser")
        ComputationBrowser.resize(664, 481)
        self.verticalLayout = QVBoxLayout(ComputationBrowser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(ComputationBrowser)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(32, 0))

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignLeft)

        self.cmbComputations = QComboBox(ComputationBrowser)
        self.cmbComputations.setObjectName(u"cmbComputations")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cmbComputations.sizePolicy().hasHeightForWidth())
        self.cmbComputations.setSizePolicy(sizePolicy1)
        self.cmbComputations.setMaximumSize(QSize(148, 16777215))

        self.horizontalLayout.addWidget(self.cmbComputations)

        self.btnReload = QPushButton(ComputationBrowser)
        self.btnReload.setObjectName(u"btnReload")

        self.horizontalLayout.addWidget(self.btnReload)

        self.btnOpenEditor = QPushButton(ComputationBrowser)
        self.btnOpenEditor.setObjectName(u"btnOpenEditor")

        self.horizontalLayout.addWidget(self.btnOpenEditor)

        self.btnCreateComputation = QPushButton(ComputationBrowser)
        self.btnCreateComputation.setObjectName(u"btnCreateComputation")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btnCreateComputation.sizePolicy().hasHeightForWidth())
        self.btnCreateComputation.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.btnCreateComputation, 0, Qt.AlignLeft)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.layoutActionInfoView = QHBoxLayout()
        self.layoutActionInfoView.setObjectName(u"layoutActionInfoView")

        self.verticalLayout.addLayout(self.layoutActionInfoView)


        self.retranslateUi(ComputationBrowser)

        QMetaObject.connectSlotsByName(ComputationBrowser)
    # setupUi

    def retranslateUi(self, ComputationBrowser):
        ComputationBrowser.setWindowTitle(QCoreApplication.translate("ComputationBrowser", u"Computation Browser", None))
        self.label.setText(QCoreApplication.translate("ComputationBrowser", u"Computation:", None))
        self.btnReload.setText(QCoreApplication.translate("ComputationBrowser", u"Reload", None))
        self.btnOpenEditor.setText(QCoreApplication.translate("ComputationBrowser", u"Open in editor", None))
        self.btnCreateComputation.setText(QCoreApplication.translate("ComputationBrowser", u"Create new", None))
    # retranslateUi

