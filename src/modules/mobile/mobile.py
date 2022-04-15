import kivy
import requests

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time

kivy.require("2.0.0")


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

        print(self.IMAGE)

        with open(filename, 'rb') as f:
            r = requests.post('http://127.0.0.1:8000/upload_image', files={filename: f})
            self.IMAGE = "r.content"

        print(self.IMAGE)

        print("Captured")


class Mobile(App):
    def build(self):
        return View()


if __name__ == '__main__':
    Mobile().run()
