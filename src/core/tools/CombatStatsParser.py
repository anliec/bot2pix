from core import dofus

import pytesseract
import cv2
import re


def read_pa():
    pa_image = dofus.PA_R.capture()
    h, w, c = pa_image.shape
    red = cv2.threshold(pa_image[:, :, 2], thresh=200, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
    blue = cv2.threshold(pa_image[:, :, 0], thresh=200, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
    thresh = red & blue
    thresh = cv2.resize(thresh, (w * 10, h * 10))
    thresh = cv2.blur(thresh, (7, 7))
    text = pytesseract.image_to_string(thresh, config='--psm 6', lang='fra')
    print(text)
    res = re.findall("(\d+)", text)
    assert len(res) > 0
    return int(res)


def read_pm():
    pm_image = dofus.PM_R.capture()
    h, w, c = pm_image.shape
    thresh = cv2.threshold(pm_image[:, :, 0], thresh=200, maxval=255, type=cv2.THRESH_BINARY_INV)[1]
    thresh = cv2.resize(thresh, (w * 10, h * 10))
    thresh = cv2.blur(thresh, (7, 7))
    text = pytesseract.image_to_string(thresh, config='--psm 6', lang='fra')
    print(text)
    res = re.findall("(\d+)", text)
    assert len(res) > 0
    return int(res)