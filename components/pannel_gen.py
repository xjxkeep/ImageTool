# Form implementation generated from reading ui file '.\components\pannel.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(365, 189)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_7 = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_7.setMaximumSize(QtCore.QSize(16777215, 300))
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.ColorDisp = QtWidgets.QLabel(parent=self.groupBox_7)
        self.ColorDisp.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ColorDisp.setObjectName("ColorDisp")
        self.gridLayout_7.addWidget(self.ColorDisp, 2, 0, 1, 1)
        self.cancelOneBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.cancelOneBut.setObjectName("cancelOneBut")
        self.gridLayout_7.addWidget(self.cancelOneBut, 3, 0, 1, 1)
        self.ChoseColorBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.ChoseColorBut.setObjectName("ChoseColorBut")
        self.gridLayout_7.addWidget(self.ChoseColorBut, 2, 3, 1, 1)
        self.backBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.backBut.setObjectName("backBut")
        self.gridLayout_7.addWidget(self.backBut, 0, 0, 1, 1)
        self.clearBoardBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.clearBoardBut.setObjectName("clearBoardBut")
        self.gridLayout_7.addWidget(self.clearBoardBut, 0, 3, 1, 1)
        self.applyAllBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.applyAllBut.setObjectName("applyAllBut")
        self.gridLayout_7.addWidget(self.applyAllBut, 4, 6, 1, 1)
        self.applyOneBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.applyOneBut.setObjectName("applyOneBut")
        self.gridLayout_7.addWidget(self.applyOneBut, 4, 0, 1, 1)
        self.cancelColBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.cancelColBut.setObjectName("cancelColBut")
        self.gridLayout_7.addWidget(self.cancelColBut, 3, 4, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=self.groupBox_7)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_7.addWidget(self.label_9, 2, 4, 1, 1)
        self.applyRowBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.applyRowBut.setObjectName("applyRowBut")
        self.gridLayout_7.addWidget(self.applyRowBut, 4, 3, 1, 1)
        self.cancelRowBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.cancelRowBut.setObjectName("cancelRowBut")
        self.gridLayout_7.addWidget(self.cancelRowBut, 3, 3, 1, 1)
        self.cancelAllBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.cancelAllBut.setObjectName("cancelAllBut")
        self.gridLayout_7.addWidget(self.cancelAllBut, 3, 6, 1, 1)
        self.applyColBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.applyColBut.setObjectName("applyColBut")
        self.gridLayout_7.addWidget(self.applyColBut, 4, 4, 1, 1)
        self.rectBoarderSizeSpin = QtWidgets.QSpinBox(parent=self.groupBox_7)
        self.rectBoarderSizeSpin.setProperty("value", 4)
        self.rectBoarderSizeSpin.setObjectName("rectBoarderSizeSpin")
        self.gridLayout_7.addWidget(self.rectBoarderSizeSpin, 2, 6, 1, 1)
        self.scaleSpin = QtWidgets.QDoubleSpinBox(parent=self.groupBox_7)
        self.scaleSpin.setSingleStep(0.2)
        self.scaleSpin.setProperty("value", 1.75)
        self.scaleSpin.setObjectName("scaleSpin")
        self.gridLayout_7.addWidget(self.scaleSpin, 1, 6, 1, 1)
        self.label_12 = QtWidgets.QLabel(parent=self.groupBox_7)
        self.label_12.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_7.addWidget(self.label_12, 1, 4, 1, 1)
        self.addMagnifierBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.addMagnifierBut.setObjectName("addMagnifierBut")
        self.gridLayout_7.addWidget(self.addMagnifierBut, 1, 3, 1, 1)
        self.removeMagnifierBut = QtWidgets.QPushButton(parent=self.groupBox_7)
        self.removeMagnifierBut.setObjectName("removeMagnifierBut")
        self.gridLayout_7.addWidget(self.removeMagnifierBut, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_7, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_7.setTitle(_translate("Form", "图像标注设置"))
        self.ColorDisp.setText(_translate("Form", "当前颜色"))
        self.cancelOneBut.setText(_translate("Form", "取消当前"))
        self.ChoseColorBut.setText(_translate("Form", "选择颜色"))
        self.backBut.setText(_translate("Form", "撤销"))
        self.clearBoardBut.setText(_translate("Form", "清空"))
        self.applyAllBut.setText(_translate("Form", "应用所有"))
        self.applyOneBut.setText(_translate("Form", "应用当前"))
        self.cancelColBut.setText(_translate("Form", "取消列"))
        self.label_9.setText(_translate("Form", "边框大小(Px)："))
        self.applyRowBut.setText(_translate("Form", "应用行"))
        self.cancelRowBut.setText(_translate("Form", "取消行"))
        self.cancelAllBut.setText(_translate("Form", "取消所有"))
        self.applyColBut.setText(_translate("Form", "应用列"))
        self.label_12.setText(_translate("Form", "放大比例："))
        self.addMagnifierBut.setText(_translate("Form", "添加放大镜"))
        self.removeMagnifierBut.setText(_translate("Form", "删除放大镜"))
