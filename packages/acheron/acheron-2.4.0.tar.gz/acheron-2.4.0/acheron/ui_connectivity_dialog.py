# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'connectivity_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_ConnectivityDialog(object):
    def setupUi(self, ConnectivityDialog):
        if not ConnectivityDialog.objectName():
            ConnectivityDialog.setObjectName(u"ConnectivityDialog")
        ConnectivityDialog.resize(356, 190)
        self.verticalLayout = QVBoxLayout(ConnectivityDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.modbusLabel = QLabel(ConnectivityDialog)
        self.modbusLabel.setObjectName(u"modbusLabel")
        font = QFont()
        font.setBold(True)
        self.modbusLabel.setFont(font)

        self.gridLayout.addWidget(self.modbusLabel, 0, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(20, 13, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.unitIdLabel = QLabel(ConnectivityDialog)
        self.unitIdLabel.setObjectName(u"unitIdLabel")
        self.unitIdLabel.setEnabled(False)

        self.gridLayout.addWidget(self.unitIdLabel, 2, 1, 1, 1)

        self.blankLabel = QLabel(ConnectivityDialog)
        self.blankLabel.setObjectName(u"blankLabel")

        self.gridLayout.addWidget(self.blankLabel, 2, 2, 1, 1)

        self.unitId = QSpinBox(ConnectivityDialog)
        self.unitId.setObjectName(u"unitId")
        self.unitId.setEnabled(False)
        self.unitId.setMinimum(1)
        self.unitId.setMaximum(247)

        self.gridLayout.addWidget(self.unitId, 2, 3, 1, 1)

        self.channelSocketLabel = QLabel(ConnectivityDialog)
        self.channelSocketLabel.setObjectName(u"channelSocketLabel")
        self.channelSocketLabel.setFont(font)

        self.gridLayout.addWidget(self.channelSocketLabel, 3, 0, 1, 4)

        self.modbusCheckBox = QCheckBox(ConnectivityDialog)
        self.modbusCheckBox.setObjectName(u"modbusCheckBox")

        self.gridLayout.addWidget(self.modbusCheckBox, 1, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.modbusDetails = QPushButton(ConnectivityDialog)
        self.modbusDetails.setObjectName(u"modbusDetails")

        self.horizontalLayout.addWidget(self.modbusDetails)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 2, 1, 2)

        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(10, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ConnectivityDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ConnectivityDialog)
        self.buttonBox.accepted.connect(ConnectivityDialog.accept)
        self.buttonBox.rejected.connect(ConnectivityDialog.reject)
        self.modbusCheckBox.toggled.connect(self.unitIdLabel.setEnabled)
        self.modbusCheckBox.toggled.connect(self.unitId.setEnabled)

        QMetaObject.connectSlotsByName(ConnectivityDialog)
    # setupUi

    def retranslateUi(self, ConnectivityDialog):
        ConnectivityDialog.setWindowTitle(QCoreApplication.translate("ConnectivityDialog", u"Device Connectivity", None))
        self.modbusLabel.setText(QCoreApplication.translate("ConnectivityDialog", u"Modbus TCP", None))
        self.unitIdLabel.setText(QCoreApplication.translate("ConnectivityDialog", u"Modbus Unit ID", None))
        self.blankLabel.setText("")
        self.channelSocketLabel.setText(QCoreApplication.translate("ConnectivityDialog", u"Channel Socket", None))
        self.modbusCheckBox.setText(QCoreApplication.translate("ConnectivityDialog", u"Enable Modbus TCP access", None))
        self.modbusDetails.setText(QCoreApplication.translate("ConnectivityDialog", u"Register Details...", None))
    # retranslateUi

