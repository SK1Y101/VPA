from _core import settings,module,say,listen,logtext

def init():
    if module.checkmodule("wolframalpha","queries") == True:
        import wolframalpha

def search(text=""):
    import wolframalpha
    say("\n-- Querying wolfram alpha --")
    try:
        res = wolframalpha.Client("J4QG62-EJQ32EUYQY").query(text)
        say("Wolfram results for query:")
        print("----------")
        if len(list(res.pods)) == 0:
            say("No available data")
        else:
            for pod in res.pods:
                if str(pod.text) != "None":
                    print(pod.text)
        print("----------")
        if len(list(res.pods)) == 0:
            ui = listen("Would you like me to perform a google search?\n>")
            for x in ["Y","y","YES","Yes","yes"]:
                if x in ui:
                    googlesearch(text)
                    break
    except:
        say("Wolfram alpha dosen't appear to be available right now")
        logtext("Failed to query wolframalpha for: "+text)

def googlesearch(text=""):
    try:
        say("Opening a google search for: "+text)
        subprocess.call("start www.google.com/search?q="+text.replace(" ","+"),shell=True)
    except:
        say("Google dosen't apear to be available right now")
        logtext("Failed to open a google search for: "+text)

if __name__ != "__main__":
    init()
