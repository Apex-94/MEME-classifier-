from PIL import Image
from os import listdir
from os.path import splitext

target_directory = r'C:\Users\user\PycharmProjects\MEME-classifier-\data\offensive memes'
target = '.jpg'

for file in listdir(target_directory):
    filename, extension = splitext(file)
    try:
        if extension not in ['.py', target]:
            im = Image.open(filename + extension)
            im.save(filename + target)
    except OSError:
        print('Cannot convert %s' % file)