import os
from kivy.factory import Factory
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.image import Image as kivyImage
from kivy.uix.camera import Camera
from scannerProcess import process_parking_sign
from ocrtest import ocr_space_file
from PIL import Image

# Allt androidrelaterat handlar främst om kamerapermissions när applikationen körs
from android.permissions import request_permissions, Permission
from android.storage import app_storage_path
request_permissions(
    [
        Permission.CAMERA,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
    ]
)


# app_storage = app_storage_path() + '/IMG_temp.png'  för android app, skriv './IMG_temp.png' annars
app_storage = app_storage_path() + 'IMG_temp.png'

class cameraBack(BoxLayout):
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png(app_storage)

    #Konvertera till lägre upplösning s.a. den godtas av API
        im = Image.open(app_storage)
        rgb_im = im.convert('RGB')
        rgb_im.save(app_storage_path() + 'IMG_temp2.jpg', 'JPEG', optimize = True, quality = 10)



class imgPop(Popup):
    #Ta bort bilden från cache så att den laddas om korrekt
    def removePic(self):
        if os.path.exists(app_storage):
            im2 = kivyImage(source=app_storage)
            im2.remove_from_cache()

    #getter för bildpath
    def getPath(self):
        return app_storage

    #call process_image
    def returnText(self):
        return process_parking_sign(app_storage_path() + 'IMG_temp2.jpg')

class ParkingApp(App):
    def build(self):
         return cameraBack()


if __name__ == "__main__":
    ParkingApp().run()
