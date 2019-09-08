from PyQt5.QtWidgets import QDialog,QPushButton,QLabel,QLineEdit,QCheckBox

class Parameter():
    def __init__(self,name):
        self.name = name
        self.isInInclude = False
        self.defaulfComment = ""
        self.newComment = ""
        self.currentComment = ""

    def setName(self,name):
        self.name = name
        
    def setValue(self,value):
        self.defaulfValue = value
        self.newValue = value
        self.currentValue = value
    
    def setLineIndex(self,index):
        self.lineIndex = index

    def setComment(self,comment):
        self.defaulfComment = comment
        self.newComment = comment
        self.currentComment = comment
    
    def setFile(self,file):
        self.parentFile = file

    def setInInclude(self,inInclude=False):
        self.isInInclude = inInclude

    def setUi(self,label,lineEdit,defaultButton,CommentEdit,editCommentButton,defaultCommentButton):
        self.Plabel = label
        self.PlineEdit = lineEdit
        self.defaultbutton = defaultButton
        self.commentLineEdit = CommentEdit
        self.editCommentButton = editCommentButton
        self.defaulfCommentButton = defaultCommentButton
        self.buttonsSetup()
        
    def buttonsSetup(self):
        self.defaultbutton.clicked.connect(self.default)
        self.editCommentButton.clicked.connect(self.enableEdit)
        self.defaulfCommentButton.clicked.connect(self.SavedefaultComment)
    
    def save(self):
        self.currentValue = self.newValue
        self.newValue = self.PlineEdit.text()
        self.parentFile.ChangeParameter(self)

    def default(self):
        self.currentValue = self.newValue
        self.newValue = self.defaulfValue
        self.PlineEdit.setText(self.defaulfValue) 
        self.parentFile.ChangeParameter(self)
        
    def enableEdit(self):
        self.commentLineEdit.setEnabled(True)

    def saveComment(self):
        if self.commentLineEdit.isEnabled():
            self.currentComment = self.newComment
            self.newComment = self.commentLineEdit.text()
            self.parentFile.ChangeComment(self)

    def SavedefaultComment(self):
        if self.commentLineEdit.isEnabled():
            self.currentComment = self.newComment
            self.newComment = self.defaulfComment
            self.commentLineEdit.setText(self.defaulfComment) 
            self.parentFile.ChangeComment(self)

            
class Module():
    def __init__(self,name):
        self.moduleName = name

    def setParametersList(self,parametersList):
        self.parameterList = parametersList


    def setupButtons(self,dialog):
        self.dialog = dialog
        self.saveAllValueButton = QPushButton("Save All",self.dialog)
        self.defaultAllValueButton = QPushButton("Default All",self.dialog)
        self.editAllCommentsButton = QPushButton("Edit All",self.dialog)
        self.saveAllCommentsButton = QPushButton("Save All",self.dialog)
        self.defaultAllCommentButton = QPushButton("Default All",self.dialog)
        self.saveAllValueButton.clicked.connect(self.saveAllValues)
        self.defaultAllValueButton.clicked.connect(self.defaultAllValues)
        self.editAllCommentsButton.clicked.connect(self.editAllComments)
        self.saveAllCommentsButton.clicked.connect(self.saveAllComments)
        self.defaultAllCommentButton.clicked.connect(self.defaultAllComments)


    def saveAllValues(self):
        for parameter in self.parameterList:
            parameter.save()
    
    def defaultAllValues(self):
        for parameter in self.parameterList:
            parameter.default()

    def editAllComments(self):
        for parameter in self.parameterList:
            parameter.enableEdit()

    def saveAllComments(self):
        for parameter in self.parameterList:
            parameter.saveComment()

    def defaultAllComments(self):
        for parameter in self.parameterList:
            parameter.SavedefaultComment()
    
    def setGroupBox(self,groupbox):
        self.groupBox = groupbox
    
class ModuleInstance(Module):
    def __init__(self,name,moduleName):
        super().__init__(moduleName)
        self.instanceName = name
        self.falseName = ""
    
    def setFalseName(self,falseName):
        self.falseName = falseName

class TestBench():
    def __init__(self,name):
        self.TestBenchName = name
    
    def setInstanceList(self,instanceList):
        self.instanceList = instanceList
    
    def setModesList(self,modesList):
        self.modesList = modesList

    def setupModesButtons(self,dialog):
        self.dialog = dialog
        self.saveAllModesButton = QPushButton("Save All",self.dialog)
        self.defaultAllModesButton = QPushButton("Default All",self.dialog)
        self.checkAllButton = QPushButton("Check All",self.dialog)
        self.unCheckAllButton = QPushButton("Uncheck All",self.dialog)
        
        self.saveAllModesButton.clicked.connect(self.saveAllModes)
        self.defaultAllModesButton.clicked.connect(self.defaultAllModes)
        self.checkAllButton.clicked.connect(self.checkAllModes)
        self.unCheckAllButton.clicked.connect(self.unCheckAllModes)

        self.saveAllModesButton.setMinimumHeight(30)
        self.defaultAllModesButton.setMinimumHeight(30)
        self.checkAllButton.setMinimumHeight(30)
        self.unCheckAllButton.setMinimumHeight(30)
    
    def saveAllModes(self):
        for mode in self.modesList:
            mode.saveMode()
        self.dialog.verilogFile.writeFile()
    
    def defaultAllModes(self):
        for mode in self.modesList:
            mode.defaultMode()
        self.dialog.verilogFile.writeFile()
    
    def checkAllModes(self):
        for mode in self.modesList:
            mode.checkMode()
    
    def unCheckAllModes(self):
        for mode in self.modesList:
            mode.unCheckMode()
        

