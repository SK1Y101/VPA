import datetime,os,subprocess,urllib.request,urllib.error,csv,zipfile,shutil,threading,time,webbrowser,sys
from tkinter import *
from tkinter.ttk import *

ostype=sys.platform
globals()["sep"]="/"
if "win" in ostype:
    globals()["sep"]="\\"
globals()["Main_Data_Dir"]=os.path.expanduser("~")+sep+"LOaBIS"
globals()["iconpath"]=Main_Data_Dir+sep+"Loa_icon.ico"

def choosedirectory():
    _logtext("Launching module installer",1)
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
    Open=setbutton(Buttons,"Install",8,lambda:instdirectory(Entries),3,0)
    Info=Text(main,width=30,height=8)

    Buttons.grid(row=2,column=0,padx=5,pady=5,sticky=W)
    Info.grid(row=2,column=1,padx=5,pady=5,sticky=N+S+E+W)

    bindcom(Entries,['<Double-1>','<<ListboxSelect>>'],[lambda x:Open.invoke(),lambda x:changeinfo(Entries,Info)])
    updateentries(Entries)
    changeinfo(Entries,Info)
    main.bind("<Destroy>",lambda x:savedatafile())
    mainloop()

def instdirectory(entry):
    from tkinter.filedialog import askdirectory
    _logtext("Installing new LOaBIS Version from online")
    main = genwindow("Install LOaBIS",posx=100,posy=100,resize=False)
    globals()["Direc"]=askdirectory(title="Select LOaBIS Locations")+sep+"Loa"
    if not os.path.exists(Direc):
        os.makedirs(Direc)
    globals()["mtext"],globals()["ttext"],globals()["progress"]=StringVar(),StringVar(),Progressbar(main,mode="indeterminate")

    versions=[]
    if not os.path.isfile(Main_Data_Dir+sep+"temp_VPA.zip"):
        getonlinefiles([getdat(getonlinemodules(),"VPA")])
    with zipfile.ZipFile(Main_Data_Dir+sep+"temp_VPA.zip","r") as Zip:
        with Zip.open("changelog.txt") as change:
            a=str(change.read())[2:-1].replace("\\r","").replace("\r","").replace("\\n","\n").split("\n\n")
            for y in a[0:10]:
                versions.append(y.split(":")[0])
    _logtext("Fetching "+str(len(versions))+" most recent versions: "+str(versions))

    settop(main)

    Name_text=Label(main,text="Name")
    Dir_text=Label(main,text="Directory")
    Ver_choice,Ver_text,Ver=dropdown(main,"Install Version","Select Version",versions,2,0,1,W)
    Dir=Entry(main)
    Name=Entry(main)
    
    Name_text.grid(row=0,column=0,padx=5,pady=5)
    Name.grid(row=0,column=1,padx=5,pady=5)
    Dir_text.grid(row=1,column=0,padx=5,pady=5)
    Dir.grid(row=1,column=1,padx=5,pady=5)
    Dir.insert(0,Direc+sep)
    Dir.configure(state=DISABLED)

    Accept=setbutton(main,"Accept",20,lambda:instloa(name,Ver_choice,main,entry),3,0)
    Cancel=setbutton(main,"cancel",20,main.destroy,3,1)

    mainloop()

def instloa(name,version,main,entry):
    _logtext("Installing LOaBIS Version "+str(version))
    extracttoloc(Main_Data_Dir+sep+"temp_VPA.zip",Direc,version.get())
    globals()["Focus_Dir"]=[0,0,Direc+sep+"LOaBIS.py"]
    modinst(Direc+sep)
    if os.path.isfile(Direc+sep+"temp_VPA.zip"):
        os.remove(Direc+sep+"temp_VPA.zip")
    _logtext("Installed successfully, returning to version select")
    returndirs(name,main,entry)

def bindcom(binder="",select=[],command=[]):
    for x in range(len(select)):
        binder.bind(select[x],command[x])

def dropdown(window="",text="",default="",options=[],row=0,column=0,columnspan=1,sticky="",dropsticky=""):
    choice=StringVar()
    choices=[default]+options
    text=Label(window,text=text)
    option=OptionMenu(window,choice,*choices)
    text.grid(row=row,column=column,columnspan=columnspan,sticky=sticky)
    option.grid(row=row,column=int(column+columnspan),sticky=dropsticky)
    return choice,text,option

def checkbox(window="",text="",value=0,row=0,column=0,columnspan=1,sticky=""):
    chkvar=IntVar()
    if value=="False":
        value=False
    chkvar.set(bool(value))
    button=Checkbutton(window,variable=chkvar)
    text=Label(window,text=text)
    text.grid(row=row,column=column,columnspan=columnspan,sticky=sticky)
    button.grid(row=row,column=int(column+columnspan))
    return chkvar,text,button

def setbutton(window="",text="",width=10,command="",row=0,column=0,padx=5,pady=5,sticky="",columnspan=1):
    button=Button(window,text=text,width=width,command=command)
    button.grid(row=row,column=column,padx=padx,pady=pady,columnspan=columnspan,sticky=sticky)
    return button

def setscrollbox(window="",width=0,height=0,row=0,column=0,scolumn=0,columnspan=1,pady=0,padx=0,wtype=0):
    if wtype==2:
        Box=Text(window,width=width,height=height)
    elif wtype==1:
        Box=Canvas(window,width=width,height=height)
    else:
        Box=Listbox(window,width=width,height=height)
    Scroll=Scrollbar(window)
    Box.grid(row=row,column=column,columnspan=columnspan,pady=pady,padx=padx,sticky=N+S+E+W)
    Scroll.grid(row=row,column=columnspan+max(column+1,scolumn),pady=pady,padx=padx,sticky=N+S)
    Box.config(yscrollcommand=Scroll.set)
    Scroll.config(command=Box.yview)
    return Box, Scroll

