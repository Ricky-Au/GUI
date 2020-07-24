import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(800, 400)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw_graph()

    def draw_graph(self):
        painter = QtGui.QPainter(self.label.pixmap())
        # initialize instance of pen for axis
        axis = QtGui.QPen()
        axis.setColor(QtGui.QColor('white'))
        painter.setPen(axis)
        painter.setOpacity(1)
        # draw x axis
        painter.drawLine(50, 350, 750, 350)
        # draw y axis
        painter.drawLine(50, 10, 50, 350)

        # draw opacity tick marker
        tick = QtGui.QPen()
        tick.setColor(QtGui.QColor('white'))
        painter.setPen(tick)
        painter.setOpacity(0.25)
        painter.drawLine(650, 10, 650, 350)
        painter.drawLine(550, 10, 550, 350)
        painter.drawLine(450, 10, 450, 350)
        painter.drawLine(350, 10, 350, 350)
        painter.drawLine(250, 10, 250, 350)
        painter.drawLine(150, 10, 150, 350)
        
        # draw text
        x_label = QtGui.QPen()
        x_label.setColor(QtGui.QColor('white'))
        painter.setPen(x_label)
        painter.setOpacity(1)
        font = QtGui.QFont()

        # font.setFamily('Times')
        # font.setBold(True)
        font.setPointSize(10)
        painter.setFont(font)

        painter.drawText(650, 360, '0')
        painter.drawText(550, 360, '-10')
        painter.drawText(450, 360, '-20')
        painter.drawText(350, 360, '-30')
        painter.drawText(250, 360, '-40')
        painter.drawText(150, 360, '-50')
        painter.drawText(50, 360, '-60')


        painter.end()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()