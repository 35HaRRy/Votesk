
from Tools import *

from copy import *

apiDefaultTemplate = {
        "jsonrpc": "2.0",
         "method": "",
         "id": 1,
         "params": {}
    }

apiRequestTemplates = {
    "Input": apiDefaultTemplate,
    "Addons": apiDefaultTemplate,
    "GUI": apiDefaultTemplate
}

verbApiMethodParis = {
    "back": "Input.Back",
    "down": "Input.Down",
    "execute action": "Input.ExecuteAction",
    "home": "Input.Home",
    "info": "Input.Info",
    "left": "Input.Left",
    "right": "Input.Right",
    "select": "Input.Select",
    "send text": "Input.SendText",
    "show codec": "Input.ShowCodec",
    "show osd": "Input.ShowOSD",
    "up": "Input.Up",

    "open plugin": "Addons.ExecuteAddon",

    "current control": "GUI.GetProperties"
}

kodiTaskDefaultTemplate = {
    "Verb": "",
    "Rule": {
        "Count": 1
    },
    "Params": {}
}

def getKodiTask(verb, params=None, rule=None, ruleCount=1, useSleep=True):
    tempTemplate = deepcopy(kodiTaskDefaultTemplate)

    tempTemplate["Verb"] = verb

    if not params is None:
        tempTemplate["Params"] = params

    if not rule is None:
        tempTemplate["Rule"] = rule

    tempTemplate["Rule"]["Count"] = ruleCount
    tempTemplate["Rule"]["UseSleep"] = useSleep

    return tempTemplate

currentControlTask = getKodiTask("current control", params={"properties": ["currentcontrol", "currentwindow"]}, useSleep=False)
controlRuleTemplate = {"Count": 1, "UseSleep": False, "Task": currentControlTask}

def getControlRule(ruleType="WhileNotEqual", labelPrefix=currentControlLabelPrefix, label="[..]"):
    tempTemplate = deepcopy(controlRuleTemplate)

    tempTemplate[ruleType] = labelPrefix + label
    return tempTemplate
