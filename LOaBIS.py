import os,csv,importlib,datetime

def getcom(text=""):
    text = text+" "
    for x in settings.cwords:
        if x in text:
            x = settings.funcs[settings.cwords.index(x)]
            break
    try:
        globals()[x.replace(" ","")](text.replace(x,"").replace(settings.cwords[settings.funcs.index(x)],""))
    except Exception as inst:
        logtext("ERROR IN CODE EXECUTION:\n--------------------\n"+str(type(inst))+"\n-"+str(inst)+"\nDon't do ^That until the developers can fix it.\n--------------------")
        say("Function '"+text[0:text.index(" ")]+"' Does not exist")
    if x != "goodbye":
        interface()

def _say(text=""):
    for x in str(text)+"\n":
        sys.stdout.write(x)
        sleep(0.003)

def interface():
    say("\nWhat would you like me to do?")
    text = listen("> ")
    getcom(text)

def logtext(text="null"):
    text = text[0].upper()+text[1:len(text)]+"\n"
    y = open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text)
    y.close()

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    logtext("Initialising")
    modules = next(os.walk(os.getcwd()))[1]
    modules.sort()
    
    if "__pycache__" in modules:
        modules.pop(modules.index("__pycache__"))

    from _core import settings
    settings.addglobal("version",'""',True)
    f = open("_core/corememory.txt","r")
    file = csv.reader(f)
    mem = []
    for row in file:
        mem = mem+row
    settings.addglobal("mem",mem,True)
    f.close()
    settings.version = str(mem[mem.index("version number")+1])
    mem = []
    
    for x in modules:
        exec("from "+str(x)+" import *")
    logtext("Modules found: "+str(modules))
        
    from _core import settings
    settings.addglobal("funcs",[])
    settings.addglobal("cwords",[])
    settings.addglobal("desc",[])

    startup()

    _say("Importing functions:")
    import_start = datetime.datetime.now()
    for x in modules:
        if not x in settings.dont_inst:
            try:
                a = []
                f = open(x+"/commands.txt","r")
                file = csv.reader(f)
                for row in file:
                    line=row[0]
                    command=line.split(":")[0]
                    function = line.split(":")[1]
                    settings.funcs.append(function)
                    settings.cwords.append(command)
                    settings.desc.append(row[1])
                    a.append(function)
                f.close()
                logtext("Importing functions from: "+x+"; "+str(a))
            except:
                pass
        else:
            pass
    import_time = divmod((datetime.datetime.now()-import_start).total_seconds(), 60)
    logtext("All function imported, took "+str(import_time[0]*60+import_time[1])+" seconds")
    settings.funcs.append("null")
    settings.cwords.append("null ")
    settings.desc.append("a null function")
    _say("All found functions have been succesfully imported")
    
    elapsed_time = divmod((datetime.datetime.now()-start_time).total_seconds(), 60)
    logtext("Import successfull, took "+str(elapsed_time[0]*60+elapsed_time[1])+" seconds")
    
    interface()
