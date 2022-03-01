import sys, os


from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# def on_button_clicked():
#     alert = QMessageBox()
#     alert.setText('You clicked the button!')
#     alert.exec()


######################
# app = QApplication([])

# title = "Bounding App"

# screen_dim = (1600, 900)

# width = 650
# height = 400

# left = int(screen_dim[0]/2 - width/2)
# top = int(screen_dim[1]/2 - height/2)

# ###
# b1 = QPushButton("test 1")
# b2 = QPushButton("test 2")
# ###

# window = QWidget() 
# layout = QVBoxLayout()

# layout.addWidget(b1)
# layout.addWidget(b2)

# b1.clicked.connect(on_button_clicked)

# window.setLayout(layout)
# window.show()

# window.setWindowTitle(title)
# window.setGeometry( left,  top,  width,  height)

# app.exec_()
######################



class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setFont(QFont('Arial', 20))
    
    def setPixmap(self, image):
        super().setPixmap(image)

    
class AppDemo(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1920, 1080)
        self.setAcceptDrops(True)

        self.points = []

        self.file_path = None
        self.mouse_pos = None
        self.clicked = 0
        self.focus = 0
        self.double_click = [0, None]
        self.circle_size = 10

        alert = QMessageBox()
        alert.setText('Drag and drop a photo to start')
        alert.exec()

        self.mainLayout = QVBoxLayout()
        self.image = None

        self.setLayout(self.mainLayout)
        self.showMaximized()

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
            self.image = QImage(event.mimeData().urls()[0].toLocalFile())
            self.update()
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        print('CLICK')
        self.focus = 0
        pos = event.pos()
        if(event.button() == Qt.LeftButton):
            for i in self.points:
                if i.x()-self.circle_size <= pos.x() < i.x()+self.circle_size and i.y()-self.circle_size <= pos.y() < i.y()+self.circle_size:
                    self.focus = 1
                    break

            if not self.focus:
                self.clicked = 1
                if len(self.points) < 2 : self.points.append(pos)

        self.update()
        return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        print('DOUBLE CLICK')
        pos = event.pos()
        if(event.button() == Qt.LeftButton):
            for i in self.points:
                if i.x()-self.circle_size <= pos.x() < i.x()+self.circle_size and i.y()-self.circle_size <= pos.y() < i.y()+self.circle_size:
                    self.double_click = [1, i] 
                    self.focus = 0
                    break
            

        return super().mouseDoubleClickEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.image != None:
            painter.drawImage(0, 0, self.image)

        
        if self.double_click[0] and self.focus:
            print('double click detected\n\n')
            self.clicked = 0
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.red))
            
            self.points.pop(self.points.index(self.double_click[1]))
            self.points.append(self.double_click[1])

            for i in self.points:
                painter.drawEllipse(i, self.circle_size, self.circle_size)   

                     

        if self.clicked:
            print('click detected\n\n')
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.red))

            for i in self.points:
                painter.drawEllipse(i, self.circle_size, self.circle_size)
           
            self.clicked = 0
            self.double_click = [0, None]
        
            

        if len(self.points) == 2:
            painter.setPen(QPen(Qt.black,  5, Qt.SolidLine))
            painter.setBrush(Qt.NoBrush)

            painter.drawRect(self.points[0].x(), self.points[0].y(), self.points[1].x()-self.points[0].x(), self.points[1].y()-self.points[0].y())


        painter.end()
        







app = QApplication([])

demo = AppDemo()
demo.show()

app.exec_()


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