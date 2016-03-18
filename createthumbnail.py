from PIL import Image
import os

size = (256, 256)
files = os.listdir("images")

for f in files:
    img = Image.open("images/" + f)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save("thumbnails/%s" % f)
