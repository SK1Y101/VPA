import sys,os,csv,datetime,importlib,random
from _core import module
from time import sleep
module.modversion("_core","0.1.61","url")
module.dont_overwrite(["log.txt","UpdaterData.txt"])

def startup():
    from _core import settings,module
    _say("\n-- | Inintialising Startup Procedure | --")
    try:
        settings.addglobal("user",str(os.getlogin()[0].upper()+os.getlogin()[1:len(os.getlogin())]),True)
    except:
        settings.addglobal("user","User",True)
    settings.addglobal("self",'"'+str(os.path.basename(sys.argv[0]))+'"',True)
    settings.addglobal("mem",[],True)
    settings.addglobal("corepass",'"corepass"',True)
    settings.addglobal("cwords",[],True)
    settings.addglobal("funcs",[],True)
    settings.addglobal("desc",[],True)
    settings.addglobal("software",'""',True)
    settings.addglobal("version",'""',True)
    settings.addglobal("funcsatshutdown",[])
    try:
        y = settings.modules
        x = settings.dont_inst
        fas = settings.funcsatshutdown
        importlib.reload(settings)
    except:
        importlib.reload(settings)
    try:
        settings.modules = y
        settings.dont_inst = x
        settings.funcsatshutdown = fas
    except:
        module.init()
        
    readmemory()
    checkbackup()
    software = settings.software
    version = settings.version
    _say("-- | startup completed succesfully | --\n-- Initialising at time: "+str(datetime.datetime.now())+" --\n"+software+" "+version+"\n")
    logtext("starting "+software+" version "+version)
    
def logtext(text="null"):
    text = text[0].upper()+text[1:len(text)]+"\n"
    y = open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text)
    y.close()

def checkbackup():
    logtext("Checking backup")
    self = settings.self
    mem = settings.mem
    _say("-- Checking Core --")
    f = open("_core/corememory.txt","r")
    m = f.read()
    f.close()
    codecore = m[m.index("backup")+7:len(m)]
    _say("-- Comparing Core with backup --")
    f = open(self,"r")
    me = f.read()
    f.close()
    if me != codecore:
        logtext("Core modified, requesting pass")
        if _listen("Core pass required:\n> ") !=settings.corepass:
            say("-- Restoring Core --")
            f = open(self,"w")
            f.write(codecore)
            f.close()
            _say("-- Core Restored to backup version --")
            logtext("Core restored to backup")
            sys.exit()
        else:
            _say("-- Manual overwrite of Core --")
            logtext("core overwritten")
            writebackup()
    else:
        _say("-- No errors encountered --")
        logtext("Core backup check complete")

def writebackup():
    logtext("Writing core backup")
    mem = settings.mem
    self = settings.self
    _say("-- Reading self --")
    f = open(self,"r")
    m = f.read()
    f.close()
    t = mem.index("backup")
    mem = mem[0:t+1]
    mem.append(str(m)[0:len(str(m))-1])
    _say("-- Preparing Core for backup --")
    f = open("_core/corememory.txt","w")
    for x in mem:
        f.write(str(x)+"\n")
    f.close()
    _say("-- Core backup complete --")
    logtext("core backup complete")

def readmemory():
    logtext("Reading memory")
    _say("-- Initialising memory retrieval --")
    f = open("_core/corememory.txt","r")
    file = csv.reader(f)
    mem = []
    for row in file:
        mem = mem+row
    settings.addglobal("mem",mem,True)
    f.close()
    _say("-- memory retrieval complete --")
    settings.software = str(mem[mem.index("software name")+1])
    settings.version = str(mem[mem.index("version number")+1])
    try:
        user = mem[mem.index(str(os.getlogin()[0].upper()+os.getlogin()[1:len(os.getlogin())]))+1]
    except:
        user = "User"
    logtext("Memory loaded")
    
def _say(text=""):
    for x in str(text)+"\n":
        sys.stdout.write(x)
        sleep(0.003)

def say(text=""):
    for x in str(text)+"\n":
        sys.stdout.write(x)
        sleep(0.003)

