
from SpeechToText import *

def main(argv):
    taskText = None
    speechToText = SpeechToText()

    try:
        opts, args = getopt.getopt(argv, "ht:m:", ["taskText=", "module="])
    except getopt.GetoptError:
        print "-t <taskText> -m <module>"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print "-t <taskText> -m <module>"
            sys.exit()
        elif opt in ("-t", "--taskText"):
            taskText = arg
        elif opt in ("-m", "--module"):
            speechToText = SpeechToText(arg)

    if not taskText:
        speechToText.start()
    else:
        dispatcher = Dispatcher(taskText)
        dispatcher.dispatch()

if __name__ == "__main__":
    main(sys.argv[1:])