import os

from gtts import gTTS
from playsound import playsound
from google_translate_py import Translator

import kivy
import requests

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
import time

from kivy.core.window import Window

Window.size = (580, 500)

Builder.load_string('''
<View>:
    orientation: 'vertical'
    Spinner:
        id: langage
        size_hint: .1, .1
        pos_hint: {'right': 1, 'top': 1}
        text: "fr"
        values: ["fr", "en", "es", "nl", "da", "cs", "de", "hi", "id", "it", "ja", "zh-cn", "zh-tw"]
    Camera:
        id: camera
        resolution: (1440, 960)
        play: True
        allow_stretch: True
    Label:
        id: label_result
        text: ''
        size_hint_y: None
        height: '48dp'
        opacity: 0
        disabled: True
    Spinner:
        id: spinner_model
        size_hint_y: None
        height: '48dp'
        text: "Choice mode"
        values: ["catvsdog", "digit", "letter"]
    ToggleButton:
        id: capture_btn
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')

kivy.require('2.0.0')


class View(BoxLayout):
    sound = SoundLoader.load('data/src_kivy_garden_xcamera_data_shutter.wav')

    def capture(self) -> None:
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        capture_btn = self.ids["capture_btn"]
        label = self.ids["label_result"]
        langage = self.ids["langage"].text

        if self.sound and camera.play:
            self.sound.play()

        if not camera.play:
            capture_btn.text = "Capture"
            camera.play = True
            label.text = ''
            label.opacity = 0
            label.disabled = True
            return

        camera.play = False
        capture_btn.text = "Retry"

        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = "IMG_{}.png".format(timestr)
        camera.export_to_png(filename)
        # pil_image = Image.frombytes(mode='RGBA', size=camera.texture.size, data=camera.texture.pixels)
        # numpy_picture = numpy.array(pil_image)
        r = requests.post(url='http://127.0.0.1:8000/upload_image/' + self.ids["spinner_model"].text,
                          files={'image': open(filename, 'rb')})

        label.text = "It's a " + r.text
        label.opacity = 1
        label.disabled = False

        # translate
        res = Translator().translate(r.text, "en", langage) if r.text in ("dog", "cat") else r.text
        # sound
        filename_mp3 = "./res.mp3"
        tts = gTTS(text=res, lang=langage)
        tts.save(filename_mp3)
        playsound(filename_mp3)
        os.remove(filename_mp3)

        if r.text in ("dog", "cat"):
            playsound("data/" + r.text + ".wav")

        os.remove(filename)


class APP(App):
    def build(self) -> View:
        return View()


if __name__ == "__main__":
    APP().run()
