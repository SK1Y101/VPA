import sys,os,csv,datetime,importlib
from time import sleep

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
    try:
        y = settings.modules
        x = settings.dont_inst
        importlib.reload(settings)
    except:
        importlib.reload(settings)
    try:
        settings.modules = y
        settings.dont_inst = x
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
    say("goodbye")
    logtext("Closing software\n")

def showhelp(text=""):
    say("commands: description")
    for x in range(len(settings.cwords)):
        say(settings.cwords[x]+": "+settings.desc[x])
