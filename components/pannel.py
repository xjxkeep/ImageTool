import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget
from components.pannel_gen import Ui_Form
from PyQt6.QtWidgets import *


class Pannel(QWidget,Ui_Form):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)

        self.applyOneBut.clicked.connect(parent.applyImageOperation)
        self.applyRowBut.clicked.connect(parent.applyImageOperationRows)
        self.applyAllBut.clicked.connect(parent.applyImageOperationALL)
        self.applyColBut.clicked.connect(parent.applyImageOperationColumns)

        self.cancelOneBut.clicked.connect(parent.cancelImageOperation)
        self.cancelColBut.clicked.connect(parent.cancelImageOperationColumns)
        self.cancelRowBut.clicked.connect(parent.cancelImageOperationRows)
        self.cancelAllBut.clicked.connect(parent.cancelImageOperationALL)

        self.addMagnifierBut.clicked.connect(parent.draw_board.add_mag)
        self.scaleSpin.valueChanged.connect(parent.draw_board.set_scale)
        self.backBut.clicked.connect(parent.draw_board.back)
        self.rectBoarderSizeSpin.valueChanged.connect(parent.draw_board.set_boarder_width)
        self.ChoseColorBut.clicked.connect(parent.setBoarderColor)
        self.ColorDisp.setStyleSheet(f"color: rgb(255,0,0);")
        # self.saveImgBut.clicked.connect(parent.save_image)
        self.clearBoardBut.clicked.connect(parent.draw_board.clear)

 