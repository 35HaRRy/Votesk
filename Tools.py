
import sys, getopt, datetime

def log(text):
    # isPrinting = config["Mode"] == "Debug":
    isPrinting = True
    if isPrinting:
        print("{0}: {1}".format(datetime.datetime.now(), text))
