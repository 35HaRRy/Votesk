
import time
import speech_recognition as sr

from Dispatcher import *

class SpeechToText(object):

    def __init__(self, module=None):
        self.module = module
        if not module:
            self.module = "wit.ai"

        self.recognizer = sr.Recognizer()

    def start(self):
        microPhone = sr.Microphone()
        with microPhone as source:
            self.recognizer.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

        # start listening in the background (note that we don't have to do this inside a `with` statement)
        self.stop_listening = self.recognizer.listen_in_background(microPhone, self.callback)

        while True:
            time.sleep(0.1)

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            log("Say something!")
            try:
                audio = self.recognizer.listen()
            except StandardError as se:
                audio = None
                log("Speech recognizer error: {0}".format(se))

        return audio

    def callback(self, recognizer, audio):
        log("callback calisti.")

        dispatcher = Dispatcher(self.toText(audio))
        if dispatcher.dispatch() == "close":
            try:
                self.stop_listening()
            except StandardError as se:
                log("callback error: {0}".format(se))

    def toText(self, audio):
        text = ""

        if self.module == "google":
            # recognize speech using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                # text = self.recognizer.recognize_google(audio, key = "AIzaSyAt6XMqNbCjAukkCOFhbITY0AqLvLjLI24")
                text = self.recognizer.recognize_google(audio, key = "AIzaSyCbyjzYuzvAvXAg-4h1HeSj1LdPljCb4yc")
                log("Google Speech Recognition thinks you said " + text)
            except sr.UnknownValueError:
                log("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                log("Could not request results from Google Speech Recognition service; {0}".format(e))
            except AssertionError as e:
                log("AssertionError; {0}".format(e))

        elif self.module == "wit.ai":
            # recognize speech using Wit.ai
            WIT_AI_KEY = "26WIGDJ5IMHG53XGBQQ4ZZ7MHGFIUDRJ" # Wit.ai keys are 32-character uppercase alphanumeric strings
            try:
                from pprint import pprint
                # log("Wit.ai recognition results:")
                # plog(r.recognize_wit(audio, key = WIT_AI_KEY, show_all = True)) # pretty-print the recognition result
                text = self.recognizer.recognize_wit(audio, key = WIT_AI_KEY)
                log("Wit.ai thinks you said " + text)
            except sr.UnknownValueError:
                log("Wit.ai could not understand audio")
            except sr.RequestError as e:
                log("Could not request results from Wit.ai service; {0}".format(e))
            except AssertionError as e:
                log("AssertionError; {0}".format(e))

        return text