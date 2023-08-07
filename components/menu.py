import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget
from components.menu_gen import Ui_Form
from PyQt6.QtWidgets import *


class Menu(QWidget,Ui_Form):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        self.heiSpin.setDisabled(True)
        self.widSpin.setDisabled(True)
        self.imgFolderBut.clicked.connect(parent.openImageFolder)
        self.exportWordBut.clicked.connect(parent.exportWord)

        self.rowSpin.valueChanged.connect(parent.changeRow)
        self.colSpin.valueChanged.connect(parent.changeColumn)

        self.rowFirst.clicked.connect(parent.setRowFirst)
        self.colFirst.clicked.connect(parent.setColFirst)
        self.sizeGroup.buttonClicked.connect(self.size_options)

        
    def size_options(self):
        cid = self.sizeGroup.checkedId()
        # print(cid)
        if cid == -4:
            self.heiSpin.setDisabled(True)
            self.widSpin.setDisabled(True)
            
        elif cid == -5:
            self.heiSpin.setDisabled(False)
            self.widSpin.setDisabled(False)

            
        elif cid == -2:
            self.heiSpin.setDisabled(True)
            self.widSpin.setDisabled(False)
            
        elif cid == -3:
            self.heiSpin.setDisabled(False)
            self.widSpin.setDisabled(True)
            