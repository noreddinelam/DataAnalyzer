import os

import kivy
import requests
import numpy

from PIL import Image
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

Builder.load_string('''
<View>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
    Label:
        text: 
        size_hint_y: None
        height: '48dp'
        opacity: 0
        disabled: True 
    ToggleButton:
        id: capture_btn
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')

kivy.require('2.0.0')


class View(BoxLayout):
    IMAGE = "None"

    def capture(self) -> None:
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        capture_btn = self.ids["capture_btn"]

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

        with open(filename, 'rb') as f:
            r = requests.post(url='http://127.0.0.1:8000/upload_image', files={'image': f})
            print(r.json())

        print("Captured")

        os.remove(filename)


class Test(App):
    def build(self) -> View:
        return View()
