import datetime, os, sys
from updater import *
from tkinter import *
from tkinter.ttk import *

ostype=sys.platform
globals()["sep"]="/"
if "win" in ostype:
    globals()["sep"]="\\"
globals()["Main_Data_Dir"]=os.path.expanduser("~")+sep+"LOaBIS"
globals()["iconpath"]=Main_Data_Dir+sep+"Loa_icon.ico"

def choosedirectory():
    _logtext("Launching module wizard",1)
    checkicon()
    main=genwindow("Choose Directory",posx=100,posy=100)
    globals()["Dir_Data"]=[]
    if not os.path.exists(Main_Data_Dir):
        os.makedirs(Main_Data_Dir)
    loaddatafile()

    Headers=Label(main,text="Version   Name\t\t     Directory").grid(row=0,column=0,columnspan=3,padx=5,pady=5,sticky=W)
    Entries,Scroll=setscrollbox(main,70,10,1,0,3,3,5,5)
    Buttons=Frame(main)
    Add=setbutton(Buttons,"Add",8,lambda:adddirectory(Entries),0,0)
    Edit=setbutton(Buttons,"Edit",8,lambda:editdirectory(Entries),0,1)
    Remove=setbutton(Buttons,"Remove",8,lambda:removedirectory(Entries),1,0)
    Open=setbutton(Buttons,"Open",8,lambda:opendirectory(Entries),1,1)
    Quit=setbutton(Buttons,"Quit",8,main.destroy,2,0)
    Launch=setbutton(Buttons,"Select",8,lambda:startmain(Entries,main),2,1)
    Dupe=setbutton(Buttons,"Duplicate",8,lambda:dupedirectory(Entries),3,0,5,5,W+E,2)
    Info=Text(main,width=30,height=8)

    Buttons.grid(row=2,column=0,padx=5,pady=5,sticky=W)
    Info.grid(row=2,column=1,padx=5,pady=5,sticky=N+S+E+W)

    bindcom(Entries,['<Double-1>','<<ListboxSelect>>'],[lambda x:Open.invoke(),lambda x:changeinfo(Entries,Info)])
    updateentries(Entries)
    changeinfo(Entries,Info)
    main.bind("<Destroy>",lambda x:savedatafile())
    mainloop()

def editdirectory(Entries=""):
    if Dir_Data:
        show=getshow(Entries)
        _logtext("Editing directory "+str(show[0]))
        Edit=genwindow("Edit Directory",posx=150,posy=150,resize=False)

        Name_text,Name=enterbox(Edit,"Name",show[0].replace(" ",""))
        Dir_text,Dir=enterbox(Edit,"Directory",show[2],1)
        Ver_text,Ver=enterbox(Edit,"Version",show[1],2,state=DISABLED)
        Accept=setbutton(Edit,"Accept",20,lambda:returndir(Name,Edit,Entries),3)
        Change=setbutton(Edit,"Change Directory",20,lambda:returndir(Name,Edit,Entries),3,1)

        globals()["Found_ver"],globals()["Found_dir"]=show[1:3]

        mainloop()

def enterbox(main="",text="",entrytext="",row=0,column=0,padx=5,pady=5,state=NORMAL):
    Entertext=Label(main,text=text)
    Enter=Entry(main)
    
    Entertext.grid(row=row,column=column,padx=padx,pady=pady)
    Enter.grid(row=row,column=column+1,padx=padx,pady=pady,sticky=W+E)
    
    Enter.insert(END,entrytext)
    Enter.configure(state=state)
    return Entertext,Enter

def adddirectory(Entries=""):
    _logtext("Adding new directory")
    Add_new=genwindow("Add New Directory",posx=150,posy=150,resize=False)

    Name_text=Label(Add_new,text="Name")
    Dir_text=Label(Add_new,text="Directory")
    Ver_text=Label(Add_new,text="Version")
    Name=Entry(Add_new)
    Dir=Entry(Add_new)
    Ver=Entry(Add_new)
    Accept=setbutton(Add_new,"Accept",20,lambda:returndir(Name,Add_new,Entries),3,0)
    Change=setbutton(Add_new,"Change Directory",20,lambda:returndir(Name,Add_new,Entries),3,0)

    Name_text.grid(row=0,column=0,padx=5,pady=5)
    Dir_text.grid(row=1,column=0,padx=5,pady=5)
    Ver_text.grid(row=2,column=0,padx=5,pady=5)
    Name.grid(row=0,column=1,padx=5,pady=5)
    Dir.grid(row=1,column=1,padx=5,pady=5)
    Ver.grid(row=2,column=1,padx=5,pady=5)
    getdir(Dir,Ver,Add_new)

    mainloop()

