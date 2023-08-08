import math
import sys
import typing
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QWidget, QVBoxLayout,QLineEdit,QMainWindow,QPushButton,QFileDialog
from PyQt6.QtGui import QPixmap,QMouseEvent
from PyQt6.QtCore import Qt,QRect
import os
from gen_word_table import add_pic_to_cell, add_text_to_cell
from docx import Document


class TableItem(QWidget):
    def __init__(self,img_path=None,text=None,size=120, parent=None) -> None:
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        
        self.img_path=img_path
        self.text=text
        self.isize=size
        self.label = QLabel()
        self.label.setScaledContents(True)
        self.label.setFixedSize(size,size)
        if img_path is None:
            self.pixmap=None
        else:
            self.pixmap=QPixmap(img_path)
            self.label.setPixmap(self.pixmap)
            self.label.setFixedSize(size,int(size*(self.pixmap.height()/self.pixmap.width())))
        self.layout().addWidget(self.label)
        self.text_label = QLineEdit(text)
        self.text_label.setStyleSheet("border: none;background-color: transparent;")
        self.layout().addWidget(self.text_label)
        self.text_label.textChanged.connect(self.updateText)
    
    def reloadPixmap(self):
        if self.img_path is None:return
        self.setPixmap(QPixmap(self.img_path))

    def updateText(self):
        self.text=self.text_label.text()

    def copy(self):
        cp=TableItem()
        cp.setPixmap(self.pixmap)
        cp.img_path=self.img_path
        cp.setText(self.text)
        return cp
    
    def setText(self,text):
        self.text=text
        self.text_label.setText(text)
    
    def setPixmap(self,pixmap):
        self.pixmap=pixmap
        self.label.setPixmap(self.pixmap)

        self.label.setFixedSize(self.isize,int(self.isize*(self.pixmap.height()/self.pixmap.width())))
        self.label.setScaledContents(True)
    
    def pixmapResize(self,w=None,h=None):
        if w is None and h is None:return
        if w==0 or h==0:return
        if w is None:
            self.setPixmap(self.pixmap.scaledToHeight(int(h)))
        elif h is None:
            self.setPixmap(self.pixmap.scaledToWidth(int(w)))
        else:

            self.setPixmap(self.pixmap.scaled(int(w),int(h)))
    
class CustomTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.sort_mode=True
        self.col_first=False
        self.init_ui()
        self.source_row = -1
        self.source_col = -1
        self.img_cnt=0
        self.setRowCount(0)
        self.setColumnCount(0)

    def _add_widget(self, row, col,img_path,text):
        # item_widget=self._get_widget(img_path,text)
        item_widget=TableItem(img_path,text)
        self.setCellWidget(row, col, item_widget)

    def init_ui(self):
        self.resize(800,500)
        self.setRowCount(0)
        self.setColumnCount(0)
        self.horizontalHeader().setSectionsMovable(True)
        self.verticalHeader().setSectionsMovable(True)
        self.setDragEnabled(True)  # Enable drag and drop
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.rearrange(4)
    
    def cellWidget(self, row: int, column: int) -> TableItem:
        return super().cellWidget(row, column)

    def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(e)
        row=self.rowAt(e.pos().y())
        col=self.columnAt(e.pos().x())
        widget=self.cellWidget(row,col)
        if widget is None:
            return

        label=widget.text_label
        # 设置label选中且全选
        label.setFocus()
        label.selectAll()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.source_row = self.rowAt(event.pos().y())
            self.source_col = self.columnAt(event.pos().x())
        super().mousePressEvent(event)

    def dropEvent(self, event):
        if self.source_row != -1 and self.source_col != -1:
            # if not event or not event.position().y:
            target_row = self.rowAt(int(event.position().y()))
            target_col = self.columnAt(int(event.position().x()))
            
            source_widget = self.cellWidget(self.source_row, self.source_col)
            target_widget = self.cellWidget(target_row, target_col)
            self.clearSelection()
            self.setCurrentCell(target_row,target_col)
            
            
            if source_widget is None and target_widget is None:
                return
            if source_widget is None:
                self.setCellWidget(self.source_row, self.source_col, target_widget.copy())
                self.removeCellWidget(target_row, target_col)
                self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                return
            if target_widget is None:
                self.setCellWidget(target_row, target_col, source_widget.copy())
                self.removeCellWidget(self.source_row, self.source_col)
                self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                return
            
            self.setCellWidget(self.source_row, self.source_col, target_widget.copy())
            self.setCellWidget(target_row, target_col, source_widget.copy())
            
            self.source_row = -1
            self.source_col = -1

    def uniformSize(self,w=None,h=None) :
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                widget=self.cellWidget(i,j)
                if widget is None:continue
                widget.pixmapResize(w,h)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    def appendPixmaps(self,paths:list[str]):
        col_first=self.col_first
        widgets=[]
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                widget=self.cellWidget(i,j)
                if widget is not None:
                    widgets.append(widget.copy())
        for path in paths:
            text=os.path.basename(path)
            text=text[:text.rfind('.')]
            widget=TableItem(path,text)
            widgets.append(widget)
        if col_first:
            col=self.columnCount()
            if col==0:col=1
            row=math.ceil(len(widgets)/col)
        else:
            row=self.rowCount()
            if row==0:row=1
            col=math.ceil(len(widgets)/row)
        self.setRowCount(row)
        self.setColumnCount(col)
        self.clearContents()
        widgets=sorted(widgets,key=lambda x:x.text)
        self.img_cnt+=len(widgets)
        if col_first:
            for i,widget in enumerate(widgets):
                self.setCellWidget(i//col,i%col,widget)
        else:
            for i,widget in enumerate(widgets):
                self.setCellWidget(i%row,i//row,widget)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def rearrange(self,row=None,col=None,col_first:bool=False):
        col_first=self.col_first
        widgets=[]
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                widget=self.cellWidget(i,j)
                if widget is not None:
                    widgets.append(widget.copy())
        if row is None and col is None:
            row=int(math.sqrt(self.img_cnt))
            col=math.ceil(self.img_cnt/row)
        elif row is None:
            row=math.ceil(len(widgets)/col)
        elif col is None:
            col=math.ceil(len(widgets)/row)

        
        self.setRowCount(row)
        self.setColumnCount(col)
        self.clearContents()
        
        widgets=list(sorted(widgets,key=lambda x:x.text))
        hheader = self.horizontalHeader()
        vheader = self.verticalHeader()
        # print(widgets)
        if col_first:
            for r in range(row):
                for c in range(col):
                    if len(widgets)==0:break
                    self.setCellWidget(vheader.logicalIndex(r),hheader.logicalIndex(c),widgets.pop(0))
            
        else:
            for c in range(col):
                for r in range(row):
                    if len(widgets)==0:break
                    self.setCellWidget(vheader.logicalIndex(r),hheader.logicalIndex(c),widgets.pop(0))
            
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    
    def loadFolder(self,folder,col=5):
        self.clearContents()
        self.img_cnt=len(os.listdir(folder))
        row=math.ceil(self.img_cnt/col)
        self.setRowCount(row)
        self.setColumnCount(col)

        for i,file in enumerate(os.listdir(folder)):
            if not file.endswith(('.jpg',".png",".bmp")): continue
            file=os.path.splitext(file)[0]
            self._add_widget(i//col,i%col,os.path.join(folder,file),file)
        # self.rearrange(5,sort,row_first)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
    def exportImage(self,folder):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                widget=self.cellWidget(i,j)
                if widget is None:
                    continue
                
                label=widget.label
                name=widget.text
                if name=="":
                    name=f"{i}-{j}.jpg"
                else:
                    name=f"{name}.jpg"
                label.pixmap().save(os.path.join(folder,name))

    def exportWord(self,filepath):
        document = Document()
        # document.sections[0].top_margin = Cm(0)
        # document.sections[0].bottom_margin = Cm(0)
        # document.sections[0].left_margin = Cm(0)
        # document.sections[0].right_margin = Cm(0)
        
        if not os.path.exists(os.path.join(os.path.dirname(filepath),"images")):
            os.makedirs(os.path.join(os.path.dirname(filepath),"images"))
        g_row = self.rowCount()
        g_col = self.columnCount()

        width = (21.59-3.18-3.18) / g_col
        table = document.add_table(rows=g_row, cols=g_col) 
        row_index = 0

        hheader = self.horizontalHeader()
        vheader = self.verticalHeader()
        for r in range(g_row):
            # todo fix bug 
            add_row_flag = False
            for c in range(g_col):
                widget = self.cellWidget(vheader.logicalIndex(r), hheader.logicalIndex(c))
                if widget is None: continue
                label = widget.label
                pixmap = label.pixmap()
                text = widget.text
                if text=="":text =f"{r}-{c}"
                img_path = os.path.join(os.path.dirname(filepath),"images",text+".jpg")
                pixmap.save(img_path)
                
                add_pic_to_cell(table, row_index, c, img_path, width)
                add_text_to_cell(table, row_index, c, text, width)
            row_index += 1

        table.autofit = True
        
        document.save(filepath)
