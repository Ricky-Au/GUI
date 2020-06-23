# ---------------------------------------------------------------------------------
#    GUI prototype
# 
# A script to save data created from the program sending the data to text file 
# and test the functionality of multiple different windows under one main gui.

#    Written by: Ricky Au
# ---------------------------------------------------------------------------------
#    Version:    7
#    By:         Ricky Au
#    Notes:      Added read from previous save file using Regular expressions (Regex)
#                Added more nicer layout and tool tip to main window
#                
# ---------------------------------------------------------------------------------
#    Version:    6 - May 28, 2020
#    By:         Ricky Au
#    Notes:      Added input line to allow user to input data
#                Added restriction to input line to only take in numbers
#                Added refresh button to increment screen to allow user to see edit they make
#                Added reset button to set number to 0
#                
# ---------------------------------------------------------------------------------
#    Version:    5 - May 22, 2020
#    By:         Ricky Au
#    Notes:      Added better version of Increment window where user can see real
#                time number changes when user presses increment button
# ---------------------------------------------------------------------------------
#    Version:    4 - 
#    By:         Ricky Au
#    Notes:      Added the ability to send number from increment window to txt file 
#                
# ---------------------------------------------------------------------------------
#    Version:    3 - 
#    By:         Ricky Au
#    Notes:      Modified code to be more dynamic allowing seperate user functions
#                to not be tied together
#                
# ---------------------------------------------------------------------------------
#    Version:    2 -
#    By:         Ricky Au
#    Notes:      Created a secondary function that tests if program can handle 
#                multiple programs at the same time
#                
# ---------------------------------------------------------------------------------
#    Version:    1 - 
#    By:         Ricky Au
#    Notes:      Created a simple UI that links to one function the incrementor
#                Which increments the number when user presses the button
#                
# ---------------------------------------------------------------------------------

# import system and regex 
import sys, re
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QLabel, QGridLayout, QLineEdit, QMessageBox, QToolTip
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator, QFont


display_num = 0

# Main GUI that has buttons that connect to other functions
class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()


    def initUI(self):
        QWidget.__init__(self) 
        global display_num
        
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Main Window')

        layout = QGridLayout()

        QToolTip.setFont(QFont('SansSerif', 10))


        self.line_edit = QLineEdit() 
        self.onlyInt = QIntValidator()
        self.line_edit.setValidator(self.onlyInt)
        self.line_edit.setToolTip('Input number you want to start incrementor at')
        layout.addWidget(self.line_edit)
        

        self.lbtn = QPushButton('save inputed number', self)
        self.lbtn.clicked.connect(self.on_click_input)
        layout.addWidget(self.lbtn)        


        self.IncBtn = QPushButton('Increment-Window', self)
        self.IncBtn.clicked.connect(self.incrementWind)
        self.IncBtn.resize(self.IncBtn.sizeHint())
        layout.addWidget(self.IncBtn)


        self.mbtn = QPushButton('Multi-Window', self)
        self.mbtn.clicked.connect(self.show_child)
        self.children = []             # place to save child window references
        layout.addWidget(self.mbtn)


        self.qbtn = QPushButton('Close whole program', self)
        self.qbtn.clicked.connect(QApplication.instance().quit)
        self.qbtn.resize(self.qbtn.sizeHint())
        layout.addWidget(self.qbtn)

        self.setLayout(layout)

    def show_child(self):
        child = Child() 
        child.setWindowTitle('test if title works for child')
        child.show() 
        self.children.append(child)    # save new window ref in list

    def incrementWind(self):
        self.iWindow = Incrementor()
        self.iWindow.show()

    def on_click_input(self):
        global display_num
        if (self.line_edit.text() == ''):
            display_num = 0
        else:
            print(self.line_edit.text())
            display_num = int(self.line_edit.text())

    # currently only works on the main UI window when user presses the X on the top right of application
    def closeEvent(self,event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if (reply == QMessageBox.Yes):
            event.accept()
        else:
            event.ignore()
        
    
# Incrementor window class that allows the user to increment a number on the screen and then another button that
# saves the number into a seperate txt file
class Incrementor(QWidget):
    def __init__(self):
        super(Incrementor,self).__init__()
        self.show_Incrementor()

        
    def show_Incrementor(self):
        QWidget.__init__(self)
        print('show_inc')
        global display_num

        self.setGeometry(900, 300, 350, 350)
        self.setWindowTitle('Increment window title check')

        self.layout = QVBoxLayout()
        self.label = QLabel('press button to increment ')
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.addbtn = QPushButton('add 1 to number', self)

        self.num_label = QLabel(self)
        self.num_label.setText(str(display_num))

        self.addbtn.clicked.connect(lambda: self.on_click()) 
        self.addbtn.resize(self.addbtn.sizeHint())
        self.addbtn.move(0,50)

        self.textfilebtn = QPushButton('make text file of current number', self)
        self.textfilebtn.clicked.connect(lambda: self.on_click_new_txt_file())
        self.textfilebtn.resize(self.textfilebtn.sizeHint())
        self.textfilebtn.move(20,90)

        self.resetbtn = QPushButton('reset display number',self)
        self.resetbtn.clicked.connect(lambda: self.on_click_reset())
        self.resetbtn.resize(self.resetbtn.sizeHint())
        self.resetbtn.move(20,110)

        self.refreshbtn = QPushButton('refresh display number',self)
        self.refreshbtn.clicked.connect(lambda: self.on_click_refresh())
        self.refreshbtn.resize(self.refreshbtn.sizeHint())
        self.refreshbtn.move(20,140)

        self.readfilebtn = QPushButton('read previous save file', self)
        self.readfilebtn.clicked.connect(lambda: self.on_click_read_txt_file())
        self.readfilebtn.resize(self.readfilebtn.sizeHint())
        self.readfilebtn.move(20,200)


    @pyqtSlot()    
    def on_click(self):
        val = self.current_num()
        self.num_label.setText(str(val))
        self.num_label.adjustSize()

    def current_num(self):
        global display_num
        # print('add 1')
        display_num = display_num + 1
        # print(number)
        return display_num

    @pyqtSlot()   
    def on_click_new_txt_file(self):
        global display_num
        file = open("number.txt" , "w")
        file.write("number is " + str(display_num))
        print("file made")
        file.close()
    
    @pyqtSlot()
    def on_click_reset(self):
        global display_num
        display_num = 0
        self.num_label.setText(str(display_num))
        self.num_label.adjustSize()
    
    @pyqtSlot()
    def on_click_refresh(self):
        global display_num
        self.num_label.setText(str(display_num))
        self.num_label.adjustSize()

    @pyqtSlot()
    def on_click_read_txt_file(self):
        global display_num
        try:
            file = open("number.txt" , "r")
            text = file.read()
            number_list = re.findall(r"[-+]?\d*\.\d+|\d+", text)
            number = number_list[0]
            display_num = int(number)
            self.num_label.setText(str(display_num))
            self.num_label.adjustSize()
            file.close()
        except:
            print("no previous save data")

        


class Child(QWidget):
    def __init__(self):
        super().__init__()

class Controller:

    def __init__(self):
        pass

    def show_main(self):
        self.window = MainWindow()
        self.window.show()

    def show_increment(self):
        self.window_two = Incrementor()
        self.window_two.show()

def main():	
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

