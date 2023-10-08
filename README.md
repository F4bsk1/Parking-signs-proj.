# ProjINDA-Parkeringstolkare-tillsvidare-
A mobile application for interperting parking signs. By taking a picture of a parking sign the application will interpret when, where or if you can park at the location. Further details;
A simple interface which is direct linked to the camera. Push the button of the desired sign, and it will return a message of the rules for parking at the location. The imageprocessing will consist of two ways of interpreting the sign, text and color. The program should be able to detect different colors of different signs, where conclusions of classifications can be drawn. When a classifications is made, the regex tries to match the text, and if a match is made, an output is produced.

Currently the goal is to make this application available for android phones. If there's time left, we will try to make it available for IOS aswell.
The imageprocesser will be made using OpenCV, the package isn't super perfect and not all pictures can be interpreted. That's why we have a vision of making our own dataset with which we can train our ML model using pytorch. This seems pretty hard, and will only be made if there is reasonable time left. We've therefore resorted to using an online API which runs tesseract, [ocr.space](https://ocr.space). Which isn't as cool, but this project is more of a proof of concept. This will require any potential users to get thier own API-key.

## --- Installing ---

Due to using an online API for interperting the images, each user will have to get their own key, and add it to the source files. This also mean that you have to compile the application yourself. This won't be too difficult since that is handled by buildozer. All dependencies are written in the buildozer.spec file, and will be downloaded when buildozer is run.

1. Clone repository

Where ever you'd like

2. Edit the ocrtest.py, and add your own API key

You have to sign up for the free API key at [ocr.space](https://ocr.space). Once you have it, write it down in the function that lies in ocrtest.py:
>def ocr_space_file(filename, overlay=False, api_key="copy key here", language="eng"):

3. Install buildozer

Buildozer is available for all operating systems. Windows might be an issue. Otherwise just pip install buildozer.

4. Prepare your target phone

Make sure your android phone has debug mode unlocked, and turn on usb debugging.

5. Compile

Connect your phone to your computer. Run buildozer targeted for android:

>buildozer android debug deploy

It might work








