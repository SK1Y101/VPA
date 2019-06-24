import os, subprocess,threading, datetime
from tkinter import *
from tkinter.ttk import *

def init():
    try:
        globals()["data"] = getdata("UpdaterData.txt")
        globals()["def_dir"] = os.getcwd()
        globals()["directories"] = []
        globals()["vpadirectory"] = ""
        if data[data.index("default_directory")+1] == "None":
            logtext("No default directory found, opening wizard")
            startup()
        else:
            logtext("Starting Module Updater")
            globals()["vpadirectory"] = removeextension(data[data.index("default_directory")+1])
            main()
    except Exception as inst:
        logtext("ERROR IN CODE EXECUTION:\n--------------------\n"+str(type(inst))+"\n-"+str(inst)+"\nDon't do ^That until the developers can fix it.\n--------------------")

def logtext(text="null"):
    text = text[0].upper()+text[1:len(text)]+"\n"
    y = open("log.txt","a")
    y.write("["+str(datetime.datetime.now())+"] - "+text)
    y.close()

def removeextension(dird=""):
    y = dird
    for x in range(len(y)):
        if y[len(y)-1-x] in ["/","\\"]:
            break
    y = y[0:len(y)-1-x]
    return y

def openDir(dird=""):
    try:
        try:
            subprocess.Popen('explorer "{0}"'.format(def_dir))
        except:
            subprocess.Popen('explorer "{0}"'.format(dird))
    except:
        subprocess.Popen('explorer "{0}"'.format(os.getcwd()))

def getVPAversion(dird=""):
    try:
        if dird != "":
            f = open(dird+"\\_core\\corememory.txt","r")
        else:
            f = open(def_dir+"\\_core\\corememory.txt","r")
        y = f.read().split("\n")
        f.close()
        return y[y.index("version number")+1]
    except:
        return "0.0.00"

def getinstalled():
    modules = next(os.walk(vpadirectory))[1]
    modules.sort()
    if "__pycache__" in modules:
        modules.pop(modules.index("__pycache__"))
    for x in modules:
        modules[modules.index(x)] = x+"\\__init__.py"
    return modules

def getversions():
    modules = getinstalled()
    mem = []
    logtext("Fetching installed module data for "+str(modules))
    for x in modules:
        f = open(x,"r")
        y = f.read()
        f.close()
        z = y[y.index("modversion")+len("modversion"):y.index(")")+1]
        z = z.replace("(","").replace(")","").replace('"',"").split(",")
        mem.append(z[0])
        mem.append(z[1])
        mem.append(z[2])
    logtext("Data retrieved")
    return mem

def getonlinever(name="VPA",url="https://www.dropbox.com/sh/yucoglcwxirfkoq/AAATgGPh961ept6AHtWN8CyFa?dl=0"):
    import urllib.request
    response = urllib.request.urlopen(url)
    y = response.read().decode('utf-8')
    response.close()
    ver = []
    webhost = str(url[0:3+len(url.split("//")[0])+url.split("//")[1].index("/")])
    y = y.split(webhost)
    for x in y:
        if "/"+name+"%" in x:
            z = (webhost+x)
            aa = [z[z.index(name+"%20")+len(name)+3:z.index("?dl=0")],z[0:z.index('"')]]
            if not aa in ver:
                ver.append(aa)
            z=""
            aa=""
    logtext("Fetching most up to date VPA version data")
    return ver

def getonlinemodules():
    import urllib.request
    url = 'https://www.dropbox.com/s/lhixedpidsarpxk/Modules.txt?dl=1' #dl=1 is important
    u = urllib.request.urlopen(url)
    data = u.read()
    u.close()
    with open("Tempfile.txt", "wb") as f :
        f.write(data)
    f.close()
    logtext("Fetching Modules")

def getmoduleurl():
    import csv
    mem=[]
    getonlinemodules()
    f = open("Tempfile.txt","r")
    file = csv.reader(f)
    for row in file:
        mem.append(row[0])
        mem.append(row[1])
    f.close()
    os.remove("Tempfile.txt")
    return mem

