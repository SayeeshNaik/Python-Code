import pytesseract
from PIL import Image
import requests

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\SaishNaik\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
def captcha_solver(image_path):
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image, config='--psm 6')
        numbers = ''.join(filter(str.isdigit, extracted_text))
        return numbers
    except Exception as e: return e

def captcha_solver_php(php_url):
    try:
        response = requests.get(php_url)
        response.raise_for_status() 
        with open("temp_captcha.jpg", 'wb') as file:
            file.write(response.content)
        captcha = captcha_solver("temp_captcha.jpg")
        return captcha
    except: None
        

