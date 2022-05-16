import numpy as np
import cv2
import pytesseract

def pytess_detec(img_gray, digits_only, debug_mode):
    T, img_binary = cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU)

# -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# outputbase digits

    if(digits_only):
        pytess_config = r'--oem 3 --psm 8 outputbase digits'
    else:
        pytess_config = r'--oem 3 --psm 7'

    string_out = pytesseract.image_to_string(img_binary, config=pytess_config)

    if(debug_mode):
        cv2.imshow("x", img_binary)
    
    return string_out.strip()

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    img = cv2.imread("samples/NurseIDP1111.png",cv2.IMREAD_GRAYSCALE)
    digits_only = True
    print(pytess_detec(img, digits_only, debug_mode=True))

"""
Page segmentation modes:
0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
                        bypassing hacks that are Tesseract-specific.
"""
