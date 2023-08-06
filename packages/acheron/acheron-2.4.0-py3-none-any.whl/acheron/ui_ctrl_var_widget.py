# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ctrl_var_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSlider, QWidget)

class Ui_CtrlVarWidget(object):
    def setupUi(self, CtrlVarWidget):
        if not CtrlVarWidget.objectName():
            CtrlVarWidget.setObjectName(u"CtrlVarWidget")
        CtrlVarWidget.resize(121, 19)
        self.horizontalLayout = QHBoxLayout(CtrlVarWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.nameLabel = QLabel(CtrlVarWidget)
        self.nameLabel.setObjectName(u"nameLabel")

        self.horizontalLayout.addWidget(self.nameLabel)

        self.slider = QSlider(CtrlVarWidget)
        self.slider.setObjectName(u"slider")
        self.slider.setMinimumSize(QSize(50, 0))
        self.slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.slider)


        self.retranslateUi(CtrlVarWidget)

        QMetaObject.connectSlotsByName(CtrlVarWidget)
    # setupUi

    def retranslateUi(self, CtrlVarWidget):
        CtrlVarWidget.setWindowTitle(QCoreApplication.translate("CtrlVarWidget", u"Ctrl Var Widget", None))
        self.nameLabel.setText(QCoreApplication.translate("CtrlVarWidget", u"Ctrl Var Name", None))
    # retranslateUi

