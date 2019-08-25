from PyQt5.QtWidgets import QApplication
from mainWindow import mainWindow

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)       
    mainWindow = mainWindow()
    mainWindow.show()
    sys.exit(app.exec())