def _listen(text=""):
    for x in str(text):
        sys.stdout.write(x)
        sleep(0.003)
    text = input()
    return text

def listen(text=""):
    for x in str(text):
        sys.stdout.write(x)
        sleep(0.003)
    text = input()
    return text

def goodbye(text=""):
    say("-- Quiting... Saving data... --")
    for x in settings.funcsatshutdown:
        try:
            try:
                exec("from .. import "+str(x.split(".")[0]))
            except:
                try:
                    exec("from . import "+str(x.split(".")[0]))
                except:
                    exec("import "+str(x.split(".")[0]))
            try:
                exec(str(x.split(".")[0]).replace("()","")+"()")
            except:
                exec(str(x).replace("()","")+"()")
        except Exception as inst:
            logtext("ERROR IN CODE EXECUTION:\n--------------------\n"+str(type(inst))+"\n-"+str(inst)+"\nDon't do ^That until the developers can fix it.\n--------------------")
    settings.addglobal("funcsatshutdown",[],True)
    writebackup()
    say("-- Shutdown complete, goodbye --")
    logtext("Closing software\n")

def showhelp(text=""):
    say("commands: description\n(Some functions have been ommitted due to shared functionality, to see all functions, type fullhelp)")
    for x in range(len(settings.cwords)):
        if settings.funcs.index(settings.funcs[settings.cwords.index(settings.cwords[x])]) == x:
            say(settings.cwords[x]+": "+settings.desc[x])

def showfullhelp(text=""):
    say("commands: description")
    for x in range(len(settings.cwords)):
        say(settings.cwords[x]+": "+settings.desc[x])

def encrypt(text="",key="`"):
    y=""
    text = text.replace(chr(9),"____-__-").replace(chr(10),"____-_-_")
    for x in range(len(str(text))):
        y+=chr(((ord(text[x])+ord(key[x%len(key)])-128)%96)+32)
    return y

def decrypt(text="",key="`"):
    y=""
    for x in range(len(str(text))):
        y+=chr(((ord(text[x])-ord(key[x%len(key)])-128)%96)+32)
    return y.replace("____-__-",chr(9)).replace("____-_-_",chr(10))

def decryptfromfile(file="",pas=""):
    ##will return a list of the decrypted contents of the file
    try:
        f = open(file,"r")
        m = decrypt(f.read(),file+pas).split(chr(10))
        f.close()
        y=[]
        for x in m:
            y.append(decrypt(x.split("__-_--__")[1],x.split("__-_--__")[0]).split(","))
        return y
    except:
        return []
    
def encrypttofile(file="",m=[],pas=""):
    ##will encrypt a list into a file
    y=""
    for x in m:
        key=""
        w=""
        for v in x:
            w+=v+","
        for z in range(random.randint(30,50)):
            key+=chr(random.randint(32,96))
        y+=key+"__-_--__"+encrypt(w[:-1],key)+"____-_-_"
    f = open(file,"w")
    f.write(encrypt(y[:-4],file+pas))
    f.close()

def resetpip(text=""):
    import subprocess
    logtext("user has selected to remove pip modules")
    x = str(subprocess.check_output("pip list",shell=True))
    x = x[2:len(x)-1]
    not_inst = []
    modules = []
    while ")" in x:
        x = x[0:x.index("(")-1]+"\n"+x[x.index(")")+5:len(x)]
    while "\n" in x:
        modules.append(x[0:x.index("\n")])
        x = x[x.index("\n")+1:len(x)]

    modules.pop(modules.index("pip"))
    modules.pop(modules.index("setuptools"))
    modules.pop(modules.index("virtualenv"))
        
    if listen("Are you sure you wish to remove pip modules?\n> ").lower() in ["yes","y"]:
        for x in modules:
            logtext("Uninstalling: "+x)
            say("uninstalling: "+x)
            subprocess.call("pip uninstall "+str(x))
        say("Pip modules uninstalled, You will have to close the software to prevent major system erros")