class ModulsExtractor():
    def __init__(self,dialog):
        self.dialog = dialog
        self.buttonsSetup()
        verilogFile = self.dialog.verilogFile
        if verilogFile.moduleType == "module":
            verilogFile.Module.setupButtons(self.dialog)
            moduleParameters = verilogFile.Module.parameterList
            for parameter in moduleParameters:
                self.setParameterButtons(parameter)
                parameter.setFile(self.dialog.verilogFile)
        elif verilogFile.moduleType == "testBench":
            verilogFile.testBench.setupModesButtons(self.dialog)
            testBenchInstances = verilogFile.testBench.instanceList
            for instance in testBenchInstances:
                instance.setupButtons(self.dialog)
                listOfParameters = instance.parameterList
                for parameter in listOfParameters:
                    self.setParameterButtons(parameter)
                    parameter.setFile(self.dialog.verilogFile)
            for mode in verilogFile.testBench.modesList:
                mode.setModeUi(self.dialog)
                mode.setFile(verilogFile)


    def setParameterButtons(self,parameter):
        label = QLabel(parameter.name,self.dialog)
        lineEdit = QLineEdit(parameter.defaulfValue,self.dialog)
        defaultButton = QPushButton("Default",self.dialog)
        commentEdit = QLineEdit(parameter.defaulfComment,self.dialog)
        commentEdit.setDisabled(True)
        commentEditButton = QPushButton("Edit",self.dialog)
        commentDefaultButton = QPushButton("Default",self.dialog)
        parameter.setUi(label,lineEdit,defaultButton,commentEdit,commentEditButton,commentDefaultButton)
    
    def buttonsSetup(self):
        self.saveAllButton = QPushButton("Save All",self.dialog)
        self.defaultAllButton = QPushButton("Default All",self.dialog)
        self.compileButton = QPushButton("Compile",self.dialog)
        self.RunButton = QPushButton("Run",self.dialog)
        self.saveAllButton.setMinimumHeight(50)
        self.defaultAllButton.setMinimumHeight(50)
        self.compileButton.setMinimumHeight(50)
        self.RunButton.setMinimumHeight(50)
        self.saveAllButton.setMinimumWidth(600)
        self.defaultAllButton.setMinimumWidth(600)
        self.compileButton.setMinimumWidth(600)
        self.RunButton.setMinimumWidth(600)
        self.saveAllButton.clicked.connect(self.saveAll)
        self.defaultAllButton.clicked.connect(self.defaultAll)
        self.compileButton.clicked.connect(self.dialog.verilogFile.compileFile)
        self.RunButton.clicked.connect(self.dialog.verilogFile.runFile)

    def saveAll(self):
        if self.dialog.verilogFile.moduleType == "testBench":
            for instance in self.dialog.verilogFile.testBench.instanceList:
                instance.saveAllValues()
                instance.saveAllComments()
            for mode in self.dialog.verilogFile.testBench.modesList:
                mode.saveMode()
        elif self.dialog.verilogFile.moduleType == "module":
            self.dialog.verilogFile.Module.saveAllValues()
            self.dialog.verilogFile.Module.saveAllComments()
        self.dialog.verilogFile.writeFile()

    def defaultAll(self):
        if self.dialog.verilogFile.moduleType == "testBench":
            for instance in self.dialog.verilogFile.testBench.instanceList:
                instance.defaultAllValues()
                instance.defaultAllComments()
            for mode in self.dialog.verilogFile.testBench.modesList:
                mode.defaultMode()
        elif self.dialog.verilogFile.moduleType == "module":
            self.dialog.verilogFile.Module.defaultAllValues()
            self.dialog.verilogFile.Module.saveAllComments()
        self.dialog.verilogFile.writeFile()   

class Mode():
    def __init__(self,name):
        self.modeName = name
        self.isDefinednew = False
        self.isDefinedcurrent = False
        self.isDefineddefault = False
        self.lineIndex = None

    def setFile(self,file):
        self.parentFile = file

    def setIsDefined(self,isDefined):
        self.isDefinednew = isDefined
        self.isDefinedcurrent = isDefined
        self.isDefineddefault = isDefined

    def setlineIndex(self,lineIndex):
        if self.isDefinednew:
            self.lineIndex = lineIndex
        else:
            self.lineIndex = None
    
    def setModeUi(self,dialog):
        self.checkBox = QCheckBox(self.modeName,dialog)
        self.checkBox.setChecked(self.isDefineddefault)    

    def saveMode(self):
        self.isDefinedcurrent = self.isDefinednew
        self.isDefinednew = self.checkBox.isChecked()
        self.parentFile.changeMode(self)

    def defaultMode(self):
        self.isDefinedcurrent = self.isDefinednew
        self.isDefinednew = self.isDefineddefault
        self.checkBox.setChecked(self.isDefineddefault)
        self.parentFile.changeMode(self)

    def checkMode(self):
        self.checkBox.setChecked(True)

    def unCheckMode(self):
        self.checkBox.setChecked(False)

    