# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rf_test_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QWidget)

class Ui_RFTestDialog(object):
    def setupUi(self, RFTestDialog):
        if not RFTestDialog.objectName():
            RFTestDialog.setObjectName(u"RFTestDialog")
        RFTestDialog.resize(251, 413)
        self.gridLayout = QGridLayout(RFTestDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(RFTestDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 17, 0, 1, 4)

        self.verticalSpacer_8 = QSpacerItem(10, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_8, 16, 0, 1, 4)

        self.stopChannelLabel = QLabel(RFTestDialog)
        self.stopChannelLabel.setObjectName(u"stopChannelLabel")
        self.stopChannelLabel.setEnabled(False)

        self.gridLayout.addWidget(self.stopChannelLabel, 8, 2, 1, 1)

        self.startFreqLabel = QLabel(RFTestDialog)
        self.startFreqLabel.setObjectName(u"startFreqLabel")
        self.startFreqLabel.setEnabled(False)

        self.gridLayout.addWidget(self.startFreqLabel, 7, 2, 1, 1)

        self.hopCount = QSpinBox(RFTestDialog)
        self.hopCount.setObjectName(u"hopCount")
        self.hopCount.setEnabled(False)
        self.hopCount.setMaximum(65535)

        self.gridLayout.addWidget(self.hopCount, 11, 3, 1, 1)

        self.hopInterval = QSpinBox(RFTestDialog)
        self.hopInterval.setObjectName(u"hopInterval")
        self.hopInterval.setEnabled(False)
        self.hopInterval.setMinimum(1)
        self.hopInterval.setMaximum(65535)

        self.gridLayout.addWidget(self.hopInterval, 10, 3, 1, 1)

        self.rxCarrierRadioButton = QRadioButton(RFTestDialog)
        self.rxCarrierRadioButton.setObjectName(u"rxCarrierRadioButton")

        self.gridLayout.addWidget(self.rxCarrierRadioButton, 14, 1, 1, 3)

        self.hopCountLabel = QLabel(RFTestDialog)
        self.hopCountLabel.setObjectName(u"hopCountLabel")
        self.hopCountLabel.setEnabled(False)

        self.gridLayout.addWidget(self.hopCountLabel, 11, 2, 1, 1)

        self.txCarrierRadioButton = QRadioButton(RFTestDialog)
        self.txCarrierRadioButton.setObjectName(u"txCarrierRadioButton")

        self.gridLayout.addWidget(self.txCarrierRadioButton, 13, 1, 1, 3)

        self.hopIntervalLabel = QLabel(RFTestDialog)
        self.hopIntervalLabel.setObjectName(u"hopIntervalLabel")
        self.hopIntervalLabel.setEnabled(False)

        self.gridLayout.addWidget(self.hopIntervalLabel, 10, 2, 1, 1)

        self.testModeLabel = QLabel(RFTestDialog)
        self.testModeLabel.setObjectName(u"testModeLabel")
        font = QFont()
        font.setBold(True)
        self.testModeLabel.setFont(font)

        self.gridLayout.addWidget(self.testModeLabel, 12, 0, 1, 2)

        self.fixedChannelLabel = QLabel(RFTestDialog)
        self.fixedChannelLabel.setObjectName(u"fixedChannelLabel")

        self.gridLayout.addWidget(self.fixedChannelLabel, 2, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(20, 13, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(20, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 2, 1, 1, 1)

        self.stopChannel = QSpinBox(RFTestDialog)
        self.stopChannel.setObjectName(u"stopChannel")
        self.stopChannel.setEnabled(False)
        self.stopChannel.setMaximum(100)
        self.stopChannel.setSingleStep(2)
        self.stopChannel.setValue(78)

        self.gridLayout.addWidget(self.stopChannel, 8, 3, 1, 1)

        self.fixedDuration = QSpinBox(RFTestDialog)
        self.fixedDuration.setObjectName(u"fixedDuration")
        self.fixedDuration.setMaximum(65535)

        self.gridLayout.addWidget(self.fixedDuration, 4, 3, 1, 1)

        self.txModulatedRadioButton = QRadioButton(RFTestDialog)
        self.txModulatedRadioButton.setObjectName(u"txModulatedRadioButton")

        self.gridLayout.addWidget(self.txModulatedRadioButton, 15, 1, 1, 3)

        self.testTypeLabel = QLabel(RFTestDialog)
        self.testTypeLabel.setObjectName(u"testTypeLabel")
        self.testTypeLabel.setFont(font)

        self.gridLayout.addWidget(self.testTypeLabel, 0, 0, 1, 2)

        self.startChannel = QSpinBox(RFTestDialog)
        self.startChannel.setObjectName(u"startChannel")
        self.startChannel.setEnabled(False)
        self.startChannel.setMaximum(100)
        self.startChannel.setSingleStep(2)
        self.startChannel.setValue(2)

        self.gridLayout.addWidget(self.startChannel, 6, 3, 1, 1)

        self.startChannelLabel = QLabel(RFTestDialog)
        self.startChannelLabel.setObjectName(u"startChannelLabel")
        self.startChannelLabel.setEnabled(False)

        self.gridLayout.addWidget(self.startChannelLabel, 6, 2, 1, 1)

        self.fixedChannel = QSpinBox(RFTestDialog)
        self.fixedChannel.setObjectName(u"fixedChannel")
        self.fixedChannel.setMaximum(100)
        self.fixedChannel.setSingleStep(2)
        self.fixedChannel.setValue(2)

        self.gridLayout.addWidget(self.fixedChannel, 2, 3, 1, 1)

        self.fixedRadioButton = QRadioButton(RFTestDialog)
        self.fixedRadioButton.setObjectName(u"fixedRadioButton")
        self.fixedRadioButton.setChecked(True)

        self.gridLayout.addWidget(self.fixedRadioButton, 1, 1, 1, 3)

        self.stopFreqLabel = QLabel(RFTestDialog)
        self.stopFreqLabel.setObjectName(u"stopFreqLabel")
        self.stopFreqLabel.setEnabled(False)

        self.gridLayout.addWidget(self.stopFreqLabel, 9, 2, 1, 1)

        self.fixedDurationLabel = QLabel(RFTestDialog)
        self.fixedDurationLabel.setObjectName(u"fixedDurationLabel")

        self.gridLayout.addWidget(self.fixedDurationLabel, 4, 2, 1, 1)

        self.sweepRadioButton = QRadioButton(RFTestDialog)
        self.sweepRadioButton.setObjectName(u"sweepRadioButton")

        self.gridLayout.addWidget(self.sweepRadioButton, 5, 1, 1, 3)

        self.centerFreqLabel = QLabel(RFTestDialog)
        self.centerFreqLabel.setObjectName(u"centerFreqLabel")

        self.gridLayout.addWidget(self.centerFreqLabel, 3, 2, 1, 1)

        self.stopFreq = QLabel(RFTestDialog)
        self.stopFreq.setObjectName(u"stopFreq")
        self.stopFreq.setEnabled(False)

        self.gridLayout.addWidget(self.stopFreq, 9, 3, 1, 1)

        self.startFreq = QLabel(RFTestDialog)
        self.startFreq.setObjectName(u"startFreq")
        self.startFreq.setEnabled(False)

        self.gridLayout.addWidget(self.startFreq, 7, 3, 1, 1)

        self.centerFreq = QLabel(RFTestDialog)
        self.centerFreq.setObjectName(u"centerFreq")

        self.gridLayout.addWidget(self.centerFreq, 3, 3, 1, 1)

        self.gridLayout.setColumnStretch(3, 1)
        QWidget.setTabOrder(self.fixedRadioButton, self.fixedChannel)
        QWidget.setTabOrder(self.fixedChannel, self.fixedDuration)
        QWidget.setTabOrder(self.fixedDuration, self.sweepRadioButton)
        QWidget.setTabOrder(self.sweepRadioButton, self.startChannel)
        QWidget.setTabOrder(self.startChannel, self.stopChannel)
        QWidget.setTabOrder(self.stopChannel, self.hopInterval)
        QWidget.setTabOrder(self.hopInterval, self.hopCount)
        QWidget.setTabOrder(self.hopCount, self.txCarrierRadioButton)
        QWidget.setTabOrder(self.txCarrierRadioButton, self.rxCarrierRadioButton)
        QWidget.setTabOrder(self.rxCarrierRadioButton, self.txModulatedRadioButton)

        self.retranslateUi(RFTestDialog)
        self.buttonBox.accepted.connect(RFTestDialog.accept)
        self.buttonBox.rejected.connect(RFTestDialog.reject)
        self.fixedRadioButton.toggled.connect(self.fixedChannelLabel.setEnabled)
        self.fixedRadioButton.toggled.connect(self.fixedChannel.setEnabled)
        self.fixedRadioButton.toggled.connect(self.fixedDurationLabel.setEnabled)
        self.fixedRadioButton.toggled.connect(self.fixedDuration.setEnabled)
        self.sweepRadioButton.toggled.connect(self.startChannelLabel.setEnabled)
        self.sweepRadioButton.toggled.connect(self.startChannel.setEnabled)
        self.sweepRadioButton.toggled.connect(self.stopChannelLabel.setEnabled)
        self.sweepRadioButton.toggled.connect(self.stopChannel.setEnabled)
        self.sweepRadioButton.toggled.connect(self.hopIntervalLabel.setEnabled)
        self.sweepRadioButton.toggled.connect(self.hopInterval.setEnabled)
        self.sweepRadioButton.toggled.connect(self.hopCountLabel.setEnabled)
        self.sweepRadioButton.toggled.connect(self.hopCount.setEnabled)
        self.fixedRadioButton.toggled.connect(self.centerFreqLabel.setEnabled)
        self.fixedRadioButton.toggled.connect(self.centerFreq.setEnabled)
        self.sweepRadioButton.toggled.connect(self.startFreqLabel.setEnabled)
        self.sweepRadioButton.toggled.connect(self.startFreq.setEnabled)
        self.sweepRadioButton.toggled.connect(self.stopFreqLabel.setEnabled)
        self.sweepRadioButton.toggled.connect(self.stopFreq.setEnabled)

        QMetaObject.connectSlotsByName(RFTestDialog)
    # setupUi

    def retranslateUi(self, RFTestDialog):
        RFTestDialog.setWindowTitle(QCoreApplication.translate("RFTestDialog", u"RF Test", None))
        self.stopChannelLabel.setText(QCoreApplication.translate("RFTestDialog", u"Stop Channel", None))
        self.startFreqLabel.setText(QCoreApplication.translate("RFTestDialog", u"Start Frequency", None))
        self.hopInterval.setSuffix(QCoreApplication.translate("RFTestDialog", u" ms", None))
        self.rxCarrierRadioButton.setText(QCoreApplication.translate("RFTestDialog", u"RX Carrier", None))
        self.hopCountLabel.setText(QCoreApplication.translate("RFTestDialog", u"Hop Count (0=\u221e)", None))
        self.txCarrierRadioButton.setText(QCoreApplication.translate("RFTestDialog", u"TX Carrier", None))
        self.hopIntervalLabel.setText(QCoreApplication.translate("RFTestDialog", u"Hop Interval", None))
        self.testModeLabel.setText(QCoreApplication.translate("RFTestDialog", u"Test Mode", None))
        self.fixedChannelLabel.setText(QCoreApplication.translate("RFTestDialog", u"Channel", None))
        self.fixedDuration.setSuffix(QCoreApplication.translate("RFTestDialog", u" ms", None))
        self.txModulatedRadioButton.setText(QCoreApplication.translate("RFTestDialog", u"TX Modulated Carrier", None))
        self.testTypeLabel.setText(QCoreApplication.translate("RFTestDialog", u"Test Type", None))
        self.startChannelLabel.setText(QCoreApplication.translate("RFTestDialog", u"Start Channel", None))
        self.fixedRadioButton.setText(QCoreApplication.translate("RFTestDialog", u"Fixed Frequency", None))
        self.stopFreqLabel.setText(QCoreApplication.translate("RFTestDialog", u"Stop Frequency", None))
        self.fixedDurationLabel.setText(QCoreApplication.translate("RFTestDialog", u"Duration (0=\u221e)", None))
        self.sweepRadioButton.setText(QCoreApplication.translate("RFTestDialog", u"Sweep", None))
        self.centerFreqLabel.setText(QCoreApplication.translate("RFTestDialog", u"Center Frequency", None))
        self.stopFreq.setText(QCoreApplication.translate("RFTestDialog", u"2478 MHz", None))
        self.startFreq.setText(QCoreApplication.translate("RFTestDialog", u"2402 MHz", None))
        self.centerFreq.setText(QCoreApplication.translate("RFTestDialog", u"2402 MHz", None))
    # retranslateUi

