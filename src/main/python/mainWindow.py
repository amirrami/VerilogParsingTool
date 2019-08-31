from PyQt5.QtWidgets import QMainWindow,QVBoxLayout,QHBoxLayout,QGroupBox,QPushButton,QWidget,QAction
from PyQt5.QtWidgets import QMessageBox,QLabel,QLineEdit
from PyQt5.QtWidgets import QFileDialog,QTextEdit,QFormLayout
from PyQt5 import QtCore,QtGui
import sys
from fileMenu import FileMenu
from EditDialog import EditDialog
from VerilogFile import VerilogFile

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 400
        self.width = 300
        self.height = 150
        self.title = "Verilog Parsing Tool"
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.mainMenu = self.menuBar()
        self.fileMenu = FileMenu(self,self.mainMenu.addMenu('&File'))
        self.set_Interface()
        self.verilogFilesList = []
        
    def set_Interface(self):
        openFileButton = QPushButton("Open File",self)
        openFileButton.setMinimumHeight(60)
        openFileButton.clicked.connect(self.file_open)
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(openFileButton)
        groupBox = QGroupBox("Please Browse a Verilog File:")
        groupBox.setLayout(horizontalLayout)
        virticalLayout = QVBoxLayout()
        virticalLayout.addWidget(groupBox)
        widget = QWidget()
        widget.setLayout(virticalLayout)
        self.setCentralWidget(widget)



    def file_open(self):
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getOpenFileName(self,"Verilog file", "","Verilog Files (*.v *.sv)", options=options)
        #if fileName:
            try:
                VFile = open("/home/amir/Downloads/work/MentorIntern/VerilogParsingTool/testCases/addsub.sv",'r')
            except IOError:
                QMessageBox.warning(self, 'Can Not Open File', "Please Make Sure The the File Is Not Corrupted!!")
            else:
                vfileObject = VerilogFile(VFile)
                self.verilogFilesList.append(vfileObject)