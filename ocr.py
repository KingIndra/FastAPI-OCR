import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/OCR/Tesseract-OCR/tesseract.exe'

def read_image(img_path, lang='eng'):
    try:
        return pytesseract.image_to_string(img_path, lang=lang)
    except Exception as err:
        print(err)
        return "[ERROR] Unable to process file: {0}".format(img_path)
