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
        self.title = "Verilog Parsing Tool"
        self.setWindowTitle(self.title)
        self.setMinimumHeight(300)
        self.setMinimumWidth(1200)
        self.verilogFile = VFile
        self.moduleExtractor = ModulsExtractor(self)
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.create_Actions()
        self.uiSetup()
        
    def create_Actions(self):
        actions = CreateAction()
        #self.closeFile = actions.create("&Open File",self,"Ctrl+T",'Close File')
        #self.closeDialog.triggered.connect(self.closeDialog)
        self.saveFile = actions.create("&Save File",self,"Ctrl+S",'Save File')
        self.saveFile.triggered.connect(self.moduleExtractor.saveAll)
        self.fileMenu.addAction(self.saveFile)
        self.defaultFile = actions.create("&Defualt File",self,"Ctrl+D",'Default File')
        self.defaultFile.triggered.connect(self.moduleExtractor.defaultAll)
        self.fileMenu.addAction(self.defaultFile)

    def uiSetup(self):
        vboxInner = QVBoxLayout()
        if self.verilogFile.moduleType == "testBench":
            instacesList =  self.verilogFile.testBench.instanceList
            for instance in instacesList:
                self.setupParameterCommentsBox(instance)
                self.setupParameterValueBox(instance)
                hbox = QHBoxLayout()
                hbox.addWidget(self.valuesGroupBox)
                hbox.addWidget(self.commentsGroupBox)
                instanceGroupBox = QGroupBox("Instance "+instance.instanceName+" Of Module "+instance.moduleName)
                instanceGroupBox.setLayout(hbox)
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
        #saveAll button and defaultAll button in innerLayout
        vBoxOuter.addWidget(self.moduleExtractor.defaultAllButton)
        vBoxOuter.addWidget(self.moduleExtractor.saveAllButton)
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
            commentSaveForm.addRow(parameter.saveCommentButton,parameter.defaulfCommentButton)
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
            SaveButtonForm.addRow(parameter.saveButton,parameter.defaultbutton)   
        #add savaAllValuesButton and DefaultAllValuesButton
        valuesButtonsHBox.addWidget(module.saveAllValueButton)
        valuesButtonsHBox.addWidget(module.defaultAllValueButton)
        #add Values Forms to H Box
        valuesFormsHBox.addLayout(labelAndInputForm)
        valuesFormsHBox.addLayout(SaveButtonForm)
        valuesVBox.addLayout(valuesFormsHBox)
        valuesVBox.addLayout(valuesButtonsHBox)
        self.valuesGroupBox.setLayout(valuesVBox)