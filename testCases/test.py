
import os,platform,sys,subprocess

#print(platform.system())

os.chdir("D:/VerilogParsingTool-master/VerilogParsingTool/testCases")
#print(os.getcwd())
if platform.system() == "Linux" and str(platform.dist()[0]) == "Ubuntu":
            compileCommand = "vlog "
            myCmd = os.popen('dir *.v *.sv').read().split("\n")
            for command in myCmd:
                compileCommand += command+ " "
            os.system(compileCommand)
elif platform.system() == "Windows":
    files = os.listdir()
    for file in files:
        if file.endswith(".sv") or file.endswith(".v"):
            print(file)
    #print(l)
    #result = []
    #process = subprocess.Popen('dir /b *.v *.sv',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE )
    #for line in process.stdout:
    #    result.append(line)
    #errcode = process.returncode
    #for line in result:
    #    print(line)
    #compileCommand = "vlog "
    #os.system("dir /b *.v *.sv")
    #myCmd = os.popen('dir /b *.v *.sv').read().split("\n")
    #for command in myCmd:
    #    compileCommand += command+ " "
    #print(compileCommand)
    #os.system(compileCommand)
        
        #print(os.name)
        #print(platform.system())
        #print(platform.release())
        #print(str(platform.dist()[0]))
        
        
        #os.system("gnome-terminal -e 'bash -c \"subl *.v *.sv;ls *.v *.sv; bash\" '")