def initialload():
    logtext("Initialisation")
    ptext.set("Getting VPA versions")
    progress.start()
    globals()["online_version"] = getonlinever()
    ptext.set("Getting local versions")
    globals()["local_version"] = getVPAversion()
    ptext.set("Loading Module base")
    globals()["online_modules"] = getmoduleurl()
    ptext.set("Retrieving local modules")
    globals()["local_modules"] = getversions()
    logtext("Modules, directories and versions retrieved")
    progress.stop()
    progress.configure(maximum=int(len(online_modules)))
    globals()["module_versions"] = []

    latestcorever,latestcoredl = (online_version[len(online_version)-1])[0].replace(".rar","").replace(".zip",""),(online_version[len(online_version)-1])[1]
    if latestcorever > local_version:
        core_update = "available"
    else:
        core_update = "-"

    if core_update !="-":
        b = Button(ml,text=core_update,command=lambda n="_core",l=latestcorever,ldl=latestcoredl: updatever(n,l,ldl)).grid(row=1,column=1,sticky=W+E)
    else:
        b = Button(ml,text=core_update,state=DISABLED).grid(row=1,column=1,sticky=W+E)
        
    b = Button(ml,text="VPA Core",command=lambda n="_core",l=latestcorever,v=online_version: onnameclick(n,l,v),state=DISABLED).grid(row=1,column=2,sticky=W+E)
    b = Button(ml,text=local_version,state=DISABLED).grid(row=1,column=3,sticky=W+E)
    b = Button(ml,text=latestcorever,state=DISABLED).grid(row=1,column=4,sticky=W+E)

    updatetable()
        
    ptext.set("Loading complete!")
    logtext("Initialisation complete")
    progress.configure(value=0)

def updatetable():
    logtext("Fetching new module data")
    for x in range(int(len(online_modules)/2)):
        ptext.set(str(x+1)+"/"+str(int(len(online_modules)/2))+" - Retrieving "+str(online_modules[2*x]))
        name = online_modules[2*x]
        module_versions.append(name)
        module_versions.append(getonlinever(str(online_modules[2*x]),online_modules[2*x+1]))
        progress.step(1)
        
        latetsverdl = ((module_versions[2*x+1])[len(module_versions[2*x+1])-1])[1].replace("?dl=0","?dl=1")
        latestver = ((module_versions[2*x+1])[len(module_versions[2*x+1])-1])[0].replace(".rar","").replace(".zip","")
        try:
            installedver = local_modules[local_modules.index(name)+1]
            if latestver > installedver:
                updates = "available"
            else:
                updates="-"
            installed=1
        except:
            installed=0
            installedver = "0.0.00"
            updates = "-"
            
        if installed == 1:
            tickvar = BooleanVar()
            tickvar.set(True)
            if latestver != installedver:
                mods_to_inst.append(name)
                mods_to_inst.append(installedver)
                mods_to_inst.append(latestver)
            b = Checkbutton(ml,text="Installed",variable=tickvar,command=lambda v=tickvar,n=name,cv=installedver,lv=latestver: ontick(v,n,cv,lv)).grid(ipadx=10,row=x+2,column=0,sticky=W+E)
        else:
            tickvar = BooleanVar()
            tickvar.set(False)
            b = Checkbutton(ml,text="Installed",variable=tickvar,command=lambda v=tickvar,n=name,cv=installedver,lv=latestver: ontick(v,n,cv,lv)).grid(ipadx=10,row=x+2,column=0,sticky=W+E)
            
        if (installed == 1) and (updates!="-"):
            b = Button(ml,text=updates,command=lambda n=name,l=latestver,ldl=latetsverdl: updatever(n,l,ldl)).grid(row=x+2,column=1,sticky=W+E)
        else:
            b = Button(ml,text=updates,state=DISABLED).grid(row=x+2,column=1,sticky=W+E)
        if installedver == "0.0.00":
            instvertext = "-"
        else:
            instvertext = installedver
        versions = module_versions[2*x+1]
        b = Button(ml,text=name,command=lambda n=name,l=latestver,v=versions: onnameclick(n,l,v)).grid(row=x+2,column=2,sticky=W+E)
        b = Button(ml,text=instvertext,state=DISABLED).grid(row=x+2,column=3,sticky=W+E)
        b = Button(ml,text=latestver,state=DISABLED).grid(row=x+2,column=4,sticky=W+E)
        progress.step(1)
        #use "command=lambda: ["function"](x, y, z, ...)" to pass variables into a function.

