
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
    "ahow codec": "Input.ShowCodec",
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

def getKodiTask(verb, params = None, rule = None, ruleCount = 1):
    tempTemplate = deepcopy(kodiTaskDefaultTemplate)

    tempTemplate["Verb"] = verb

    if not params is None:
        tempTemplate["Params"] = params

    if not rule is None:
        tempTemplate["Rule"] = rule
    tempTemplate["Rule"]["Count"] = ruleCount

    return tempTemplate