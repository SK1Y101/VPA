def init():
    globals()["reminders"] = []
    globals()["dont_inst"] = []
    globals()["modules"] = ['pip', 'requests', 'setuptools', 'virtualenv']
    globals()["version"] = ""
    globals()["software"] = ""
    globals()["corepass"] = "corepass"
    globals()["mem"] = []
    globals()["self"] = "LOaBIS.py"
    globals()["desc"] = []
    globals()["cwords"] = []
    globals()["funcs"] = []
    ##all new globals are written before this
    ##this will load all of the defined globals
    globals()["user"] = "User"
    ##an example global

def addglobal(name="",value="",redefine=False):
    ##add a global, with given values
    if not name in globals():
        f = open("_core/settings.py","r")
        m = f.read()
        f.close()
        n = [m[0:16],m[16:len(m)]]
        m = n[0]+'globals()["'+str(name)+'"] = '+str(value)+"\n    "+n[1]
        f = open("_core/settings.py","w")
        f.write(m)
        f.close()
        return str(name)+" added successfully"
    #if the global doesn't exist, rewrite it into the file
    else:
        if redefine != False:
            globals()[str(name)] = value
            return str(name)+" redefined to "+str(value)
        else:
            return str(name)+" already a module"
        #else check if the user wishes to redefine the variable

if __name__ != "__main__":
    init()
    ##call the function to initialise the globals on startup
