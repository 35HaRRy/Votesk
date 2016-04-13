
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
            self.applyRule(task)

    def extractIntent(self):
        # regular expressioni duzenle - verbu kaldir
        self.taskComponents = matchTextToComponents(self.intent["Verb"] + " " + self.intent["Objects"], taskPacks)
        if "ExtractMethod" in self.taskComponents:
            extractMethod = getattr(self, self.taskComponents["ExtractMethod"])
            extractMethod()

    def applyRule(self, task):
        for i in range(0, task["Rule"]["Count"], 1):
            if "WhileNotEqual" in task["Rule"] or "WhileNotContain" in task["Rule"] or "WhileEqual" in task["Rule"]:
                whileRule = "WhileNotEqual"
                if "WhileNotContain" in task["Rule"]:
                    whileRule = "WhileNotContain"
                elif "WhileEqual" in task["Rule"]:
                    whileRule = "WhileEqual"

                taskResponse = parseKeyValue(task["Rule"][whileRule], self.applyTask(task["Rule"]["Task"]))
                whileRuleValue = task["Rule"][whileRule].split("-")[-1].lower()

                while not (("WhileNotEqual" in whileRule and whileRuleValue == taskResponse.lower())
                            or ("WhileEqual" in whileRule and whileRuleValue != taskResponse.lower())
                            or ("WhileNotContain" in whileRule and whileRuleValue in taskResponse.lower())
                            or ("WhileContain" in whileRule and whileRuleValue not in taskResponse.lower())):
                    self.applyTask(task)
                    taskResponse = parseKeyValue(task["Rule"][whileRule], self.applyTask(task["Rule"]["Task"]))
            elif "NotEqual" in task["Rule"]:
                taskResponse = parseKeyValue(task["Rule"]["NotEqual"], self.applyTask(task["Rule"]["Task"]))
                if task["Rule"]["NotEqual"].split("-")[-1] == taskResponse:
                    raise Exception("Kodi gorevi kosul saglandigi icin sonlandi. NotEqual: {0}".format(taskResponse))
                else:
                    self.applyTask(task)
            else:
                self.applyTask(task)

    def applyTask(self, task):
        if not task["Verb"] == "sleep":
            method = verbApiMethodParis[task["Verb"]]

            kodiRequest = apiRequestTemplates[method.split(".")[0]]
            kodiRequest["method"] = method
            kodiRequest["params"] = task["Params"]

            response = requests.post(config["KodiRemoteAddress"], data = str(kodiRequest).replace("'", "\""))
            response = json.loads(response.text)

            log("Kodi single task: {0}".format(str(task).replace("'", "\"")))
            log("Kodi single task request: {0}".format(str(kodiRequest).replace("'", "\"")))
            log("Kodi single task response: {0}".format(response))
            log(".........................................................................")

            if "error" in response:
                raise Exception("Kodi gorevi hata ile sonanlandi. Error: {0}".format(response["error"]))

            if task["Rule"]["UseSleep"]:
                sleeptime = config["DefaultSleepTime"]
                if "SleepTime" in task["Rule"]:
                    sleeptime = task["Rule"]["SleepTime"]

                sleepRule = {"UseSleep": False}
                if "SleepRule" in task["Rule"]:
                    sleepRule = task["Rule"]["SleepRule"]

                self.applyRule(getKodiTask("sleep", params= {"Time": sleeptime}, rule= sleepRule))

            return response
        else:
            log("Kodi single task sleep: {0}".format(task["Params"]["Time"]))
            log(".........................................................................")
            sleep(task["Params"]["Time"])

    def repeatTask(self):
        count = textToInteger(str(self.taskComponents["Counter"]))
        self.tasks.append(getKodiTask(self.intent["Verb"], ruleCount = count))

    def findTask(self):
        self.tasks.append(getKodiTask("open plugin", params = {"addonid": "plugin.video.icefilms"}))
        # digerlerinde arama ? ve uygulamanin acilisina gitme

        self.tasks.append(getKodiTask("down", rule = getControlRuleTemplate(label= "[Search]"), useSleep= False))
        self.tasks.append(getKodiTask("select", rule = {"SleepRule": getControlRuleTemplate(label= "Tamam")}))

        rule1 = {"SleepRule": getControlRuleTemplate(ruleType= "WhileEqual", label= "")}
        self.tasks.append(getKodiTask("send text", params= {"text": self.taskComponents["ItemName"]}, rule= rule1))

        # self.tasks.append(getKodiTask("down"))

        if not self.taskComponents["Order"] is None:
            self.tasks.append(getKodiTask("select", rule= rule1))
            # self.tasks.append(getKodiTask("up"))

            rule2 = {"SleepRule": getControlRuleTemplate(ruleType= "WhileNotContain", label= "season")}
            self.tasks.append(getKodiTask("select", rule= rule2))

            self.tasks.append(getKodiTask("up"))
            self.tasks.append(getKodiTask("select"))
            