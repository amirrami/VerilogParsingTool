from PyQt5.QtWidgets import QDialog,QFormLayout,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,QLineEdit,QScrollArea
from PyQt5.QtWidgets import QGroupBox,QAction,QMenuBar,QSpacerItem,QSizePolicy,QMainWindow,QWidget
from CreateActions import CreateAction
from Parameter import Parameter,ModulsExtractor,Module,ModuleInstance

class EditDialog(QMainWindow):
    def __init__(self,VFile):
        super().__init__()
        self.left = 400
        self.top = 200
        self.width = 0
        self.height = 0
        #self.setMinimumHeight(300)
        #self.setMinimumWidth(1200)
        self.showMaximized()
        self.verilogFile = VFile
        self.moduleExtractor = ModulsExtractor(self)
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.create_Actions()
        self.uiSetup()
        if self.verilogFile.moduleType == "testBench":
            self.setWindowTitle("Test Bench "+self.verilogFile.testBench.TestBenchName)
        elif self.verilogFile.moduleType == "module":
            self.setWindowTitle("Module "+self.verilogFile.Module.moduleName)
        
    def create_Actions(self):
        actions = CreateAction()
        self.openFile = actions.create("&Open File",self,"Ctrl+O",'Open File')
        self.openFileAnotherWindow = actions.create("&Open File In New Window",self,"Ctrl+A",'Open File In New Window') 
        self.saveFile = actions.create("&Save File",self,"Ctrl+S",'Save File')
        self.defaultFile = actions.create("&Defualt File",self,"Ctrl+D",'Default File')
        self.closeDialog = actions.create("&Terminate File",self,"Ctrl+T",'Terminate File')
        self.openFile.triggered.connect(self.close)
        self.openFile.triggered.connect(self.verilogFile.parent.file_open)
        self.openFileAnotherWindow.triggered.connect(self.verilogFile.parent.file_open)
        self.saveFile.triggered.connect(self.moduleExtractor.saveAll)
        self.defaultFile.triggered.connect(self.moduleExtractor.defaultAll)
        self.closeDialog.triggered.connect(self.close)
        self.fileMenu.addAction(self.openFile)
        self.fileMenu.addAction(self.openFileAnotherWindow)
        self.fileMenu.addAction(self.saveFile)
        self.fileMenu.addAction(self.defaultFile)
        self.fileMenu.addAction(self.closeDialog)

        

    def uiSetup(self):
        vboxInner = QVBoxLayout()
        if self.verilogFile.moduleType == "testBench":
            if self.verilogFile.testBench.modesList:
                checkBoxesVBox = QVBoxLayout()
                modesButtonsVBox = QVBoxLayout()
                HBoxContainer = QHBoxLayout()
                for mode in self.verilogFile.testBench.modesList:
                    checkBoxesVBox.addWidget(mode.checkBox)
                modesButtonsVBox.addWidget(self.verilogFile.testBench.checkAllButton)
                modesButtonsVBox.addWidget(self.verilogFile.testBench.unCheckAllButton)
                modesButtonsVBox.addWidget(self.verilogFile.testBench.defaultAllModesButton)
                modesButtonsVBox.addWidget(self.verilogFile.testBench.saveAllModesButton)
                HBoxContainer.addLayout(checkBoxesVBox)
                HBoxContainer.addLayout(modesButtonsVBox)
                modesGroupBox = QGroupBox("Modes Of Test Bench "+self.verilogFile.testBench.TestBenchName)
                modesGroupBox.setLayout(HBoxContainer)
                vboxInner.addWidget(modesGroupBox)
            instacesList =  self.verilogFile.testBench.instanceList
            for instance in instacesList:
                self.setupParameterCommentsBox(instance)
                self.setupParameterValueBox(instance)
                hbox = QHBoxLayout()
                hbox.addWidget(self.valuesGroupBox)
                hbox.addWidget(self.commentsGroupBox)
                instanceGroupBox = QGroupBox("Instance "+instance.instanceName+" Of Module "+instance.moduleName)
                instanceGroupBox.setLayout(hbox)
                instance.setGroupBox(instanceGroupBox)
                vboxInner.addWidget(instanceGroupBox)
            gruopBoxString = "Test Bench " + self.verilogFile.testBench.TestBenchName 
        elif self.verilogFile.moduleType == "module":
            module = self.verilogFile.Module
            self.setupParameterCommentsBox(module)
            self.setupParameterValueBox(module)    
            hbox = QHBoxLayout()
            hbox.addWidget(self.valuesGroupBox)
            hbox.addWidget(self.commentsGroupBox)
            vboxInner.addLayout(hbox)
            gruopBoxString = "Parameter List Of Module " + self.verilogFile.Module.moduleName
        outerGroupBox = QGroupBox(gruopBoxString)
        #group box have outer layout
        widget = QWidget()
        widget.setLayout(vboxInner)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(widget)
        vbox = QVBoxLayout()
        vbox.addWidget(scrollArea)
        outerGroupBox.setLayout(vbox)
        #vbox to be set as the main layout 
        vBoxOuter = QVBoxLayout()
        vBoxOuter.addWidget(outerGroupBox)
        #saveAll,default,compile,Run buttons 
        outerButtonsForm = QFormLayout()
        outerButtonsForm.addRow(self.moduleExtractor.saveAllButton,self.moduleExtractor.compileButton)
        outerButtonsForm.addRow(self.moduleExtractor.defaultAllButton,self.moduleExtractor.RunButton)
        vBoxOuter.addLayout(outerButtonsForm)
        widget = QWidget()
        widget.setLayout(vBoxOuter)
        self.setCentralWidget(widget)
    
    def setupParameterCommentsBox(self,module):
        self.commentsGroupBox = QGroupBox("Parameters Comments")
        commentsButtonsHBox = QHBoxLayout()
        commentsVBox = QVBoxLayout()
        commentsFormsHBox = QHBoxLayout()
        commentSaveForm = QFormLayout()
        commentEditForm = QFormLayout()
        for parameter in module.parameterList:
            parameter.commentLineEdit.setMinimumWidth(300)
            commentEditForm.addRow(parameter.editCommentButton,parameter.commentLineEdit)
            commentSaveForm.addRow(parameter.defaulfCommentButton)
        #add savaAllCommentsButton and DefaultAllCommentsButtn
        commentsButtonsHBox.addWidget(module.editAllCommentsButton)
        commentsButtonsHBox.addWidget(module.saveAllCommentsButton)
        commentsButtonsHBox.addWidget(module.defaultAllCommentButton)
        #add comments Forms to HBox
        commentsFormsHBox.addLayout(commentEditForm)
        commentsFormsHBox.addLayout(commentSaveForm)
        commentsVBox.addLayout(commentsFormsHBox)
        commentsVBox.addLayout(commentsButtonsHBox)
        self.commentsGroupBox.setLayout(commentsVBox)


    def setupParameterValueBox(self,module):
        self.valuesGroupBox = QGroupBox("Parameters Value")
        valuesButtonsHBox = QHBoxLayout()
        valuesVBox = QVBoxLayout()
        valuesFormsHBox = QHBoxLayout()
        labelAndInputForm = QFormLayout()
        SaveButtonForm = QFormLayout()
        #the parameters inputs and save buttons
        for parameter in module.parameterList:
            parameter.PlineEdit.setMinimumWidth(150)
            labelAndInputForm.addRow(parameter.Plabel,parameter.PlineEdit)
            SaveButtonForm.addRow(parameter.defaultbutton)   
        #add savaAllValuesButton and DefaultAllValuesButton
        valuesButtonsHBox.addWidget(module.saveAllValueButton)
        valuesButtonsHBox.addWidget(module.defaultAllValueButton)
        #add Values Forms to H Box
        valuesFormsHBox.addLayout(labelAndInputForm)
        valuesFormsHBox.addLayout(SaveButtonForm)
        valuesVBox.addLayout(valuesFormsHBox)
        valuesVBox.addLayout(valuesButtonsHBox)
        self.valuesGroupBox.setLayout(valuesVBox)