def checkicon():
    a,b=[".ico",".gif"],["htlqveg9moprz42/Loa_icon.ico?dl=0","e9p2o0cnhvm62dp/Loa_icon.gif?dl=0"]
    _logtext("Checking LOaBIS Icon download")
    for x in range(2):
        if not os.path.isfile(iconpath.replace(".ico",a[x])):
            _logtext(iconpath.replace(".ico",a[x])+" not found")
            if connect():
                link="https://www.dropbox.com/s/"+b[x]
                urllib.request.urlretrieve(link,iconpath.replace(".ico",a[x]))

def seticon(main,icon=iconpath):
    try:
        return main.iconbitmap(icon)
    except:
        return False

def loaddatafile(directory=Main_Data_Dir):
    try:
        _logtext("Loading directory data")
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

def attempt(data="",find="",default="",lst=False):
    ret=""
    try:
        if lst==True:
            ret=data.split("<"+find+">")[1].split("</"+find+">")[0].split("\n")
            temp,_temp=ret,[]
            for x in range(len(temp)):
                if len(str(temp[x])) < 20:
                    _temp=[x]+_temp
            for x in _temp:
                ret.pop(x)
        else:
            ret=data.split("<"+find+">")[1].split("</"+find+">")[0].replace("\n","")
    except:
        ret=default
    return ret

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

def default_dir():
    _logtext("Fetching default directory")
    dire=str(os.getcwd())+sep+"LOaBIS.py"
    info=os.stat(dire)
    if os.path.isfile(dire):
        Dir_Data.append([makelen("Default",20),getactualver(dire,"0.2.00"),dire,now(),datetime.datetime.fromtimestamp(info.st_ctime).strftime('%Y-%m-%d %H:%M:%S').replace("-","/"),info.st_size])

def savedatafile(directory=Main_Data_Dir):
    _logtext("Saving data")
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

def getshow(entry):
    try:
        a=entry.curselection()[0]
    except:
        a=0
    ret=Dir_Data[a]
    ret[3],ret[5]="",""
    return getmissing(Dir_Data[a])

def opendirectory(entry):
    if Dir_Data:
        show=getshow(entry)
        try:
            os.startfile(str(show[2]).replace("//LOaBIS.py","").replace("/LOaBIS.py","").replace("\\LOaBIS.py","").replace("\LOaBIS.py",""))
        except:
            subprocess.Popen('explorer "{0}"'.format(os.getcwd()))

def removedirectory(entry):
    from tkinter import messagebox
    if Dir_Data:
        show=getshow(entry)
        if messagebox.askokcancel(title="Remove",default="cancel",icon="error",message="Are you sure you want to remove:\n\n"+str(show[0])+"\n"+str(show[1])+"\n"+str(show[2])):
            Dir_Data.remove(show)
            updateentries(entry)

def getactualver(directory,ver,module="_core"):
    try:
        with open(directory.replace("LOaBIS.py",str(module)+sep+"__init__.py"),"r") as f:
            vers=(str(f.read()).split("module.module(")[1].split(")")[0].split(",")[1])[1:-1]
        return vers
    except:
        return ver

def instext(text="",ins=[]):
    try:
        text.delete(0.0,END)
    except:
        text.delete(1.0,END)
    text.configure(state=NORMAL)
    for x in ins:
        text.insert(END,x)
    text.configure(state=DISABLED)

def changeinfo(entry,text):
    if Dir_Data:
        show=getshow(entry)
        ver=getactualver(show[2],show[1])
        a=["Version:   "+str(ver)+"\n","Created:   "+str(show[4])+"\n","Added:     "+str(show[3])+"\n","Size:      "+str(show[5])+" Bytes\n","Name:      "+str(show[0][0:16])+"...\n","Directory:\n"+str(show[2])+"\n"]
    else:
        a=["No Versions Found"]
    instext(text,a)

def editdirectory(Entries=""):
    if Dir_Data:
        show=getshow(Entries)
        _logtext("Editing directory "+str(show[0]))
        Edit=genwindow("Edit Directory",posx=150,posy=150,resize=False)

        Name_text=Label(Edit,text="Name")
        Dir_text=Label(Edit,text="Directory")
        Ver_text=Label(Edit,text="Version")
        Name=Entry(Edit)
        Dir=Entry(Edit)
        Ver=Entry(Edit)
        Accept=setbutton(Edit,"Accept",20,lambda:returndirs(Name,Edit,Entries),3)
        Change=setbutton(Edit,"Change Directory",20,lambda:returndirs(Name,Edit,Entries),3,1)

        Name_text.grid(row=0,column=0,padx=5,pady=5)
        Dir_text.grid(row=1,column=0,padx=5,pady=5)
        Ver_text.grid(row=2,column=0,padx=5,pady=5)
        Name.grid(row=0,column=1,padx=5,pady=5)
        Dir.grid(row=1,column=1,padx=5,pady=5)
        Ver.grid(row=2,column=1,padx=5,pady=5)
        Dir.insert(END,show[2])
        Name.insert(END,show[0].replace(" ",""))
        Ver.insert(END,show[1])
        Ver.configure(state=DISABLED)
        globals()["Found_ver"],globals()["Found_dir"]=show[1:3]

        mainloop()

