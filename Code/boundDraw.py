import sys, os
import json

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setFont(QFont('Arial', 20))
    
    def setPixmap(self, image):
        super().setPixmap(image)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1920, 1080)
        self.setAcceptDrops(True)

        self.path = None
        self.filename = None
        
        self.begin = QPoint(-10, -10)   #set begin point out of screen
        self.end = QPoint(-10, -10)     #set begin point out of screen
        self.c_radius = 5

        alert = QMessageBox()
        alert.setText('Drag and drop a photo to start')
        alert.exec()

        self.moving_b = False
        self.moving_e = False

        self.mainLayout = QVBoxLayout()
        self.image = None
        self.setLayout(self.mainLayout)

        self.showMaximized()

    def paintEvent(self, event):
        qp = QPainter(self)

        if self.image != None:
            qp.drawImage(0, 0, self.image)

        #####################

        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(QRect(self.begin, self.end))  

        #####################
        
        qp.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        qp.setBrush(QBrush(Qt.blue)) 
        qp.drawEllipse(self.begin, self.c_radius, self.c_radius)
        qp.drawEllipse(self.end, self.c_radius, self.c_radius)

        #####################  

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            self.path = event.mimeData().urls()[0].toLocalFile()
            self.filename = self.path.split('/')[-1]
            self.image = QImage(self.path)
            self.update()
            event.accept()
        else:
            event.ignore()


    def mousePressEvent(self, event):
        n_pos = event.pos()
        if (self.begin.x() - 15 <= n_pos.x() <= self.begin.x() + 15) and (self.begin.y() - 15 <= n_pos.y() <= self.begin.y() + 15) :
            self.moving_b = True
            self.moving_e = False
            self.begin = event.pos()
        
        elif (self.end.x() - 15 <= n_pos.x() <= self.end.x() + 15) and (self.end.y() - 15 <= n_pos.y() <= self.end.y() + 15) :
            self.moving_e = True
            self.moving_b = False
            self.end = event.pos()

        else:
            self.moving_b = False
            self.moving_e = False
            self.begin = event.pos()
            self.end = event.pos()

        self.update()

    def mouseMoveEvent(self, event):
        if self.moving_b:
            self.begin = event.pos()
        else:
            self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos() if not self.moving_b else self.end

        print(f"Point 1: {self.begin.x(), self.begin.y()}")
        print(f"Point 2 {self.end.x(), self.end.y()}")
        self.update()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_S) and (event.modifiers() == Qt.ControlModifier) and self.filename != None:
            new_info = {
                        self.filename : [
                            {
                                'begin' : [self.begin.x(), self.begin.y()],
                                'end'   : [self.end.x(), self.end.y()]
                            }
                        ]
                    }
            
            file = open('coordinates.json', 'r')
            file_str = file.read()
            file.close()

            if file_str:
                data = json.loads(file_str)
                if(self.filename not in data):
                    data.update(new_info)

                else:
                    data[self.filename] = new_info[self.filename]
                jsonString = json.dumps(data)

            else:
                jsonString = json.dumps(new_info)
            
            file = open('coordinates.json', 'w')
            file.write(jsonString)
            file.close()
            

            

                

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())




    
# class AppDemo(QWidget):
#     def __init__(self) -> None:
#         super().__init__()
#         self.resize(1920, 1080)
#         self.setAcceptDrops(True)

#         self.points = []

#         self.file_path = None
#         self.mouse_pos = None
#         self.clicked = 0
#         self.focus = 0
#         self.double_click = [0, None]
#         self.circle_size = 10

#         alert = QMessageBox()
#         alert.setText('Drag and drop a photo to start')
#         alert.exec()

#         self.mainLayout = QVBoxLayout()
#         self.image = None

#         self.setLayout(self.mainLayout)
#         self.showMaximized()

    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasImage:
    #         event.accept()
    #     else:
    #         event.ignore()
        
    # def dragMoveEvent(self, event):
    #     if event.mimeData().hasImage:
    #         event.accept()
    #     else:
    #         event.ignore()

    # def dropEvent(self, event):
    #     if event.mimeData().hasImage:
    #         event.setDropAction(Qt.CopyAction)
    #         self.image = QImage(event.mimeData().urls()[0].toLocalFile())
    #         self.update()
    #         event.accept()
    #     else:
    #         event.ignore()

#     def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
#         print('CLICK')
#         self.focus = 0
#         pos = event.pos()
#         if(event.button() == Qt.LeftButton):
#             for i in self.points:
#                 if i.x()-self.circle_size <= pos.x() < i.x()+self.circle_size and i.y()-self.circle_size <= pos.y() < i.y()+self.circle_size:
#                     self.focus = 1
#                     break

#             if not self.focus:
#                 self.clicked = 1
#                 if len(self.points) < 2 : self.points.append(pos)

#         self.update()
#         return super().mousePressEvent(event)

#     def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
#         print('DOUBLE CLICK')
#         pos = event.pos()
#         if(event.button() == Qt.LeftButton):
#             for i in self.points:
#                 if i.x()-self.circle_size <= pos.x() < i.x()+self.circle_size and i.y()-self.circle_size <= pos.y() < i.y()+self.circle_size:
#                     self.double_click = [1, i] 
#                     self.focus = 0
#                     break
            

#         return super().mouseDoubleClickEvent(event)

#     def paintEvent(self, event):
#         painter = QPainter(self)

#         if self.image != None:
#             painter.drawImage(0, 0, self.image)

        
#         if self.double_click[0] and self.focus:
#             print('double click detected\n\n')
#             self.clicked = 0
#             painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
#             painter.setBrush(QBrush(Qt.red))
            
#             self.points.pop(self.points.index(self.double_click[1]))
#             self.points.append(self.double_click[1])

#             for i in self.points:
#                 painter.drawEllipse(i, self.circle_size, self.circle_size)   

                     

#         if self.clicked:
#             print('click detected\n\n')
#             painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
#             painter.setBrush(QBrush(Qt.red))

#             for i in self.points:
#                 painter.drawEllipse(i, self.circle_size, self.circle_size)
           
#             self.clicked = 0
#             self.double_click = [0, None]
        
            

#         if len(self.points) == 2:
#             painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
#             painter.setBrush(Qt.NoBrush)

#             painter.drawRect(self.points[0].x(), self.points[0].y(), self.points[1].x()-self.points[0].x(), self.points[1].y()-self.points[0].y())


#         painter.end()
        







# app = QApplication([])

# demo = AppDemo()
# demo.show()

# app.exec_()


# import sys


# class MouseTracker(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#         self.setMouseTracking(True)

#     def initUI(self):
#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle('Mouse Tracker')
#         self.label = QLabel(self)
#         self.label.resize(200, 40)
#         self.show()

#     def eventFilter(self, source, event):

#         return super().eventFilter(source, event)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MouseTracker()
#     sys.exit(app.exec_())