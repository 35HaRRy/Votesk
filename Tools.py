
import sys, getopt, datetime, re

from Config import *

def log(text):
    isPrinting = config["Mode"] == "Debug"
    if isPrinting:
        print("{0}: {1}".format(datetime.datetime.now(), text))
