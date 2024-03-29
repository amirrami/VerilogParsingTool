import re
from Parameter import Parameter,Module,ModuleInstance,TestBench,Mode



class Parser():
    def __init__(self,lines,text):
        self.VerilogLines = lines
        self.verilogText = text
        self.moduleType = ""
        self.includeFile = False
        
    def startParsing(self):
        self.moduleNameParser()

    def setVerilogLines(self,lines):
        self.VerilogLines = lines
        

    def moduleNameParser(self):
        testBenchMatch = re.search(r'(?i)module\s+([a-zA-Z0-9_$]*)\s*[(]*\s*[)]*;',self.verilogText)
        if testBenchMatch:
            self.testBench = TestBench(testBenchMatch.group(1))
            self.moduleType = "testBench"
            self.parseModes()
            self.TBParameterParser()
        else:
            testBenchWithHash = re.search(r"(?i)module\s+([a-zA-Z0-9_$]*)\s*#[(]\s*[)]\s*[(]\s*[)]\s*;",self.verilogText)
            if testBenchWithHash:
                self.testBench = TestBench(testBenchWithHash.group(1))
                self.moduleType = "testBench"
                self.parseModes()
                self.TBParameterParser()
            else:
                moduleTest = re.search(r'(?i)module\s+([a-zA-Z0-9_$]*)\s*[(]([\s\S]+)[)];',self.verilogText)
                if moduleTest:
                    self.module = Module(moduleTest.group(1))
                    self.moduleType = "module"
                    self.moduleParameterParser()
                else:
                    moduleWithHash = re.search(r"(?i)module\s+([a-zA-Z0-9_$]*)\s*#[(][\s\S]*[)]\s*[(]",self.verilogText)
                    if moduleWithHash:
                        self.moduleType = "module"
                        self.module = Module(moduleWithHash.group(1))
                        self.moduleParameterParser()
    
    #normal module Parser
    def moduleParameterParser(self):
        moduleParameterList = []
        lineNumber = len(self.VerilogLines)
        for index in range(lineNumber):
            match = re.search(r"(?i)parameter\s+([a-zA-Z0-9_$]*)\s*=\s*([^,\n;/)]*)",self.VerilogLines[index])
            if match:
                parameter = Parameter(match.group(1))
                parameter.setValue(match.group(2))
                parameter.setLineIndex(index)
                matchComment = re.search(r'\s*//\s*(.*)',self.VerilogLines[index])
                if matchComment:
                    parameter.setComment(matchComment.group(1))
                else:
                    parameter.setComment("")
                moduleParameterList.append(parameter)
        self.module.setParametersList(moduleParameterList)
                
    #test bench parser
    def TBParameterParser(self):
        listOfInstances = []
        intance = re.findall(r"((`ifdef|`ifndef)[a-zA-Z0-9_$.,\/\"'`)(\s]*`endif|[a-zA-Z0-9_$]+)\s*#\s*[(]([a-zA-Z0-9_$.,\/\"'`)(\s]*)[)]\s*([a-zA-Z0-9_$]+)",self.verilogText)
        if intance:
            for i in range(len(intance)):
                if re.search(r"(`ifdef|`ifndef)",intance[i][0]):
                    moduleName = self.instanceNameCorrection(intance[i][0])
                    Instance = ModuleInstance(intance[i][3],moduleName)
                    Instance.setFalseName(intance[i][0])
                else:
                    Instance = ModuleInstance(intance[i][3],intance[i][0])
                intanceParameterList = []
                # add space at the begin of parameters inside hash to conpensate error for the first parameter 
                # which need to have a space
                textInsideHash = " " + intance[i][2]
                 #to find all parameter inside the "#"
                parametersInsideHash = re.findall(r"\s*[^\/][.]\s*([a-zA-Z0-9_$]+)\s*[(]\s*([`a-zA-Z0-9_$'\".]+)\s*[)]\s*[,]?[ \/]*([a-zA-Z0-9_$'`\"\/, ]*)",textInsideHash)
                #parsing every parameter line
                for parameterLine in parametersInsideHash:
                    valueFound = False
                    commentFound = False
                    #condition to check if the parameter name has ` so we search for define
                    if re.search(r"[`]",parameterLine[1]):
                        parameter = re.search(r"[`][ ]*([a-zA-Z0-9_$]*)",parameterLine[1])
                        for i in range(len(self.VerilogLines)):
                            defineMatch = re.search(r"[`](?i)define[ ]+"+parameter.group(1)+"[ ]+([a-zA-Z0-9_']+)",self.VerilogLines[i])
                            if defineMatch:
                                valueFound = True
                                param = Parameter(parameterLine[0])
                                param.setValue(defineMatch.group(1))
                                param.setLineIndex(i)
                                matchComment = re.search(r'\s*//\s*(.*)',self.VerilogLines[i])
                                if matchComment:
                                    commentFound = True
                                    param.setComment(matchComment.group(1))
                                break
                            elif re.search(r"[.][ ]*"+parameterLine[0]+"[ (]*"+parameterLine[1],self.VerilogLines[i]):
                                index = i     
                    else:
                        for i in range(len(self.VerilogLines)):
                            parameter = re.search(r"(?i)parameter\s+"+parameterLine[1]+"\s*=\s*([^,\n;/)]*)",self.VerilogLines[i])
                            if parameter:
                                valueFound = True
                                param = Parameter(parameterLine[0])
                                param.setValue(parameter.group(1))
                                param.setLineIndex(i)
                                matchComment = re.search(r'\s*//\s*(.*)',self.VerilogLines[i])
                                if matchComment:
                                    commentFound = True
                                    param.setComment(matchComment.group(1))
                                break
                            elif re.search(r"[.][ ]*"+parameterLine[0]+"[ (]*"+parameterLine[1],self.VerilogLines[i]):
                                index = i   
                    if not valueFound:
                        if self.includeFile:
                            valueFound,listOfValues = self.parseIncludeFile(parameterLine[1])
                        if not valueFound:
                            param = Parameter(parameterLine[0])
                            param.setValue(parameterLine[1])
                            param.setLineIndex(index)
                            param.setComment(parameterLine[2])
                        else:
                            param = Parameter(parameterLine[0])
                            param.setValue(listOfValues[0])
                            param.setLineIndex(listOfValues[1])
                            param.setComment(listOfValues[2])
                            param.setInInclude(True)
                    intanceParameterList.append(param)
                Instance.setParametersList(intanceParameterList)
                listOfInstances.append(Instance)
            self.testBench.setInstanceList(listOfInstances)

    def parseIncludeFile(self,parameterName):
        valueFound = False
        commentFound = False
        listOfValues = []
        if re.search(r"[`]",parameterName):
            parameter = re.search(r"[`][ ]*([a-zA-Z0-9_$]*)",parameterName)
            for i in range(len(self.includeFileLines)):
                defineMatch = re.search(r"[`](?i)define[ ]+"+parameter.group(1)+"[ ]+([a-zA-Z0-9_'\"]+)",self.includeFileLines[i])
                if defineMatch:
                    valueFound = True
                    listOfValues.append(defineMatch.group(1))
                    listOfValues.append(i)
                    matchComment = re.search(r'\s*//\s*(.*)',self.includeFileLines[i])
                    if matchComment:
                        commentFound = True
                        listOfValues.append(matchComment.group(1))
                    else:
                        listOfValues.append("")
                    break    
        else:
            for i in range(len(self.includeFileLines)):
                parameter = re.search(r"(?i)parameter\s+"+parameterName+"\s*=\s*([^,\n;/)]*)",self.includeFileLines[i])
                if parameter:
                    valueFound = True
                    listOfValues.append(parameter.group(1))
                    listOfValues.append(i)
                    matchComment = re.search(r'\s*//\s*(.*)',self.includeFileLines[i])
                    if matchComment:
                        commentFound = True
                        listOfValues.append(matchComment.group(1))
                    else:
                        listOfValues.append("")
                    break
        return valueFound,listOfValues


    def getIncludeFile(self):
        includeMatch = re.search(r'[`][ ]*(?i)include[ ]*["](.+)["]',self.verilogText)
        if includeMatch:
            return includeMatch.group(1)
        else:
            return False

    def setIncludeFileLines(self,lines):
        self.includeFileLines = lines
        self.includeFile = True

    def getModuleType(self):
        return self.moduleType

    def getModule(self):
        if self.moduleType == "module":
            return self.module
    
    def gettestBench(self):
        if self.moduleType == "testBench":
            return self.testBench

    def parseModes(self):
        modes = set()
        modesList = []
        #to detect all modes all across the file and put in set so its repeated
        for line in self.VerilogLines:
            line =  " " + line
            modeMatch = re.search(r"[^\/]\s*(`ifdef|`ifndef|`elsif)\s*([a-zA-Z0-9_$'`\"\/,.]+)",line)
            if modeMatch:
                modes.add(modeMatch.group(2))
        for mode in modes:
            testBenchMode = Mode(mode)
            length = len(self.VerilogLines)
            for i in range(length):
                line = " " + self.VerilogLines[i]
                modeDefined = re.search(r"[^\/]\s*`(?i)define\s+"+mode,line)
                if modeDefined:
                    testBenchMode.setIsDefined(True)
                    testBenchMode.setlineIndex(i)
                    break
            modesList.append(testBenchMode)
        self.testBench.setModesList(modesList)

            
        

    def instanceNameCorrection(self,falseName):
        lines = falseName.split("\n")
        isDefined = False
        trueName = ""
        for i in range(len(lines)):
            ifdefMatch = re.search(r"(`ifdef|`ifndef|`elsif)\s*([a-zA-Z0-9_$]+)",lines[i])
            elseMatch = re.search(r"`else",lines[i])
            if ifdefMatch:
                toSearchMode = ifdefMatch.group(2)
                for mode in self.testBench.modesList:
                    if mode.modeName == toSearchMode:
                        if (ifdefMatch.group(1) == "`ifdef" or ifdefMatch.group(1) == "`elsif") and mode.isDefinednew:
                            match = re.search(r"([a-zA-Z0-9_$]+)",lines[i+1])
                            if match:
                                trueName = match.group(1)
                                isDefined = True
                        elif ifdefMatch.group(1) == "`ifndef" and not mode.isDefinednew:
                            match = re.search(r"([a-zA-Z0-9_$]+)",lines[i+1])
                            if match:
                                trueName = match.group(1)
                                isDefined = True
            elif elseMatch and not isDefined:
                match = re.search(r"([a-zA-Z0-9_$]+)",lines[i+1])
                if match:
                    trueName = match.group(1)   
        return trueName
