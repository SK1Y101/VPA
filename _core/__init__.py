import csv,sys,datetime,os,random,subprocess
from . import module
from time import sleep

def main():
    module.module("_core","0.2.05","N/A")
    module.startup([checkbackup])

def init():
    globals()["coremem"],globals()["self"]=[],str(os.path.basename(sys.argv[0]))

def say(text=""):
    for x in str(text)+"\n":
        sys.stdout.write(x)
        sleep(0.003)

def makelen(text="",leng=0,inte=0):
    text=str(text)
    while len(text)<leng:
        if inte==1:
            text="0"+text
        else:
            text+=" "
    return text[0:leng]

def quicksay(text=""):
    print(text)

def _say(text=""):
    for x in "System: "+str(text)+"\n":
        sys.stdout.write(x)
        sleep(0.003)

def listen(text=""):
    for x in str(text)+"\n> ":
        sys.stdout.write(x)
        sleep(0.003)
    return input()

def showhelp(text=""):
    if module.cwords:
        reqlen=int(len(max(module.cwords,key=len)))
        say(makelen("commands",reqlen)+": description\n(Some functions have been ommitted due to shared functionality, to see all functions, type fullhelp)")
        for x in range(len(module.cwords)):
            if module.funcs.index(module.funcs[module.cwords.index(module.cwords[x])])==x:
                say(makelen(module.cwords[x],reqlen)+": "+module.desc[x])
    else:
        say("No functions available to show help!")

def showfullhelp(text=""):
    if module.cwords:
        reqlen=int(len(max(module.cwords,key=len)))
        say(makelen("commands",reqlen)+": description")
        for x in range(len(module.cwords)):
            say(makelen(module.cwords[x],reqlen)+": "+module.desc[x])
    else:
        say("No functions available to show help!")

def _logtext(text="null"):
    text=text[0].upper()+text[1:len(text)]+"\n"
    y=open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text)
    y.close()

def getdata(filepath=""):
    f=open(str(filepath),"r")
    file=csv.reader(f)
    mem=[]
    for row in file:
        mem +=row
    f.close()
    return mem

def savedata(filepath="",data=[]):
    mem=""
    for x in data:
        mem=mem+x+"\n"
    f=open(str(filepath),"w")
    f.write(mem)
    f.close()

def getmodinfo(module=""):
    try:
        f=open(str(module)+"/__init__.py")
        m=f.read()
        f.close()
        name,ver,url=m.split("module.module(")[1].split(")")[0].replace('"',"").split(",")
        mods,startup,persist,depend,shutdown,old,new=[],[],[],[],[],[],[]
        try:
            if not name=="_core":
                mods=m.split("module.needs([")[1].split("])")[0].replace('"',"").split(",")
        except:
            mods=[]
        try:
            if not name=="_core":
                depend=m.split("module.hasdependancy([")[1].split("])")[0].replace('"',"").split(",")
        except:
            depend=[]
        try:
            startup=m.split("module.startup([")[1].split("])")[0].replace('"',"").split(",")
        except:
            startup=[]
        try:
            if not name=="_core":
                persist=m.split("module.persist([")[1].split("])")[0].replace('"',"").split(",")
        except:
            persist=[]
        try:
            if not name=="_core":
                shutdown=+m.split("module.shutdown([")[1].split("])")[0].replace('"',"").split(",")
        except:
            shutdown=[]
        try:
            if not name=="_core":
                replaced=m.split("module.replacefunction([")[1].split("])")[0].replace('"',"").replace(",[","").replace("[","")
                old,new=replaced.split("]")[0].split(","),replaced.split("]")[1].split(","),
        except:
            old,new=[],[]

        return name,ver,url,mods,depend,startup,persist,shutdown,old,new
    except:
        return module,"0.0.00","None",[],[],[],[],[],[],[]

def simver(corever="",modver=""):
    minv=corever.split(".")[0]+"."+corever.split(".")[1]+".00"
    if minv<=modver<=corever:
        return 2
    elif (minv.split(".")[0:2]==modver.split(".")[0:2]) or (corever.split(".")[0:2]==modver.split(".")[0:2]):
        return 1
    else:
        return 0

def checkdata(data=[]):
    tempdata=[]
    for x in data:
        tempdata.append(str(x))
    from collections import Counter
    _logtext("Checking "+str(len(tempdata))+" data lists")
    out=Counter(tempdata).most_common(1)[0][0]
    _logtext("Data entry "+str(tempdata.index(out))+" returned as suspected true value")
    return data[tempdata.index(out)]

