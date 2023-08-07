
from PyQt6.QtGui import QPixmap,QImage
import numpy as np
# from PIL import ImageQt
# def qpix_to_cvimg(qtpixmap):
#     pil=ImageQt.fromqpixmap(qtpixmap)
#     cvimg=np.array(pil)
#     cvimg=cv2.cvtColor(cvimg,cv2.COLOR_RGB2BGR)
#     return cvimg

# def cvimg_to_qimg(cvimg):

#     height, width, depth = cvimg.shape
#     cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
#     qimg = QImage(cvimg.data, width, height, width * depth, QImage.Format.Format_RGB888)

#     return qimg

# def cvimg_to_qpix(cvimg):
#     qimg=cvimg_to_qimg(cvimg)
#     return QPixmap.fromImage(qimg)


def pil_to_qimg(pilimg):
    cvimg=np.array(pilimg)
    height, width, depth = cvimg.shape
    qimg = QImage(cvimg.data, width, height, width * depth, QImage.Format.Format_RGB888)
    return qimg

def pil_to_qpix(pilimg):
    return QPixmap.fromImage(pil_to_qimg(pilimg))
    