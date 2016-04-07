
import requests

from Tasks import *
from KodiRequestTemplates import *

class Kodi(object):

    def __init__(self, intent):
        self.intent = intent
        self.taskComponents = {}
        self.tasks = []

    def run(self):
        self.extractIntent()

        breakAll = False
        for task in self.tasks:
            for i in range(0, task["Rule"]["Count"], 1):
                if "WhileNotEqual" in task["Rule"]:
                    taskResponse = parseKeyValue(task["Rule"]["WhileNotEqual"], self.applyTask(task["Rule"]["Task"]))

                    whileNotEqual = task["Rule"]["WhileNotEqual"].split("-")[-1]
                    while not whileNotEqual == taskResponse:
                        if not "error" in self.applyTask(task):
                           taskResponse = parseKeyValue(task["Rule"]["WhileNotEqual"], self.applyTask(task["Rule"]["Task"]))
                        else:
                            log("Kodi gorevi hata ile sonanlandi.")
                            breakAll = True
                            break
                elif "NotEqual" in task["Rule"]:
                    taskResponse = parseKeyValue(task["Rule"]["NotEqual"], self.applyTask(task["Rule"]["Task"]))
                    if task["Rule"]["NotEqual"].split("-")[-1] == taskResponse:
                        breakAll = True
                        break
                    else:
                        if "error" in self.applyTask(task):
                            log("Kodi gorevi hata ile sonanlandi.")
                            breakAll = True
                            break
                else:
                    if "error" in self.applyTask(task):
                        log("Kodi gorevi hata ile sonanlandi.")
                        breakAll = True
                        break

                if breakAll:
                    break

    def extractIntent(self):
        # regular expressioni duzenle - verbu kaldir
        self.taskComponents = matchTextToComponents(self.intent["Verb"] + " " + self.intent["Objects"], taskPacks)
        if "ExtractMethod" in self.taskComponents:
            extractMethod = getattr(self, self.taskComponents["ExtractMethod"])
            extractMethod()

    def applyTask(self, task):
        method = verbMethodParis[task["Verb"]]

        kodiRequest = requestTemplates[method.split(".")[0]]
        kodiRequest["method"] = method
        kodiRequest["params"] = task["Params"]

        if task["Verb"] == "send text":
            test = "ediyorum"

        response = requests.post(config["KodiRemoteAddress"], data = str(kodiRequest).replace("'", "\""))
        log("Kodi single task ({0}) result: {1}".format(str(kodiRequest).replace("'", "\""), response.text))

        return response.text

    # default task templates
    def repeatTask(self):
        count = textToInteger(str(self.taskComponents["Counter"]))
        self.tasks.append({"Verb": self.intent["Verb"], "Rule": {"Count": count}, "Params": {}})

    def findTask(self):
        self.tasks.append({"Verb": "open plugin", "Rule": {"Count": 1}, "Params": {"addonid": "plugin.video.icefilms"}})
        # digerlerinde arama ?

        self.tasks.append({"Verb": "down", "Params": {}, "Rule": {"Count": 1, "WhileNotEqual": "result-currentcontrol-label-[Search]", "Task": currentControlTask}})

        self.tasks.append({"Verb": "select", "Params": {}, "Rule": {"Count": 1}})
        self.tasks.append({"Verb": "send text", "Params": {"text": self.taskComponents["ItemName"]}, "Rule": {"Count": 1}})
        self.tasks.append({"Verb": "up", "Params": {}, "Rule": {"Count": 1}})

        if not self.taskComponents["Order"] is None:
            self.tasks.append({"Verb": "select", "Params": {}, "Rule": {"Count": 1, "NotEqual": "result-currentcontrol-label-[..]", "Task": currentControlTask}})
            for i in range(0, 2, 1):
                self.tasks.append({"Verb": "up", "Params": {}, "Rule": {"Count": 1}})
                self.tasks.append({"Verb": "select", "Params": {}, "Rule": {"Count": 1}})
            