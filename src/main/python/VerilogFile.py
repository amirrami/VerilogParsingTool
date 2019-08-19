from PyQt5.QtWidgets import QMessageBox
from verilogParser import Parser
from EditDialog import EditDialog,Parameter,ParametersList
import re

class VerilogFile():
    def __init__(self,file):
        self.VFile = file
        self.verilogLines = []
        self.verilogParameters = []
        self.parametersLineIndexes = []
        self.commentsList = []
        self.readAndParse()

    def readAndParse(self):
        print(self.VFile , "\tOpened")
        self.verilogLines = self.VFile.readlines()
        self.VFile.close()
        self.parser = Parser(self.verilogLines)
        self.verilogParameters , self.parametersLineIndexes,self.commentsList = self.parser.parserOutput()
        self.openDialog()
        
    def openDialog(self):
        self.fileEditDialog = EditDialog(self)
        self.fileEditDialog.show()

    def ChangeParameter(self,parameter):
        editedLine = self.verilogLines[parameter.lineIndex]
        editedLine = editedLine.replace(parameter.currentValue,parameter.newValue)
        self.verilogLines[parameter.lineIndex] = editedLine

    def ChangeComment(self,parameter):
        if parameter.newComment == "" and parameter.currentComment == "":
            match = re.search(r'//',self.verilogLines[parameter.lineIndex])
            if match:
                editedLine = self.verilogLines[parameter.lineIndex]
                editedLine = editedLine.replace("//","")
                self.verilogLines[parameter.lineIndex] = editedLine
        elif parameter.newComment == "":
            self.verilogLines[parameter.lineIndex] = re.sub(r'\s*(//*)(\s*).*',"",self.verilogLines[parameter.lineIndex])
        elif parameter.currentComment == "":
            match = re.search(r'//',self.verilogLines[parameter.lineIndex])
            if match:
                editedLine = self.verilogLines[parameter.lineIndex]
                if parameter.newComment == "":
                    editedLine = editedLine.replace("//","")
                else:
                    editedLine = editedLine.replace("//","//"+parameter.newComment)
                self.verilogLines[parameter.lineIndex] = editedLine
            else:
                editedLine = self.verilogLines[parameter.lineIndex]
                editedLine = editedLine.replace("\n"," //"+parameter.newComment+"\n")
                self.verilogLines[parameter.lineIndex] = editedLine
        else:
            editedLine = self.verilogLines[parameter.lineIndex]
            editedLine = editedLine.replace(parameter.currentComment,parameter.newComment)
            self.verilogLines[parameter.lineIndex] = editedLine

    def writeFile(self):
        self.VFile = open(self.VFile.name,'w')
        self.VFile.writelines(self.verilogLines)
        self.VFile.flush()