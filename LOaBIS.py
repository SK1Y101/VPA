import sys, threading, datetime, os
from time import sleep

def _say(text=""):
    for x in str(text)+"\n":
        sys.stdout.write(x)
        sleep(0.003)

def _logtext(text="null"):
    y = open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text[0].upper()+text[1:len(text)]+"\n")
    y.close()

def getmem(text="",coremem=[]):
    if not text[0] == "<":
        text = "<"+text+">"
    if not coremem:
        coremem = getcoredata()
    return coremem[coremem.index(text)+1:coremem.index("</"+text[1:len(text)])]

def getcom(text=""):
    text+=" "
    for x in module.cwords:
        if x in text:
            x = module.funcs[module.cwords.index(x)]
            break
    _logtext("Function: "+x.replace(" ","")+" requested by user")
    try:
        globals()[x.replace(" ","")](text.replace(x,"").replace(module.cwords[module.funcs.index(x)],""))
    except Exception as e:
        _logtext("Could not perform function: "+str(x)+"\nError: "+str(type(e))+"; "+str(e))
        say("The function, "+str(x)+" could not be executed\n")
    if not x.replace(" ","") == "closesoftware":
        getcom(listen("What would you like to do?"))

if __name__ == "__main__":
    try:
        start_time = datetime.datetime.now()
        _logtext("Initialising Software")
        _say("Initialising Software")
        modules = next(os.walk(os.getcwd()))[1]
        modules.sort()

        if "__pycache__" in modules:
            modules.pop(modules.index("__pycache__"))

        if "_core" in modules:
            modules.pop(modules.index("_core"))

        _logtext(str(len(modules))+" Modules located: "+str(modules))

        from _core import *
        init()
        corever = getmodinfo("_core")[1]
        _logtext("Core version: "+corever+" Loaded")

        stable = 0
        unstable = 0
        not_inst = []

        _logtext("Checking module dependancies")
        _say("Checking module dependancies")
        a = modules
        for x in a:
            b = getmodinfo(x)
            depend = b[4]
            if depend:
                if depend in modules:
                    modules.pop(modules.index(x))
                    modules.insert(modules.index(depend)+1,x)
                else:
                    not_inst.append(x)
                    modules.pop(modules.index(x))
        if len(a)-len(modules):
            _logtext(str(len(a)-len(modules))+" Modules missing dependencies")
                
        _logtext("Loading modules")
        _say("Loading modules")
        for x in modules:
            a = getmodinfo(x)
            modver = a[1]
            needed = a[3]
            b = simver(corever,modver)
            if b != 0:
                if module.checkmods(needed):
                    exec("from "+str(x)+" import *")
                    if b == 1:
                        stable+=1
                    else:
                        unstable+=1
                else:
                    not_inst.append(x)
                    modules.pop(modules.index(x))
            else:
                not_inst.append(x)
                modules.pop(modules.index(x))
        if stable:
            _logtext(str(stable)+" stable Modules loaded")
        if unstable:
            _logtext(str(unstable)+" Unstable Modules loaded")
        if not_inst:
            _logtext(str(len(not_inst))+" Modules prevented from loading: "+str(not_inst))
        _say(str(len(not_inst))+" Modules prevented from loading")

        import_start = datetime.datetime.now()
        modules.insert(0,"_core")
        _logtext("Importing functions from: "+str(modules))
        _say("Importing functions")
        for x in modules:
            try:
                a = []
                f = open(x+"/commands.txt","r")
                file = csv.reader(f)
                for row in file:
                    module.funcs.append(row[0].split(":")[1])
                    command = row[0].split(":")[0]
                    if not command[-1:] == " ":
                        command+=" "
                    module.cwords.append(command)
                    module.desc.append(row[1])
                    a.append(row[0].split(":")[1])
                f.close()
                _logtext("Importing functions from: "+str(x)+"; "+str(a))
            except Exception as e:
                _logtext("Could not load functions from: "+str(x)+"\nError: "+str(type(e))+"; "+str(e))
        import_time = divmod((datetime.datetime.now()-import_start).total_seconds(),60)
        _logtext("Function import complete, took "+str(import_time[0]*60+import_time[1])+" seconds")
        module.funcs.append("null")
        module.cwords.append("null")
        module.desc.append("a null function")

        _logtext("Retrieving startup functions")
        _say("Retrieving startup functions")
        a = 0
        for x in modules:
            start = getmodinfo(x)[5]
            if start:
                a+=1
                for y in start:
                    module.startfunc.append(y)                
        if module.startfunc:
            _say(str(len(module.startfunc))+" Startup functions located, executing")
            _logtext(str(len(module.startfunc))+" Startup functions loaded from "+str(a)+" modules")
            for x in module.startfunc:
                try:
                    globals()[str(x)]()
                except Exception as e:
                    _logtext("Could not perform startup function: "+str(x)+"\nError: "+str(type(e))+"; "+str(e))
        else:
            _logtext("No startup functions required")

        _logtext("Retrieving shutdown functions")
        _say("Retrieving shutdown functions")
        a = 0
        for x in modules:
            shutdown = getmodinfo(x)[7]
            if shutdown:
                a+=1
                for y in shutdown:
                    module.shutdownfunc.append(y)                
        if module.startfunc:
            _logtext(str(len(module.shutdownfunc))+" Shutdown functions loaded from "+str(a)+" modules")
        else:
            _logtext("No shutdown functions required")
            
        _logtext("Retrieving persistent functions")
        _say("Retrieving persistent functions")
        a = 0
        for x in modules:
            pers = getmodinfo(x)[6]
            if pers:
                a+=1
                module.permods.append(x)
                for y in pers:
                    module.persistfunc.append(y)
        if module.persistfunc:
            _say("Starting up "+str(len(module.persistfunc))+" persistent functions")
            _logtext(str(len(module.startfunc))+" Persistent functions loaded from "+str(a)+" modules")
            ##WRITE CODE HERE TO RUN PERSISTENT FUNCTIONS> Please
        else:
            _logtext("No persistent functions loaded")

        elapsed_time = divmod((datetime.datetime.now()-start_time).total_seconds(),60)
        _logtext("Import successfull, took "+str(elapsed_time[0]*60+elapsed_time[1])+" seconds")
        _say("Software initialised")
        print()

        coremem = getcoredata()
        for x in getmem("logo",coremem):
            print(x)
        _say((getmem("software",coremem))[0])
        _say("Version "+corever+" developed by "+str(getmem("development",coremem)[0]).split("\t")[0])
        print()

        getcom(listen("What would you like to do?"))
        
    except Exception as e:
        _logtext("Software aborted unexpectedly, Consider submitting log to developers.\nError: "+str(type(e))+"; "+str(e)+"\n")
