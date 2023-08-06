# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'radio_panel.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_RadioPanel(object):
    def setupUi(self, RadioPanel):
        if not RadioPanel.objectName():
            RadioPanel.setObjectName(u"RadioPanel")
        RadioPanel.resize(141, 270)
        self.actionConnectAnyBootloader = QAction(RadioPanel)
        self.actionConnectAnyBootloader.setObjectName(u"actionConnectAnyBootloader")
        self.actionConnectSpecificBootloader = QAction(RadioPanel)
        self.actionConnectSpecificBootloader.setObjectName(u"actionConnectSpecificBootloader")
        self.actionConnectNoStreaming = QAction(RadioPanel)
        self.actionConnectNoStreaming.setObjectName(u"actionConnectNoStreaming")
        self.actionBulkClaim = QAction(RadioPanel)
        self.actionBulkClaim.setObjectName(u"actionBulkClaim")
        self.actionBulkUpdateFirmware = QAction(RadioPanel)
        self.actionBulkUpdateFirmware.setObjectName(u"actionBulkUpdateFirmware")
        self.actionConnectSpecificSerial = QAction(RadioPanel)
        self.actionConnectSpecificSerial.setObjectName(u"actionConnectSpecificSerial")
        self.actionClear = QAction(RadioPanel)
        self.actionClear.setObjectName(u"actionClear")
        self.verticalLayout = QVBoxLayout(RadioPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.detailScanButton = QPushButton(RadioPanel)
        self.detailScanButton.setObjectName(u"detailScanButton")

        self.horizontalLayout.addWidget(self.detailScanButton)

        self.clearButton = QToolButton(RadioPanel)
        self.clearButton.setObjectName(u"clearButton")

        self.horizontalLayout.addWidget(self.clearButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.deviceList = QListWidget(RadioPanel)
        self.deviceList.setObjectName(u"deviceList")
        self.deviceList.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.verticalLayout.addWidget(self.deviceList)

        self.connectButton = QPushButton(RadioPanel)
        self.connectButton.setObjectName(u"connectButton")

        self.verticalLayout.addWidget(self.connectButton)

        self.disconnectButton = QPushButton(RadioPanel)
        self.disconnectButton.setObjectName(u"disconnectButton")

        self.verticalLayout.addWidget(self.disconnectButton)

        self.advancedMenuButton = QPushButton(RadioPanel)
        self.advancedMenuButton.setObjectName(u"advancedMenuButton")

        self.verticalLayout.addWidget(self.advancedMenuButton)

        self.ctrlVarLayout = QVBoxLayout()
        self.ctrlVarLayout.setObjectName(u"ctrlVarLayout")

        self.verticalLayout.addLayout(self.ctrlVarLayout)

        self.line = QFrame(RadioPanel)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.goToRemoteButton = QPushButton(RadioPanel)
        self.goToRemoteButton.setObjectName(u"goToRemoteButton")

        self.verticalLayout.addWidget(self.goToRemoteButton)


        self.retranslateUi(RadioPanel)

        QMetaObject.connectSlotsByName(RadioPanel)
    # setupUi

    def retranslateUi(self, RadioPanel):
        RadioPanel.setWindowTitle(QCoreApplication.translate("RadioPanel", u"Radio Panel", None))
        RadioPanel.setTitle(QCoreApplication.translate("RadioPanel", u"Radio", None))
        self.actionConnectAnyBootloader.setText(QCoreApplication.translate("RadioPanel", u"Connect Any Bootloader", None))
        self.actionConnectSpecificBootloader.setText(QCoreApplication.translate("RadioPanel", u"Connect Specific Bootloader...", None))
        self.actionConnectNoStreaming.setText(QCoreApplication.translate("RadioPanel", u"Connect (No Streaming)", None))
        self.actionBulkClaim.setText(QCoreApplication.translate("RadioPanel", u"Bulk Claim", None))
#if QT_CONFIG(tooltip)
        self.actionBulkClaim.setToolTip(QCoreApplication.translate("RadioPanel", u"Bulk Claim", None))
#endif // QT_CONFIG(tooltip)
        self.actionBulkUpdateFirmware.setText(QCoreApplication.translate("RadioPanel", u"Bulk Update Firmware", None))
        self.actionConnectSpecificSerial.setText(QCoreApplication.translate("RadioPanel", u"Connect Specific Serial...", None))
        self.actionClear.setText(QCoreApplication.translate("RadioPanel", u"Clear Scan List", None))
#if QT_CONFIG(tooltip)
        self.actionClear.setToolTip(QCoreApplication.translate("RadioPanel", u"Clear Scan List", None))
#endif // QT_CONFIG(tooltip)
        self.detailScanButton.setText(QCoreApplication.translate("RadioPanel", u"Detail Scan...", None))
        self.clearButton.setText(QCoreApplication.translate("RadioPanel", u"Clear", None))
        self.connectButton.setText(QCoreApplication.translate("RadioPanel", u"Connect", None))
        self.disconnectButton.setText(QCoreApplication.translate("RadioPanel", u"Disconnect", None))
        self.advancedMenuButton.setText(QCoreApplication.translate("RadioPanel", u"Advanced Menu", None))
        self.goToRemoteButton.setText(QCoreApplication.translate("RadioPanel", u"Go To Remote Tab", None))
    # retranslateUi

