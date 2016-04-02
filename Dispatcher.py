
from Tools import *

class Dispatcher(object):

    def __init__(self, task):
        self.task = task

    def dispatch(self):
        result = "unsuccessful"

        if self.task == "close":
            result = self.task
        else:
            result = "successful"

        log(result)
        return result