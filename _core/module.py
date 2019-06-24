import subprocess, sys, datetime
from time import sleep
globals()["funcs"] = []
globals()["cwords"] = []
globals()["desc"] = []
globals()["startfunc"] = []
globals()["persistfunc"] = []
globals()["permods"] = []
globals()["shutdownfunc"] = []

def module(name="",version="",url=""):
    return True
    #used to define the module version. URL not required, but for some reason i like to have it anyway.

def needs(modules=[]):
    return True
    #used to set a list of pythonic modules that a LOaBIS module requires

def startup(funcs=[]):
    return True
    #used to set a list of functions that must be performed at launch

def shutdown(funcs=[]):
    return True
    #used to set a list of functions to be execeuted at shutdown.

def persist(funcs=[]):
    return True
    #used to set a list of functions that will be performed at regular intervals

def hasdependancy(mods=[]):
    return True
    #used to set a list of LOaBIS functions that must be loaded before itself

def dont_overwrite(files=[]):
    return True
    #required bu the updater to prevent it replacing data files.

def _logtext(text="null"):
    y = open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text[0].upper()+text[1:len(text)]+"\n")
    y.close()

def getmods():
    x = str(subprocess.check_output("pip3 list",shell=True))
    x = x[2:len(x)-1]
    mods = []
    while ")" in x:
        x = x[0:x.index("(")-1]+"\n"+x[x.index(")")+5:len(x)]
    while "\n" in x:
        mods.append(x[0:x.index("\n")])
        x = x[x.index("\n")+1:len(x)]
    globals()["Mods"] = mods
    return mods
            
def checkmods(modules=[]):
    try:
        if len(Mods) == 0:
            getmods()
    except:
        getmods()
    for x in modules:
        x = x.replace(" ","")
        if x not in Mods:
            if not installmodule(x):
                return False
    return True

def installmodule(mod=""):
    _logtext("Module: "+mod+" not installed, installing now")
    if sys.platform == "win32":
        subprocess.call("pip3 install "+str(mod),shell=True)
    else:
        subprocess.call("sudo pip3 install "+str(mod),shell=True)
    if mod in getmods():
        _logtext("module: "+mod+" installed")
        return True
    else:
        _logtext("module: "+mod+" could not be installed")
        return False
