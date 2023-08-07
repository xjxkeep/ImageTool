from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui, QtCore,QtWidgets
from PIL import Image, ImageQt, ImageDraw
from utils import pil_to_qpix
import numpy as np

class MoveableBox(QLabel):
    geometryChanged = pyqtSignal(QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.__isTracking = False
        self.__startPos = QPoint(0, 0)
        self.__endPos = QPoint(0, 0)
        self.board_width = 4
        self.board_color = (255, 0, 0)
        self.fix_pos = None
        self.border_style="dotted"
        self.setStyleSheet(f"""
            border-width: {self.board_width}px;
            border-style: {self.border_style};
            border-color: rgb{self.board_color};
            background-color: rgba(0,0,0,0);""")

    def set_board_width(self, width):
        self.board_width = width
        self.setStyleSheet(f"""
            border-width: {self.board_width}px;
            border-style: {self.border_style};
            border-color: rgb{self.board_color};""")

    def set_board_color(self, color):
        self.board_color = color
        self.setStyleSheet(f"""
            border-width: {self.board_width}px;
            border-style: {self.border_style};
            border-color: rgb{self.board_color};""")

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        self.setStyleSheet(f"""
            border-width: {self.board_width + 3}px;
            border-style: {self.border_style};
            border-color: rgb{self.board_color};""")
        if event.button() == Qt.MouseButton.LeftButton:
            self.__isTracking = True
            self.__startPos = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if self.__isTracking:
            self.__endPos = event.pos()
            r = QRect(self.pos() + self.__endPos - self.__startPos, self.size())

            self.setGeometry(r)
            self.geometryChanged.emit(r)

    def mouseReleaseEvent(self, event):
        self.setStyleSheet(f"""
            border-width: {self.board_width}px;
            border-style: {self.border_style};
            border-color: rgb{self.board_color};""")
        if event.button() == Qt.MouseButton.LeftButton:
            self.__isTracking = False


class SelectRect(MoveableBox):

    def __init__(self, parent: QLabel):
        super().__init__(parent)
        self.__isResize = False
        
        

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.RightButton:
            self.__isResize = True
            self.fix_pos = self.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        super().mouseMoveEvent(event)
        if self.__isResize:
            x1 = self.x()
            x2 = event.pos().x() + self.x()
            y1 = self.y()
            y2 = event.pos().y() + self.y()
            r = QRect(QPoint(min(x1, x2), min(y1, y2)), QPoint(max(x1, x2), max(y1, y2)))
            # print(r.width()*r.height())
            self.setGeometry(r)
            self.geometryChanged.emit(r)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.RightButton:
            self.__isResize = False


class MagniBox(MoveableBox):
    def __init__(self, parent: QLabel, selected: SelectRect):
        super().__init__(parent)
        self.__scale = 1.5
        self.__selected = selected
        self.setScaledContents(True)
        qpix = parent.pixmap()
        pil_img = ImageQt.fromqpixmap(qpix)
        rect = selected.geometry()
        crop_img = pil_img.crop((rect.left(), rect.top(), rect.right(), rect.bottom()))
        crop_qpix = pil_to_qpix(crop_img)
        self.setPixmap(crop_qpix)

    def parent(self) -> QLabel:
        return super().parent()

    def handle_source_changed(self, rect: QRect):
        qpix = self.parent().pixmap()
        pil_img = ImageQt.fromqpixmap(qpix)
        crop_img = pil_img.crop((rect.left(), rect.top(), rect.right(), rect.bottom()))
        self.resize(rect.size() * self.__scale)
        crop_qpix = pil_to_qpix(crop_img)
        self.setPixmap(crop_qpix)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        p = self.pos()
        r = QRect(p, self.size())
        if r.left() < 20:
            p.setX(0)
        if self.parent().width() - r.right() < 20:
            p.setX(self.parent().width() - self.width())
        if r.top() < 20:
            p.setY(0)
        if self.parent().height() - r.bottom() < 20:
            p.setY(self.parent().height() - self.height())
        self.setGeometry(QRect(p, self.size()))

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, v):
        self.__scale = v
        self.resize(int(v * self.__selected.width()), int(v * self.__selected.height()))