def adddirectory(Entries=""):
    _logtext("Adding new directory")
    Add_new=genwindow("Add New Directory",posx=150,posy=150,resize=False)

    Name_text=Label(Add_new,text="Name")
    Dir_text=Label(Add_new,text="Directory")
    Ver_text=Label(Add_new,text="Version")
    Name=Entry(Add_new)
    Dir=Entry(Add_new)
    Ver=Entry(Add_new)
    Accept=setbutton(Add_new,"Accept",20,lambda:returndirs(Name,Add_new,Entries),3,0)

    Name_text.grid(row=0,column=0,padx=5,pady=5)
    Dir_text.grid(row=1,column=0,padx=5,pady=5)
    Ver_text.grid(row=2,column=0,padx=5,pady=5)
    Name.grid(row=0,column=1,padx=5,pady=5)
    Dir.grid(row=1,column=1,padx=5,pady=5)
    Ver.grid(row=2,column=1,padx=5,pady=5)
    getdir(Dir,Ver,Add_new)

    mainloop()

def returndirs(Name="",main="",entry=""):
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

def now():
    date_time=str(datetime.datetime.now())
    return date_time[0:4]+"/"+date_time[5:7]+"/"+date_time[8:10]+" "+date_time[11:13]+":"+date_time[14:16]

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

def updateentries(entry):
    entry.delete(0,END)
    for x in Dir_Data:
        ver=getactualver(x[2],x[1])
        entry.insert(END," "+ver+"      "+x[0]+" "+x[2])
        entry.select_set(first=0)

def settop(main=""):
    main.attributes('-topmost', True)
    main.attributes('-topmost', False)

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
        tfl()
        installer()

def tfl(val=0):
    _logtext("Loading")
    main=genwindow("Loading")
    globals()["ptext"]=StringVar()
    globals()["mtext"]=StringVar()
    globals()["ttext"]=StringVar()
    globals()["progress"]=Progressbar(main,mode="indeterminate")
    progresstext=Label(main,textvariable=ptext,justify=CENTER)
    minortext=Label(main,textvariable=mtext,justify=CENTER)
    timetext=Label(main,textvariable=ttext,justify=CENTER)
    progresstext.pack(pady=10)
    minortext.pack(pady=10)
    progress.pack(padx=10,fill="x")
    timetext.pack(pady=10)
    progress.start(5)

    t1=threading.Thread(target=lambda:loadthread(Focus_Dir,main,val),name="Load")
    t1.start()
    mainloop()

def threadingload(main=""):
    globals()["min_download_days"]=-1
    tfl(1)
    installer()

def getlastdl():
    global Found_dir
    try:
        _logtext("Fetching last download time")
        with open(Main_Data_Dir+sep+"UpdaterData.txt","r") as f:
            m=f.read()
        dlow=attempt(m,"Download",datetime.datetime(2000,1,1))
        globals()["last_download"]=datetime.datetime(int(dlow.split("-")[0]),int(dlow.split("-")[1]),int(dlow.split("-")[2].split(" ")[0]))
    except:
        globals()["last_download"]=datetime.datetime.fromtimestamp(os.stat(Main_Data_Dir+sep+"temp_VPA.zip").st_ctime)

def loadthread(show,main,val=0):
    global last_download
    _logtext("Checking settings")
    ptext.set("Loading Local Data")
    mtext.set("Checking settings")
    download=False
    getlastdl()
    if not os.path.isfile(Main_Data_Dir+sep+"temp_VPA.zip"):
        download=True
    else:
        if (datetime.datetime.now()-last_download).days > min_download_days:
            download=True
    a="Fetching local modules"
    _logtext(a)
    mtext.set(a)
    globals()["localmods"]=getlocalmodules(show[2])
    ptext.set("Loading Online Data")
    mtext.set("Establishing Connection")
    ttext.set("Unknown time remaining")
    connection=connect()
    if connection:
        if download:
            a="Fetching online modules"
            _logtext(a)
            mtext.set(a)
            allmods=getonlinemodules()
            mtext.set(str(len(allmods))+" found")
            progress.stop()
            progress.configure(mode="determinate",maximum=int(1+len(allmods)))
            getonlinefiles(allmods)
            progress.step()
            globals()["last_download"],globals()["min_download_days"]=datetime.datetime.now(),mindlday
        else:
            a="Fetching online LOaBIS version"
            _logtext(a)
            mtext.set(a)
            progress.stop()
            progress.configure(mode="determinate",maximum=2)
            mtext.set("Fetching LOaBIS Versions")
            getonlinefiles([getdat(getonlinemodules(),"VPA")])
            progress.step()
            if str(autoupdate)=="True":
                mtext.set("Installing newest LOaBIS Version")
                time.sleep(2)
                thisdir=Focus_Dir[2].replace("LOaBIS.py","__Temp__")
                tempfiles,filenames=getoverwrites(Focus_Dir[2].replace("LOaBIS.py",sep+getdat(Data,x)[0]))
                extracttoloc(Main_Data_Dir+sep+"temp_"+getdat(Data,x)[0]+".zip",thisdir,modinstver[x])
                modinst(thisdir+sep,getdat(Data,x)[0],tempfiles,filenames)
                if os.path.isdir(thisdir):
                    shutil.rmtree(thisdir)
            progress.step()
        mtext.set("Loading complete")
        savedatafile(Main_Data_Dir)
        setdata(Main_Data_Dir)
        time.sleep(1)
        main.destroy()
        if val==1:
            popup("Changes","The updated module data will be applied when the main installer window closed.\n\nPlease close the main installer")
    elif os.path.isfile(Main_Data_Dir+sep+"temp_VPA.zip"):
        a="Connection not established, using backup"
        _logtext(a)
        ttext.set("2 Seconds remaining")
        mtext.set(a)
        setdata(Main_Data_Dir)
        time.sleep(1)
        main.destroy()
        if val==1:
            popup("Changes","The updated module data will be applied when the main installer window closed.\n\nPlease close the main installer")
    else:
        a="Connection not established, Terminating"
        _logtext(a)
        mtext.set(a)
        ttext.set("1 Second remaining")
        time.sleep(1)
        main.destroy()
        if val==1:
            popup("Changes","The updated module data will be applied when the main installer window closed.\n\nPlease close the main installer")

