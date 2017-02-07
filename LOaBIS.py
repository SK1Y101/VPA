#Loacal Operations and Basic Inteligence System
import os,sys,csv,wolframalpha,subprocess,datetime
import speech_recognition as sr
from random import randint
from time import sleep

def startup():
    say("-- | Inintialising Startup Procedure | --")
    try:
        globals()["user"] = str(os.getlogin()[0].upper()+os.getlogin()[1:len(os.getlogin())])
    except:
        globals()["user"] = "User"
    ##fb: LOaBIS.Py@gmail.com , L0abis21
    globals()["app_id"] = "J4QG62-EJQ32EUYQY"
    globals()["client"] = wolframalpha.Client(app_id)
    globals()["r"] = sr.Recognizer()
    globals()["start_menu"] = "C:/Users/Owner/AppData/Roaming/Microsoft/Windows/Start Menu"
    globals()["self"] = str(os.path.basename(sys.argv[0]))
    globals()["mem"] = []
    globals()["reminders"] = []
    globals()["sro"] = 0
    globals()["ttso"] = 0
    globals()["lpass"] = "loabis"
    globals()["cwords"] = ["turn ","set ","remind me ","what are ","what is ","search ","google","run ","goodbye ","setup ","configure ","null "]
    globals()["funcs"] = ["turn","setitem","createreminder","search","search","search","google","run","goodbye","setup","setup","null"]
    #Define all required variables
    readmemory()
    checkbackup()
    loadreminder()
    ##Run backups and get memory
    software = str(mem[mem.index("software")+1])
    version = str(mem[mem.index("version")+1])
    try:
        globals()["ttso"] = mem[mem.index(user)+2]
        globals()["sro"] = mem[mem.index(user)+3]
        globals()["user"] = mem[mem.index(user)+1]
    except:
        globals()["user"] = user
    say("-- | Loabis startup completed succesfully | --\n-- Initialising at time: "+str(datetime.datetime.now())+" --\n"+software+" "+version+"\n")
    checkreminder()
    
def tts(text=""):
    if int(ttso) == 1:
        from gtts import gTTS
        tts = gTTS(text)
        tts.save("speech.mp3")
        subprocess.call("speech.mp3", shell=True)
        say(text)
        sleep(len(text)/12) #6.42857142857)
        subprocess.call("taskkill /f /im wmplayer.exe", shell=True)
        os.remove("speech.mp3")
    else:
        say(text)
    
def say(text=""):
    text+="\n"
    for x in str(text):
        sys.stdout.write(x)
        sleep(0.003)

def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        say("Say something:")
        audio = r.listen(source)
    text = "null"
    try:
        text = r.recognize_google(audio)
        say("> "+text)
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Google error; {0}".format(e))
    return text

def getui(text=""):
    for x in str(text):
        sys.stdout.write(x)
        sleep(0.003)
    if int(sro) == 1:
        text = listen()
    else:
        text = input()
    return text
    
def checkbackup():
    global mem
    say("-- Checking Core --")
    f = open("Loabis_Core/loabis_mem.txt","r")
    m = f.read()
    f.close()
    core = m[m.index("backup")+7:len(m)]
    say("-- Comparing LOaBIS Core with backup --")
    f = open(self,"r")
    loabis = f.read()
    f.close()
    if loabis != core:
        if getui("LOaBIS Core pass required:\n> ") != lpass:
            say("-- Restoring LOaBIS Core --")
            f = open(self,"w")
            f.write(core)
            f.close()
            say("-- LOaBIS Core Restored to backup version --")
            sys.exit()
        else:
            say("-- Manual overwrite of LOaBIS Core --")
            writebackup()
    else:
        say("-- LOaBIS Core fine, no errors encountered --")

def writebackup():
    global mem
    say("-- Reading LOaBIS --")
    f = open(self,"r")
    m = f.read()
    f.close()
    t = mem.index("backup")
    mem = mem[0:t+1]
    mem.append(str(m)[0:len(str(m))-1])
    say("-- Preparing Core for backup --")
    f = open("Loabis_Core/loabis_mem.txt","w")
    for x in mem:
        f.write(str(x)+"\n")
    f.close()
    say("-- Core backup complete --")

def readmemory():
    global mem, user
    say("-- Initialising LOaBIS memory retrieval --")
    f = open("Loabis_Core/loabis_mem.txt","r")
    file = csv.reader(f)
    mem = []
    for row in file:
        mem = mem+row
    f.close()
    say("-- LOaBIS memory retrieval complete --")
    t = mem.index("backup")
    software = str(mem[mem.index("software")+1])
    version = str(mem[mem.index("version")+1])
    try:
        user = mem[mem.index(str(os.getlogin()[0].upper()+os.getlogin()[1:len(os.getlogin())]))+1]
    except:
        user = user
    
def getcom(text=""):
    text = text+" "
    for x in cwords:
        if x in text:
            x = funcs[cwords.index(x)]
            break
    try:
        globals()[x.replace(" ","")](text.replace(x,"").replace(cwords[funcs.index(x)],""))
    except:
        tts("Function '"+text[0:text.index(" ")]+"' Does not exist")
    if x != "goodbye":
        textinterface()