def getcoredata():
    try:
        _logtext("Retreiving core data files")
        try:
            globals()["coremem"]=getdata("_core/corememory.txt")
        except:
            globals()["coremem"]=getdata("corememory.txt")
        _logtext("Data core retrieval complete")
    except:
        _logtext("An issue occured loading data, using temporary backup")
        globals()["coremem"]=[]
    return coremem

def checkbackup():
    if len(coremem)==0:
        getcoredata()
    a="Retrieving core backup"
    _logtext(a)
    _say(a)
    try:
        codecore=coremem[coremem.index("<backup>")+1:coremem.index("</backup>")]
    except:
        codecore=getdata(self)
        _logtext("No core backup available")
    _logtext("Comparing core to backup")
    me=getdata(self)
    if me !=codecore:
        _logtext("Modified core detected, requesting pass")
        if input("Corepass required:\n> ") !="LOaBIS":
            f=open(self,"w")
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
    a="writing core backup"
    _logtext(a)
    _say(a)
    if len(coremem)==0:
        getcoredata()
    me=getdata(self)
    _logtext("Updating backup with core")
    if "<backup>" in coremem:
        mem=coremem[0:coremem.index("<backup>")+1]+me+coremem[coremem.index("</backup>"):len(coremem)]
    else:
        mem=coremem+["<backup>"]+me+["</backup>"]
    _logtext("writing backups")
    savedata("_core/corememory.txt",mem)
    mem,a=[],"Core backup complete"
    _logtext(a)
    _say(a)

def closesoftware(text=""):
    print()
    start_time=datetime.datetime.now()
    _logtext("Shutting down software, Checking shutdown functions")
    if module.shutdownfunc:
        _say("Performing shutdown functions")
        for x in module.shutdownfunc:
            a=1
        _logtext("Shutdown functions completed")
    else:
        _logtext("No shutdown functions required")
    writebackup()
    elapsed_time=divmod((datetime.datetime.now()-start_time).total_seconds(),60)
    _logtext("shutdown completed successfully, took "+str(elapsed_time[0]*60+elapsed_time[1])+" seconds\n")
    _say("Shutdown completed successfully, you may now quit the program safely")

def multiply(text="",maxv=2**16):
    a=1
    for x in str(text):
        a*=ord(x)
    return a%maxv

def startlocalserver(port=10000):
    import socket
    server=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    server.bind(("localhost",port))
    server.listen(1)
    return server

def addlocalclient(server=""):
    client,address=server.accept()
    send_message(client,"connection established")
    return client

def send_message(client="",message=""):
    length=str(len(message))
    while len(length)<8:
        length="0"+length
    client.send(str(length).encode("utf-8"))
    client.send(str(message[0:10**8]).encode("utf-8"))

def get_message(client=""):
    message=str(client.recv(int(client.recv(8).decode("utf-8"))).decode("utf-8"))
    return message

def getmem(text="",coremem=[]):
    if not text[0]=="<":
        text="<"+text+">"
    if not coremem:
        coremem=getcoredata()
    return coremem[coremem.index(text)+1:coremem.index("</"+text[1:len(text)])]

def getmods(txt=""):
    mod=str(txt).replace(" ","").replace("pip","").replace("setuptools","")
    mod=''.join([i for i in mod if not i.isdigit()])
    mod = list(filter(None, mod.replace(".","").split("\\r\\n")))
    return mod[2:-1]

def getpip():
    try:
        subprocess.call("python -m pip install --upgrade pip",shell=True)
    except:
        pass
    try:
        try:
            return subprocess.check_output("pip3 list",shell=True)
        except:
            return subprocess.check_output("pip list",shell=True)
    except:
        return ""

def remmods(mod=[]):
    for x in mod:
        try:
            subprocess.call("pip3 uninstall "+str(x))
        except:
            subprocess.call("pip uninstall "+str(x))

def clearpip(text=""):
    a="Removing non-essential pip modules"
    _logtext(a)
    _say(a)
    remmods(getmods(getpip()))
    a="Removal finished"
    _logtext(a)
    _say(a)

def encrypt(text="",key="`"):
    y=""
    text=text.replace(chr(9),"____-__-").replace(chr(10),"____-_-_")
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
        f=open(file,"r")
        m=decrypt(f.read(),file+pas).split(chr(10))
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
    f=open(file,"w")
    f.write(encrypt(y[:-4],file+pas))
    f.close()
