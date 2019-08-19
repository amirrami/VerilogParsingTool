from PyQt5.QtWidgets import QAction

class CreateAction():
    
    def create(self,action,widget,shortCut,statusTip):
        createdAction = QAction(action,widget)
        createdAction.setShortcut(shortCut)
        createdAction.setStatusTip(statusTip)
        return createdAction