def dupething(show,Entries):
    from shutil import copytree
    _logtext("Fetching directory info")
    Found_dir,Found_ver=show[2].replace(sep+"LOaBIS.py","_copy"+sep+"LOaBIS.py"),show[1]
    copytree(show[2].replace(sep+"LOaBIS.py",""),Found_dir.replace(sep+"LOaBIS.py",""))
    name=makelen("C. "+show[0],20)
    Dir_Data.append([name,Found_ver,Found_dir,now(),show[4],show[5]])
    _logtext("Directory duplicated")
    updateentries(Entries)

def dupedirectory(Entries=""):
    from tkinter import messagebox
    from shutil import rmtree
    if Dir_Data:
        _logtext("Duplicating directory")
        show=getshow(Entries)
        if not os.path.isdir(show[2].replace(sep+"LOaBIS.py","_copy")):
            dupething(show,Entries)
        else:
            _logtext("Duplicate directory already exists")
            if messagebox.askokcancel(title="Copy Error",default="cancel",icon="error",message="A copy of that directory already exists, copy anyway?"):
                rmtree(show[2].replace(sep+"LOaBIS.py","_copy"),ignore_errors=True)
                oldcopy=getdat(Dir_Data,show[2].replace(sep+"LOaBIS.py","_copy"+sep+"LOaBIS.py"))
                if oldcopy:
                    Dir_Data.remove(oldcopy)
                _logtext("Overwriting old duplicate")
                dupething(show,Entries)

def removedirectory(entry):
    from tkinter import messagebox
    if Dir_Data:
        show=getshow(entry)
        if messagebox.askokcancel(title="Remove",default="cancel",icon="error",message="Are you sure you want to remove:\n\n"+str(show[0])+"\n"+str(show[1])+"\n"+str(show[2])):
            Dir_Data.remove(show)
            updateentries(entry)

def opendirectory(entry):
    if Dir_Data:
        show=getshow(entry)
        try:
            os.startfile(str(show[2]).replace("//LOaBIS.py","").replace("/LOaBIS.py","").replace("\\LOaBIS.py","").replace("\LOaBIS.py",""))
        except:
            subprocess.Popen('explorer "{0}"'.format(os.getcwd()))

