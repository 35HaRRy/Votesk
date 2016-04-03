
import requests

from Tasks import *

class Kodi(object):

    def __init__(self, intent):
        self.intent = intent
        self.taskComponents = {}
        self.taskes = []

    def run(self):
        self.extractIntent()

        for task in self.taskes:
            self.applyTask(task)

    def extractIntent(self):
        self.taskComponents = matchTextToComponents(self.intent["Objects"], taskPacks)
        if "ExtractMethod" in self.taskComponents:
            extractMethod = getattr(self, self.taskComponents["ExtractMethod"])
            extractMethod()

    def applyTask(self, task):
        kodiRequest = config["KodiRequestTemplate"]
        # parse task

        response = requests.post(config["KodiRemoteAddress"], data = str(kodiRequest).replace("'", "\""))
        log("Kodi single task ({0}) result: {1}".format(str(kodiRequest).replace("'", "\""), response.text))

    def repeatTask(self):
        for i in range(0, int(self.taskComponents["Counter"]), 1):
            self.taskes.append({ "Verb": self.intent["Verb"], "Objects": "" })