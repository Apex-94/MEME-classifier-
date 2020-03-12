# from PIL import Image
# # import pytesseract
# # import argparse
# # import cv2
# # import os
# # # pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR'  # your path may be different
# #
# # def ocr_core(filename):
# #     """
# #     This function will handle the core OCR processing of images.
# #     """
# #     text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
# #     return text
# #
# # print(ocr_core(r'C:\Users\user\PycharmProjects\MEME-classifier-\data\offensive memes\0056.jpg'))
from PIL import Image
import numpy as np
import os
import sys
import subprocess
import tempfile
import shlex
import glob
from pathlib import Path
import re
import string
import csv

tesseract_cmd = 'tesseract'


def give_temp_name():
    tmpfile = tempfile.NamedTemporaryFile(prefix="tess_")
    return tmpfile.name


def del_file(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def run_tesseract(input_filename, output_filename_base, lang=None):
    command = [tesseract_cmd, input_filename, output_filename_base]

    if lang is not None:
        command += ['-l', lang]

    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    status = proc.wait()
    error_string = proc.stderr.read()
    proc.stderr.close()
    return status, error_string


def image_to_string(image):
    if len(image.split()) == 4:
        r, g, b, a = image.split()
        image = Image.merge("RGB", (r, g, b))

    input_file_name = '%s.bmp' % give_temp_name()
    output_file_name_base = give_temp_name()
    output_file_name = '%s.txt' % output_file_name_base
    try:
        image.convert('RGB').save(input_file_name)
        status, error_string = run_tesseract(input_file_name, output_file_name_base, lang='eng')

        f = open(output_file_name, 'rb')
        try:
            return f.read().decode('utf-8').strip()
        finally:
            f.close()
    finally:
        del_file(input_file_name)
        del_file(output_file_name)


# def spell_check(text):
# 	text = text.replace(" u ", " you ").replace(' ur ', ' your ')
# 	text = text.replace(text[0], text[0].upper(), 1)
# 	return text

def main():
    l = []
    i = 0
    # for filepath in glob.iglob(r"C:\Users\user\PycharmProjects\MEME-classifier-\data\offensive memes"):
    #     (l.append(filepath))
    paths = Path(r'C:\Users\user\PycharmProjects\MEME-classifier-\data\offensive memes').glob('**/*.png')
    for path in paths:
        # for i in range(len(l)):
        filename = str(path)
        # filename = "in/" + input("Image of text to recognize: in/")
        image = Image.open(filename)
        text = image_to_string(image)
        text = text.replace('\n', ' ').lower()
        text = re.sub(' +', ' ', text)
        text = "".join(l for l in text if l not in string.punctuation)
        l.append(text)
        l.append(filename)
        print("OCR sucessfull for ")
        print(i)
        i += 1
        # text = spell_check(text)
        # l.append(zip(text,filename))
        # # print ("Text recognized as: '" + str(text) + "'")
        # # print("For file"+filename)
        # print(str(l[i]))
        # i=i+1
    # with open('output', 'wb') as myfile:
    #     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #     wr.writerow(l)
    np.savetxt("output", l, delimiter=",", fmt='%s')


main()
