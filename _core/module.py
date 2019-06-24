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
    '''used to define the module version.
    name    the name of the module
    version the LOaBIS version the module is designed to run for
    url     the web address of the online repository storing the module
    ie:
    module("reminders","0.2.02","N/A")
    -tells LOaBIS which version the module was written for, helps prevent errors from redundant programing and when updating the modules'''
    return True

def needs(modules=[]):
    '''used to set a list of pythonic modules that a LOaBIS module requires
    modules is a list containing all of the python modules (always a list, even if there is only one requirement.)
    ie
    needs(["wolframalpha","six"])
    -tells LOaBIS to check for, and download wolframalpha and six, if they are not on the host machine'''
    return True

def startup(funcs=[]):
    '''used to set a list of functions that must be performed at launch
    (always a list, even if there is only one requirement.)
    ie:
    startup([loadreminders])
    -tells LOaBIS to run loadreminders on startup'''
    return True

def shutdown(funcs=[]):
    '''used to set a list of functions to be execeuted at shutdown.
    (always a list, even if there is only one requirement.)
    ie:
    shutdown([savereminders])
    -tells LOaBIS to run savereminders when it shutsdown'''
    return True

def persist(funcs=[]):
    '''used to set a list of functions that will be performed at regular intervals
    (always a list, even if there is only one requirement.)
    ie:
    persist([fetchdata])
    -tells LOaBIS to run fetchdata at regular intervals'''
    return True

def hasdependancy(mods=[]):
    '''used to set a list of LOaBIS functions that must be loaded before itself
    (always a list, even if there is only one requirement.)
    ie:
    hasdependancy([basicui])
    -tells LOaBIS to load basicui first'''
    return True

def dont_overwrite(files=[]):
    '''required by the updater to prevent it replacing data files.
    (always a list, even if there is only one requirement.)
    ie:
    dont_overwrite(["reminders.txt"])
    -prevents the updater from overwriting reminders.txt'''
    return True

def replacefunction(funcs=[],replacement=[]):
    '''this is used to allow the overwritting of one funcion to another, each function in the replacement list must map to the function it will replace in the funcs list
    (always a list, even if there is only one requirement.)
    ie:
    replacefunction([say,listen],[speak,hear])
    -replaces the functions say and listen with speak and hear'''
    return True

def _logtext(text="null"):
    '''Writes the text to the runtime log
    ie:
    _logtext("Initialisation started")
    '''
    y = open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text[0].upper()+text[1:len(text)]+"\n")
    y.close()

def getmods():
    '''gets all of the installed LOaBIS Modules'''
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
    '''loads all of the LOaBIS modules, unless they've already been loaded
    ie:
    checkmods(["reminders","queries","basicui"])'''
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
    '''Installs the required python module if not found
    ie:
    installmodule("wolframalpha")'''
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