def ontick(v="",name="",current="",newest=""):
    if v.get():
        if current != newest:
            mods_to_inst.append(name)
            mods_to_inst.append(current)
            mods_to_inst.append(newest)
        if name in mods_to_uninst:
            x=mods_to_uninst.index(name)
            mods_to_uninst.pop(x)
            mods_to_uninst.pop(x)
            mods_to_uninst.pop(x)
    else:
        if current != "0.0.00":
            mods_to_uninst.append(name)
            mods_to_uninst.append(current)
            mods_to_uninst.append(newest)
        if name in mods_to_inst:
            x=mods_to_inst.index(name)
            mods_to_inst.pop(x)
            mods_to_inst.pop(x)
            mods_to_inst.pop(x)
        
    #if name in local_modules:
        #print(local_modules[local_modules.index(name):local_modules.index(name)+3])

def openurl(url=""):
    subprocess.call("start "+url,shell=True)
    
def onnameclick(name="",latestver="",vers=""):
    try:
        installedver = local_modules[local_modules.index(name)+1]
    except:
        installedver = "-"
    url = online_modules[online_modules.index(name)+1]
    
    popup = Toplevel()
    popup.title("Module Info")
    popup.columnconfigure(0,weight=1)
    popup.columnconfigure(1,weight=1)
    #messagebox.showinfo(title=name,message="Latest version: "+latestver)

    n = Label(popup,text="Name: "+name+"\n").grid(row=0,column=0,sticky=W+E)
    iv = Label(popup,text="Installed version: "+installedver+"\n").grid(row=0,column=1,sticky=W+E)
    u = Button(popup,text="Download URL",command=lambda ur=url: openurl(ur)).grid(row=2,column=0,sticky=W+E)
    av = Label(popup,text="Available Versions:").grid(row=1,column=0,sticky=W+E)
    
    options=[]
    for x in vers:
        options.append(x[0].replace(".rar","").replace(".zip",""))
    options.sort(reverse=True)
    options.insert(0,options[0])
    v = StringVar()
    v.set(options[0])
    om = OptionMenu(popup,v,*options).grid(row=1,column=1,sticky=W+E)
    
    b = Button(popup,text="Install selected version",command=lambda a=v, n=name, v=vers: instalver(a,v,n)).grid(row=2,column=1,sticky=W+E)
    #print(name,latestver,"\n\n",vers)

def instalver(v="",vers="",name=""):
    logtext("Instaling new versions")
    vertoinst = v.get()
    for x in vers:
        if vertoinst in x[0]:
            break
    url = x[1]
    updatever(name,vertoinst,url.replace("?dl=0","?dl=1"))

