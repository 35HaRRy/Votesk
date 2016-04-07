
defaultTemplate = {
        "jsonrpc": "2.0",
         "method": "",
         "id": 1,
         "params": {}
    }

requestTemplates = {
    "Input": defaultTemplate,
    "Addons": defaultTemplate,
    "GUI": defaultTemplate
}

verbMethodParis = {
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