class DrawBoard(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.resize(500, 500)
        self.__create_box = False
        self.boxs = []
        self.mags = []
        self.click_pos = None
        self.board_color = (255, 0, 0)
        self.board_width = 4
        self.mag_scale = 1.75
        self.top_box = None
        self.child_idx = 0

    def isEmpty(self):
        return len(self.boxs) == 0
    
    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        self.resize(a0.size())

        super().setPixmap(a0)
        for box in self.boxs:
            mag: MagniBox = box.get('mag', None)
            if mag is None: continue
            mag.handle_source_changed(box['select'].geometry())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.__create_box = True
            box = SelectRect(self)
            box.setGeometry(QRect(event.pos(), QSize(1, 1)))
            box.set_board_color(self.board_color)
            box.set_board_width(self.board_width)
            box.show()
            self.click_pos = event.pos()
            self.boxs.append({"select": box})
        elif event.button() == Qt.MouseButton.RightButton:
            self.click_pos = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        # if event.button()==Qt.MouseButton.LeftButton:
        if len(self.boxs) == 0: return
        if self.__create_box:
            box = self.boxs[-1]["select"]
            x1 = int(self.click_pos.x())
            x2 = int(event.pos().x())
            y1 = int(self.click_pos.y())
            y2 = int(event.pos().y())
            box.setGeometry(QRect(QPoint(min(x1, x2), min(y1, y2)), QPoint(max(x1, x2), max(y1, y2))))

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self.__create_box = False
            # self.add_mag()

    def add_mag(self):
        if len(self.boxs) == 0: return
        box = self.boxs[-1]
        sel = box['select']
        mag_box = MagniBox(self, sel)
        mag_box.set_board_color(sel.board_color)
        mag_box.set_board_width(sel.board_width)
        mag_box.scale = self.mag_scale
        sel.geometryChanged.connect(mag_box.handle_source_changed)
        mag_box.show()
        mag = self.boxs[-1].get('mag')
        if mag:
            mag.setVisible(False)
            del mag
        self.boxs[-1]['mag'] = mag_box

    def back(self):
        if len(self.boxs) > 0:
            box = self.boxs[-1]
            mag = box.get('mag', None)
            if mag:
                mag.setVisible(False)
                box['mag'] = None
                del mag
                return True
            sel = box['select']
            sel.setVisible(False)
            self.boxs.pop()
            del sel
            return True
        return False

    def clear(self):
        while self.back():
            pass

    def getPreviewImage(self, qpix=None):
        qpix = qpix or self.pixmap()
        ws, hs = self.pixmap().width(), self.pixmap().height()
        w, h = qpix.width(), qpix.height()
        wratio = w / ws
        hratio = h / hs
        pil_img = ImageQt.fromqpixmap(qpix)
        draw = ImageDraw.Draw(pil_img)
        if len(self.boxs) > 0:
            err=False
            for box in self.boxs:
                # try:
                sel: SelectRect = box['select']
                mag: MagniBox = box.get('mag')
                r = sel.geometry()
                left, top, right, bottom = r.left() * wratio, r.top() * hratio, r.right() * wratio, r.bottom() * hratio
                rleft, rright, rtop, rbottom = np.round([left, right, top, bottom]).astype('int')
                if mag:
                    rm = mag.geometry()
                    crop_img = pil_img.crop((rleft, rtop,rright, rbottom))
                    crop_img = crop_img.resize((int(rm.width() * wratio), int(rm.height() * hratio)))
                    pil_img.paste(crop_img, (int(rm.x() * wratio), int(rm.y() * hratio)))
                    left, top, right, bottom = rm.left() * wratio, rm.top() * hratio, rm.right() * wratio, rm.bottom() * hratio
                    left, right, top, bottom = np.round([left, right, top, bottom]).astype('int')
                    draw.rectangle((left, top, right, bottom), outline=sel.board_color, width=sel.board_width)
                draw.rectangle((rleft, rtop, rright, rbottom), outline=sel.board_color, width=sel.board_width)
                # except:
                #     err=True
            if err:
                QMessageBox.information(self,"错误","图像大小不一致，部分图像无法应用成功。")
                    
        qpix = pil_to_qpix(pil_img)
        return qpix


class DrawPannel(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(DrawPannel, self).__init__(parent)
        self.resize(300, 300)
        self.draw_board = DrawBoard()
        hlayout = QtWidgets.QHBoxLayout(self)
        hlayout.addWidget(self.draw_board)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setWidget(self.draw_board)
        self.home = parent

    def set_home(self, home):
        self.home = home

    def setPixmap(self, qpix: QPixmap):
        self.draw_board.setPixmap(qpix)

    def add_mag(self):
        self.draw_board.add_mag()

    def back(self):
        self.draw_board.back()

    def setBoarderColor(self, color):
        self.draw_board.board_color = color

    def set_boarder_width(self, width):
        self.draw_board.board_width = width

    def set_scale(self, scale):
        if scale == 0: scale = 1
        self.draw_board.mag_scale = scale

    def getPreviewImage(self, qpix=None):
        return self.draw_board.getPreviewImage(qpix)

    def clear(self):
        self.draw_board.clear()
        # return super().closeEvent(a0)


if __name__ == '__main__':
    # 使用例子
    import sys
    # from PySide6 import QtWidgets
    # from PySide2 import QtWidgets
    from PyQt5 import QtWidgets
    # from qt_material import apply_stylesheet

    app = QApplication(sys.argv)
    # setup stylesheet
    # apply_stylesheet(app, theme='default.xml')

    w = DrawPannel()
    w.setPixmap(QPixmap(r'1.jpg'))
    w.show()
    sys.exit(app.exec())
