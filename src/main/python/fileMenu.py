from CreateActions import CreateAction
from PyQt5.QtWidgets import QAction,QWidget,QFileDialog,QMessageBox
from verilogParser import Parser
from EditDialog import EditDialog
from VerilogFile import VerilogFile


class FileMenu():
    def __init__(self,widget,fileMenu):
        self.parent = widget
        self.fileMenu = fileMenu
        self.create_Actions()
        self.adjust_fileMenu()
        
    def create_Actions(self):
        actions = CreateAction()
        self.openFile = actions.create("&Open File",self.parent,"Ctrl+O",'Open File')
        self.openFile.triggered.connect(self.parent.file_open)
 
    def adjust_fileMenu(self):
        self.fileMenu.addAction(self.openFile)            