import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import time

kivy.require("2.0.0")


class View(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class Mobile(App):
    def build(self):
        return View()


if __name__ == '__main__':
    Mobile().run()
