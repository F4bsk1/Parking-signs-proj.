import cv2
import pytesseract
import re

def scanner_Process(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img)
    return text


def interpret_parking_sign(text):
    duration_regex = re.compile(r'(\d+\s*(?:min|hour|hr)s?)')
    durations = duration_regex.findall(text)

    return durations

    return te