def setdata(dire=""):
    _logtext("Formating found module data")
    #Data=[["name","screenname","author","description","url","file",["version","max loa version","min loa version","required","changelog"]]]
    globals()["Data"]=[]
    globals()["SmallData"]=[]
    files=next(os.walk(dire))[2]
    files.remove("UpdaterData.txt")
    files.remove("Loa_icon.ico")
    files.remove("Loa_icon.gif")
    for x in files:
        try:
            with zipfile.ZipFile(dire+sep+x,"r") as Zip:
                temp=[]
                with Zip.open("metadata.txt") as meta:
                    a=str(meta.read())[2:-1].replace("\\r","").replace("\r","")
                    for y in ["name","screenname","author","description","url"]:
                        try:
                            temp.append(a.split(y+":")[1].replace("\\n","\n").split("\n")[0])
                        except:
                            temp.append("N/A")
                temp.append(dire+sep+x)
                with Zip.open("changelog.txt") as change:
                    a=str(change.read())[2:-1].replace("\\r","").replace("\r","").replace("\\n","\n").split("\n\n")
                    __temp=[]
                    for y in a:
                        _temp=[y.split(":")[0]]
                        for w in ["minver:","maxver:","required:"]:
                            try:
                                _temp.append(y.split(w)[1].split("\n")[0])
                            except:
                                _temp.append("N/A")
                        _temp.append(y)
                        __temp.append(_temp)
                    temp.append(__temp)
            Data.append(temp)
        except Exception as e:
            _logtext("Could not open: "+str(dire+sep+x)+"\nError: "+str(type(e))+"; "+str(e))
    for x in Data:
        y=[x[0],x[1],x[2],x[3],x[4],x[5],x[6][0][0],x[6][0][1],x[6][0][2]]
        if x[0] !="VPA":
            SmallData.append(y)

def average(vals=[]):
    a=0
    for x in vals:
        a+=float(x)
    return float(a/len(vals))

def getonlinefiles(modules=[]):
    time_taking=[]
    _logtext("Fetching "+str(int(len(modules)))+" online modules: "+str(modules))
    for x in modules:
        stime=datetime.datetime.now()
        name,url=x
        mtext.set(name+" - "+str(modules.index(x)+1)+"/"+str(len(modules)))
        progress.step()
        out_file,headers = urllib.request.urlretrieve(url.replace("?dl=0","?dl=1"),Main_Data_Dir+sep+"temp_"+name+".zip")
        time_taking.append((datetime.datetime.now()-stime).total_seconds())
        ttext.set("about "+str(round(average(time_taking)*(len(modules)-modules.index(x)),2))+" seconds remaining")
    _logtext("Modules loaded")

def getonlinemodules():
    url='https://www.dropbox.com/s/lhixedpidsarpxk/Modules.txt?dl=1' #dl=1 means it will rerieve a useable file (zip, or otherwise specified), as opposed to the html file of the webpage.
    data=[]
    with urllib.request.urlopen(url) as u:
        temp=str(u.read())[2:-1].replace("\\r\\n",",").split(",")
    for x in range(int(len(temp)/2)):
        data.append([temp[2*x],temp[2*x+1].replace("?dl=0","?dl=1")])
    return data

def connect():
    try:
        urllib.request.urlopen("http://216.58.192.142",timeout=1)
        return True
    except urllib.error.URLError as err:
        return False

def getlocalmodules(dire=os.getcwd()):
    modules=next(os.walk(dire.replace(sep+"LOaBIS.py","")))[1]
    modules.sort()
    if "__pycache__" in modules:
        modules.remove("__pycache__")
    _logtext("Fetching "+str(int(len(modules)))+" local modules: "+str(modules))
    for x in range(len(modules)):
        modules[x]=[modules[x],getactualver(dire.replace("LOaBIS.py","")+str(modules[x])+sep+"__init__.py","0.0.00")]
    return modules

def remexcess(text="",rem=" "):
    while text[-1]==rem:
        text=text[:-1]
    return str(text)