def returndir(Name="",main="",entry=""):
    if Name.get():
        name,info=makelen(Name.get(),30),os.stat(Found_dir)
        if Dir_Data:
            for x in range(len(Dir_Data)):
                if str((Dir_Data[x])[2])==str(Found_dir):
                    break
            if str((Dir_Data[x])[2])==str(Found_dir):
                Dir_Data.remove(Dir_Data[x])
                Dir_Data.insert(x,[name,Found_ver,Found_dir,now(),datetime.datetime.fromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S').replace("-","/"),info.st_size])
            else:
                Dir_Data.append([name,Found_ver,Found_dir,now(),datetime.datetime.fromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S').replace("-","/"),info.st_size])
        else:
            Dir_Data.append([name,Found_ver,Found_dir,now(),datetime.datetime.fromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S').replace("-","/"),info.st_size])
        updateentries(entry)
        main.destroy()

def getdir(Dir,Ver,main):
    from tkinter.filedialog import askopenfilename
    globals()["Found_dir"]=askopenfilename(defaultextension="py",filetypes=(("Python files","*.py"),("All files", "*.*")),title="Select LOaBIS Install")
    while "LOaBIS.py" not in Found_dir:
        globals()["Found_dir"]=askopenfilename(defaultextension="py",filetypes=(("Python files","*.py"),("All files", "*.*")),title="SELECT A LOABIS INSTALL!!")
    with open(Found_dir.replace("LOaBIS.py","_core/__init__.py"),"r") as f:
        globals()["Found_ver"]=(f.read().split("module.module(")[1].split(")")[0].split(",")[1])[1:-1]
    settop(main)

    Dir.delete(0,END)
    Dir.insert(END,Found_dir)
    Ver.delete(0,END)
    Ver.insert(END,Found_ver)

def getmissing(show=[]):
    _logtext("Fetching missing data")
    while len(show) < 6:
        show.append("")
    if not os.path.exists(show[2]):
        show[2]=str(os.getcwd())+sep+"LOaBIS.py"
    info=os.stat(show[2])
    if not show[0]:
        show[0]="Default"
    show[0]=makelen(show[0],30)
    if len(show[1]) !=len("0.2.00"):
        show[1]=getactualver(show[2],"0.2.00")
    if not show[3]:
        show[3]=now()
    if not show[4]:
        show[4]=datetime.datetime.fromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S').replace("-","/")
    if not show[5]:
        show[5]=info.st_size
    _logtext("Data found")
    return show

def updateentries(entry):
    entry.delete(0,END)
    for x in Dir_Data:
        ver=getactualver(x[2],x[1])
        entry.insert(END," "+ver+"      "+x[0]+" "+x[2])
        entry.select_set(first=0)

def instext(text="",ins=[],disable=1):
    text.configure(state=NORMAL)
    try:
        text.delete(0.0,END)
    except:
        text.delete(1.0,END)
    for x in ins:
        text.insert(END,x)
    if disable:
        text.configure(state=DISABLED)

def changeinfo(entry,text):
    if Dir_Data:
        show=getshow(entry)
        ver=getactualver(show[2],show[1])
        a=["Version:   "+str(ver)+"\n","Created:   "+str(show[4])+"\n","Added:     "+str(show[3])+"\n","Size:      "+str(sigfig(show[5],1))+"Bytes\n","Name:      "+str(show[0][0:16])+"...\n","Directory:\n"+str(show[2])+"\n"]
    else:
        a=["No Versions Found"]
    instext(text,a)

def getshow(entry):
    try:
        a=entry.curselection()[0]
    except:
        a=0
    ret=Dir_Data[a]
    ret[3],ret[5]="",""
    return getmissing(Dir_Data[a])

def loaddatafile(directory=Main_Data_Dir):
    try:
        with open(directory+sep+"UpdaterData.txt","r") as f:
            m=f.read()
        a=attempt(m,"Directories",[],True)
        for x in a:
            if x:
                if len(x.split(";")) <=5:
                    Dir_Data.append(getmissing(x.split(";")))
                if len(x.split(";")) >6:
                    Dir_Data.append(x.split(";")[0:6])
                else:
                    Dir_Data.append(x.split(";"))
        if not (a or Dir_Data):
            default_dir()
    except:
        default_dir()
    globals()["last_download"],globals()["mindlday"]=attempt(m,"Download",datetime.datetime(2000,1,1)),int(attempt(m,"Mindl",1))
    globals()["min_download_days"],globals()["autoupdate"]=mindlday,attempt(m,"Autoupdate","False")
    globals()["openwhenclosed"],globals()["download_all"]=attempt(m,"Openwhenclosed","False"),attempt(m,"Download_all","False")
    globals()["auto_dl_mod"]=attempt(m,"Auto_dl_mod","False")
    savedatafile()

def savedatafile(directory=Main_Data_Dir):
    with open(str(directory)+sep+"UpdaterData.txt","w") as f:
        f.write("<Directories>\n")
        for x in Dir_Data:
            x[1]=getactualver(x[2],x[1])
            w=""
            for y in x:
                w+=str(y)+";"
            f.write(w[0:-1]+"\n")
        writes=["</Directories>\n<Download>\n",str(last_download),"\n</Download>\n<Mindl>\n",str(mindlday),"\n</Mindl>\n<Autoupdate>\n",autoupdate,"\n</Autoupdate>\n<Openwhenclosed>\n",openwhenclosed,"\n</Openwhenclosed>\n<Download_all>\n",download_all,"\n</Download_all>\n<Auto_dl_mod>\n",auto_dl_mod,"\n</Auto_dl_mod>"]
        for x in writes:
            f.write(x)

def default_dir():
    _logtext("Fetching default directory")
    dire=str(os.getcwd())+sep+"LOaBIS.py"
    info=os.stat(dire)
    Dir_Data.append([makelen("Default",20),getactualver(dire,"0.2.00"),dire,now(),datetime.datetime.fromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S').replace("-","/"),info.st_size])

def getlocalmodules(dire=os.getcwd()):
    modules=next(os.walk(dire.replace(sep+"LOaBIS.py","")))[1]
    modules.sort()
    if "__pycache__" in modules:
        modules.remove("__pycache__")
    _logtext("Fetching "+str(int(len(modules)))+" local modules: "+str(modules))
    _temp=[]
    for x in range(len(modules)):
        if os.path.exists(dire.replace("LOaBIS.py","")+str(modules[x])+sep+"__init__.py"):
            _temp.append([modules[x],getactualver(dire.replace("LOaBIS.py","")+str(modules[x])+sep+"__init__.py","0.0.00")])
    return _temp

def _logtext(text="null",newline=0):
    text=text[0].upper()+text[1:len(text)]+"\n"
    with open("log.txt","a") as y:
        if newline==1:
            y.write("\n")
        y.write("["+str(datetime.datetime.now())+"] - "+text)

def startmain(entry,prev):
    if Dir_Data:
        _logtext("Initialising module instalation")
        savedatafile()
        show=getshow(entry)
        globals()["Focus_Dir"]=show
        prev.destroy()
        choosemodule()

def returnindex(lst=[],idx=0,ign=[]):
    a=[]
    for x in lst:
        a.append(x[idx])
    for x in ign:
        b=getdat(a,x)
        if b:
            a.remove(b)
    if not a:
        a=["null"]
    return a

def sigfig(num=0,computing=0):
    a=[1E-24,1E-21,1E-18,1E-15,1E-12,1E-9,1E-6,1E-3,1,1E3,1E6,1E9,1E12,1E15,1E18,1E21,1E24,1E100]
    if computing:
        a=[0,0,0,0,0,0,0,0,1,1024,1024**2,1024**3,1024**4,1024**5,1024**6,1024**7,1024**8,1024**33]
    b=["Yocto","Zepto","Atto","Femto","Pico","Nano","Micro","Milli","","Kilo","Mega","Giga","Terra","Peta","Exa","Zetta","Yotta","Gogol"]
    for x in range(int(len(a))):
        if num<=a[x]:
            break
    if a[x] in [1,0]:
        return str(int(num/a[x-1]))+" "+str(b[x-1])
    else:
        return str(round(num/a[x-1],3))+" "+str(b[x-1])

def getinfoinfo(a="",b="",c=""):
    Info.configure(state=NORMAL)
    if drop.get() == "null":
        Info.configure(text=makelen("    name:",25)+"null\n"+makelen("    compat. Ver.:",21)+"Unknown\n"+makelen("    Main size:",24)+"0 Bytes")
    else:
        Info.configure(text=makelen("    name:",25)+str(drop.get())+"\n"+makelen("    compat. Ver.:",21)+str(getdat(localmods,drop.get())[1])+"\n"+makelen("    Main size:",24)+str(sigfig(os.stat(Focus_Dir[2].replace("LOaBIS.py",str(drop.get())+"//__init__.py")).st_size,1))+"Bytes")
    Info.configure(state=DISABLED)

def checklist(actual="",default=""):
    while len(actual) < len(default):
        actual.append("")
    for x in range(len(default)):
        if actual[x]:
            default[x]=actual[x]
    return default

def loadoldmod(main="",name=""):
    if name=="null":
        popup("Error","\nYou must select a module to load!")
    else:
        moduledir=Focus_Dir[2].replace("LOaBIS.py",str(name)+sep)
        main.destroy()
        name,screenname,author,description,homepage=checklist(getmeta(moduledir+"metadata.txt"),[name,name,"N/A","N/A","N/A"])
        modulever=getactualver(Focus_Dir[2],Focus_Dir[1],str(name))
        a,b=["commands.txt","__init__.py","metadata.txt","changelog.txt"],["",'def setup():\n    module.module("'+str(name)+'","'+str(modulever)+'","N/A")\n\n','name:'+str(name)+'\nscreenname:'+str(screenname)+'\nauthor:'+str(author)+'\ndescription:'+str(description)+'\nhomepage:'+str(homepage),'0.0:\nminver:'+str(min(modulever,Focus_Dir[1]))+'\nmaxver:'+str(max(modulever,Focus_Dir[1]))+'\nrequired:N/A']
        for x in range(len(a)):
            if not os.path.isfile(moduledir+a[x]):
                with open(moduledir+a[x],"w") as f:
                    f.write(b[x])
        startwizard(name)

def getmeta(file=""):
    _temp=[]
    try:
        with open(file,"r") as f:
            m=f.read()
        for x in ["name","screenname","author","description","homepage"]:
            if x in m:
                _temp.append(m.split(x+":")[1].split("\n")[0])
            else:
                _temp.append("")
    except:
        pass
    return _temp

def createnewmod(main="",name="",screenname="",author="",description="",homepage=""):
    if name and screenname and (" " not in name):
        _logtext("New Module "+str(name)+" created")
        moduledat=[name,screenname]+checklist([author,description,homepage],["N/A","N/A","N/A"])
        main.destroy()
        moduledir=Focus_Dir[2].replace("LOaBIS.py",str(name)+sep)
        os.mkdir(moduledir)
        a,b=["commands.txt","__init__.py","metadata.txt","changelog.txt"],["",'def setup():\n    module.module("'+str(name)+'","'+str(Focus_Dir[1])+'","N/A")\n\n','name:'+str(name)+'\nscreenname:'+str(screenname)+'\nauthor:'+str(author)+'\ndescription:'+str(description)+'\nhomepage:'+str(homepage),'0.0:\nminver:'+str(Focus_Dir[1])+'\nmaxver:'+str(Focus_Dir[1])+'\nrequired:N/A\nCreated the module']
        for x in range(len(a)):
            with open(moduledir+a[x],"w") as f:
                f.write(b[x])
        startwizard(name)
    else:
        popup("Error","\nYou must add a module name and screen name")

def choosemodule():
    _logtext("Selecting LOaBIS Module")
    globals()["localmods"]=getlocalmodules(Focus_Dir[2])
    modulestart=genwindow(title="Choose module to edit",resize=False)
    titletext=Label(modulestart,text="Module selection:").grid(row=0,column=0,columnspan=2,pady=5,padx=5,sticky=W)
    seperator(modulestart,row=1)
    modsreturned=returnindex(localmods,0,["_core"])
    globals()["drop"]=dropdown(modulestart,"  Select a pre-existing module:",modsreturned[0],modsreturned,2,0,1,W)[0]
    globals()["Info"]=Label(modulestart,state=DISABLED)
    launchpre=Button(modulestart,text="Launch with pre-existing module",command=lambda:loadoldmod(modulestart,drop.get())).grid(row=4,column=0,columnspan=2,padx=5,pady=5)
    Info.grid(row=3,column=0,columnspan=2,pady=5,padx=5,sticky=W)
    drop.trace("w",getinfoinfo)
    getinfoinfo()
    seperator(modulestart,row=5)

    newmodtext=Label(modulestart,text="Create new module:\n(* are not required at this stage)").grid(row=6,column=0,columnspan=2,pady=5,padx=5,sticky=W+E)
    name_text,Name=enterbox(modulestart,"Module Name","",7)
    Screen_text,Screen=enterbox(modulestart,"Screen Name","",8)
    Author_text,Author=enterbox(modulestart,"Author Name *","",9)
    Desc_text,Desc=enterbox(modulestart,"Description *","",10)
    Url_text,Url=enterbox(modulestart,"Homepage Url *","",11)
    Start=Button(modulestart,text="Create",command=lambda:createnewmod(modulestart,Name.get(),Screen.get(),Author.get(),Desc.get(),Url.get())).grid(row=20,column=1,padx=5,pady=5,sticky=W+E)
    Help=Button(modulestart,text="Help",command=lambda:popup("Help","Module creation help:\n[* are not required at this stage]\n\n  Module name:\n    The internal name (ie: _core) which is used by scripts to reference this module.\n    (MUST BE ONE WORD)\n\n  Screen name:\n    The name of the module (ie: LOaBIS Core), which will be shown on the module installer.\n    (Can be anything really)\n\n  Author Name: *\n    The name of the module creator\n\n  Description: *\n    A summary of the module contents")).grid(row=20,column=0,padx=5,pady=5,sticky=W+E)

    mainloop()

def savemodulechanges(files=[],boxes=[]):
    for x in range(len(files)):
        with open(module_dir+str(files[x]),"w") as f:
            f.write(boxes[x].get("1.0",'end-1c'))

def loadmodulechanges(files=[],boxes=[]):
    for x in range(len(files)):
        with open(module_dir+str(files[x]),"r") as f:
            instext(boxes[x],[f.read()],0)

def returnfromfile(file="",returnitem="",enditem="\n",returnindex=0,default="N/A"):
    with open(file,"r") as f:
        m=f.read()
    if returnitem:
        return str(m.split(returnitem)[1].split(enditem)[0])
    else:
        return str(str(m[0:]).split(":")[0])

def replaceinfile(file="",replaceitem="",enditem="\n",replacement="",replaceindex=0):
    with open(file,"r") as f:
        m=f.read()
    if replaceitem:
        _tmp=[m.index(replaceitem),m.split(replaceitem)[1].index(enditem)+m.index(replaceitem)+len(replaceitem)+len(enditem)]
        m=m[:_tmp[0]]+str(replacement)+m[_tmp[1]:]
    else:
        m=m[:replaceindex]+str(replacement)+m[replaceindex:]
    with open(file,"w") as f:
        f.write(m)
    m=None

def addnewversion(main="",version="",maxv="",minv="",name="",req="",change=""):
    if version<=returnfromfile(module_dir+"changelog.txt","",":"):
        popup("Error","\nModule version must be greater than the previous one")
    elif version and maxv and minv and (maxv>=minv):
        name,req=checklist([name,req],["","N/A"])
        main.destroy()
        packtozip(module_dir,str(module_name)+" "+str(returnfromfile(module_dir+"changelog.txt","",":")))
        savemodulechanges(["__init__.py","commands.txt","metadata.txt","changelog.txt"],textboxinputs)
        if name:
            name=' - The "'+str(name)+'" update'
        if (returnfromfile(module_dir+"changelog.txt","minver:",enditem="\n",default=minv) != minv) or (returnfromfile(module_dir+"changelog.txt","maxver:",enditem="\n",default=maxv) != maxv):
            if change!="":
                change+="\n"
            change+="added compatability for new LOaBIS Version"
        replaceinfile(module_dir+"changelog.txt","","",str(version)+":"+name+"\nminver:"+minv+"\nmaxver:"+maxv+"\nrequired:"+req+"\n"+change+"\n\n")
        replaceinfile(module_dir+"__init__.py",'module.module("'+str(module_name)+'","',",",'module.module("'+str(module_name)+'","'+Focus_Dir[1]+'",')
        loadmodulechanges(["__init__.py","commands.txt","metadata.txt","changelog.txt"],textboxinputs)
        popup("Complete","\nThe new version has been succesfully created!\n\nA formated zip file containing the release is in the same directory as the module wizard")
    else:
        popup("Error","\nPlease check that the details given are correct")

def addnewver(directory=""):
    newver=genwindow(title="New Version",resize=False)
    newmodtext=Label(newver,text="Create new version:\n(* are not required)").grid(row=0,column=0,columnspan=2,pady=5,padx=5,sticky=W+E)
    _Ver=enterbox(newver,"Version number",returnfromfile(module_dir+"changelog.txt","",":"),1)[1]
    compattext=Label(newver,text="Loabis version compatability:").grid(row=2,pady=5)
    _compatmax=enterbox(newver,"Maximum compatible",Focus_Dir[1],3)[1]
    _compatmin=enterbox(newver,"Minimum compatible",Focus_Dir[1],4)[1]
    seperator(newver,row=5)
    _Name=enterbox(newver,"Version name *","",6)[1]
    _Req=enterbox(newver,"Required modules *",returnfromfile(module_dir+"changelog.txt","required:"),7)[1]
    _quit=Button(newver,text="Close",command=newver.destroy).grid(row=8,column=0,pady=5,padx=5,sticky=W+E)
    _accept=Button(newver,text="Accept",command=lambda:addnewversion(newver,_Ver.get(),_compatmax.get(),_compatmin.get(),_Name.get(),_Req.get())).grid(row=8,column=1,pady=5,padx=5,sticky=W+E)

    mainloop()

def packtozip(directory="",name=""):
    import shutil
    shutil.make_archive(str(name),'zip',str(directory))

def findfrommod(file="",search=""):
    if not file[-3:]==".py":
        file+=sep+"__init__.py"
    with open(file,"r") as f:
        m=f.read()

    end=""
    for x in search[::-1]:
        if x in ["(","[","{"]:
            end+=x
        if not x in ["(","[","{"]:
            break
    end=end.replace("(",")").replace("[","]").replace("{","}")

    try:
        _temp = m.split(search)[1].split(end)[0].replace('"',"").split(",")
        return _temp
    except:
        return []

def retfuncs(file=""):
    if not file[-3:]==".py":
        file+=sep+"__init__.py"
    with open(file,"r") as f:
        m=f.read()

    a,_temp=m.split("def "),[]
    for x in a[1:]:
        namee,description=x.split("(")[0],""
        varse=x.split("(")[1].split(")")[0].split(",")
        if "'''" in x.split("\n")[1]:
            description=x.split("'''")[1]
        _temp.append([namee,varse,description])
    return _temp

def fetchuseable(direc="",name=""):
    global loa_funcs,py_funcs,loa_mods,py_mods
    sea=direc+sep+name
    pymods=findfrommod(sea,"module.needs([")
    if pymods != []:
        py_mods = pymods
    loamods=[name]+findfrommod(sea,"module.hasdependancy([")
    if loamods != []:
        loa_mods = loamods
    for x in loa_mods:
        loa_funcs.append(retfuncs(direc+sep+x))

def missing(frame="",row=0,column=0,gp=1,span=1):
    text=textlabel(frame,"This is an incomplete or unfinished\narea, please wait for content updates",row,column,5,10,gp,span)
    return text

def textlabel(main="",text="",row=0,column=0,padx=5,pady=5,gp=1,span=1):
    text=Label(main,text=text)
    if gp:
        text.pack(padx=padx,pady=pady)
    else:
        text.grid(padx=padx,pady=pady,column=column,row=row,columnspan=span)
    return text

def startwizard(name=""):
    globals()["loa_funcs"]=[]
    globals()["py_funcs"]=[]
    globals()["loa_mods"]=[]
    globals()["py_mods"]=[]
    globals()["home_dir"]=Focus_Dir[2].replace("//LOaBIS.py","").replace("/LOaBIS.py","").replace("\\LOaBIS.py","").replace("\LOaBIS.py","")
    fetchuseable(home_dir,name)
    mainwizard(name)

def seperator(main="",orient="H",row=0,column=0):
    if orient == "H":
        sep=Separator(main,orient=HORIZONTAL)
        sep.grid(row=row,column=column,columnspan=100,sticky=W+E,pady=5)
    else:
        sep=Separator(main,orient=VERTICAL)
        sep.grid(row=row,column=column,rowpan=100,sticky=N+S,padx=5)
    return sep

def quitwizard(main=""):
    from tkinter import messagebox
    if messagebox.askokcancel(title="Quit",default="cancel",icon="error",message="Are you sure you want to quit the wizard?\n\n(any changes will be lost)"):
        main.destroy()

def getimportedmodules(path=""):
    _logtext("Fetching imported modules")
    mods,funcs,docs,igno,sub=[module_name],[],[],[],[]
    with open(path+"__init__.py","r") as f:
        m=f.read()

    if "from " in m:
        for x in m.split("from ")[1:]:
            a=x.split("\n")[0]
            #mods+=[a.split(" ")[0]+"."+a.split("import ")[1]]
            igno+=[a.split("import ")[1]]
    if "import" in m:
        for x in m.split("import "):
            if "," in x:
                mods+=x.split("\n")[0].replace(" ","").replace("from","").replace("*","").split(",")
    for x in igno:
        if x in mods:
            mods.remove(x)

    _logtext("Fetching functions from imported modules")
    for x in mods:
        a=dir()
        if "." in x:
            exec("from "+x.split(".")[0]+" import "+x.split(".")[1])
        else:
            try:
                exec("from "+str(x)+" import *")
            except:
                exec("import "+str(x))
        mods[mods.index(x)]=x.split(".")[0]
        b=dir()
        c=b
        for y in a:
            if y in b:
                c.remove(y)
        for z in c:
            if z in mods:
                c.remove(z)
        _a=[]
        for u in c:
            try:
                try:
                    _a.append(getattr(globals()[str(x)],str(u)).__doc__)
                except:
                    exec("from "+x+" import "+u)
                    _a.append(globals()[str(u)].__doc__)
            except:
                _a.append("No DocString Available")
        funcs.append(c)
        docs.append(_a)

    _logtext(str(len(mods))+" modules loaded with "+str(length(funcs))+" functions")
    return mods,funcs,docs

def length(lst=[]):
    lnt=0
    for y in lst:
        try:
            if [str(y)]!=list(y):
                lnt+=len(y)
            else:
                lnt+=1
        except:
            lnt+=1
    return lnt

def myfuncs(dire=""):
    _logtext("getting module functions")
    func,text,doc=[],[],[]
    with open(dire+"__init__.py","r") as f:
        m=f.read()
    a=m.split("def ")[1:]
    for x in a:
        b="None"
        func.append(x.split("(")[0])
        text.append(x.split(":")[0])
        if '"""' in x:
            b=x.split('"""')[1]
        doc.append(b)
    return func,text,doc

def change_modmod(*args):
    modfunctext.destroy()
    modfuncdrop.destroy()
    try:
        globals()["modfunc"],globals()["modfunctext"],globals()["modfuncdrop"]=dropdown(functab,"Function",impfunc[impmod.index(modmod.get())][0],impfunc[impmod.index(modmod.get())],6,dropsticky="ew")
    except:
        globals()["modfunc"],globals()["modfunctext"],globals()["modfuncdrop"]=dropdown(functab,"Function",["None found"],["None found"],6,dropsticky="ew")
        #modfunc.trace('w',change_modfunc)

def simfunc(function=""):
    import difflib
    _f=[]
    for x in impfunc:
        for y in x:
            _f.append(impmod[impfunc.index(x)]+"."+y)
    a,b=sorted(_f, key=lambda x: difflib.SequenceMatcher(None, x.split(".")[1], function).ratio(), reverse=True),"The 10 most similar functions to:\n'"+str(function)+"' are:\n"
    for x in a[0:10]:
        b+="\n"+x
    return b

def insrt(txt="",text=""):
    txt.insert(INSERT,str(text))

def add_modfunc(txt):
    from inspect import signature
    mod=impmod.index(modmod.get())
    func=impfunc[mod].index(modfunc.get())
    try:
        _f=module_func[1][module_func[0].index(modfunc.get())]
    except:
        _f=str(modmod.get()+".").replace(module_name+".","")+str(impfunc[mod][func])
        try:
            try:
                _f+=str(signature(getattr(globals()[str(modmod.get())],str(modfunc.get()))))
            except:
                _f+=str(signature(globals()[str(modfunc.get())]))
        except:
            _f+="()"
    insrt(txt,str(_f))

def makefunc(mods,coms,chan):
    main=genwindow(title="Create a new function")
    missing(main)

def editfunc(mods,coms,chan):
    main=genwindow(title="Edit a function")
    missing(main)

def mainwizard(name=""):
    _logtext("Launching main wizard")
    globals()["main"]=genwindow(title="Module wizard for:   "+remexcess(Focus_Dir[0])+" v"+str(Focus_Dir[1]),resize=False)
    globals()["module_name"]=str(name)
    globals()["module_dir"]=home_dir+sep+str(name)+sep
    globals()["module_func"]=myfuncs(module_dir)
    globals()["tabr"]=Notebook(main)
    globals()["tabs"]=Notebook(main)
    globals()["impmod"],globals()["impfunc"],globals()["impdoc"]=getimportedmodules(module_dir)
    title = textlabel(main,text="Editing:\n"+str(module_name)+", version "+str(returnfromfile(module_dir+"changelog.txt","",":"))+"\nLOaBIS, version: "+str(Focus_Dir[1]))

    globals()["functab"],modtab,tab1,tab2,tab3,tab4=Frame(tabr),Frame(tabr),Frame(tabs),Frame(tabs),Frame(tabs),Frame(tabs)
    tabr.add(functab,text="Fuctions")
    tabr.add(modtab,text="Module")
    tabr.pack(fill="both",expand=True,padx=5,pady=5,side=LEFT)
    tabs.add(tab1,text="Main Module script")
    tabs.add(tab2,text="User commands list")
    tabs.add(tab3,text="Metadata")
    tabs.add(tab4,text="Changelog")
    tabs.pack(fill="both",expand=True,padx=5,pady=5)
    
    #First tabs
    #tab 1
    title=textlabel(functab,"Search by name:",0,0,gp=0)

    funcsearchtext,funcsearchbox=enterbox(functab,"Search","",1,0)
    funcseatch=Button(functab,text="Search",command=lambda:popup("Search functions",simfunc(funcsearchbox.get()),padx=10,pady=10)).grid(row=2,column=1,padx=5,pady=5)
    seperator(functab,"H",3,0)

    title=textlabel(functab,"Search by module:",4,0,gp=0)
    globals()["modmod"]=dropdown(functab,"Module",impmod[0],impmod,5,dropsticky="ew")[0]
    modmod.trace('w',change_modmod)
    globals()["modfunc"],globals()["modfunctext"],globals()["modfuncdrop"]=dropdown(functab,"Function",impfunc[impmod.index(modmod.get())][0],impfunc[impmod.index(modmod.get())],6,dropsticky="ew")

    seperator(functab,"H",8,0)
    title=textlabel(functab,"Creation:",9,0,gp=0)
    createfunc=Button(functab,text="Create function",command=lambda:makefunc(mod_enter,coms_enter,change_enter)).grid(row=10,column=0,padx=5,pady=5)
    editfunc=Button(functab,text="Edit function",command=donothing).grid(row=10,column=1,padx=5,pady=5)

    #tab 2
    missing(modtab)    

    #Second tabs
    #tab1
    mod_enter=setscrollbox(tab1,50,20,1,1,1,1,5,5,2)[0]
    funcinsert=Button(functab,text="Insert at cursor",command=lambda:add_modfunc(mod_enter)).grid(row=7,column=1,padx=5,pady=5)

    #tab2
    coms_enter=setscrollbox(tab2,50,20,1,1,1,1,5,5,2)[0]

    #tab3
    meta_enter=setscrollbox(tab3,50,20,1,1,1,1,5,5,2)[0]

    #tab4
    change_enter=setscrollbox(tab4,50,20,1,1,1,1,5,5,2)[0]

    loadmodulechanges(["__init__.py","commands.txt","metadata.txt","changelog.txt"],[mod_enter,coms_enter,meta_enter,change_enter])
    globals()["textboxinputs"]=[mod_enter,coms_enter,meta_enter,change_enter]

    newvb=Button(main,text="Create new version",command=lambda:addnewver(module_dir)).pack(side=LEFT,pady=5,padx=5)
    saveb=Button(main,text="Save changes",command=lambda:savemodulechanges(["__init__.py","commands.txt","metadata.txt","changelog.txt"],[mod_enter,coms_enter,meta_enter,change_enter])).pack(side=LEFT,pady=5,padx=5)
    quitb=Button(main,text="Quit wizard",command=lambda:quitwizard(main)).pack(side=LEFT,pady=5,padx=5)

choosedirectory()
