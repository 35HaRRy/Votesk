
import sys, getopt, datetime, re, simplejson as json

from Config import *

def log(text):
    isPrinting = config["Mode"] == "Debug"
    if isPrinting:
        print("{0}: {1}".format(datetime.datetime.now(), text))

def parseKeyValue(key, value):
    keys = key.split("-")

    if not "errors" in value:
        for i in range(0, len(keys) - 1, 1):
            tempValue = tempValue[keys[i]]

        return tempValue
    else:
        return keys[-1]

def textToInteger(text):
    try:
        return int(text)
    except ValueError:
        integerText = [ "zero", "one", "two", "tree", "four", "five", "six", "seven", "eight", "nine", "ten" ]
        return integerText.index(text)