
import sys, getopt

from SpeechToText import *
from Dispatcher import *

def main(argv):
    speechToText = SpeechToText()

    try:
        opts, args = getopt.getopt(argv, "ht:m:", ["task=", "module="])
    except getopt.GetoptError:
        print "-t <task> -m <module>"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "-t <task> -m <module>"
            sys.exit()
        elif opt in ("-t", "--task"):
            task = arg
        elif opt in ("-m", "--module"):
            speechToText = SpeechToText(arg)

    if not task:
        task = speechToText.start()

    dispatcher = Dispatcher(task)
    print("Dispatch mission is {0}".format(dispatcher.dispatch()))

if __name__ == "__main__":
    main(sys.argv[1:])