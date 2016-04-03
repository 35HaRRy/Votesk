
from Kodi import *

class Dispatcher(object):

    def __init__(self, taskText):
        self.taskText = taskText
        self.intent = {}

    def dispatch(self):
        result = "unsuccessful"

        try:
            self.intent = matchTextToComponents(self.taskText.lower(), tasks)
            if "IntentMethod" in self.intent:
                intentMethod = getattr(self, self.intent["IntentMethod"])
                intentMethod()

                result = "successful"
        except StandardError as se:
            log(se)

        log("Dispatch result is " + result)
        return result

    def workOnPi(self):
        if self.intent["Verb"] == "stop" and self.intent["Objects"] == "listening":
            sys.exit()

    def workOnKodi(self):
        log("Kodi calisti. Verb: {0}, Objects: {1}".format(self.intent["Verb"], self.intent["Objects"]))

        self.kodi = Kodi(self.intent)
        self.kodi.run()