import re

class Parser():
    def __init__(self,lines):
        self.VerilogLines = lines
        self.parameters = []
        self.lineIndexes = []
        self.commentsList = []
        self.parameterParser()
    
    def moduleNameParser(self):
        pass

    def parameterParser(self):
        lineNumber = len(self.VerilogLines)
        for index in range(lineNumber):
            match = re.search(r'[Pp]arameter\s+(.+)\s*=\s*(.+);',self.VerilogLines[index])
            if match:
                print("found")
                print(match.group(1),match.group(2))
                self.parameters.append({match.group(1):match.group(2)})
                self.lineIndexes.append(index)
                matchComment = re.search(r'\s*//\s*(.*)',self.VerilogLines[index])
                if matchComment:
                    print(matchComment.group(1))
                    self.commentsList.append(matchComment.group(1))
                else:
                    self.commentsList.append("")

    def parserOutput(self):
        return self.parameters,self.lineIndexes,self.commentsList
        
