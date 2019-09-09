from PyQt5.QtWidgets import QDialog,QFormLayout,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,QLineEdit
from PyQt5.QtWidgets import QGroupBox,QWidget,QDesktopWidget
from Parameter import Parameter,ModulsExtractor,Module,ModuleInstance


class OptionsDialog(QDialog):
    def __init__(self,option):
        super().__init__()
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowTitle(option+" Configurations")
