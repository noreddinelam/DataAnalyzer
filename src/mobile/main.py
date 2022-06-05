import os

from src.api.api import run_api_server
from threading import Thread

import kivy
import requests

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
import time

Builder.load_string('''
<View>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
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
        id: spinner_id
        size_hint_y: None
        height: '48dp'
        text: "Choice mode"
        values: ["Cat or dog", "letter", "number"]
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
        spinner = self.ids["spinner_id"]

        if self.sound and camera.play:
            self.sound.play()

        if not camera.play:
            capture_btn.text = "Capture"
            camera.play = True
            return

        camera.play = False
        capture_btn.text = "Retry"

        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = "IMG_{}.png".format(timestr)
        camera.export_to_png(filename)
        # pil_image = Image.frombytes(mode='RGBA', size=camera.texture.size, data=camera.texture.pixels)
        # numpy_picture = numpy.array(pil_image)
        r = requests.post(url='http://127.0.0.1:8000/upload_image/' + spinner.text, files={'image': open(filename, 'rb')})
        print(r.json())

        print("Captured")

        os.remove(filename)


class Test(App):
    def build(self) -> View:
        return View()


if __name__ == "__main__":
    try:
        Thread(target=run_api_server).start()
        Thread(target=Test().run()).start()
    except KeyboardInterrupt:
        exit()
