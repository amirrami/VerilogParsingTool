from PyQt5.QtWidgets import QDialog,QFormLayout,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,QLineEdit
from PyQt5.QtWidgets import QGroupBox,QAction,QMenuBar,QSpacerItem,QSizePolicy,QMainWindow,QWidget
from CreateActions import CreateAction
from Parameter import Parameter,ParametersList

class EditDialog(QMainWindow):
    def __init__(self,VFile):
        super().__init__()
        self.left = 400
        self.top = 200
        self.width = 0
        self.height = 0
        self.title = "Verilog Parsing Tool"
        self.setWindowTitle(self.title)
        self.verilogFile = VFile
        self.parameterList = ParametersList(self.verilogFile.verilogParameters,
                                self.verilogFile.parametersLineIndexes,
                                self.verilogFile.commentsList,self)
        self.mainMenu = self.menuBar()
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.create_Actions()
        self.uiSetup()
        
    def create_Actions(self):
        actions = CreateAction()
        #self.closeFile = actions.create("&Open File",self,"Ctrl+T",'Close File')
        #self.closeDialog.triggered.connect(self.closeDialog)
        self.saveFile = actions.create("&Save File",self,"Ctrl+S",'Save File')
        self.saveFile.triggered.connect(self.parameterList.saveAll)
        self.fileMenu.addAction(self.saveFile)

    def setupParameterValueBox(self):
        self.valuesGroupBox = QGroupBox("Parameters Value")
        valuesButtonsHBox = QHBoxLayout()
        valuesVBox = QVBoxLayout()
        valuesFormsHBox = QHBoxLayout()
        labelAndInputForm = QFormLayout()
        SaveButtonForm = QFormLayout()
        #the parameters inputs and save buttons
        for parameter in self.parameterList.getList():
            labelAndInputForm.addRow(parameter.Plabel,parameter.PlineEdit)
            SaveButtonForm.addRow(parameter.saveButton,parameter.defaultbutton)
            
        #add savaAllValuesButton and DefaultAllValuesButton
        valuesButtonsHBox.addWidget(self.parameterList.saveAllValueButton)
        valuesButtonsHBox.addWidget(self.parameterList.defaultAllValueButton)
        
        #add Values Forms to H Box
        valuesFormsHBox.addLayout(labelAndInputForm)
        valuesFormsHBox.addLayout(SaveButtonForm)

        valuesVBox.addLayout(valuesFormsHBox)
        valuesVBox.addLayout(valuesButtonsHBox)
       
        self.valuesGroupBox.setLayout(valuesVBox)

    
    def setupParameterCommentsBox(self):
        self.commentsGroupBox = QGroupBox("Parameters Comments")
        commentsButtonsHBox = QHBoxLayout()
        commentsVBox = QVBoxLayout()
        commentsFormsHBox = QHBoxLayout()
        commentSaveForm = QFormLayout()
        commentEditForm = QFormLayout()
        for parameter in self.parameterList.getList():
            commentEditForm.addRow(parameter.commentLineEdit,parameter.editCommentButton)
            commentSaveForm.addRow(parameter.saveCommentButton,parameter.defaulfCommentButton)
        #add savaAllCommentsButton and DefaultAllCommentsButtn
        commentsButtonsHBox.addWidget(self.parameterList.editAllCommentsButton)
        commentsButtonsHBox.addWidget(self.parameterList.saveAllCommentsButton)
        commentsButtonsHBox.addWidget(self.parameterList.defaultAllCommentButton)

         #add comments Forms to HBox
        commentsFormsHBox.addLayout(commentEditForm)
        commentsFormsHBox.addLayout(commentSaveForm)

        commentsVBox.addLayout(commentsFormsHBox)
        commentsVBox.addLayout(commentsButtonsHBox)
        self.commentsGroupBox.setLayout(commentsVBox)

    def uiSetup(self):
        self.setupParameterCommentsBox()
        self.setupParameterValueBox()
        if self.verilogFile.isTestBench:
            gruopBoxString = "Test Bench " + self.verilogFile.moduleName
        else:
            gruopBoxString = "Parameter List Of Module " + self.verilogFile.moduleName
        outerGroupBox = QGroupBox(gruopBoxString)
        #saveAll button and defaultAll button in innerLayout
        vboxInner = QVBoxLayout()
        vboxInner.addWidget(self.parameterList.defaultAllButton)
        vboxInner.addWidget(self.parameterList.saveAllButton)
        #out vertical layout have 1 horizontal 1 one vertical
        hBoxOuter = QHBoxLayout()
        hBoxOuter.addWidget(self.valuesGroupBox)
        hBoxOuter.addWidget(self.commentsGroupBox)
        vboxOuter = QVBoxLayout()
        vboxOuter.addLayout(hBoxOuter)
        vboxOuter.addLayout(vboxInner)
        #group box have outer layout
        outerGroupBox.setLayout(vboxOuter)
        #vbox to be set as the main layout 
        vbox = QVBoxLayout()
        #verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #vbox.addItem(verticalSpacer)
        vbox.addWidget(outerGroupBox)
        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

    