def updatever(name="",latestver="",url=""):
    import zipfile, urllib.request, shutil
    progress.configure(maximum=4)
    y=0
    try:
        if ".zip" in url:
            file_name = vpadirectory.replace("/","\\")+"\\"+"Temp.zip"
            logtext("Fetching data from "+url)
            with urllib.request.urlopen(url.replace("?dl=0","?dl=1")) as response, open(file_name, 'wb') as out_file:
                ptext.set("Collecting "+name+".zip")
                progress.step()
                y+=1
                shutil.copyfileobj(response, out_file)
                ptext.set("Extracting to "+vpadirectory)
                progress.step()
                y+=1
            logtext("Checking overwrite conflicts")
            old_files = ""
            try:
                f = open(name+str("//__init__.py"),"r")
                overwrites = f.read()
                f.close()
                if "module.dont_overwrite([" in overwrites:
                    old_files = ((m.split("module.dont_overwrite([")[1]).split("])")[0]).replace('"',"").split(",")
                tempfiles = []
                for x in old_files:
                    f = open(name+"//"+x,"r")
                    tempfiles.append(f.read())
                    f.close()
            except:
                logtext("No local version of "+name+" found")
            logtext("Extracting "+name)
            zip_file = zipfile.ZipFile(str(file_name.replace("\\","\\\\").replace("/","\\\\")),"r")
            zip_file.extractall(path=vpadirectory.replace("/","\\"))
            zip_file.close()
            os.remove(file_name)
            ptext.set(name+" Extracted, Updating")
            logtext(name+" Updated to "+latestver)
            for x in old_files:
                f = open(name+"//"+x,"w")
                f.write(tempfiles[old_files.index(x)])
                f.close()
            logtext("Updating "+name)
            progress.step()
            y+=1
            if name == "_core":
                latestcorever,latestcoredl = (online_version[len(online_version)-1])[0].replace(".rar","").replace(".zip",""),(online_version[len(online_version)-1])[1]
                core_update = "-"
                b = Button(ml,text=core_update,state=DISABLED).grid(row=1,column=1,sticky=W+E)
                b = Button(ml,text="VPA Core",command=lambda n="_core",l=latestcorever,v=online_version: onnameclick(n,l,v),state=DISABLED).grid(row=1,column=2,sticky=W+E)
                b = Button(ml,text=latestcorever,state=DISABLED).grid(row=1,column=3,sticky=W+E)
                b = Button(ml,text=latestcorever,state=DISABLED).grid(row=1,column=4,sticky=W+E)
                master.title("Module instalation - VPA "+latestcorever+" -- "+str(vpadirectory))
            else:
                versions = module_versions[int(module_versions.index(name)/2)+1]
                b = Button(ml,text="-",state=DISABLED).grid(row=int(module_versions.index(name)/2+2),column=1,sticky=W+E)
                b = Button(ml,text=name,command=lambda n=name,l=latestver,v=versions: onnameclick(n,l,v)).grid(row=int(module_versions.index(name)/2+2),column=2,sticky=W+E)
                b = Button(ml,text=latestver,state=DISABLED).grid(row=int(module_versions.index(name)/2+2),column=3,sticky=W+E)
                b = Button(ml,text=latestver,state=DISABLED).grid(row=int(module_versions.index(name)/2+2),column=4,sticky=W+E)
            logtext("Updated "+name)
        elif ".rar" in url:
            print("Not yet implemented")
            logtext("Unsuported filetype for: "+name+" v."+latestver+" @ "+url)
        elif (".rar" not in url) and (".zip" not in url):
            print("Unsuported filetype")
            logtext("Unsuported filetype for: "+name+" v."+latestver+" @ "+url)
    except Exception as inst:
        logtext("ERROR IN CODE EXECUTION:\n--------------------\n"+str(type(inst))+"\n-"+str(inst)+"\nDon't do ^That until the developers can fix it.\n--------------------")
        #from tkinter import messagebox
        z = ["collecting name","saving file","extracting file","applying update"]
        if messagebox.askokcancel(icon="error",title="Error",message="Error: "+z[y]+"\nOpen the directory?"):
            openDir()
    ptext.set("Finished")
    progress.configure(value=0)

def getVPAnewdirectory():
    global vpadirectory
    global def_dir
    global data
    def_dir,dir_name,ver = getVPAdirectory()
    if not def_dir == "None":
        data[data.index("default_directory")+1] = def_dir
    vpadirectory = removeextension(def_dir)
    
