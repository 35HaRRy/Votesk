
import requests

from time import  sleep

from Tasks import *
from KodiTemplates import *

class Kodi(object):

    def __init__(self, intent):
        self.intent = intent
        self.taskComponents = {}
        self.tasks = []

    def run(self):
        self.extractIntent()

        for task in self.tasks:
            for i in range(0, task["Rule"]["Count"], 1):
                if "WhileNotEqual" in task["Rule"]:
                    taskResponse = parseKeyValue(task["Rule"]["WhileNotEqual"], self.applyTask(task["Rule"]["Task"]))

                    whileNotEqual = task["Rule"]["WhileNotEqual"].split("-")[-1]
                    while not taskResponse == whileNotEqual:
                        self.applyTask(task)
                        taskResponse = parseKeyValue(task["Rule"]["WhileNotEqual"], self.applyTask(task["Rule"]["Task"]))
                elif "NotEqual" in task["Rule"]:
                    taskResponse = parseKeyValue(task["Rule"]["NotEqual"], self.applyTask(task["Rule"]["Task"]))
                    if task["Rule"]["NotEqual"].split("-")[-1] == taskResponse:
                        raise Exception("Kodi gorevi kosul saglandigi icin sonlandi. NotEqual: {0}".format(taskResponse))
                    else:
                        self.applyTask(task)
                else:
                    self.applyTask(task)

    def extractIntent(self):
        # regular expressioni duzenle - verbu kaldir
        self.taskComponents = matchTextToComponents(self.intent["Verb"] + " " + self.intent["Objects"], taskPacks)
        if "ExtractMethod" in self.taskComponents:
            extractMethod = getattr(self, self.taskComponents["ExtractMethod"])
            extractMethod()

    def applyTask(self, task):
        if not task["Verb"] == "sleep":
            method = verbApiMethodParis[task["Verb"]]

            kodiRequest = apiRequestTemplates[method.split(".")[0]]
            kodiRequest["method"] = method
            kodiRequest["params"] = task["Params"]

            if task["Verb"] == "send text":
                test = "ediyorum"

            response = requests.post(config["KodiRemoteAddress"], data = str(kodiRequest).replace("'", "\""))
            response = json.loads(response.text)
            log("Kodi single task ({0}) result: {1}".format(str(kodiRequest).replace("'", "\""), response))

            if "error" in response:
                raise Exception("Kodi gorevi hata ile sonanlandi. Error: {0}".format(response["error"]))

            return response
        else:
            log("Kodi single task sleep: {0}".format(task["Params"]["Time"]))
            sleep(task["Params"]["Time"])

    def repeatTask(self):
        count = textToInteger(str(self.taskComponents["Counter"]))
        self.tasks.append(getKodiTask(self.intent["Verb"], ruleCount = count))

    def findTask(self):
        self.tasks.append(getKodiTask("back"))

        self.tasks.append(getKodiTask("open plugin", params = {"addonid": "plugin.video.icefilms"})) # digerlerinde arama ?
        self.tasks.append(getKodiTask("down", rule = {"Count": 1, "WhileNotEqual": "result-currentcontrol-label-[Search]", "Task": currentControlTask}))

        self.tasks.append(getKodiTask("select"))
        self.tasks.append(getKodiTask("sleep", params= {"Time": 0.5}, rule={"Count": 1, "WhileNotEqual": "result-currentcontrol-label-Tamam", "Task": currentControlTask}))
        self.tasks.append(getKodiTask("send text", params= {"text": self.taskComponents["ItemName"]}))
        # self.tasks.append(getKodiTask("sleep", params= {"Time": 0.5}, rule={"Count": 1, "WhileNotEqual": "result-currentcontrol-label-" + self.taskComponents["ItemName"], "Task": currentControlTask}))
        self.tasks.append(getKodiTask("up"))

        if not self.taskComponents["Order"] is None:
            self.tasks.append({"Verb": "select", "Params": {}, "Rule": {"Count": 1, "NotEqual": "result-currentcontrol-label-[..]", "Task": currentControlTask}})
            for i in range(0, 2, 1):
                self.tasks.append(getKodiTask("up"))
                self.tasks.append(getKodiTask("select"))
            