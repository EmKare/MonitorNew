import pytesseract
from PIL import Image

# Open the image file
image = Image.open('C:/Users/DELL/Desktop/Untitled3.png')#C:\Users\DELL\Desktop\MyJourney\Python\ParkingApp\Monitor\mapToAdd.py

# Perform OCR using PyTesseract
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)