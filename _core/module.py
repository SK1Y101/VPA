try:
    from _core import settings
except:
    import settings
import subprocess,datetime

def init():
    x = str(subprocess.check_output("pip list",shell=True))
    x = x[2:len(x)-1]
    modules = []
    while ")" in x:
        x = x[0:x.index("(")-1]+"\n"+x[x.index(")")+5:len(x)]
    while "\n" in x:
        modules.append(x[0:x.index("\n")])
        x = x[x.index("\n")+1:len(x)]
    settings.addglobal("modules",modules,True)
    settings.addglobal("dont_inst",[],True)

def logtext(text="null"):
    text = text[0].upper()+text[1:len(text)]+"\n"
    y = open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text)
    y.close()
    
def installmodule(mod=""):
    print("Installing module: "+mod+" Please wait a moment")
    logtext("module: "+mod+" not installed, installing now")
    subprocess.call("pip install "+str(mod),shell=True)
    init()
    if mod in settings.modules:
        logtext("module: "+mod+" installed")
        return True
    else:
        logtext("module: "+mod+" could not be installed")
        return False

def checkmodule(mod="",core="",inst=True):
    if not mod in settings.modules:
        if inst == True:
            x = installmodule(mod)
            if x == False:
                stopmodule(core,mod)
                return False
            else:
                return True
        else:
            logtext("module: "+mod+" could not be installed")
            stopmodule(core,mod)
            return False
    else:
        return True

def stopmodule(core="",mod=""):
    try:
        print("Instalation of module: "+mod+" Failed, "+core+" will not be loaded")
        settings.dont_inst.append(core)
        logtext("No module: "+mod+" has prevented loading of functions: "+a)
    except:
        pass

if __name__ != "__main__":
    init()
