# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pxmarkerdialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PxMarkerDialog(object):
    def setupUi(self, PxMarkerDialog):
        PxMarkerDialog.setObjectName("PxMarkerDialog")
        PxMarkerDialog.resize(400, 300)
        self.btn_confirm_box = QtWidgets.QDialogButtonBox(PxMarkerDialog)
        self.btn_confirm_box.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.btn_confirm_box.setOrientation(QtCore.Qt.Vertical)
        self.btn_confirm_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btn_confirm_box.setObjectName("btn_confirm_box")
        self.pxmarker_table_widget = QtWidgets.QTableWidget(PxMarkerDialog)
        self.pxmarker_table_widget.setGeometry(QtCore.QRect(10, 20, 271, 261))
        self.pxmarker_table_widget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.pxmarker_table_widget.setObjectName("pxmarker_table_widget")
        self.pxmarker_table_widget.setColumnCount(3)
        self.pxmarker_table_widget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.pxmarker_table_widget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.pxmarker_table_widget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.pxmarker_table_widget.setHorizontalHeaderItem(2, item)
        self.pxmarker_table_widget.horizontalHeader().setDefaultSectionSize(50)
        self.pxmarker_table_widget.horizontalHeader().setMinimumSectionSize(40)
        self.pxmarker_table_widget.horizontalHeader().setStretchLastSection(True)
        self.pxmarker_table_widget.verticalHeader().setVisible(False)
        self.pxmarker_table_widget.verticalHeader().setHighlightSections(False)

        self.retranslateUi(PxMarkerDialog)
        self.btn_confirm_box.accepted.connect(PxMarkerDialog.accept)
        self.btn_confirm_box.rejected.connect(PxMarkerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PxMarkerDialog)

    def retranslateUi(self, PxMarkerDialog):
        _translate = QtCore.QCoreApplication.translate
        PxMarkerDialog.setWindowTitle(_translate("PxMarkerDialog", "Dialog"))
        item = self.pxmarker_table_widget.horizontalHeaderItem(0)
        item.setText(_translate("PxMarkerDialog", "Class"))
        item = self.pxmarker_table_widget.horizontalHeaderItem(1)
        item.setText(_translate("PxMarkerDialog", "Color"))
        item = self.pxmarker_table_widget.horizontalHeaderItem(2)
        item.setText(_translate("PxMarkerDialog", "Feature"))

