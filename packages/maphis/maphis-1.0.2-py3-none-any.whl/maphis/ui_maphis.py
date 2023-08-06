# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maphis.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QHBoxLayout, QLabel, QListView, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MAPHIS(object):
    def setupUi(self, MAPHIS):
        if not MAPHIS.objectName():
            MAPHIS.setObjectName(u"MAPHIS")
        MAPHIS.resize(925, 481)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MAPHIS.sizePolicy().hasHeightForWidth())
        MAPHIS.setSizePolicy(sizePolicy)
        self.actionCreateProject = QAction(MAPHIS)
        self.actionCreateProject.setObjectName(u"actionCreateProject")
        self.actionOpenProject = QAction(MAPHIS)
        self.actionOpenProject.setObjectName(u"actionOpenProject")
        self.actionRecentlyOpened = QAction(MAPHIS)
        self.actionRecentlyOpened.setObjectName(u"actionRecentlyOpened")
        self.actionRecentlyOpened.setEnabled(False)
        self.actionImportPhotos = QAction(MAPHIS)
        self.actionImportPhotos.setObjectName(u"actionImportPhotos")
        self.actionImportPhotos.setEnabled(False)
        self.actionVersion = QAction(MAPHIS)
        self.actionVersion.setObjectName(u"actionVersion")
        self.actionUndo = QAction(MAPHIS)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MAPHIS)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionRedo.setShortcutContext(Qt.WindowShortcut)
        self.actionOpen_project_folder = QAction(MAPHIS)
        self.actionOpen_project_folder.setObjectName(u"actionOpen_project_folder")
        self.actionOpen_project_folder.setEnabled(False)
        self.actionExit = QAction(MAPHIS)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSave = QAction(MAPHIS)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave.setEnabled(False)
        self.centralwidget = QWidget(MAPHIS)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.imageListLayout = QVBoxLayout()
        self.imageListLayout.setObjectName(u"imageListLayout")
        self.imageListLayout.setContentsMargins(0, -1, -1, -1)
        self.tagsLayout = QHBoxLayout()
        self.tagsLayout.setObjectName(u"tagsLayout")
        self.tagsLayout.setContentsMargins(-1, 0, -1, -1)
        self.lblSortBy = QLabel(self.centralwidget)
        self.lblSortBy.setObjectName(u"lblSortBy")
        sizePolicy.setHeightForWidth(self.lblSortBy.sizePolicy().hasHeightForWidth())
        self.lblSortBy.setSizePolicy(sizePolicy)

        self.tagsLayout.addWidget(self.lblSortBy)

        self.cmbSortOrders = QComboBox(self.centralwidget)
        self.cmbSortOrders.addItem("")
        self.cmbSortOrders.addItem("")
        self.cmbSortOrders.setObjectName(u"cmbSortOrders")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cmbSortOrders.sizePolicy().hasHeightForWidth())
        self.cmbSortOrders.setSizePolicy(sizePolicy1)

        self.tagsLayout.addWidget(self.cmbSortOrders)


        self.imageListLayout.addLayout(self.tagsLayout)

        self.imageListView = QListView(self.centralwidget)
        self.imageListView.setObjectName(u"imageListView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.imageListView.sizePolicy().hasHeightForWidth())
        self.imageListView.setSizePolicy(sizePolicy2)
        self.imageListView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.imageListView.setSelectionMode(QAbstractItemView.MultiSelection)
        self.imageListView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.imageListLayout.addWidget(self.imageListView)


        self.horizontalLayout.addLayout(self.imageListLayout)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy3)
        self.tabLabelEditor = QWidget()
        self.tabLabelEditor.setObjectName(u"tabLabelEditor")
        self.tabWidget.addTab(self.tabLabelEditor, "")
        self.tabMeasurements = QWidget()
        self.tabMeasurements.setObjectName(u"tabMeasurements")
        self.tabWidget.addTab(self.tabMeasurements, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        MAPHIS.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MAPHIS)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 925, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        MAPHIS.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MAPHIS)
        self.statusbar.setObjectName(u"statusbar")
        MAPHIS.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuFile.addAction(self.actionCreateProject)
        self.menuFile.addAction(self.actionOpenProject)
        self.menuFile.addAction(self.actionRecentlyOpened)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImportPhotos)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_project_folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionVersion)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)

        self.retranslateUi(MAPHIS)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MAPHIS)
    # setupUi

    def retranslateUi(self, MAPHIS):
        MAPHIS.setWindowTitle(QCoreApplication.translate("MAPHIS", u"MAPHIS", None))
        self.actionCreateProject.setText(QCoreApplication.translate("MAPHIS", u"&New project...", None))
#if QT_CONFIG(shortcut)
        self.actionCreateProject.setShortcut(QCoreApplication.translate("MAPHIS", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpenProject.setText(QCoreApplication.translate("MAPHIS", u"&Open project...", None))
#if QT_CONFIG(shortcut)
        self.actionOpenProject.setShortcut(QCoreApplication.translate("MAPHIS", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionRecentlyOpened.setText(QCoreApplication.translate("MAPHIS", u"&Recent projects", None))
        self.actionImportPhotos.setText(QCoreApplication.translate("MAPHIS", u"&Import photos...", None))
#if QT_CONFIG(shortcut)
        self.actionImportPhotos.setShortcut(QCoreApplication.translate("MAPHIS", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.actionVersion.setText(QCoreApplication.translate("MAPHIS", u"&Version", None))
        self.actionUndo.setText(QCoreApplication.translate("MAPHIS", u"&Undo", None))
#if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(QCoreApplication.translate("MAPHIS", u"Ctrl+Z", None))
#endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(QCoreApplication.translate("MAPHIS", u"&Redo", None))
#if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(QCoreApplication.translate("MAPHIS", u"Ctrl+Y", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen_project_folder.setText(QCoreApplication.translate("MAPHIS", u"Show project &folder in explorer", None))
        self.actionExit.setText(QCoreApplication.translate("MAPHIS", u"E&xit", None))
        self.actionSave.setText(QCoreApplication.translate("MAPHIS", u"&Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MAPHIS", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.lblSortBy.setText(QCoreApplication.translate("MAPHIS", u"Sort by", None))
        self.cmbSortOrders.setItemText(0, QCoreApplication.translate("MAPHIS", u"image name", None))
        self.cmbSortOrders.setItemText(1, QCoreApplication.translate("MAPHIS", u"time of import", None))

        self.cmbSortOrders.setCurrentText(QCoreApplication.translate("MAPHIS", u"image name", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLabelEditor), QCoreApplication.translate("MAPHIS", u"Label editor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMeasurements), QCoreApplication.translate("MAPHIS", u"Measurements", None))
        self.menuFile.setTitle(QCoreApplication.translate("MAPHIS", u"&File", None))
        self.menuAbout.setTitle(QCoreApplication.translate("MAPHIS", u"&About", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MAPHIS", u"&Edit", None))
    # retranslateUi

