import cv2
import pytesseract
import re
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import os

def scanner_Process(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    text = pytesseract.image_to_string(img)
    return text

def interpret_parking_sign(text):
    duration_regex = re.compile(r'(\d+\s*(?:min|hour|hr)s?)')
    weekdays_regex = re.compile(r'\b(måndag|tisdag|onsdag|torsdag|fredag|lördag|söndag)\b', re.IGNORECASE)
    dates_regex = re.compile(r'\b(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})\b')

    durations = duration_regex.findall(text)
    weekdays_regex = weekdays_regex.findall(text)
    dates_regex = dates_regex.findall(text)
    
    return durations, weekdays_regex, dates_regex

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


def process_parking_sign(image_path):
    text = scanner_Process(image_path)
    durations, weekdays, dates = interpret_parking_sign(text)

    if not durations and not weekdays and not dates:
        dominant_color = detect_color(image_path)
        if dominant_color == "blue" or dominant_color == "red":
            return 'No parking allowed'
        else:
            return f'Color detected: {dominant_color}. Unable to interpret the sign'

    return {
        'durations': durations,
        'weekdays': weekdays,
        'dates': dates
    }



# Set the directory where you saved the parking sign images
script_dir = os.path.dirname(os.path.abspath(__file__))
image_directory = os.path.join(script_dir, "parkin-signs-pic")


# Iterate through the images in the directory
for image_filename in os.listdir(image_directory):
    # Check if the file is an image (you can modify this to include more image extensions if needed)
    if image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(image_directory, image_filename)
        print(f"Processing image: {image_filename}")
        
        # Process the parking sign and print the result
        result = process_parking_sign(image_path)
        print(f"Result: {result}\n")








