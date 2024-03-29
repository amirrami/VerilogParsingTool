from PyQt5.QtWidgets import QMessageBox
from verilogParser import Parser
from EditDialog import EditDialog,Parameter
import re,platform,sys,subprocess,os


class VerilogFile():
    def __init__(self,file,mainWindow):
        self.VFile = file
        self.includeFile = ""
        self.verilogLines = []
        self.verilogText = ""
        self._fileEdited = False
        self._includeFileEdited = False
        self.parent = mainWindow
        self.readAndParse()


    def readAndParse(self):
        self.verilogLines = self.VFile.readlines()
        self.VFile = open(self.VFile.name,'r')
        self.verilogText = self.VFile.read()
        self.VFile.close()
        self.parser = Parser(self.verilogLines,self.verilogText)
        includeFilePath = self.parser.getIncludeFile()
        if includeFilePath:
            self.openIncludeFile(includeFilePath)
        self.parser.startParsing()
        self.moduleType = self.parser.getModuleType()
        if self.moduleType == "module":
            self.Module = self.parser.getModule()
        elif self.moduleType == "testBench":
            self.testBench = self.parser.gettestBench()
        self.openDialog()
        
    def openDialog(self):
        self.fileEditDialog = EditDialog(self)
        self.fileEditDialog.show()

    def ChangeParameter(self,parameter):
        if parameter.currentValue != parameter.newValue:
            if parameter.isInInclude:
                self._includeFileEdited = True
                editedLine = self.includeFileLines[parameter.lineIndex]
                editedLine = editedLine.replace(parameter.currentValue,parameter.newValue,1)
                self.includeFileLines[parameter.lineIndex] = editedLine
            else:
                self._fileEdited = True
                editedLine = self.verilogLines[parameter.lineIndex]
                editedLine = editedLine.replace(parameter.currentValue,parameter.newValue,1)
                self.verilogLines[parameter.lineIndex] = editedLine
            self.checkParameterSimilarity(parameter)
        
# code to match if two parameters inside diffrent instances have the same parameter in testBench
    def checkParameterSimilarity(self,parameter):
        if self.moduleType == "testBench":
            for instance in self.testBench.instanceList:
                for param in instance.parameterList:
                    self.checks(param,parameter)
        elif self.moduleType == "module":
            for param in self.Module.parameterList:
                self.checks(param,parameter)
                        
    
    def checks(self,param,parameter):
        if parameter != param:
            if (parameter.isInInclude and param.isInInclude) or (not parameter.isInInclude and not param.isInInclude) :
                if parameter.lineIndex == param.lineIndex:
                    param.currentValue = param.newValue
                    param.newValue = parameter.newValue
                    param.PlineEdit.setText(parameter.newValue)
                    param.currentComment = param.newComment
                    param.newComment = parameter.newComment
                    param.commentLineEdit.setText(parameter.newComment)


    def ChangeComment(self,parameter):
        if parameter.newComment != parameter.currentComment:
            if parameter.isInInclude:
                self._includeFileEdited = True
                editedLine = self.includeFileLines[parameter.lineIndex]
            else:
                self._fileEdited = True
                editedLine = self.verilogLines[parameter.lineIndex]
            if parameter.newComment == "" and parameter.currentComment == "":
                match = re.search(r'//',editedLine)
                if match:
                    editedLine = editedLine.replace("//","",1)
            elif parameter.newComment == "":
                editedLine = re.sub(r'\s*(//*)(\s*).*',"",editedLine,1)
            elif parameter.currentComment == "":
                match = re.search(r'//',editedLine)
                if match:
                    if parameter.newComment == "":
                        editedLine = editedLine.replace("//","",1)
                    else:
                        editedLine = editedLine.replace("//","//"+parameter.newComment,1)
                else:
                    editedLine = editedLine.replace("\n"," //"+parameter.newComment+"\n",1)
            else:
                editedLine = re.sub(parameter.currentComment,parameter.newComment,editedLine,1)
            if parameter.isInInclude:
                self.includeFileLines[parameter.lineIndex] = editedLine
            else:
                self.verilogLines[parameter.lineIndex] = editedLine
            self.checkParameterSimilarity(parameter)

    def writeFile(self):
        if self.includeFile and self._includeFileEdited:
            self._includeFileEdited = False
            self.includeFile = open(self.includeFile.name,'w')
            self.includeFile.writelines(self.includeFileLines)
            self.includeFile.flush()
        if self._fileEdited:
            self._fileEdited = False
            self.VFile = open(self.VFile.name,'w')
            self.VFile.writelines(self.verilogLines)
            self.VFile.flush()
    
    def openIncludeFile(self,includeFilePath):
        try:
            self.includeFile = open(includeFilePath,"r")
            self.includeFileLines = self.includeFile.readlines()
            self.parser.setIncludeFileLines(self.includeFileLines)
        except:
            QMessageBox.information(self.parent,"Include File Not Found","The Include File Is Not In The Path specified!!")
        
            
            
        
    def changeMode(self,mode):
        if mode.isDefinednew != mode.isDefinedcurrent:
            if mode.lineIndex!=None and not mode.isDefinednew:
                self.verilogLines.pop(mode.lineIndex)
                self.changeLineIndexes(False,mode.lineIndex)
                mode.lineIndex = None
                self._fileEdited = True
            elif mode.lineIndex == None:
                self.verilogLines.insert(0,"`define "+mode.modeName + "\n")
                self.changeLineIndexes(True,0)
                mode.lineIndex = 0
                self._fileEdited = True
            ##to change instance module if its name contain a ifdef condition
            self.parser.setVerilogLines(self.verilogLines)
            for instance in self.testBench.instanceList:
                if instance.falseName:
                    trueName = self.parser.instanceNameCorrection(instance.falseName)
                    instance.moduleName = trueName
                    instance.groupBox.setTitle("Instance "+instance.instanceName+" Of Module "+instance.moduleName)

    def changeLineIndexes(self,isAdded,changedIndex):
        if self.moduleType == "testBench":
            for instance in self.testBench.instanceList:
                for parameter in instance.parameterList:
                    if isAdded:
                        parameter.lineIndex +=1
                    else:
                        if parameter.lineIndex > changedIndex:
                            parameter.lineIndex -=1
            for mode in self.testBench.modesList:
                if mode.lineIndex!=None:
                    if isAdded:
                        mode.lineIndex +=1
                    else:
                        if mode.lineIndex > changedIndex:
                            mode.lineIndex -=1



    def linux_distribution(self):
        try:
            return platform.linux_distribution()
        except:
            return "N/A"

    def compileFile(self):
        dir_path = os.path.dirname(os.path.realpath(self.VFile.name))
        if dir_path != "":
            os.chdir(dir_path)
        compileCommand = "vlog "
        files = os.listdir()
        for file in files:
            if file.endswith(".sv") or file.endswith(".v"):
                compileCommand += file+ " "
        compileCommand = compileCommand.rstrip()
        print(compileCommand)
        if platform.system() == "Windows":
            os.system("start \"\" cmd /k \""+compileCommand)
        else:
            os.system(compileCommand)


    def runFile(self):
        dir_path = os.path.dirname(os.path.realpath(self.VFile.name))
        if dir_path != "":
            os.chdir(dir_path)
        runCommand = "vsim work." +os.path.basename(self.VFile.name)
        if platform.system() == "Windows":
            os.system("start \"\" cmd /k \""+runCommand)
        else:
            os.system(runCommand)
        