from PyQt5.QtWidgets import QDialog,QPushButton,QLabel,QLineEdit

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

    def setUi(self,label,lineEdit,savebutton,defaultButton,CommentEdit,editCommentButton,saveCommentButton,defaultCommentButton):
        self.Plabel = label
        self.PlineEdit = lineEdit
        self.saveButton = savebutton
        self.defaultbutton = defaultButton
        self.commentLineEdit = CommentEdit
        self.editCommentButton = editCommentButton
        self.saveCommentButton = saveCommentButton
        self.defaulfCommentButton = defaultCommentButton
        self.buttonsSetup()
        
    def buttonsSetup(self):
        self.saveButton.clicked.connect(self.save)
        self.defaultbutton.clicked.connect(self.default)
        self.editCommentButton.clicked.connect(self.enableEdit)
        self.saveCommentButton.clicked.connect(self.saveComment)
        self.defaulfCommentButton.clicked.connect(self.SavedefaultComment)
    
    def save(self,allOrNot=False):
        self.currentValue = self.newValue
        self.newValue = self.PlineEdit.text()
        self.parentFile.ChangeParameter(self)
        if not allOrNot:
            self.parentFile.writeFile()
    
    def default(self,allOrNot=False):
        self.currentValue = self.newValue
        self.newValue = self.defaulfValue
        self.PlineEdit.setText(self.defaulfValue) 
        self.parentFile.ChangeParameter(self)
        if not allOrNot:
            self.parentFile.writeFile()
    
    def enableEdit(self):
        self.commentLineEdit.setEnabled(True)

    def saveComment(self,allOrNot=False):
        if self.commentLineEdit.isEnabled():
            self.currentComment = self.newComment
            self.newComment = self.commentLineEdit.text()
            self.parentFile.ChangeComment(self)
            if not allOrNot:
                self.parentFile.writeFile()

    def SavedefaultComment(self,allOrNot=False):
        if self.commentLineEdit.isEnabled():
            self.currentComment = self.newComment
            self.newComment = self.defaulfComment
            self.commentLineEdit.setText(self.defaulfComment) 
            self.parentFile.ChangeComment(self)
            if not allOrNot:
                self.parentFile.writeFile()
            
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
            parameter.save(True)
        self.dialog.verilogFile.writeFile()
    
    def defaultAllValues(self):
        for parameter in self.parameterList:
            parameter.default(True)
        self.dialog.verilogFile.writeFile()

    def editAllComments(self):
        for parameter in self.parameterList:
            parameter.enableEdit()

    def saveAllComments(self):
        for parameter in self.parameterList:
            parameter.saveComment(True)
        self.dialog.verilogFile.writeFile()

    def defaultAllComments(self):
        for parameter in self.parameterList:
            parameter.SavedefaultComment(True)
        self.dialog.verilogFile.writeFile()    
    
class ModuleInstance(Module):
    def __init__(self,name,moduleName):
        super().__init__(moduleName)
        self.instanceName = name

class TestBench():
    def __init__(self,name):
        self.TestBenchName = name
    
    def setInstanceList(self,instanceList):
        self.instanceList = instanceList


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
            testBenchInstances = verilogFile.testBench.instanceList
            for instance in testBenchInstances:
                instance.setupButtons(self.dialog)
                listOfParameters = instance.parameterList
                for parameter in listOfParameters:
                    self.setParameterButtons(parameter)
                    parameter.setFile(self.dialog.verilogFile)

    def setParameterButtons(self,parameter):
        label = QLabel(parameter.name,self.dialog)
        lineEdit = QLineEdit(parameter.defaulfValue,self.dialog)
        saveButton = QPushButton("Save",self.dialog)
        defaultButton = QPushButton("Default",self.dialog)
        commentEdit = QLineEdit(parameter.defaulfComment,self.dialog)
        commentEdit.setDisabled(True)
        commentEditButton = QPushButton("Edit",self.dialog)
        commentSaveButton = QPushButton("Save",self.dialog)
        commentDefaultButton = QPushButton("Default",self.dialog)
        parameter.setUi(label,lineEdit,saveButton,defaultButton,commentEdit,commentEditButton,commentSaveButton,commentDefaultButton)
    
    def buttonsSetup(self):
        self.saveAllButton = QPushButton("Save All",self.dialog)
        self.defaultAllButton = QPushButton("Default All",self.dialog)

        self.saveAllButton.clicked.connect(self.saveAll)
        self.defaultAllButton.clicked.connect(self.defaultAll)

    def saveAll(self):
        if self.dialog.verilogFile.moduleType == "testBench":
            for instance in self.dialog.verilogFile.testBench.instanceList:
                instance.saveAllValues()
                instance.saveAllComments()
        elif self.dialog.verilogFile.moduleType == "module":
            self.dialog.verilogFile.Module.saveAllValues()
            self.dialog.verilogFile.Module.saveAllComments()    

    def defaultAll(self):
        if self.dialog.verilogFile.moduleType == "testBench":
            for instance in self.dialog.verilogFile.testBench.instanceList:
                instance.defaultAllValues()
                instance.defaultAllComments()
        elif self.dialog.verilogFile.moduleType == "module":
            self.dialog.verilogFile.Module.defaultAllValues()
            self.dialog.verilogFile.Module.saveAllComments()   

    
    