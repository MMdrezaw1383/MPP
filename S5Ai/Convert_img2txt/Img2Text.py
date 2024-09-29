from PIL import Image
# export text from img
import pytesseract

import pathlib
from googletrans import Translator
translator = Translator()

pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/Cellar/tesseract/5.4.1/bin/tesseract"

per_text = ""
ans = input("translated? ")

for path in pathlib.Path("per_pics").iterdir():
    if path.is_file():
        img = path
        per_text += pytesseract.image_to_string(Image.open(img) ,lang="fas")
        per_text += 50 * "_" + "\n"
        
text = ""       
for path in pathlib.Path("eng_pics").iterdir():
    if path.is_file():
        img = path
        eng = pytesseract.image_to_string(Image.open(img) ,lang="eng")
        if "y" in ans:
            t = translator.translate(eng ,src="en",dest="fa")
            text += t.text
        else:
            text += eng
            
        text +="\n" + 50 * "_" + "\n"

with open("text.txt",mode="w",encoding="utf-8") as t:
    t.write(text)

