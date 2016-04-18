
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
            if "WhileKodiWorking" in task["Rule"]:
                task["Rule"]["WhileEqual"] = currentControlLabelPrefix + parseKeyValue(currentControlLabelPrefix, self.applyTask(currentControlTask))
                # task["Rule"]["WhileEqual"] = currentWindowLabelPrefix

            if "WhileNotEqual" in task["Rule"] or "WhileNotContain" in task["Rule"] or "WhileEqual" in task["Rule"]:
                whileRule = "WhileNotEqual"
                if "WhileNotContain" in task["Rule"]:
                    whileRule = "WhileNotContain"
                elif "WhileEqual" in task["Rule"]:
                    whileRule = "WhileEqual"

                taskResponse = parseKeyValue(task["Rule"][whileRule], self.applyTask(task["Rule"]["Task"]))
                whileRuleValue = task["Rule"][whileRule].replace(currentControlLabelPrefix, "").replace(currentWindowLabelPrefix, "").lower()

                controlCounter = 0
                while not (("WhileNotEqual" in whileRule and whileRuleValue == taskResponse.lower()) or ("WhileEqual" in whileRule and whileRuleValue != taskResponse.lower())
                            or ("WhileNotContain" in whileRule and whileRuleValue in taskResponse.lower()) or ("WhileContain" in whileRule and whileRuleValue not in taskResponse.lower())):
                    self.applyTask(task)
                    taskResponse = parseKeyValue(task["Rule"][whileRule], self.applyTask(task["Rule"]["Task"]))

                    controlCounter += 1
                    if controlCounter == config["ControlCounter"]:
                        raise StandardError("sorgu donguye girdigi icin sonlandirildi.")
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

            response = requests.post(config["KodiRemoteAddress"], data=str(kodiRequest).replace("'", "\""))
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

                sleepRule = None
                if "SleepRule" in task["Rule"]:
                    sleepRule = task["Rule"]["SleepRule"]

                self.applyRule(getKodiTask("sleep", params={"Time": sleeptime}, rule=sleepRule, useSleep=False))

            return response
        else:
            log("Kodi single task sleep: {0}".format(task["Params"]["Time"]))
            log(".........................................................................")
            sleep(task["Params"]["Time"])

    def repeatTask(self):
        count = textToInteger(str(self.taskComponents["Counter"]))
        self.tasks.append(getKodiTask(self.intent["Verb"], ruleCount=count))

    def findTask(self):
        self.tasks.append(getKodiTask("open plugin", params={"addonid": "plugin.video.icefilms"})) # digerlerinde arama ? ve uygulamanin acilisina gitme

        self.tasks.append(getKodiTask("down", rule=getControlRule(label="[Search]"), useSleep=False))
        self.tasks.append(getKodiTask("select", rule={"SleepRule": getControlRule(label="Done")}))
        # rule1 = {"SleepRule": getControlRule(ruleType="WhileEqual", label="")}
        self.tasks.append(getKodiTask("send text", params={"text": self.taskComponents["ItemName"]}, rule={"SleepRule": getControlRule(ruleType="WhileKodiWorking")}))

        if not self.taskComponents["Order"] is None:
            self.tasks.append(getKodiTask("down", rule=getControlRule(ruleType="WhileNotContain", label=self.taskComponents["ItemName"])))
            self.tasks.append(getKodiTask("select", rule={"SleepRule": getControlRule(ruleType= "WhileKodiWorking")}))
            self.tasks.append(getKodiTask("up", rule=getControlRule(ruleType="WhileNotContain")))
            self.tasks.append(getKodiTask("up"))
            self.tasks.append(getKodiTask("select", rule={"SleepRule": getControlRule(ruleType="WhileKodiWorking")}))
            self.tasks.append(getKodiTask("up"))
            self.tasks.append(getKodiTask("select"))
            