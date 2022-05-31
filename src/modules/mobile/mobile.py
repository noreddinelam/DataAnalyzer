import kivy
import requests

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
        resolution: (740, 580)
        play: True
    Label:
        text: 
        size_hint_y: None
        height: '48dp'
        opacity: 0
        disabled: True 
    Button:
        id: capture_btn
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button:
        id: retry_btn
        text: 'Retry'
        size_hint_y: None
        height: '48dp'
        on_press: root.retry()
        opacity: 0
        disabled: True
    
''')

kivy.require('2.0.0')

class View(BoxLayout):

    IMAGE = "None"

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        filename = "IMG_{}.png".format(timestr)
        camera.export_to_png(filename)
        camera.play = False

        with open(filename, 'rb') as f:
            r = requests.post(url='http://127.0.0.1:8000/upload_image', files={'image': f})
            print(r.json())

        print("Captured")

        capture_btn = self.ids["capture_btn"]
        capture_btn.opacity = 0
        capture_btn.disabled = True

        retry_btn = self.ids["retry_btn"]
        retry_btn.opacity = 1
        retry_btn.disabled = False


    def retry(self):

        camera = self.ids['camera']
        camera.play = True

        retry_btn = self.ids["retry_btn"]
        retry_btn.opacity = 0
        retry_btn.disabled = True

        capture_btn = self.ids["capture_btn"]
        capture_btn.opacity = 1
        capture_btn.disabled = False


class Test(App):
    def build(self):
        return View()

if __name__ == '__main__':
    Test().run()



