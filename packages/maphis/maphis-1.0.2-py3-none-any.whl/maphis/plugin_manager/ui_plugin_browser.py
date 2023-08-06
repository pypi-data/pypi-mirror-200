# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plugin_browser.ui'
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


class Ui_PluginBrowser(object):
    def setupUi(self, PluginBrowser):
        if not PluginBrowser.objectName():
            PluginBrowser.setObjectName(u"PluginBrowser")
        PluginBrowser.resize(570, 490)
        self.verticalLayout = QVBoxLayout(PluginBrowser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(PluginBrowser)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(32, 0))

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignLeft)

        self.cmbPlugins = QComboBox(PluginBrowser)
        self.cmbPlugins.setObjectName(u"cmbPlugins")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cmbPlugins.sizePolicy().hasHeightForWidth())
        self.cmbPlugins.setSizePolicy(sizePolicy1)
        self.cmbPlugins.setMaximumSize(QSize(148, 16777215))

        self.horizontalLayout.addWidget(self.cmbPlugins)

        self.btnReload = QPushButton(PluginBrowser)
        self.btnReload.setObjectName(u"btnReload")

        self.horizontalLayout.addWidget(self.btnReload)

        self.btnOpenPluginFolder = QPushButton(PluginBrowser)
        self.btnOpenPluginFolder.setObjectName(u"btnOpenPluginFolder")

        self.horizontalLayout.addWidget(self.btnOpenPluginFolder)

        self.btnCreatePlugin = QPushButton(PluginBrowser)
        self.btnCreatePlugin.setObjectName(u"btnCreatePlugin")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btnCreatePlugin.sizePolicy().hasHeightForWidth())
        self.btnCreatePlugin.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.btnCreatePlugin, 0, Qt.AlignLeft)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(PluginBrowser)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lblPluginDescription = QLabel(self.groupBox)
        self.lblPluginDescription.setObjectName(u"lblPluginDescription")

        self.horizontalLayout_2.addWidget(self.lblPluginDescription)


        self.verticalLayout.addWidget(self.groupBox)

        self.tabComputations = QTabWidget(PluginBrowser)
        self.tabComputations.setObjectName(u"tabComputations")
        self.tabRegions = QWidget()
        self.tabRegions.setObjectName(u"tabRegions")
        self.tabComputations.addTab(self.tabRegions, "")
        self.tabProperties = QWidget()
        self.tabProperties.setObjectName(u"tabProperties")
        self.tabComputations.addTab(self.tabProperties, "")
        self.tabGeneralActions = QWidget()
        self.tabGeneralActions.setObjectName(u"tabGeneralActions")
        self.tabComputations.addTab(self.tabGeneralActions, "")
        self.tabTools = QWidget()
        self.tabTools.setObjectName(u"tabTools")
        self.tabComputations.addTab(self.tabTools, "")

        self.verticalLayout.addWidget(self.tabComputations)


        self.retranslateUi(PluginBrowser)

        self.tabComputations.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(PluginBrowser)
    # setupUi

    def retranslateUi(self, PluginBrowser):
        PluginBrowser.setWindowTitle(QCoreApplication.translate("PluginBrowser", u"Plugin Browser", None))
        self.label.setText(QCoreApplication.translate("PluginBrowser", u"Plugin:", None))
        self.btnReload.setText(QCoreApplication.translate("PluginBrowser", u"Reload", None))
        self.btnOpenPluginFolder.setText(QCoreApplication.translate("PluginBrowser", u"Open plugin folder", None))
        self.btnCreatePlugin.setText(QCoreApplication.translate("PluginBrowser", u"Create new", None))
        self.groupBox.setTitle(QCoreApplication.translate("PluginBrowser", u"Description", None))
        self.lblPluginDescription.setText("")
        self.tabComputations.setTabText(self.tabComputations.indexOf(self.tabRegions), QCoreApplication.translate("PluginBrowser", u"Region computations", None))
        self.tabComputations.setTabText(self.tabComputations.indexOf(self.tabProperties), QCoreApplication.translate("PluginBrowser", u"Property computations", None))
        self.tabComputations.setTabText(self.tabComputations.indexOf(self.tabGeneralActions), QCoreApplication.translate("PluginBrowser", u"General actions", None))
        self.tabComputations.setTabText(self.tabComputations.indexOf(self.tabTools), QCoreApplication.translate("PluginBrowser", u"Tools", None))
    # retranslateUi

