#!/usr/bin/env python
from __future__ import with_statement
from PIL import Image     
import cv2
import os
from os import listdir
from os.path import isfile, join, isdir

p='/home/salt/Desktop/projFiles/cohn-kanade-images croppedLabelled/final'
print p

with open('testFinal90.csv', 'w+') as opFile:
		dirs = [ folder for folder in listdir(p) if isdir(join(p,folder)) ]
		#opFile.write('{0}'.format('gest\t'))	
		#for h in range (1,1025):
		#	opFile.write('{0}'.format('px'+str(h)+'\t'))
		#opFile.write('{0}'.format('\n'))
		for d in range(0,len(dirs)):
			files = [ f for f in listdir(join(p,dirs[d])) if isfile(join(p,dirs[d],f)) ]
			
			print "\n---------checking files in "+str(dirs[d]+"--------------------------")
			
			for n in range(0, len(files)):
				ext = os.path.splitext(files[n])[-1].lower()
				print "checking file "+str(files[n])
				if ext != ".png":
					print "file format different skipping now"
					continue
				path=join(p,dirs[d])
				#load the pixel info
				cvImg = cv2.imread(join(path,files[n]))
				cvImgG = cv2.cvtColor(cvImg,cv2.COLOR_RGB2GRAY)
				#cv2.imshow('somehting-'+str(n),cvImgG)
				#open a file to write the pixel data
				print dirs[d]+" should be appended to col1"
				if(str(dirs[d]) == "angryCR32"):
						opFile.write('{0}'.format('angry\t'))
				elif(str(dirs[d]) == "normalCR32"):
						opFile.write('{0}'.format('normal\t'))
				elif(str(dirs[d]) == "sadCR32"):
						opFile.write('{0}'.format('sad\t'))
				elif(str(dirs[d]) == "disgustCR32"):
						opFile.write('{0}'.format('disgust\t'))
				elif(str(dirs[d]) == "happyCR32"):
						opFile.write('{0}'.format('happy\t'))
				elif(str(dirs[d]) == "anxiousCR32"):
						opFile.write('{0}'.format('anxious\t'))
				elif(str(dirs[d]) == "test"):
						opFile.write('{0}'.format('test\t'))
				
				#read the details of each pixel and write them to the file
				for x in range(0,32):
					for y in range(0,32):
						opFile.write('{0}\t'.format(cvImgG[x][y]))
						"""if(cvImgG[x][y]<125):
							#print "value:: "+str(cvImgG[x][y])+"  i="+str(x)+" and j="+str(y)+"\n"
							opFile.write('0\t')
						else:
							opFile.write('1\t')"""
				opFile.write('\n')
				print "end of file "+str(n)+"_c_r.png to csv"
			cv2.waitKey(0)