def setbar(main=""):
    menubar=Menu(main)
    filemenu=Menu(menubar, tearoff=0)
    filemenu.add_command(label="Select install",command=getnewdir)
    filemenu.add_command(label="Open directory",command=lambda:os.startfile(home_dir))
    filemenu.add_separator()
    filemenu.add_command(label="Download online modules",command=lambda:threadingload(main))
    filemenu.add_command(label="Import modules",command=donothing)
    filemenu.add_command(label="Export modules",command=donothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit",command=main.destroy)
    #settigmenu
    settingmenu=Menu(menubar, tearoff=0)
    settingmenu.add_command(label="installer settings",command=updatersetting)
    #helpmenu
    helpmenu=Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Report an issue",command=donothing)
    helpmenu.add_command(label="About",command=aboutupdater)
    helpmenu.add_separator()
    helpmenu.add_command(label="Module creation wizard",command=donothing)
    helpmenu.add_command(label="Add your module",command=donothing)
    helpmenu.add_separator()
    helpmenu.add_command(label="Contact Developers",command=donothing)
    #addmenubars
    menubar.add_cascade(label="File",menu=filemenu)
    menubar.add_cascade(label="Settings",menu=settingmenu)
    menubar.add_cascade(label="Help",menu=helpmenu)
    main.config(menu=menubar)

def launchvpa():
    _logtext("Closing installer")
    main.destroy()
    subprocess.call(['python', Focus_Dir[2]])
    if openwhenclosed=="True":
        installer()

def checka(a,default,sec):
    if a>=0:
        return a,sec
    else:
        return default,sec

def getinst(module=""):
    a=-1
    if getdat(Data,module)[1] in to_inst:
        a=1
    elif getdat(Data,module)[1] in to_uninst:
        a=0
    if any(module in sl for sl in localmods)==True:
        for x in localmods:
            if x[0]==module:
                return checka(a,1,x[1])
    else:
        return checka(a,0,"-")

def getdlver(module=[],inst="",name=""):
    if inst=="-":
        return "-",module[0],module[2]
    else:
        if inst==module[2]:
            return "-",module[0],module[2]
        else:
            return 0,module[0],module[2]

def getallowed(name=""):
    mod=getdat(Data,name)
    for x in range(int(minorver)):
        dlo=getdat(mod[6],majorver+"."+makelen(int(minorver)-x,2,1))
        if dlo !=None:
            break
    return dlo

def checkupdneeded(var,name,x):
    if var[x]==0:
        if (not name in to_upd) and getdat(localmods,name.lower()):
            to_upd.append(name)
    else:
        if name in to_upd:
            to_upd.remove(name)

def updateclick(var,name,self,x,t,ver):
    modinstver[name]=ver
    if t=="ins":
        if var[x]==0:
            if (not name in to_inst) and not getdat(localmods,name.lower()):
                to_inst.append(name)
            if name in to_uninst:
                to_uninst.remove(name)
        else:
            if (not name in to_uninst) and getdat(localmods,getdat(Data,name)[0]):
                to_uninst.append(name)
            if name in to_inst:
                to_inst.remove(name)
    elif t=="upd":
        checkupdneeded(var,name,x)
    var[x]=not var[x]
    updateupdate(updatei)
    self.configure(text=str(var[x]).replace("True","✓").replace("False","✗"))

def onclick(var,name,self,x,t):
    dlo=getallowed(name)
    if dlo !=None:
        updateclick(var,name,self,x,t,dlo[0])
    else:
        if download_all=="True":
            updateclick(var,name,self,x,t,getdat(Data,name)[6][0][0])
        else:
            popup("Inst. Err","Cannot install module with incompatible version\n\n(Or Change installer settings)")

def getdat(data=[],search=""):
    for x in data:
        if search in x:
            return x

def populate(main=""):
    main.delete(ALL)
    #Installed Update   Name Author InstalledVer LatestVer MaxLoaCompatible
    #Checkbox  checkbox Text Text   Number       Number    Number
    const=4
    for x in range(len(SmallData)):
        y=SmallData[x]
        name = y[1]
        _inst,instver=getinst(y[0])
        _upda,newest,vpamax=getdlver([y[6],y[7],y[8]],instver,y[0])
        inst[int(x+1)],upda[int(x+1)]=bool(_inst),_upda
        if _upda=="-":
            update=Button(main,text="-",state=DISABLED)
        else:
            if auto_dl_mod:
                upda[int(x+1)]=1
                checkupdneeded(upda,name,x+1)
            update=Button(main,text=str(upda[int(x+1)]).replace("True","✓").replace("False","✗").replace("1","✓").replace("0","✗"))
            update.configure(command=lambda n=name,v=upda,s=update,x=x+1:onclick(v,n,s,x,"upd"))

        instal=Button(main,text=str(inst[int(x+1)]).replace("True","✓").replace("False","✗").replace("1","✓").replace("0","✗"))
        instal.configure(command=lambda n=name,v=inst,s=instal,x=int(x+1):onclick(v,n,s,x,"ins"))
        instal.grid(row=x+const,column=0)
        update.grid(row=x+const,column=1)
        name=Button(main,text=name,command=lambda n=name,v=x:setfocus(n,v)).grid(row=x+const,column=2,sticky=W+E)
        author=Button(main,text=y[2],state=DISABLED).grid(row=x+const,column=3,sticky=W+E)
        installed=Button(main,text=instver,state=DISABLED).grid(row=x+const,column=4,sticky=W+E)
        latest=Button(main,text=newest,state=DISABLED).grid(row=x+const,column=5,sticky=W+E)
        maxver=Button(main,text=vpamax,state=DISABLED).grid(row=x+const,column=6,sticky=W+E)

def sortlist(main="",sorttype=0):
    global SmallData
    a=[0,0,1,2,0,6,7]
    Temp=sorted(SmallData, key=lambda x: x[int(a[sorttype])])
    if Temp==SmallData:
        Temp=Temp[::-1]
    SmallData=Temp
    populate(main)

def nameditem(title="",text="",row=0,column=0,padx=0,pady=0):
    name=Label(infotab11,text=title+":",foreground="gray")
    detail=Label(infotab11,text=text,wraplength=200)
    underline(name)
    name.grid(row=row,column=column,padx=padx,pady=pady,sticky=W)
    detail.grid(row=row,column=column+1,padx=padx,pady=pady,sticky=W)
    return name,detail

def makelen(text="",leng=0,inte=0):
    text=str(text)
    while len(text)<leng:
        if inte==1:
            text="0"+text
        else:
            text+=" "
    return text[0:leng]

def sorttext(text=""):
    a,y,_temp=text.split("\n"),1,text.split("\n")[0].replace("\\t","\n").replace("\\","")+"\n\n"
    for x in range(len(a)):
        if not ":" in a[x]:
            _temp+=makelen(y,2,1)+") "+a[x]+"\n"
            y+=1
    return _temp

def showchangelog(listbox,data,pos):
    width=300
    main=genwindow("Changelog",width+10,width+110)
    L1=Label(main,text="Changelog:\n")
    underline(L1)
    L1.pack(anchor="w")
    L2=Label(main,text=sorttext(data[listbox.curselection()[0]][pos]),wraplength=width).pack(fill="both",padx=5,pady=5)

def setfocus(focus,focusval):
    global infotab11,infotab1,infotab2,infotab21,Info
    DataFocus=Data.index(getdat(Data,focus))
    try:
        focusval,y=SmallData.index(getdat(SmallData,focus)),SmallData[focusval]
    except:
        b=Data[DataFocus]
        c=b[6][0]
        y=b[0],b[1],b[2],b[3],b[4],b[5],c[0],c[1]
    infotab11.destroy()
    infotab21.destroy()
    infotab11=Canvas(infotab1,width=10)
    infotab21,Scroll=setscrollbox(infotab2,30,10,1,0,3,3,5,5)
    infotab21.bind('<<ListboxSelect>>',lambda x:showchangelog(infotab21,Data[DataFocus][6],4))
    infotab11.pack()
    Name=Label(infotab11,text=y[0]).grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)
    About=Label(infotab11,text=y[3],wraplength=300).grid(row=1,column=0,columnspan=2,padx=5,sticky=W)
    s=Separator(infotab11,orient=HORIZONTAL).grid(row=2,column=0,columnspan=2,sticky=W+E,pady=5)
    ver,content=nameditem("Version",y[6],3,0,5,5)
    auth,content=nameditem("Author",y[2],4,0,5,5)
    home,content=nameditem("Homepage",y[4],5,0,5,5)
    comp,content=nameditem("Compatible",y[7],6,0,5,5)
    for x in Data[DataFocus][6]:
        ase=makelen(x[0],8)+"   "+makelen(x[1],8)+"   "+makelen(x[2],8)+"   "+makelen(x[3],8)
        infotab21.insert(END,ase)
        a,b=compatible(x[1],x[2],Focus_Dir[1]),["#ffffff","#98FB98","#32CD32"]
        infotab21.itemconfig(END,bg=b[a])