def goodbye(text=""):
    bye = ["Goodbye, "+user,"Until next time, "+user,"Happy to help you, "+user]
    tts(bye[randint(0,len(bye)-1)])
    writebackup()
    tts("Just wake me when you have need of me again!")

def textinterface():
    do = ["What would you like me to do?","Hello "+user,"Is there something I can do?",user+", can I do something for you?","Hey there"]
    tts("\n"+do[randint(0,len(do)-1)])
    text = getui("> ")
    getcom(text)

def run(text=""):
    text = text[1:len(text)-1]
    file_paths = []
    file_names = []
    locations = [start_menu,os.getcwd()]
    
    for search in locations:
        for root,directories,files in os.walk(search):
            for filename in files:
                filepath = os.path.join(root,filename) 
                file_paths.append(filepath)
                file_names.append(os.path.splitext(filename)[0])
    try:
        try:
            file = str(file_paths[file_names.index(text)].replace("\\","/"))
        except:
            file = str(file_paths[file_names.index(text+" - Shortcut")].replace("\\","/"))
        tts("running "+text.lower())
        subprocess.call(file,shell=True) #os.system('"' + file + '"')
    except:
        tts("File '"+text+"' Does not exist")

def search(text=""):
    tts("\n-- Querying wolfram alpha --")
    try:
        res = client.query(text)
        tts("Wolfram results for query:")
        print("----------")
        if len(res.pods) == 0:
            tts("No available data")
        else:
            for pod in res.pods:
                if str(pod.text) != "None":
                    print(pod.text)
        print("----------")
        if len(res.pods) == 0:
            ui = getui("Would you like me to perform a google search?\n>")
            for x in ["Y","y","YES","Yes","yes"]:
                if x in ui:
                    google(text)
                    break
    except:
        tts("Wolfram alpha dosen't appear to be available right now")

def setup(text=""):
    global user,mem,ttso,sro
    sttso = 0
    ssro = 0
    ans = ["type a","y","n"]
    if sro == 1:
        ans = ["say","yes","no"]
    if len(text)>3:
        suser = text[1:len(text)-1]
    else:
        suser = user
    tts("-- Setting up information for "+suser+" --\nplease "+ans[0]+" "+ans[1]+" or "+ans[2]+" for yes or no answers")
    tts("What is the name of "+suser+"?")
    susern = getui("> ")
    tts("What is the nickname of "+susern+"?")
    sname = getui("> ")
    tts("Enable text-to-speech for "+susern+" by default?")
    if str(ans[1]) in getui("> ").lower():
        sttso = 1
    tts("Enable speech recognition for "+susern+" by default?")
    if str(ans[1]) in getui("> ").lower():
        ssro = 1
    tts("Is the above information correct?")
    if str(ans[1]) in getui("> ").lower():
        tts("-- Saving information --")
        try:
            uloc = int(mem.index(str(os.getlogin()[0].upper()+os.getlogin()[1:len(os.getlogin())])))
            mem[uloc+4] = ssro
            mem[uloc+3] = sttso
            mem[uloc+2] = sname
            mem[uloc+1] = susern
        except:
            uloc = int(mem.index("userend"))
            mem.insert(uloc,ssro)
            mem.insert(uloc,sttso)
            mem.insert(uloc,sname)
            mem.insert(uloc,susern)
            mem.insert(uloc,str(os.getlogin()[0].upper()+os.getlogin()[1:len(os.getlogin())]))
        writebackup()
        tts("-- Information saved --")
        if suser == user:
            if len(sname) > 0:
                user = sname
            else:
                user = susern
            ttso = sttso
            sro = ssro

def google(text=""):
    try:
        tts("Opening a google search for: "+text)
        subprocess.call("start www.google.com/search?q="+text.replace(" ","+"),shell=True)
    except:
        tts("Google dosen't apear to be available right now")

def turn(text=""):
    text = text.lower().replace(" to  "," ")
    insts = [["sr","bool","sro"],["speech recognition","bool","sro"],["tts","bool","ttso"],["text to speech","bool","ttso"]]
    for x in insts:
        if str(x[0])+" " in text:
            state = text[text.index(x[0])+len(x[0])+1:len(text)].replace(" ","")
            if x[1] == "bool":
                if "on" in state:
                    tts("Turning "+x[0]+" on")
                    globals()[x[2]] = 1
                elif "off" in state:
                    tts("Turning "+x[0]+" off")
                    globals()[x[2]] = 0
            if x[1] == "float":
                tts("Setting "+x[0]+" to "+state)
                globals()[x[2]] = float(state)
    if len(state) == 0:
        tts("I could not recognise any instances")

def setitem(text=""):
    items = ["reminder","alarm","null"]
    for x in items:
        if x in text:
            break
    if x == "null":
        turn(text)
    else:
        try:
            globals()["create"+x](text.replace(x,""))
        except:
            tts("I am unable to set "+x+"s")
            
def loadreminder():
    global reminders
    f = open("Loabis_Core/reminders.txt","r")
    file = csv.reader(f)
    for row in file:
        reminders.append(row)
    f.close()

