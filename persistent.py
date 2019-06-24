import sys,time,socket,threading,datetime,os
globals()["arg"],globals()["closed"]=str(sys.argv).split("version:")[1],0
globals()["corever"],globals()["arg"]=arg.split("#")

def main():
    from _core import _say
    _say("Persistence module Initialising")
    _logpers("Initialising Persistence module")
    os.system("title LOaBIS v"+str(corever)+" - Persistence module")
    passed = str(arg[1:]).replace("['","").replace("']","")
    modules,functions=passed.split(":")[0].split(";")[0:-1],passed.split(":")[1].split(";")[1:-1]
    _logpers("Functions loaded from modules")
    for x in modules:
        exec("from "+str(x).replace("core","_core")+" import *")
    _logpers("Modules imported")
    globals()["main_program"],t=start_client(multiply("LOaBIS")),0
    t1=threading.Thread(name="checkclose",target=getclosed)
    t1.start()
    _logpers("Executing main loop")
    _say("Initialisation finalising, executing main program\n")
    while closed!=1:
        if int(datetime.datetime.now().minute)%2==0:
            if datetime.datetime.now().second==0:
                t=1
        if t==1:
            time.sleep(2)
            t=0
            _say("Executing persistence functions:\n")
            for x in functions:
                exec(str(x)+"()")

def _logpers(text="null"):
    from _core import _logtext
    _logtext("Persistence Module: "+str(text))

def getclosed():
    while True:
        message=get_message(main_program)
        if "shutdown" in message:
            break
    globals()["closed"]=1

def multiply(text="",maxv=2**16):
    a=1
    for x in str(text):
        a*=ord(x)
    return a%maxv

def get_message(client=""):
    message=str(client.recv(int(client.recv(8).decode("utf-8"))).decode("utf-8"))
    return message

def start_client(port=10000):
    _logpers("connecting to LOaBIS")
    client = socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
    client.connect(("localhost",port))
    _logpers("connection established on port: "+str(port))
    return client

try:
    main()
except Exception as e:
    _say("Unexpected abort occured")
    _logpers("Software aborted unexpectedly, Consider submitting log to developers.\nError: "+str(type(e))+"; "+str(e)+"\n")
    time.sleep(3)
