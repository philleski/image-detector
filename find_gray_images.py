#!/usr/bin/python

import datetime
import os
import sys
import tempfile
import urllib
from PIL import Image

if len(sys.argv) != 4:
    raise Exception("Usage: find_gray_images.py <input_filename (one image URL per line)> <output_filename> <error_filename>")

input_filename, output_filename, error_filename = sys.argv[1:]

local_image = tempfile.mkstemp(suffix=".jpg")[1]
opener = urllib.URLopener()
opener.addheader("Pragma", "no-cache")
with open(output_filename, "w") as ofh, open(error_filename, "w") as err:
    for ctr, line in enumerate(open(input_filename)):
        try:
            gray = True
            remote_image = line.rstrip("\n")
            if not remote_image.endswith(".jpg"):
                raise NotImplementedError("Currently only JPEG is supported.")
            opener.retrieve(remote_image, local_image)
            jpgfile = Image.open(local_image)
            width, height = jpgfile.size
            handle = jpgfile.getdata()
            for y in range(height - 5, height):   # bottom 5 pixels
                for x in range(width):   # all pixels in horizontal band
                    pixel = handle.getpixel((x, y))
                    if pixel != (128, 128, 128):
                        gray = False
            if gray:
                print '\t', remote_image
                print >>ofh, remote_image
            os.remove(local_image)
            if ctr % 100 == 0:
                print ctr, datetime.datetime.now()
        except Exception, e:
            print ">>> Exception in file: " + remote_image + str(e)
            err.write("Exception in file: " + remote_image + str(e))
