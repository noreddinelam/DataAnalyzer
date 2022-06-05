from kivy.app import App
from kivy.lang import Builder
import requests
import os

class Main(App):

    def build(self):
        return Builder.load_file("cam_app.kv")

    def change_cam(self, instance):
        camera = instance.parent.ids.xcamera
        if camera.index == 0:
            camera.index = int(camera.index) + 1
        elif camera.index == 1:
            camera.index = int(camera.index) - 1
        else:
            camera.index = camera.index

    def picture_taken(self, obj, filename):

        with open(filename, 'rb') as f:
            r = requests.post(url='http://127.0.0.1:8000/upload_image', files={'image': f})
            print(r.json())

        print("Captured")

        os.remove(filename)


if __name__ == "__main__":
    Main().run()
