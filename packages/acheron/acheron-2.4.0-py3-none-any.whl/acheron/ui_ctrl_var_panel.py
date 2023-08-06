# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ctrl_var_panel.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_CtrlVarPanel(object):
    def setupUi(self, CtrlVarPanel):
        if not CtrlVarPanel.objectName():
            CtrlVarPanel.setObjectName(u"CtrlVarPanel")
        CtrlVarPanel.resize(99, 41)
        self.verticalLayout = QVBoxLayout(CtrlVarPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.ctrlVarLayout = QVBoxLayout()
        self.ctrlVarLayout.setObjectName(u"ctrlVarLayout")

        self.verticalLayout.addLayout(self.ctrlVarLayout)

        self.verticalSpacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(CtrlVarPanel)

        QMetaObject.connectSlotsByName(CtrlVarPanel)
    # setupUi

    def retranslateUi(self, CtrlVarPanel):
        CtrlVarPanel.setWindowTitle(QCoreApplication.translate("CtrlVarPanel", u"Control Variable Panel", None))
        CtrlVarPanel.setTitle(QCoreApplication.translate("CtrlVarPanel", u"Control Variables", None))
    # retranslateUi

