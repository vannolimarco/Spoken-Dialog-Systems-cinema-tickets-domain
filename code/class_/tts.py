import pyttsx3


class Tts:
    def __init__(self, rate = 150, volume = 1):
        self.engine = pyttsx3.init()
        self.rate = rate
        self.volume = volume

    def robot_speak(self,text: str):
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()

    def set_property_voice(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == 'Microsoft Elsa Desktop - Italian (Italy)':
                self.engine.setProperty('voice', voice.id[0])
                self.engine.setProperty('rate', self.rate)  # setting up new voice rate
                self.engine.setProperty('volume', self.volume)  # setting up volume level  between 0 and 1
                break

