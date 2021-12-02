import datetime
import random
import webbrowser

import pyttsx3
import speech_recognition
import speech_recognition as sr

from PyQt5 import QtWidgets, QtGui, QtCore

from gui.mainwindow import Ui_MainWindow


class Application(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.recognizer = sr.Recognizer()
        self.audio_src = sr.Microphone()

        with self.audio_src as src:
            self.recognizer.adjust_for_ambient_noise(src, duration=5)

        self.speech_synth = pyttsx3.init()
        self.speech_synth.setProperty('voice', self.speech_synth.getProperty('voices')[1].id)

        self.commands = {
            ('hello', 'hi', 'greetings'): self.greetings,
            ('bye', 'goodbye', 'stop'): self.farewell,
            ('find', 'Google', 'search'): self.google_search,
            ('today'): self.today,
            ('help', 'about'): self.app_help
        }

        self.action_restart_sesion.triggered.connect(self.restart_session)
        self.action_about.triggered.connect(lambda: print('help'))

    def restart_session(self):
        self.text_browser.clear()

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Shift:
            try:
                print('Listening...')
                with self.audio_src as src:
                    audio_data = self.recognizer.listen(src, 5, 5)
                print('Recognizing...')
                text = self.recognizer.recognize_google(audio_data, language='en-EN')
                print(f'Recognized {text}.')
                self.handle_input(text)
            except speech_recognition.WaitTimeoutError:
                print('Listening ended.')
            except Exception as e:
                print('Error.')

    def handle_input(self, text: str):
        voice_input = text.split(' ', maxsplit=1)
        command_name = voice_input[0]
        if len(voice_input) > 1:
            command_args = voice_input[1]
        else:
            command_args = None
        print(f'{voice_input=}\n{command_name=}\n{command_args=}')

        self.append_message('user', text)

        for key in self.commands.keys():
            if command_name in key:
                self.system_response(self.commands[key](command_args))
                if command_name in ('bye', 'goodbye', 'stop'):
                    raise KeyboardInterrupt
                return

        self.system_response('Sorry. I cannot really understand you. Could you try again, please?')

    def system_response(self, result):
        self.append_message('system', result)
        self.speech_synth.say(result)
        self.speech_synth.runAndWait()

    def append_message(self, sender, text):
        if sender == 'system':
            self.text_browser.append(
                f"<p style=\" margin-top:0px; font-size:10.3pt; margin-bottom:0px; margin-left:0px; margin-right:0px; "
                f"-qt-block-indent:0; text-indent:0px;\">&gt;&gt;&gt; {text}</p>"
            )
        elif sender == 'user':
            self.text_browser.append(
                f"<p  style=\" font-size:10.3pt; margin-top:0px; margin-bottom:0px; margin-left:0px; "
                f"margin-right:0px; -qt-block-indent:0; text-indent:0px;\">&gt;&gt;&gt; {text}</p>"
            )
        else:
            raise ValueError('Unknown sender')

    def greetings(self, args):
        gs = [
            'Welcome to voice assistance application. How can I help you?',
            'Hi! What can I do for you?',
            'Hello! How can I help?'
        ]

        return random.choice(gs)

    def farewell(self, args):
        fws = [
            'Goodbye.',
            'It was a pleasure helping you. Goodbye.'
        ]

        return random.choice(fws)

    def google_search(self, args):
        URL = f'https://google.com/search?q={args}'
        webbrowser.get().open(URL)

        wbrs = [
            f"Here's a google search for '{args}'."
        ]

        return random.choice(wbrs)

    def today(self, args):
        tds = [
            f'Today is {datetime.date.today()}'
        ]

        return random.choice(tds)

    def app_help(self, args):
        return 'Voice Assistant Application is able to interact with user through natural language using voice ' \
               'recognition and voice synthesis. Application is able to greet, say goodbye, search google, etc.'
