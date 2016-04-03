
import re

from Tools import *

class Dispatcher(object):

    def __init__(self, taskText):
        self.taskText = taskText
        self.intent = {}

    def dispatch(self):
        result = "unsuccessful"

        try:
            self.matchtaskTexts()
            if not self.intent == {}:
                intentMethod = getattr(self, self.intent["Task"]["IntentMethod"])
                intentMethod()

                result = "successful"
        except StandardError as se:
            log(se)

        log("Dispatch result is " + result)
        return result

    def matchtaskTexts(self):
        self.intent = {}

        temptaskText = self.taskText.lower()
        for synonym in synonyms:
            for key, values in synonym.iteritems():
                for value in values:
                    temptaskText = temptaskText.replace(value, key)

        for task in tasks:
            p = re.compile(task["RegularExpression"])
            matches = p.match(temptaskText)

            if not matches == None:
                matches = matches.groups()

                assert len(matches) >= len(filter(lambda x: x["IsRequired"], task["SentenceComponents"])), "Need all required components"

                for i in range(0, len(task["SentenceComponents"]), 1):
                    component = task["SentenceComponents"][i]

                    self.intent[component["Name"]] = ""
                    if i < len(matches):
                        self.intent[component["Name"]] = matches[i]

                self.intent["Task"] = task

    def workOnPi(self):
        if self.intent["Verb"] == "stop" and self.intent["Objects"] == "listening":
            sys.exit()

    def workOnKodi(self):
        log("Kodi calisti. Verb: {0}, Objects: {1}".format(self.intent["Verb"], self.intent["Objects"]))