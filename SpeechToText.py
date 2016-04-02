
import speech_recognition as sr

class SpeechToText(object):

    def __init__(self, module=None):
        if not module:
            self.module = "wit.ai"

    def start(self):
        text = ""

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
            print("Say something!")
            audio = r.listen(source)

        # recognize speech using Wit.ai
        WIT_AI_KEY = "26WIGDJ5IMHG53XGBQQ4ZZ7MHGFIUDRJ" # Wit.ai keys are 32-character uppercase alphanumeric strings
        try:
            from pprint import pprint
            # print("Wit.ai recognition results:")
            # pprint(r.recognize_wit(audio, key=WIT_AI_KEY, show_all=True)) # pretty-print the recognition result
            text = r.recognize_wit(audio, key=WIT_AI_KEY)
            print("Wit.ai thinks you said " + text)
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))

        return text