def compatible(minv,maxv,locv):
    if minv<=locv<=maxv:
        return 2
    elif (minv.split(".")[0:2]==locv.split(".")[0:2]) or (maxv.split(".")[0:2]==locv.split(".")[0:2]):
        return 1
    else:
        return 0

def updateupdate(c=""):
    a,b,d="",[to_upd,to_uninst,to_inst],["Updates:\n","Remove:\n","Install:\n"]
    for y in range(3):
        a+=d[y]
        for x in b[y]:
            a+=x+"\n"
        a+="\n"
    c.delete(ALL)
    c.create_text(5,5,anchor=NW,text=a)

def extracttoloc(startpath,endpath,version):
    _logtext("extracting files from "+str(startpath)+" to "+str(endpath))
    with zipfile.ZipFile(str(startpath),"r") as zip_file:
        if getdat(zip_file.namelist(),version):
            zip_file.extract(getdat(zip_file.namelist(),version),endpath)

def getoverwrites(dire=""):
    temp,old_files=[],[]
    with open(dire+sep+"__init__.py","r") as f:
        ovr=f.read()
    if "module.dont_overwrite(" in ovr:
        try:
            old_files=((ovr.split("module.dont_overwrite([")[1]).split("])")[0]).replace('"',"").split(",")
        except:
            old_files=[((ovr.split("module.dont_overwrite(")[1]).split(")")[0]).replace('"',"")]
    for x in old_files:
        if x in os.listdir(dire):
            with open(dire+sep+x,"r") as f:
                temp.append(f.read())
        else:
            old_files.remove(x)
    return temp,old_files

def modinst(dire="",name="",tempfiles=[],filenames=[]):
    if os.path.isdir(dire):
        for x in os.listdir(dire):
            with zipfile.ZipFile(dire+x,"r") as zip_file:
                zip_file.extractall(Focus_Dir[2].replace("LOaBIS.py",""))
        if len(tempfiles)>0:
            for x in range(len(tempfiles)):
                with open(Focus_Dir[2].replace("LOaBIS.py",sep+name.lower()+sep+filenames[x]),"w") as f:
                    f.write(tempfiles[x])

def installchanges():
    _logtext("Installing changes")
    _logtext(str(int(len(to_upd)))+" Updates to be installed: "+str(to_upd))
    _logtext(str(int(len(to_uninst)))+" Modules to be uninstalled: "+str(to_uninst))
    _logtext(str(int(len(to_inst)))+" Modules to be installed: "+str(to_inst))
    tabs.select(1)
    thisdir=Focus_Dir[2].replace("LOaBIS.py","__Temp__")
    for x in to_upd:
        tempfiles,filenames=getoverwrites(Focus_Dir[2].replace("LOaBIS.py",sep+getdat(Data,x)[0]))
        extracttoloc(Main_Data_Dir+sep+"temp_"+getdat(Data,x)[0]+".zip",thisdir,modinstver[x])
        modinst(thisdir+sep,getdat(Data,x)[0],tempfiles,filenames)
    for x in to_uninst:
        try:
            shutil.rmtree(Focus_Dir[2].replace("LOaBIS.py",getdat(Data,x)[0]))
        except:
            shutil.rmtree(Focus_Dir[2].replace("LOaBIS.py",sep+getdat(Data,x)[0]))
    for x in to_inst:
        extracttoloc(Main_Data_Dir+sep+"temp_"+getdat(Data,x)[0]+".zip",thisdir,modinstver[x])
    modinst(thisdir+sep)
    if os.path.isdir(thisdir):
        shutil.rmtree(thisdir)
    _logtext("Installation complete")
    main.destroy()
    installer()