def getVPAdirectory():
    logtext("Searching for VPA Directory")
    from tkinter.filedialog import askopenfilename   
    dire = askopenfilename(defaultextension="py" , filetypes=(("Python files","*.py"),("All files", "*.*")),title="Select VPA Install to use")
    try:
        for x in range(len(dire)):
            if dire[len(dire)-x-1] == "/":
                break
        logtext("Directory found, "+str(dire[0:len(dire)-x-1].replace("/","\\"))+str(dire[len(dire)-x:len(dire)])+str(getVPAversion(dire[0:len(dire)-x])))
        return dire[0:len(dire)-x-1].replace("/","\\"),dire[len(dire)-x:len(dire)],getVPAversion(dire[0:len(dire)-x])
    except:
        return None

def getdata(file=""):
    import csv
    mem = []
    try:
        f = open(file,"r")
        file = csv.reader(f)
        for row in file:
            if row != []:
                mem.append(row[0])
        f.close()
        if mem == []:
            return ["default_directory","None","<directories>","</directories>"]
        else:
            return mem
    except FileNotFoundError:
        f = open(file,"w")
        f.write("default_directory\nNone\n<directories>\n</directories>")
        f.close()
        return ["default_directory","None","<directories>","</directories>"]

def savedata(file="UpdaterData.txt"):
    f = open(file,"w")
    for x in data:
        y = x+"\n"
        if x == data[:-1]:
            y = x
        f.write(y)
    f.close()
    logtext("Saving Updater Data")

def donothing():
    messagebox.showinfo(title="Error",message="That feature has not yet\nbeen implemented.\n\nPlease wait for future updates.")

def quitupdater():
    if messagebox.askyesno("Close updater","Are you sure you want to quit?"):
        savedata("UpdaterData.txt")
        master.destroy()
        logtext("Updater Program Quit")

def removedir():
    global data
    try:
        dirselect=dirslist.curselection()[0]-1
        if dirselect < 0:
            dirselect = "None"
    except:
        dirselect="None"
    if not dirselect=="None":
        y = data[data.index("<directories>")+1:data.index("</directories>")][dirselect]
        dirslist.delete(dirselect+1)
        logtext("Removing VPA Directory")
        data.pop(data.index(y))

def addnewdir():
    logtext("Adding New VPA Directory")
    dirn,name,ver = getVPAdirectory()
    name = name.split(".")[0]
    data.insert(data.index("</directories>"),name+";"+ver+";"+dirn+"\\"+name.replace(".py","")+".py")
    while len(name) < 20:
        name +=" "
    while len(ver) < 10:
        ver +=" "
    dirslist.insert(END,name+ver+dirn)

def renamedir():
    logtext("Renaming VPA Directory")
    global data
    try:
        dirselect=dirslist.curselection()[0]-1
        if dirselect < 0:
            dirselect = "None"
    except:
        dirselect="None"
    if not dirselect=="None":
        y = data[data.index("<directories>")+1:data.index("</directories>")][dirselect]
        getnewname()
        popup.wait_window(popup)
        z = Newname+y[y.index(";"):len(y)]
        data[data.index("<directories>")+1:data.index("</directories>")][dirselect] = z
        dirslist.delete(dirselect+1)
        y = str(z).split(";")
        data[dirselect+data.index("<directories>")+1] = y[0]+";"+y[1]+";"+y[2]
        while len(y[0]) < 20:
            y[0] +=" "
        while len(y[1]) < 10:
            y[1] +=" "
        dirslist.insert(dirselect+1,y[0]+y[1]+y[2].split(".")[0])

def getnewname():
    globals()["popup"] = Tk()
    popup.title("Rename")
    v = StringVar()
    L1 = Label(popup, text="New Name")
    L1.pack(side=LEFT)
    globals()["Enter"] = Entry(popup, textvariable=v)
    Enter.pack(side=LEFT)
    popup.bind("<Return>",returnname)
    v.set("")
    b = Button(popup,text="OK",command=returnname).pack(side=RIGHT)
    
def returnname(x=1):
    globals()["Newname"] = Enter.get()
    popup.destroy()