def savereminder():
    f = open("Loabis_Core/reminders.txt","w")
    for x in reminders:
        y = x[0]+","+x[1]+","+x[2]+"\n"
        f.write(y)
    f.close()

def checkreminder():
    global reminders
    today = datetime.date.today()
    rem = []
    for x in reminders:
        [year, month, day] = map(int,x[0].split('-'))
        [hour, minute] = map(int,x[1].split(":"))
        timedif = str(datetime.datetime(year,month,day,hour,minute)-datetime.datetime.now())
        if timedif[0] != "-":
            if "day" in timedif:
                if int(timedif[0:timedif.index("day")-1]) <= 7:
                    rem.append([timedif[0]+" day, "+timedif[timedif.index(",")+2:timedif.index(",")+7],x[2]])
            else:
                rem.append(["       "+timedif[0:2]+":"+timedif[3:5],x[2]])
        else:
            reminders.pop(reminders.index(x))
    if len(rem) > 0:
        rem.sort()
        rem.insert(0,["Time until:","Note:"])
        tts("Upcoming Reminders:\n----------")
        for x in rem:
            tts(x[0]+"\t"+x[1])
        say("----------")
    else:
        tts("No Upcoming Reminders")
    savereminder()

def createreminder(text=""):  
    text +=" "
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday","null"]
    months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
    date = ""
    time = "10:00"
    today = datetime.date.today()
    
    if "tomorrow " in text:
        date = str(today + datetime.timedelta(1))
        text = text.replace("tomorrow ","")
    if "later " in text:
        date = str(today + datetime.timedelta(1))
        text = text.replace("later ","")
    #check if there is a relative in the reminder
        
    for x in weekdays:
        if x in text:
            if "next" in text:
                date = str(today + datetime.timedelta((weekdays.index(x)-1-today.weekday())%7+1))
            else:
                date = str(today + datetime.timedelta((weekdays.index(x)-today.weekday())%7))
            text = text.replace("on "+x,"").replace("next "+x,"").replace(x,"")
    #check if there is a weekday in the reminder

    day = "1"
    if "on the" in text:
        for x in range(31):
            if str(31-x) in text:
                pl = text.index(str(31-x))
                for y in ["st","nd","rd","th"]:
                    if text[pl+2:pl+4] == y or text[pl+1:pl+3] == y:
                        try:
                            day = str(int(text[pl:pl+2]))
                        except:
                            day = str(int(text[pl:pl+1]))
                        if today.day >= int(day):
                            date = str(today.year)+"-"+str(today.month+1)+"-"+day
                        else:
                            date = str(today.year)+"-"+str(today.month)+"-"+day
                        text = text.replace("on the "+str(text[pl:pl+3+len(day)]),"")
                break
    ##check if there is a day in the reminder
            
    if int(day) < 10:
        day = "0"+str(day)
    for x in months:
        if x in text:
            mon = months.index(x)+1
            if months.index(x)+1 < 10:
                mon = "0"+str(mon)
            if today.month >= months.index(x)+1 or "next" in text:
                date = str(today.year+1)+"-"+str(mon)+"-"+day
            else:
                date = str(today.year)+"-"+str(mon)+"-"+day
            text = text.replace("in "+x,"").replace("next "+x,"").replace("of "+x,"").replace(x,"")
    ##check if there are months in the reminder
            
    if " at " in text:
        if "o'clock" in text:
            time = str(int(text[text.index("o'clock")-3:text.index("o'clock")-1]))+":00"
            text = text.replace("o'clock","")
        else:
            try:
                hour = text[text.index(":")-2:text.index(":")]
            except:
                hour = text[text.index(" at ")+4:text.index(" at ")+6]
            for x in range(24):
                if hour == str(24-x):
                    try:
                        time = text[text.index(":")-2:text.index(":")+3]
                    except:
                        time = text[text.index(" at ")+4:text.index(" at ")+6]+":00"
                    break
        text = text.replace(" at "+time," ").replace(" at "+time[0:2]," ").replace(time,"").replace(time[0:2],"")
    ##check if there is a time in the reminder
        
    while text[len(text)-1] == " ":
        text = text[0:len(text)-1]
    note = text
    if "to" in text:
        note = text[text.index("to")+3:len(text)]
    if "that" in text:
        note = text[text.index("that")+5:len(text)]
    if note[len(note)-1] == " ":
        note = note[0:-1]
    if len(date) < 10:
        year = max(int(getui("What is the year of the reminder?\n> ")),today.year)
        month = max(int(getui("What is the month of the reminder? (1 to 12)\n> ")),1)
        day = max(int(getui("What is the day of the reminder? (1 to 31)\n> ")),1)
        if month < today.month:
            year+=1
        if month == today.month and day < today.day:
            month+=1
        if month < 10:
            month = "0"+str(month)
        if day < 10:
            day = "0"+str(day)
        date = str(year)+"-"+str(month)+"-"+str(day)
    if len(note) < 2:
        note = getui("What is the note for the reminder?\n> ")
    reminders.append([date,time,note])
    tts("Reminder:\n"+date+" at "+time+"\n"+note)
    savereminder()
        
startup()
textinterface()
