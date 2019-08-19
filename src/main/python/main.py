from fbs_runtime.application_context.PyQt5 import ApplicationContext
from mainWindow import mainWindow

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    mainWindow = mainWindow()
    mainWindow.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)