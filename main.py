from resource import *
import math
import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from components.drawBoard import DrawPannel
from components.menu import Menu
from components.pannel import Pannel
from components.table import CustomTableWidget
import json
from PyQt6 import QtGui


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.container=QWidget(self)
        self.setCentralWidget(self.container)
        self.draw_board=DrawPannel()
        self.img_table=CustomTableWidget()
        self.menu=Menu(self)
        self.pannel=Pannel(self)

        drawModule=QWidget()
        self.draw_dock=QDockWidget("Draw Preview", self)
        self.draw_dock.resize(self.draw_board.size())
        self.draw_dock.setWidget(self.draw_board)
        self.draw_dock.installEventFilter(self)
        self.preview_layout=QVBoxLayout(drawModule)
        self.preview_layout.addWidget(self.draw_dock)
        self.preview_layout.addWidget(self.pannel)


        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        splitter.addWidget(self.img_table)
        splitter.addWidget(drawModule)
        splitter.setStretchFactor(1, 1)
        vlayout=QVBoxLayout(self.container)
        vlayout.addWidget(splitter)
        vlayout.addWidget(self.menu)

        copyright_label = QLabel("Copyright © 2023 Jinxin Xiong. All Rights Reserved. Contact: 715020813@qq.com")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statusBar().addPermanentWidget(copyright_label, stretch=2)

        if os.path.exists("setting.json"):
            setting = json.load(open("setting.json", 'r',encoding='utf-8'))
            self.setWindowTitle(setting.get('title',"Image Tool V1.0"))
            self.resize(setting.get('w', 800), setting.get('h', 600))
        
        
        self.setWindowIcon(QtGui.QIcon(":/1.jpeg"))
        self.img_table.clicked.connect(self.selectTableItem)
        self.menu.heiSpin.editingFinished.connect(self.changeImageSize)
        self.menu.widSpin.editingFinished.connect(self.changeImageSize)
        self.menu.exportImagesBut.clicked.connect(self.saveImages)
        self.menu.addImagesBut.clicked.connect(self.addImages)
        self.menu.clearBut.clicked.connect(self.clearSelected)
        self.menu.delImgBut.clicked.connect(self.clearSelected)

    def clearSelected(self):
        for i in self.img_table.selectedIndexes():
            self.img_table.removeCellWidget(i.row(),i.column())

    def clearTable(self):
        self.img_table.emptyClear()
        self.draw_board.clear()

    def addImages(self):
        fileNames, _ = QFileDialog.getOpenFileNames(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if len(fileNames) == 0: return
        self.img_table.appendPixmaps(fileNames)
        self.refreshDrawPreview()

    def changeImageSize(self):
        h=self.menu.heiSpin.value() if self.menu.heiSpin.isEnabled() else None
        w=self.menu.widSpin.value() if self.menu.widSpin.isEnabled() else None
        self.img_table.uniformSize(w,h)       
        self.refreshDrawPreview() 


    def selectTableItem(self, modelIndex: QModelIndex):
        if not self.draw_board.draw_board.isEmpty():
            if QMessageBox.question(
                self, '提示', '当前还有尚未应用的选框，是否清除并进入编辑其他图片？',
                QMessageBox.StandardButton.Yes,
                QMessageBox.StandardButton.No) \
                    == QMessageBox.StandardButton.No:
                return
        self.draw_board.clear()
        item = self.img_table.cellWidget(modelIndex.row(), modelIndex.column())
        if item is None: return
        self.draw_board.setPixmap(item.pixmap)
        # print(item.pixmap.size())
        self.menu.widSpin.setValue(item.pixmap.size().width())
        self.menu.heiSpin.setValue(item.pixmap.size().height())



    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        setting = {
            "w": self.width(),
            "h": self.height(),
            "title":self.windowTitle()
        }
        with open("setting.json", 'w',encoding='utf-8') as fw:
            fw.write(json.dumps(setting,ensure_ascii=False))
        return super().closeEvent(a0)

    def eventFilter(self, obj, event: QEvent):
        
        if obj == self.draw_dock and event.type() == QEvent.Type.ZOrderChange:
            self.draw_dock.resize(self.draw_board.draw_board.width()+30,self.draw_board.draw_board.height()+30)
        if obj == self.draw_dock and event.type() == QEvent.Type.Close:
            # 保存 QDockWidget 的状态
            self.draw_dock = QDockWidget("Draw Preview", self)
            self.draw_dock.resize(self.draw_board.width(),self.draw_board.height())
            self.draw_dock.setWidget(self.draw_board)
            self.preview_layout.insertWidget(0,self.draw_dock)
            self.draw_dock.installEventFilter(self)
        return super().eventFilter(obj, event)
    
    def refreshDrawPreview(self):
        if len(self.img_table.selectedIndexes()) == 0: return
        selected_index = self.img_table.selectedIndexes()[0]
        twidget = self.img_table.cellWidget(selected_index.row(), selected_index.column())
        self.draw_board.setPixmap(twidget.pixmap)

    def exportAllImages(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择图像保存的文件夹', '/')
        if not folder_path: return
        self.img_table.exportImage(folder_path)
        QMessageBox.information(self, '提示', f'保存成功！\n路径:{folder_path}')
    
    def exportWord(self):
        # print("save pdf")
        word_file, _ = QFileDialog.getSaveFileName(None, "保存word文件", "", "Word Files (*.docx)")
        if self.img_table.img_cnt==0:return 
        if not word_file: return        
        self.img_table.exportWord(word_file,["all","bottom","none"][-2-self.menu.labelGroup.checkedId()])
        QMessageBox.information(self, '提示', f'导出Word文件成功!\n文件路径:{word_file}')

    def openImageFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '打开图像文件夹', r'/')
        if folder_path=="":return
        self.img_table.loadFolder(folder_path)
        self.menu.colSpin.setValue(int(math.sqrt(self.img_table.img_cnt)))

    def saveImages(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择保存的文件夹', '/')
        if not folder_path: return
        self.img_table.exportImage(folder_path)
        QMessageBox.information(self, '提示', f'保存成功！\n路径:{folder_path}')

    def changeRow(self, v):
        if v == 0: return
        self.menu.colSpin.setValue(max(math.ceil(self.img_table.img_cnt / v),self.menu.colSpin.value()))
        
        self.img_table.rearrange(self.menu.rowSpin.value(),self.menu.colSpin.value())

    def changeColumn(self, v):
        if v == 0: return
        self.menu.rowSpin.setValue(max(math.ceil(self.img_table.img_cnt / v),self.menu.rowSpin.value()))
        self.img_table.rearrange(self.menu.rowSpin.value(),self.menu.colSpin.value())
    
    def applyImageOperation(self):
        if len(self.img_table.selectedIndexes()) == 0: return
        selected_index = self.img_table.selectedIndexes()[0]
        twidget = self.img_table.cellWidget(selected_index.row(), selected_index.column())
        qimg = self.draw_board.draw_board.getPreviewImage()
        twidget.setPixmap(qimg)
        self.refreshDrawPreview()
        self.draw_board.clear()
    
    def applyImageOperationRows(self):
        if len(self.img_table.selectedIndexes()) == 0: return
        selected_index = self.img_table.selectedIndexes()[0]
        for c in range(self.img_table.columnCount()):
            twidget = self.img_table.cellWidget(selected_index.row(), c)
            if twidget is None: break
            qimg = self.draw_board.draw_board.getPreviewImage(twidget.pixmap)
            twidget.setPixmap(qimg)
        self.refreshDrawPreview()
        self.draw_board.clear()

    def applyImageOperationColumns(self):
        if len(self.img_table.selectedIndexes()) == 0: return
        selected_index = self.img_table.selectedIndexes()[0]
        for r in range(self.img_table.rowCount()):
            twidget = self.img_table.cellWidget(r, selected_index.column())
            if twidget is None: break
            qimg = self.draw_board.draw_board.getPreviewImage(twidget.pixmap)
            twidget.setPixmap(qimg)
        self.refreshDrawPreview()
        self.draw_board.clear()

        
    def applyImageOperationALL(self):
        for r in range(self.img_table.rowCount()):
            for c in range(self.img_table.columnCount()):
                twidget = self.img_table.cellWidget(r, c)
                if twidget is None: break
                qimg = self.draw_board.draw_board.getPreviewImage(twidget.pixmap)
                twidget.setPixmap(qimg)
        self.refreshDrawPreview()
        self.draw_board.clear()
    
    def cancelImageOperation(self):
        if len(self.img_table.selectedIndexes()) == 0: return
        selected_index = self.img_table.selectedIndexes()[0]
        twidget = self.img_table.cellWidget(selected_index.row(), selected_index.column())
        twidget.reloadPixmap()
        self.draw_board.setPixmap(twidget.pixmap)

    def cancelImageOperationColumns(self):
        if len(self.img_table.selectedIndexes()) == 0: return
        selected_index = self.img_table.selectedIndexes()[0]
        for r in range(self.img_table.rowCount()):
            twidget = self.img_table.cellWidget(r, selected_index.column())
            if twidget is None: break
            twidget.reloadPixmap()
        twidget = self.img_table.cellWidget(selected_index.row(), selected_index.column())
        self.draw_board.setPixmap(twidget.pixmap)

    def cancelImageOperationRows(self):
        if len(self.img_table.selectedIndexes()) == 0: return
        selected_index = self.img_table.selectedIndexes()[0]
        for c in range(self.img_table.columnCount()):
            twidget = self.img_table.cellWidget(selected_index.row(), c)
            if twidget is None: break
            twidget.reloadPixmap()
        twidget = self.img_table.cellWidget(selected_index.row(), selected_index.column())
        self.draw_board.setPixmap(twidget.pixmap)

    def cancelImageOperationALL(self):
        for r in range(self.img_table.rowCount()):
            for c in range(self.img_table.columnCount()):
                twidget = self.img_table.cellWidget(r, c)
                if twidget is None:break
                twidget.reloadPixmap()
        if len(self.img_table.selectedIndexes()) == 0: return
        selected_index = self.img_table.selectedIndexes()[0]
        twidget = self.img_table.cellWidget(selected_index.row(), selected_index.column())
        self.draw_board.setPixmap(twidget.pixmap)


    def setColFirst(self):
        self.img_table.col_first=False
        self.img_table.rearrange(self.menu.rowSpin.value(),self.menu.colSpin.value())
    
    def setRowFirst(self):
        self.img_table.col_first=True
        self.img_table.rearrange(self.menu.rowSpin.value(),self.menu.colSpin.value())
    def setBoarderColor(self):
        color = QColorDialog.getColor(parent=self)
        if not color: return
        c = (color.red(), color.green(), color.blue())
        self.draw_board.setBoarderColor(c)

        self.pannel.ColorDisp.setStyleSheet(f"color: rgb{c};")
    

    
    
app = QApplication(sys.argv)

from components.stylesheet import MyStyleSheet
app.setStyleSheet(MyStyleSheet)
demo = MainWindow()

demo.show()

sys.exit(app.exec())
