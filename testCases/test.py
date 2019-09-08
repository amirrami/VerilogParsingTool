
import os,platform,sys


os.chdir("/home/amir/Downloads/work/MentorIntern/VerilogParsingTool/testCases")
print(os.getcwd())
if platform.system() == "Linux" and str(platform.dist()[0]) == "Ubuntu":
            compileCommand = "vlog "
            myCmd = os.popen('ls *.v *.sv').read().split("\n")
            for command in myCmd:
                compileCommand += command+ " "
            os.system(compileCommand)
        
        #print(os.name)
        #print(platform.system())
        #print(platform.release())
        #print(str(platform.dist()[0]))
        
        
        #os.system("gnome-terminal -e 'bash -c \"subl *.v *.sv;ls *.v *.sv; bash\" '")