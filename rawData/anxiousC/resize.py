#!/usr/bin/env python

import Image
import os, sys

def resizeImage(infile, output_dir, size=(32,32)):
     outfile = os.path.splitext(infile)[0]+"_r"
     extension = os.path.splitext(infile)[1]

     if (cmp(extension, ".png")):
        return

     if infile != outfile:
        try :
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(output_dir+outfile+extension,"png")
        except IOError:
            print "cannot reduce image for ", infile


if __name__=="__main__":
    
    dir = os.getcwd()
    output_dir = os.path.join(dir+"R32/")
    print "dir ="+dir+" --- \n output dir== "+output_dir+"\n\n"
    if not os.path.exists(os.path.join(dir,output_dir)):
        os.mkdir(output_dir)
    for file in os.listdir(dir):
		resizeImage(file,output_dir)
