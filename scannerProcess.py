import cv2
import re
import numpy as np
from collections import Counter
import os
from fabianasocr import ocr_space_file


# image_path variebl som omvandlas till grayscale med openCV och pyteseract gör om till text
def scanner_Process(image_path):
    #   img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    text = ocr_space_file(image_path)
    return text


# tar in texten från fkn ovan och försöker matcha med regex
def interpret_parking_sign(text):
    patterns = [
        (
            re.compile(r"IP\s+(\d+)\s+min\n(\d{1,2}-\d{1,2})", re.IGNORECASE),
            "Free parking allowed everyday of the week for {} min between {}.",
        ),
        (
            re.compile(r"OP\s+(\d+)\s+min", re.IGNORECASE),
            "No parking allowed for {} min.",
        ),
        (
            re.compile(r"P\n(\d+)\s*tim\n(\d{1,2}\s*-\s*\d{1,2})", re.IGNORECASE),
            "Free parking allowed everyday of the week for {} hours between {}.",
        ),
        (
            re.compile(r"P\n(\d+)\s*tim", re.IGNORECASE),
            "Free parking allowed everyday of the week for {} hours.",
        ),
        (
            re.compile(r"(\d+)\s+tim", re.IGNORECASE),
            "Free parking allowed everyday of the week for {} hours.",
        )
        # kan fortsätta i all evighet...
    ]

    # hitta rätt mönster och lägg till rätt etikett
    for pattern, response_template in patterns:
        match = pattern.search(text)
        if match:
            groups = match.groups()
            response = response_template.format(*groups)
            return response

    return "The sign couldn't be interpreted"  # Return default message if no pattern matches


def detect_color(image_path):
    img = cv2.imread(image_path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color ranges for blue, red, yellow, and white in HSV color space
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    lower_yellow = np.array([15, 50, 50])
    upper_yellow = np.array([35, 255, 255])

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 50, 255])

    # Create masks for each color
    mask_blue = cv2.inRange(img_hsv, lower_blue, upper_blue)
    mask_red1 = cv2.inRange(img_hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(img_hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(img_hsv, lower_white, upper_white)

    # Calculate the area of each color in the image
    area_blue = np.sum(mask_blue) / 255
    area_red = np.sum(mask_red) / 255
    area_yellow = np.sum(mask_yellow) / 255
    area_white = np.sum(mask_white) / 255

    # Find the dominant color
    max_area = max(area_blue, area_red, area_yellow, area_white)
    if max_area == area_blue:
        return "blue"
    elif max_area == area_red:
        return "red"
    elif max_area == area_yellow:
        return "yellow"
    elif max_area == area_white:
        return "white"
    else:
        return "unknown"


# kombinerar både bild och text, lite dålig logik här men inget du behöver lägga fokus på.
def process_parking_sign(image_path):
    print(
        "process_parking_sign function called"
    )  # testar så att den printar rätt, ta bort

    text = scanner_Process(image_path)
    print(f"Text recognized by OCR: {text}")  ##testar så att den printar rätt, ta bort

    interpretation = interpret_parking_sign(text)
    print(
        f"Interpretation: {interpretation}"
    )  # testar så att den printar rätt, ta bort

    if not interpretation:
        dominant_color = detect_color(image_path)
        if dominant_color == "red" or dominant_color == "yellow":
            return "No parking allowed"
        else:
            return f"Color detected: {dominant_color}. Unable to interpret the sign"

    return interpretation


# testar så att den printar rätt, ta bort
"""image_path = "2 tim gratis mellan 9-18.png"
result = process_parking_sign(image_path)
print(result)"""
