from PyQt5.QtWidgets import QDialog,QPushButton,QLabel,QLineEdit


class Parameter():
    def __init__(self,label,lineEdit,savebutton,defaultButton,index,vfile,CommentEdit,
                editCommentButton,saveCommentButton,defaultCommentButton):
        self.Plabel = label
        self.name = label.text()
        self.PlineEdit = lineEdit
        self.defaulfValue = lineEdit.text()
        self.newValue = lineEdit.text()
        self.currentValue = lineEdit.text()
        self.saveButton = savebutton
        self.defaultbutton = defaultButton
        self.lineIndex = index
        self.parentFile = vfile
        self.commentLineEdit = CommentEdit
        self.defaulfComment = self.commentLineEdit.text()
        self.newComment = self.commentLineEdit.text()
        self.currentComment = self.commentLineEdit.text()
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
            

class ParametersList():
    def __init__(self,parameters,lineIndexes,commentsList,dialog):
        self._listOfParameters = []
        self.dialog = dialog
        self.setupButtons()
        numParameters = len(parameters)
        for index in range(numParameters):
            for key in parameters[index]:
                label = QLabel(key,dialog)
                lineEdit = QLineEdit(parameters[index][key],dialog)
                saveButton = QPushButton("Save",dialog)
                defaultButton = QPushButton("Default",dialog)
                commentEdit = QLineEdit(commentsList[index],dialog)
                commentEdit.setDisabled(True)
                commentEditButton = QPushButton("Edit",dialog)
                commentSaveButton = QPushButton("Save",dialog)
                commentDefaultButton = QPushButton("Default",dialog)
                parameter = Parameter(label,lineEdit,saveButton,defaultButton,
                            lineIndexes[index],dialog.verilogFile,commentEdit,
                            commentEditButton,commentSaveButton,commentDefaultButton)
                self._listOfParameters.append(parameter)

    def setupButtons(self):
        self.saveAllButton = QPushButton("Save All",self.dialog)
        self.defaultAllButton = QPushButton("Default All",self.dialog)
        self.saveAllValueButton = QPushButton("Save All",self.dialog)
        self.defaultAllValueButton = QPushButton("Default All",self.dialog)
        self.editAllCommentsButton = QPushButton("Edit All",self.dialog)
        self.saveAllCommentsButton = QPushButton("Save All",self.dialog)
        self.defaultAllCommentButton = QPushButton("Default All",self.dialog)

        self.saveAllButton.clicked.connect(self.saveAll)
        self.defaultAllButton.clicked.connect(self.defaultAll)
        self.saveAllValueButton.clicked.connect(self.saveAllValues)
        self.defaultAllValueButton.clicked.connect(self.defaultAllValues)
        self.editAllCommentsButton.clicked.connect(self.editAllComments)
        self.saveAllCommentsButton.clicked.connect(self.saveAllComments)
        self.defaultAllCommentButton.clicked.connect(self.defaultAllComments)

        
    def getList(self):
        return self._listOfParameters

    def saveAll(self):
        for parameter in self._listOfParameters:
            parameter.save(True)
            parameter.saveComment(True)
        self.dialog.verilogFile.writeFile()

    def defaultAll(self):
        for parameter in self._listOfParameters:
            parameter.default(True)
            parameter.SavedefaultComment(True)
        self.dialog.verilogFile.writeFile()
    
    def saveAllValues(self):
        for parameter in self._listOfParameters:
            parameter.save(True)
        self.dialog.verilogFile.writeFile()
    
    def defaultAllValues(self):
        for parameter in self._listOfParameters:
            parameter.default(True)
        self.dialog.verilogFile.writeFile()

    def editAllComments(self):
        for parameter in self._listOfParameters:
            parameter.enableEdit()

    def saveAllComments(self):
        for parameter in self._listOfParameters:
            parameter.saveComment(True)
        self.dialog.verilogFile.writeFile()

    def defaultAllComments(self):
        for parameter in self._listOfParameters:
            parameter.SavedefaultComment(True)
        self.dialog.verilogFile.writeFile()    