def selectinstall():
    logtext("Selecting new VPA Install")
    global vpadirectory
    try:
        dirselect=dirslist.curselection()[0]-1
        if dirselect < 0:
            dirselect = "None"
    except:
        dirselect="None"
    if not dirselect=="None":
        if w.get():
            data[data.index("default_directory")+1] = (data[dirselect+data.index("<directories>")+1]).split(";")[2]
        else:
            data[data.index("default_directory")+1] = "None"
        savedata()
        vpadirectory = removeextension((data[dirselect+data.index("<directories>")+1]).split(";")[2])
        mini.destroy()
        logtext("New install, "+vpadirectory+" Selected for use")
        main()

def startup():
    logtext("Selecting VPA Install at startup")
    globals()["mini"] = Tk()
    mini.title("select VPA install")

    menubar = Menu(mini)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Forget VPA Install", command=removedir)
    filemenu.add_command(label="Rename VPA Install", command=renamedir)
    filemenu.add_command(label="Add New VPA Install", command=addnewdir)
    filemenu.add_command(label="Select VPA Install", command=selectinstall)
    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_command(label="Help", command=helpwindow)
    mini.config(menu=menubar)

    globals()["w"] = BooleanVar()
    def_button = Checkbutton(mini,text="Set as default",variable=w)
    
    dirs = Listbox(mini,selectmode=SINGLE,width=70,height=20,font=("Courier New", 10))
    globals()["dirslist"] = dirs
    dirs.select_set(first=0)
    dirscroll = Scrollbar(command=dirs.yview, orient=VERTICAL)
    dirs.configure(yscrollcommand=dirscroll.set)
    
    forget = Button(mini,text="Forget",command=removedir)
    rename = Button(mini,text="Rename",command=renamedir)
    addnew = Button(mini,text="Add new",command=addnewdir)
    select = Button(mini,text="Select",command=selectinstall)
    
    for x in ["Name;Version;Path"]+data[data.index("<directories>")+1:data.index("</directories>")]:
        y = x.split(";")
        acver = getVPAversion(removeextension(y[2]))
        if (y[1] != getVPAversion(removeextension(y[2]))) and (y[1] != "Version"):
            y[1] = getVPAversion(removeextension(y[2]))
        while len(y[0]) < 20:
            y[0] +=" "
        while len(y[1]) < 10:
            y[1] +=" "
        if (x.split(";")[0])[0:17]!= x.split(";")[0]:
            y[0] = y[0:17]+"..."
        dirs.insert(END,y[0]+y[1]+y[2].split(".")[0])
        
    dirs.pack()
    def_button.pack(side=LEFT)
    select.pack(side=RIGHT)
    addnew.pack(side=RIGHT)
    rename.pack(side=RIGHT)
    forget.pack(side=RIGHT)
    mainloop()
    
def launchloadthread():
    if local_new_version != "0.0.00":
        t1 = threading.Thread(target=initialload,name="Updater initialisation")
        t1.start()
    else:
        b = Label(master,text="Could not retrieve local versions, check repository")
        b.pack(pady=100)

def launchVPA():
    logtext("Terminating Updater")
    pys = []
    file_name = ""
    for file in os.listdir(vpadirectory+"\\"):
        if file.endswith(".py"):
            if file != "updater.py":
                pys.append(file)
    if not "LOaBIS.py" in pys:
        if not "VPA.py" in pys:
            if len(pys) > 1:
                for x in pys:
                    print(vpadirectory+"\\"+x)
            else:
                file_name = vpadirectory+"\\"+pys[0]
        else:
            file_name = vpadirectory+"\\VPA.py"
    else:
        file_name = vpadirectory+"\\LOaBIS.py"
    master.destroy()
    logtext("Updater terminated, Executing VPA\n")
    os.system(file_name)

