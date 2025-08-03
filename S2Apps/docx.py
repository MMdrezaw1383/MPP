#correcting all reversed farsi numbers in docx file
from docx import document

number = ''

doc = document('file path')

newt =""
for par in doc.paragraphs:
    for char in par:
        
        if char in '1234567890':
            number = char + number
            
        else:
            newt += number + char
            number = ''

    print(newt)
            
