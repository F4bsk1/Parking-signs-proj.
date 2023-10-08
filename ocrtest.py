import requests
import json

def ocr_space_file(filename, overlay=False, api_key="K88652057288957", language="eng"):
    """OCR.space API request with local file.
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        "apikey": api_key,
        "language": language,
        "OCREngine": 2
    }
    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload
        )

    #Konvertera strängindatan som är skriven i json, till json, och ta ut ParsedText
    jsondata = json.loads(r.content.decode())
    parsedText = jsondata['ParsedResults'][0]['ParsedText']

    return parsedText

# Exempel:
#test_file = ocr_space_file("test4.jpg")
#print(test_file)

