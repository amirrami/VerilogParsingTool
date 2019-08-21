import re


class Parser():
    def __init__(self,lines,text):
        self.VerilogLines = lines
        self.verilogText = text
        self.parameters = []
        self.lineIndexes = []
        self.commentsList = []
        self.moduleName = ""
        self.moduleNameParser()
        self.testBench = False

    
    def moduleNameParser(self):
        testBenchMatch = re.search(r'(?i)module\s+([a-zA-Z0-9_-]*)\s*[(]*\s*[)]*;',self.verilogText)
        if testBenchMatch:
            self.testBench = True
            print("testBench",testBenchMatch.group(1))
            self.moduleName = testBenchMatch.group(1)
            self.TBParameterParser()
        else:
            moduleTest = re.search(r'(?i)module\s+([a-zA-Z0-9_-]*)\s*[(]([\s\S]+)[)];',self.verilogText)
            if moduleTest:
                self.testBench = False
                print("module",moduleTest.group(1))
                self.moduleName = moduleTest.group(1)
                self.moduleParameterParser()
            else:
                moduleTestWithHash = re.search(r"(?i)module\s+([a-zA-Z0-9_-]*)\s*#[(]([\s\S]*)[)]\s*[(]",self.verilogText)
                if moduleTestWithHash:
                    self.testBench = False
                    print("moduleWithHash",moduleTestWithHash.group(1))
                    self.moduleName = moduleTestWithHash.group(1)
                    print(moduleTestWithHash.group(2))
                    self.moduleParameterParser()

    def moduleParameterParser(self):
        lineNumber = len(self.VerilogLines)
        for index in range(lineNumber):
            match = re.findall(r"(?i)parameter\s+([a-zA-Z0-9_-]*)\s*=\s*([^,\n;/)]*)",self.VerilogLines[index])
            if match:
                for i in range(len(match)):
                    self.parameters.append({match[i][0]:match[i][1]})
                    self.lineIndexes.append(index)
                matchComment = re.search(r'\s*//\s*(.*)',self.VerilogLines[index])
                if matchComment:
                    #print(matchComment.group(1))
                    self.commentsList.append(matchComment.group(1))
                else:
                    self.commentsList.append("")
    
    def TBParameterParser(self):
        pass

    def parserOutput(self):
        return self.parameters,self.lineIndexes,self.commentsList
      
    def getModuleName(self):
        return self.moduleName
    
    def getParameters(self):
        return self.parameters

    def getLineIndexes(self):
        return self.lineIndexes

    def getCommentList(self):
        return self.commentsList

    def getModuleType(self):
        return self.testBench