def installer():
    _logtext("Opening main installer window")
    globals()["home_dir"]=Focus_Dir[2].replace("//LOaBIS.py","").replace("/LOaBIS.py","").replace("\\LOaBIS.py","").replace("\LOaBIS.py","")
    globals()["localmods"]=getlocalmodules(Focus_Dir[2])
    width,height,title=600,300,"Module installation for:   "+remexcess(str(Focus_Dir[0]))+" - "+str(Focus_Dir[1])
    globals()["main"]=genwindow(title,width+320,height+26,width,height)
    globals()["majorver"],globals()["minorver"]=Focus_Dir[1].split(".")[0]+"."+Focus_Dir[1].split(".")[1],Focus_Dir[1].split(".")[2]
    globals()["to_inst"],globals()["to_upd"],globals()["to_uninst"],globals()["modinstver"]=[],[],[],{}
    globals()["inst"],globals()["upda"]={},{}
    setbar(main)

    globals()["tabs"]=Notebook(main)
    tab1=Frame(tabs,height=10)
    tab2=Frame(tabs,height=10)
    tabs.add(tab1,text="Manage Modules")
    tabs.add(tab2,text="Updates")
    tabs.pack(fill="both",expand=True,padx=5,pady=5)
    const=5

    Launch=Button(tab1,compound=LEFT,text="Launch "+remexcess(Focus_Dir[0]),command=launchvpa)
    Apply=Button(tab1,compound=LEFT,text="Apply changes",command=installchanges)
    Refresh=Button(tab1,text="Refresh",command=lambda:populate(canvas))
    Launch.grid(row=0,column=0,pady=5,sticky=W,padx=5)
    Refresh.grid(row=0,column=1,pady=5,padx=5)
    Apply.grid(row=0,column=2,pady=5,sticky=W,padx=5)

    canvas,Scroll=setscrollbox(tab1,width-52,height-100,1,0,const,const,5,5,1)
    globals()["updatei"],Scrolli=setscrollbox(tab2,width+260,height-50,1,0,const,const,5,5,1)
    a=["Installed","Update","Name","Author","Version","Latest","Compatibility"]
    globals()["infotab"]=Notebook(tab1)
    globals()["infotab1"],globals()["infotab2"]=Frame(infotab),Frame(infotab)
    globals()["infotab11"]=Canvas(infotab1)
    globals()["infotab21"],Scroll=setscrollbox(infotab2,30,10,1,0,3,3,5,5)
    infotab21.bind('<<ListboxSelect>>',lambda x:showchangelog(infotab21,Data[DataFocus][6],4))
    infotab11.pack()
    Name=Label(infotab2,text="Ver      MinVer   MaxVer   Required").grid(row=0,column=0,columnspan=3,sticky="W")
    infotab21.grid(row=0,column=0,columnspan=2,padx=5,pady=5,sticky=W)
    infotab.add(infotab1,text="Metadata")
    infotab.add(infotab2,text="Versions")
    infotab.grid(row=1,column=const+1,padx=5,pady=5,sticky=N+S)
    for j in a:
        butt=Button(canvas,text=j,command=lambda st=a.index(j):sortlist(canvas,st))
        butt.grid(row=0,column=a.index(j),sticky=W+E)
    s=Separator(canvas,orient=HORIZONTAL).grid(row=1,column=0,columnspan=7,sticky=W+E,pady=5)
    addvpamodupd(canvas,2)
    s=Separator(canvas,orient=HORIZONTAL).grid(row=3,column=0,columnspan=7,sticky=W+E,pady=5)
    populate(canvas)
    setfocus("VPA",0)
    updateupdate(updatei)

    mainloop()

def addvpamodupd(main="",place=0):
    x,y=0,getdat(Data,"VPA")
    inst[x],instver=0,getdat(localmods,"_core")[1]
    upda[x],newest,vpamax=getdlver([y[6][0][0],y[6][0][1],y[6][0][2]],instver,y[0])
    name=y[1]
    if autoupdate:
        upda[x]=1
        checkupdneeded(upda,name,x)
    if newest>instver:
        update=Button(main,text=str(upda[x]).replace("True","✓").replace("False","✗").replace("1","✓").replace("0","✗"))
        update.configure(command=lambda n=name,v=upda,s=update,x=x:onclick(v,n,s,x,"upd"))
        update.grid(row=place,column=1)
    else:
        update=Button(main,text="-",state=DISABLED).grid(row=place,column=1)

    instal=Button(main,text="-",state=DISABLED).grid(row=place,column=0)
    name=Button(main,text=name,command=lambda n=name:setfocus(n,0)).grid(row=place,column=2,sticky=W+E)
    author=Button(main,text=y[2],state=DISABLED).grid(row=place,column=3,sticky=W+E)
    installed=Button(main,text=instver,state=DISABLED).grid(row=place,column=4,sticky=W+E)
    latest=Button(main,text=newest,state=DISABLED).grid(row=place,column=5,sticky=W+E)
    maxver=Button(main,text=vpamax,state=DISABLED).grid(row=place,column=6,sticky=W+E)

