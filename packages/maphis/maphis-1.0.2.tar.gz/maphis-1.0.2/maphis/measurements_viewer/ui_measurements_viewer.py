# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'measurements_viewer.ui'
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


class Ui_MeasurementsViewer(object):
    def setupUi(self, MeasurementsViewer):
        if not MeasurementsViewer.objectName():
            MeasurementsViewer.setObjectName(u"MeasurementsViewer")
        MeasurementsViewer.resize(1010, 603)
        self.verticalLayout = QVBoxLayout(MeasurementsViewer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_switch_layout = QHBoxLayout()
        self.label_switch_layout.setObjectName(u"label_switch_layout")
        self.label_switch_layout.setContentsMargins(-1, 0, -1, -1)
        self.lblShowMeasurementsFor = QLabel(MeasurementsViewer)
        self.lblShowMeasurementsFor.setObjectName(u"lblShowMeasurementsFor")

        self.label_switch_layout.addWidget(self.lblShowMeasurementsFor, 0, Qt.AlignLeft)

        self.cmbLabelImages = QComboBox(MeasurementsViewer)
        self.cmbLabelImages.setObjectName(u"cmbLabelImages")

        self.label_switch_layout.addWidget(self.cmbLabelImages, 0, Qt.AlignLeft)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.label_switch_layout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.label_switch_layout)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonLayout.setContentsMargins(-1, -1, -1, 0)
        self.btnComputeMeasurements = QPushButton(MeasurementsViewer)
        self.btnComputeMeasurements.setObjectName(u"btnComputeMeasurements")

        self.buttonLayout.addWidget(self.btnComputeMeasurements)

        self.btnDelete = QPushButton(MeasurementsViewer)
        self.btnDelete.setObjectName(u"btnDelete")
        self.btnDelete.setEnabled(False)

        self.buttonLayout.addWidget(self.btnDelete)

        self.btnRecompute = QPushButton(MeasurementsViewer)
        self.btnRecompute.setObjectName(u"btnRecompute")
        self.btnRecompute.setEnabled(False)

        self.buttonLayout.addWidget(self.btnRecompute)

        self.chkColorVisually = QCheckBox(MeasurementsViewer)
        self.chkColorVisually.setObjectName(u"chkColorVisually")
        self.chkColorVisually.setChecked(True)

        self.buttonLayout.addWidget(self.chkColorVisually)

        self.btnExport = QPushButton(MeasurementsViewer)
        self.btnExport.setObjectName(u"btnExport")
        self.btnExport.setEnabled(False)

        self.buttonLayout.addWidget(self.btnExport)


        self.verticalLayout.addLayout(self.buttonLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableView = QTableView(MeasurementsViewer)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout.addWidget(self.tableView)


        self.retranslateUi(MeasurementsViewer)

        QMetaObject.connectSlotsByName(MeasurementsViewer)
    # setupUi

    def retranslateUi(self, MeasurementsViewer):
        MeasurementsViewer.setWindowTitle(QCoreApplication.translate("MeasurementsViewer", u"Form", None))
        self.lblShowMeasurementsFor.setText(QCoreApplication.translate("MeasurementsViewer", u"Showing measurements for:", None))
        self.btnComputeMeasurements.setText(QCoreApplication.translate("MeasurementsViewer", u"Compute new measurements", None))
        self.btnDelete.setText(QCoreApplication.translate("MeasurementsViewer", u"Delete selected", None))
        self.btnRecompute.setText(QCoreApplication.translate("MeasurementsViewer", u"Recompute selected", None))
        self.chkColorVisually.setText(QCoreApplication.translate("MeasurementsViewer", u"Display color data visually", None))
        self.btnExport.setText(QCoreApplication.translate("MeasurementsViewer", u"Export to [XLSX]", None))
    # retranslateUi