def applychanges():
    logtext("Applying selected changes")
    import shutil
    passinst = []
    for x in range(int(len(mods_to_inst)/3)):
        passinst.append([mods_to_inst[3*x],mods_to_inst[3*x+2],module_versions[module_versions.index(mods_to_inst[3*x])+1][-1:][0][1].replace("?dl=0","?dl=1")])
    logtext("Installing chosen modules")
    installmods(passinst)
    logtext("Uninstalling chosen modules")
    for x in range(int(len(mods_to_uninst)/3)):
        shutil.rmtree(vpadirectory+"\\"+mods_to_uninst[3*x])
    logtext("Changes Complete")

def installmods(installmods=""):
    for x in installmods:
        updatever(x[0],x[1],x[2])

def helpwindow():
    '''helpbox = Tk()
    helpbox.title("Help")
    '''
    donothing()

def main():
    globals()["mods_to_inst"] = []
    globals()["mods_to_uninst"] = []
    globals()["master"] = Tk()
    global vpadirectory
    globals()["local_new_version"] = getVPAversion(removeextension(data[data.index("default_directory")+1]))
    master.title("Module instalation - VPA "+local_new_version+" -- "+str(vpadirectory))
    master.state('zoomed')

    #Menubar stuff    
    menubar = Menu(master)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Select VPA Install", command=getVPAdirectory)
    filemenu.add_command(label="Open VPA Directory", command=openDir)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=quitupdater)
    menubar.add_cascade(label="File", menu=filemenu)

    settingmenu = Menu(menubar,tearoff=0)
    settingmenu.add_command(label="VPA settings",command=donothing)
    settingmenu.add_command(label="Installer settings",command=donothing)
    menubar.add_cascade(label="Settings", menu=settingmenu)

    menubar.add_command(label="Help", command=helpwindow)

    master.config(menu=menubar)
    
    #Progress bar stuff
    globals()["ptext"] = StringVar()
    ptext.set("Please Wait")
    progresstext = Label(master,textvariable=ptext,justify=CENTER)
    globals()["progress"] = Progressbar(master,mode="determinate")
    progresstext.pack(pady=10)
    progress.pack(padx=10,fill="x")

    #top bar buttons
    topbar = Frame(master)
    topbar.pack(fill="x",padx=10,pady=10)
    topbar.columnconfigure(0,weight=1)
    topbar.columnconfigure(1,weight=1)
    topbar.columnconfigure(2,weight=1)
    topbar.columnconfigure(3,weight=1)
    Launch = Button(topbar,text="Launch VPA",command=launchVPA).grid(row=0,column=0,sticky=W+E)
    Refresh = Button(topbar,text="Refresh",command=launchloadthread).grid(row=0,column=1,sticky=W+E)
    Addchanges = Button(topbar,text="Apply changes",command=applychanges).grid(row=0,column=2,sticky=W+E)

    ##launch the loading thread
    launchloadthread()

    #list of all the modules
    s = Style()
    s.configure("header.TButton",foreground="gray",background="black")
    globals()["ml"] = Frame(master)
    ml.pack(padx=10,fill="both")
    ml.columnconfigure(0,weight=1)
    ml.columnconfigure(1,weight=1)
    ml.columnconfigure(2,weight=20)
    ml.columnconfigure(3,weight=2)
    ml.columnconfigure(4,weight=2)
    b = Button(ml,text="Installed",style="header.TButton",state=DISABLED).grid(row=0,column=0,sticky=W+E)
    b = Button(ml,text="Update",style="header.TButton",state=DISABLED).grid(row=0,column=1,sticky=W+E)
    b = Button(ml,text="Name",style="header.TButton",state=DISABLED).grid(row=0,column=2,sticky=W+E)
    b = Button(ml,text="Installed Version",style="header.TButton",state=DISABLED).grid(row=0,column=3,sticky=W+E)
    b = Button(ml,text="Latest Version",style="header.TButton",state=DISABLED).grid(row=0,column=4,sticky=W+E)

    logtext("Initialised Main Updater program")
    
    mainloop()

if __name__ == "__main__":
    logtext("Initialising Updater Software")
    init()
