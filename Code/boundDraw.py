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
        self.file_path = None

        self.mainLayout = QVBoxLayout()

        self.photoViewer = ImageLabel()
        self.mainLayout.addWidget(self.photoViewer)

        self.setLayout(self.mainLayout)
        self.showMaximized()

    def loadButton(self):
        self.__init__()



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
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image()

            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if(event.button() == Qt.LeftButton):
            print("YES FFINALLY")
        return super().mousePressEvent(event)

    def set_image(self):
        self.photoViewer.setPixmap(QPixmap(self.file_path))
        self.photoViewer.setScaledContents(True)
        self.photoViewer.setSizePolicy( QSizePolicy.Ignored, QSizePolicy.Ignored )


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