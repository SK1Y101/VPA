from _core import settings,say,listen,logtext
import datetime,csv,os

def init():
    loadreminders()

def loadreminders(file="reminders.txt"):
    rem = []
    f = open("reminders\\"+file,"r")
    file = csv.reader(f)
    for row in file:
        rem.append(row)
    f.close()
    settings.addglobal("reminders",rem,True)

def savereminders(file="reminders.txt"):
    rem = settings.reminders
    f = open("reminders\\"+file,"w")
    for x in rem:
        y = x[0]+","+x[1]+","+x[2]+","+x[3]+"\n"
        f.write(y)
    f.close()

def checkreminders(text=""):
    rem = settings.reminders
    today = datetime.date.today()
    week = []
    for x in rem:
        [year,month,day] = map(int,x[0].split("-"))
        [hour,minute] = map(int,x[1].split(":"))
        timedif = datetime.datetime(year,month,day,hour,minute)-datetime.datetime.now()
        if str(timedif)[0] !="-":
            if int(timedif.total_seconds()) <= 604800:
                y = (str(timedif).split(":")[0]+":"+str(timedif).split(":")[1]+","+x[2]+","+x[3])
                if int(timedif.total_seconds()) < 36000:
                    y = " "+y
                if not "day" in str(timedif):
                    y = "      , "+y
                week.append(y.split(","))
        else:
            if int(x[2]) > 60:
                y = datetime.datetime(year,month,day,hour,minute)+datetime.timedelta(seconds=int(x[2]))
                while str(y-datetime.datetime.now())[0] == "-":
                    y += datetime.timedelta(seconds=int(x[2]))
                short = str(y.isoformat().split("T")[1]).split(":")
                y = str(y.isoformat().split("T")[0])+","+short[0]+":"+short[1]+","+str(x[2])+","+str(x[3])
                rem[rem.index(x)] = y
            else:
                rem.pop(rem.index(x))
    if len(week)>0:
        week.sort()
        week.insert(0,["Days ,"," Time ","Repeat time","Reminder:"])
        for x in week:
            say(x[0]+x[1]+", "+x[3])
    else:
        say("-No Upcoming Reminders-")
    savereminders()

def createreminder(text=""):
    rem = settings.reminders
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
    date = ""
    time = "10:00"
    repeat = 0
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
            if "every" in text:
                date = str(today + datetime.timedelta((weekdays.index(x)-1-today.weekday())%7+1))
                repeat = 60*60*24*7
            if "next" in text:
                date = str(today + datetime.timedelta((weekdays.index(x)-1-today.weekday())%7+1))
            else:
                date = str(today + datetime.timedelta((weekdays.index(x)-today.weekday())%7))
            text = text.replace("on "+x,"").replace("on every "+x,"").replace("every "+x,"").replace("on the next "+x,"").replace("the next "+x,"").replace("next "+x,"").replace(x,"")
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
        hour = int(time.split(":")[0])
        maxt = [20,12,18,6,6]
        mint = [18,6,12,20,20]
        rel = ["in the evening","in the morning","in the afternoon","in the night","at night"]
        for x in rel:
            if x in text:
                text = text.replace(x,"")
                if not (mint[rel.index(x)] < hour <= maxt[rel.index(x)]):
                    if not (mint[rel.index(x)] < hour+12 <= maxt[rel.index(x)]):
                        hour = mint[rel.index(x)]+1
                        break
                    else:
                        hour+=12
                        break
        text = text.replace(time,str(hour)+":"+time.split(":")[1]).replace(time[0:2],str(hour)+":"+time.split(":")[1]).replace(time[0:1],str(hour)+":"+time.split(":")[1])
        time = str(hour)+":"+time.split(":")[1]
        text = text.replace(" at "+time," ").replace(" at "+time[0:2]," ").replace(time,"").replace(time[0:2],"").replace(" at "+time[0:1],"").replace(time[0:1],"").replace(" at ","")
    ##check if there is a time in the reminder

    if " every " in text:
        repeat = 0
        dif = ["year","month","fortnight","week","day","hour","minute"]
        for x in dif:
            if x in text:
                y = text[text.index("every")+6:text.index(x)+len(x)+1]
                z = y.split(" ")[0]
                y = y.split(" ")[1]
                tim = [60*60*24*365,60*60*24*31,60*60*24*14,60*60*24*7,60*60*24,60*60,60]
                try:
                    repeat += int(z)*int(tim[dif.index(x)])
                except:
                    repeat += int(tim[dif.index(x)])
                text = text.replace(z,"").replace(y+"s","").replace(y,"").replace("and","")
                while "  " in text:
                    text = text.replace("  "," ")
        text = text.replace(" every ","")
    ##check if there is still a repeat function
                
    while text[len(text)-1] == " ":
        text = text[0:len(text)-1]
    while "  " in text:
        text = text.replace("  "," ")
    note = text
    if "to" in text:
        note = text[text.index("to")+3:len(text)]
    if "that" in text:
        note = text[text.index("that")+5:len(text)]
    if note[len(note)-1] == " ":
        note = note[0:-1]
    if len(date) < 10:
        year = max(int(listen("What is the year of the reminder?\n> ")),today.year)
        month = max(int(listen("What is the month of the reminder? (1 to 12)\n> ")),1)
        day = max(int(listen("What is the day of the reminder? (1 to 31)\n> ")),1)
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
        note = listen("What is the note for the reminder?\n> ")
    rem.append([str(date),str(time),str(repeat),str(note)])
    if repeat == 0:
        say("Reminder:\n"+date+" at "+time+" - Never repeating\n"+note)
    else:
        say("Reminder:\n"+date+" at "+time+" - repeating every: "+str(datetime.timedelta(seconds=repeat))+"\n"+note)

    rem.sort()
    savereminders()

if __name__ != "__main__":
    init()