def genwindow(title="",width=0,height=0,mwidth=0,mheight=0,posx=0,posy=0,resize=True):
    new=Tk()
    new.title(title)
    seticon(new)
    if (width>0) and (height>0):
        new.geometry('%dx%d' % (max(width,mwidth+10),max(height,mheight+10)))
    if (mwidth>0) and (mheight>0):
        new.minsize(int(min(width,mwidth)),int(min(height,mheight)))
    if not resize:
        new.resizable(0,0)
    new.geometry("+"+str(posx)+"+"+str(posy))
    settop(new)
    return new

def underline(widget=""):
    from tkinter import font
    f=font.Font(widget, widget.cget("font"))
    f.configure(underline=True)
    return widget.configure(font=f)

def updatersetting():
    setting=genwindow("settings",posx=100,posy=100,resize=False)
    title=Label(setting,text="Change installer settings")
    save=setbutton(setting,"save changes",15,lambda:changesetting(setting,checkau,dlchoice,checkowc,checkdla,checkadm),10,2,0,5,W)
    discard=setbutton(setting,"Discard changes",15,setting.destroy,10,1,0,5,W)

    title.grid(row=0,column=0,columnspan=2,sticky=W)

    updates=Label(setting,text="\nUpdates:")
    updates.grid(row=1,column=0,sticky=W,columnspan=3)
    underline(updates)
    dlchoices=[1,2,7,14,28,56]
    checkadm,admbuttontext,admbutton=checkbox(setting,"Add Module updates automatically",auto_dl_mod,2,0,3,W)
    checkau,aubuttontext,aubutton=checkbox(setting,"Automatically download new LOaBIS version on startup",autoupdate,3,0,3,W)
    dlchoice,dltimetext,dltime=dropdown(setting,"Days between checking for module updates ",mindlday,dlchoices,4,0,3,W)

    misc=Label(setting,text="\nMiscelaneous:")
    misc.grid(row=5,column=0,sticky=W,columnspan=3)
    underline(misc)
    checkowc,owcbuttontext,owcbutton=checkbox(setting,"Keep Installer open once LOaBIS is launched",openwhenclosed,6,0,3,W)
    checkdla,dlabuttontext,dlabutton=checkbox(setting,"Install a module even if the version is incompatible?",download_all,7,0,3,W)

    mainloop()

def changesetting(main,checkau,dlchoice,checkowc,checkdla,checkadm):
    _logtext("Changing installer settings")
    globals()["mindlday"]=dlchoice.get()
    globals()["min_download_days"]=mindlday
    a=["autoupdate","openwhenclosed","download_all","auto_dl_mod"]
    b=[checkau.get(),checkowc.get(),checkdla.get(),checkadm.get()]
    for x in range(len(a)):
        globals()[str(a[x])]=str(b[x]).replace("0","False").replace("1","True")
    savedatafile()
    main.destroy()

def aboutupdater():
    about=genwindow("about",posx=100,posy=100,resize=False)

    title=Label(about,text="LOaBIS -- Local Operations and Basic Intelligence System").grid(row=0,column=0,columnspan=3,pady=10)
    Authors=Label(about,text="Authors:\nSkiy (Jack Lloyd-Walters)\nXectron (Luke Skinner)\n\n2015-"+str(datetime.datetime.now().year)+" All rights Reserved\n",foreground="dark gray").grid(row=2,column=1)
    source=Label(about,text="Source",cursor="hand2",foreground="blue")
    report=Label(about,text="Report issue",cursor="hand2",foreground="blue")
    contact=Label(about,text="Contact Devs",cursor="hand2",foreground="blue")
    add=Label(about,text="Add module",cursor="hand2",foreground="blue")
    version=Label(about,text="Version v "+Focus_Dir[1]).grid(row=1,column=1)

    source.grid(row=3,column=1)
    report.grid(row=4,column=0)
    contact.grid(row=4,column=1,pady=5)
    add.grid(row=4,column=2)

    source.bind("<Button-1>",lambda x:webbrowser.open_new("https://www.dropbox.com/sh/yucoglcwxirfkoq/AAATgGPh961ept6AHtWN8CyFa?dl=0"))
    report.bind("<Button-1>",lambda x:donothing())
    contact.bind("<Button-1>",lambda x:donothing())
    add.bind("<Button-1>",lambda x:donothing())
    mainloop()

def getnewdir():
    newdir=genwindow("select another install",width=430,height=240,posx=150,posy=150,resize=False)

    Headers=Label(newdir,text="Version   Name\t\t     Directory")
    Entries,Scroll=setscrollbox(newdir,70,10,1,0,3,3,5)
    Add=setbutton(newdir,"Add",8,lambda:adddirectory(Entries),2,0)
    Quit=setbutton(newdir,"Quit",8,newdir.destroy,2,1)
    select=setbutton(newdir,"Select",8,lambda:returndir(Entries,newdir),2,2)

    Headers.grid(row=0,column=0,columnspan=3,padx=5,pady=5,sticky=W)

    updateentries(Entries)

    mainloop()

def donothing():
    popup("Error","That feature has not yet\nbeen implemented.\n\nPlease wait for future updates.")

def popup(title="",text="",posx=200,posy=200,resize=False):
    nothing=genwindow(title=title,posx=posx,posy=posy,resize=resize)
    message,okay=Label(nothing,text=text),Button(nothing,text="Okay",command=nothing.destroy)
    message.pack(pady=5)
    okay.pack(pady=5)
    mainloop()

def returndir(entry="",newdir=""):
    show=getshow(entry)
    globals()["Focus_Dir"],globals()["localmods"]=show,getlocalmodules(show[2])
    newdir.destroy()
    try:
        main.destroy()
    except:
        pass
    installer()

if __name__ == "__main__":
    choosedirectory()
    _logtext("Program terminated")
