import re


class Parser():
    def __init__(self,lines,text):
        self.VerilogLines = lines
        self.verilogText = text
        self.parameters = []
        self.lineIndexes = []
        self.commentsList = []
        self.moduleName = ""
        self.testBench = False
        self.intancesList = []
        self.moduleNameParser()
        

    def moduleNameParser(self):
        testBenchMatch = re.search(r'(?i)module\s+([a-zA-Z0-9_$]*)\s*[(]*\s*[)]*;',self.verilogText)
        if testBenchMatch:
            self.testBench = True
            print("testBench",testBenchMatch.group(1))
            self.moduleName = testBenchMatch.group(1)
            self.TBParameterParser()
        else:
            moduleTest = re.search(r'(?i)module\s+([a-zA-Z0-9_$]*)\s*[(]([\s\S]+)[)];',self.verilogText)
            if moduleTest:
                self.testBench = False
                print("module",moduleTest.group(1))
                self.moduleName = moduleTest.group(1)
                self.moduleParameterParser()
            else:
                moduleTestWithHash = re.search(r"(?i)module\s+([a-zA-Z0-9_$]*)\s*#[(][\s\S]*[)]\s*[(]",self.verilogText)
                if moduleTestWithHash:
                    self.testBench = False
                    self.moduleName = moduleTestWithHash.group(1)
                    self.moduleParameterParser()
    
    #normal module Parser
    def moduleParameterParser(self):
        lineNumber = len(self.VerilogLines)
        for index in range(lineNumber):
            match = re.findall(r"(?i)parameter\s+([a-zA-Z0-9_$]*)\s*=\s*([^,\n;/)]*)",self.VerilogLines[index])
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
    
    #test bench parser
    def TBParameterParser(self):
        intance = re.findall(r"([a-zA-Z0-9_$]+)\s*#\s*[(]([a-zA-Z0-9_$.,\/')(\s]*)[)]\s*([a-zA-Z0-9_$]+)",self.verilogText)
        if intance:
            for i in range(len(intance)):
                self.intancesList.append([intance[i][0],intance[i][2]])
                #to find all parameter inside the "#"
                parametersInsideHash = re.findall(r"[.]\s*([a-zA-Z0-9_$]+)\s*[(]\s*([a-zA-Z0-9_$'.]+)\s*[)]\s*[,]?[\/\s]*([a-zA-Z0-9-_$!@#$%^&*()_+<>?{}' ]*)",intance[i][1])
                parameterList = []
                commentList = []
                lineIndex = []
                #parsing every parameter line
                for parameterLine in parametersInsideHash:
                    valueFound = False
                    commentFound = False
                    for i in range(len(self.VerilogLines)):
                        parameter = re.search(r"(?i)parameter\s+"+parameterLine[1]+"\s*=\s*([^,\n;/)]*)",self.VerilogLines[i])
                        if parameter:
                            valueFound = True
                            parameterList.append({parameterLine[0]:parameter.group(1)})
                            lineIndex.append(i)
                            matchComment = re.search(r'\s*//\s*(.*)',self.VerilogLines[i])
                            if matchComment:
                                commentFound = True
                                commentList.append(matchComment.group(1))
                            break
                        elif re.search(r"[.]"+parameterLine[0]+"[ (]*"+parameterLine[1],self.VerilogLines[i]):
                            index = i
                    if not valueFound:
                        parameterList.append({parameterLine[0]:parameterLine[1]})
                        commentList.append(parameterLine[2])
                        lineIndex.append(index)
                    elif valueFound and not commentFound:
                        commentList.append("")
                self.parameters.append(parameterList)
                self.commentsList.append(commentList)
                self.lineIndexes.append(lineIndex) 


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

    def getInstancesList(self):
        return self.intancesList