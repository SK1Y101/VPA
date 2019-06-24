import csv,sys,datetime,os,random
from . import module
from time import sleep

def main():
    module.module("_core","0.2.00","N/A")
    module.startup([checkbackup])

def init():
    globals()["coremem"] = []
    globals()["self"] = str(os.path.basename(sys.argv[0]))

def say(text=""):
    for x in str(text)+"\n":
        sys.stdout.write(x)
        sleep(0.003)

def _say(text=""):
    for x in str(text)+"\n":
        sys.stdout.write(x)
        sleep(0.003)

def listen(text=""):
    for x in str(text)+"\n> ":
        sys.stdout.write(x)
    return input()

def showhelp(text=""):
    if module.cwords:
        say("commands: description\n(Some functions have been ommitted due to shared functionality, to see all functions, type fullhelp)")
        for x in range(len(module.cwords)):
            if module.funcs.index(module.funcs[module.cwords.index(module.cwords[x])]) == x:
                say(module.cwords[x]+": "+module.desc[x])
    else:
        say("No functions available to show help!")

def showfullhelp(text=""):
    if module.cwords:
        say("commands: description")
        for x in range(len(module.cwords)):
            say(module.cwords[x]+": "+module.desc[x])
    else:
        say("No functions available to show help!")

def _logtext(text="null"):
    text = text[0].upper()+text[1:len(text)]+"\n"
    y = open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text)
    y.close()
    
def getdata(filepath=""):
    f = open(str(filepath),"r")
    file = csv.reader(f)
    mem = []
    for row in file:
        mem +=row
    f.close()
    return mem

def savedata(filepath="",data=[]):
    mem =""
    for x in data:
        mem = mem+x+"\n"
    f = open(str(filepath),"w")
    f.write(mem)
    f.close()

def getmodinfo(module=""):
    try:
        f = open(str(module)+"/__init__.py")
        m = f.read()
        f.close()
        name,ver,url = m.split("module.module(")[1].split(")")[0].replace('"',"").split(",")
        mods,startup,persist,depend,shutdown = [],[],[],[],[]
        try:
            if not name == "_core":
                mods = m.split("module.needs([")[1].split("])")[0].replace('"',"").split(",")
        except:
            mods = []
        try:
            if not name == "_core":
                depend = m.split("module.hasdependancy([")[1].split("])")[0].replace('"',"").split(",")
        except:
            depend = []
        try:
            startup = m.split("module.startup([")[1].split("])")[0].replace('"',"").split(",")
        except:
            startup = []
        try:
            if not name == "_core":
                persist = m.split("module.persist([")[1].split("])")[0].replace('"',"").split(",")
        except:
            persist = []
        try:
            if not name == "_core":
                shutdown = m.split("module.shutdown{[")[1].split("])")[0].replace('"',"").split(",")
        except:
            shutdown = []
        return name,ver,url,mods,depend,startup,persist,shutdown
    except:
        return module,"0.0.00","None",[],[],[],[],[]

def simver(corever="",modver=""):
    if corever == modver:
        return 1
    elif (corever.split(".")[1] == modver.split(".")[1]) and (corever.split(".")[2][0] == modver.split(".")[2][0]):
        return 2
    else:
        return 0

def checkdata(data=[]):
    tempdata=[]
    for x in data:
        tempdata.append(str(x))
    from collections import Counter
    _logtext("Checking "+str(len(tempdata))+" data lists")
    out = Counter(tempdata).most_common(1)[0][0]
    _logtext("Data entry "+str(tempdata.index(out))+" returned as suspected true value")
    return data[tempdata.index(out)]

def getcoredata():
    try:
        _logtext("Retreiving core data files")
        try:
            globals()["coremem"] = getdata("_core/corememory.txt")
        except:
            globals()["coremem"] = getdata("corememory.txt")
        _logtext("Data core retrieval complete")
    except:
        _logtext("An issue occured loading data, using temporary backup")
        globals()["coremem"] = []
    return coremem

def checkbackup():
    if len(coremem) == 0:
        getcoredata()
    _logtext("Retrieving backup")
    _say("Retrieving core backup")
    try:
        codecore = coremem[coremem.index("<backup>")+1:coremem.index("</backup>")]
    except:
        codecore = getdata(self)
        _logtext("No core backup available")
    _logtext("Comparing core to backup")
    me = getdata(self)
    if me != codecore:
        _logtext("Modified core detected, requesting pass")
        if input("Corepass required:\n> ") != "LOaBIS":
            f = open(self,"w")
            for x in codecore:
                f.write(x)
            f.close()
            _logtext("Core restored to backup version")
            sys.exit()
        else:
            _logtext("Core overwrite authorised")
            writebackup()
    else:
        _logtext("Core backup check complete")
    _say("Core backup check complete")
    
def writebackup():
    _logtext("Writing core backup")
    _say("Writing core backup")
    if len(coremem) == 0:
        getcoredata()
    me = getdata(self)
    _logtext("Updating backup with core")
    if "<backup>" in coremem:
        mem = coremem[0:coremem.index("<backup>")+1]+me+coremem[coremem.index("</backup>"):len(coremem)]
    else:
        mem = coremem+["<backup>"]+me+["</backup>"]
    _logtext("writing backups")
    savedata("_core/corememory.txt",mem)
    mem = []
    _logtext("Core backup complete")
    _say("Core backup complete")

def closesoftware(text=""):
    print()
    start_time = datetime.datetime.now()
    _logtext("Shutting down software")
    _logtext("Checking shutdown functions")
    if module.shutdownfunc:
        _say("Performing shutdown functions")
        for x in module.shutdownfunc:
            a = 1
        _logtext("Shutdown functions completed")
    else:
        _logtext("No shutdown functions required")
    writebackup()
    elapsed_time = divmod((datetime.datetime.now()-start_time).total_seconds(),60)
    _logtext("shutdown completed successfully, took "+str(elapsed_time[0]*60+elapsed_time[1])+" seconds\n")
    _say("Shutdown completed successfully, you may now quit the program safely")

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
