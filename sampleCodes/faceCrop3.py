import cv2
import os

def facecrop(image):
	facedata = "haarcascade_frontalcatface_extended.xml"
	cascade = cv2.CascadeClassifier(facedata)
	img = cv2.imread(image)
	minisize = (img.shape[1],img.shape[0])
	miniframe = cv2.resize(img, minisize)
	faces = cascade.detectMultiScale(miniframe)
	for f in faces:
		x, y, w, h = [ v for v in f ]
		cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))
		sub_face = img[y:y+h, x:x+w]
		fname, ext = os.path.splitext(image)
		cv2.imwrite(fname+"_cropped_"+ext, sub_face)
	return
facecrop("1.jpg")
facecrop("2.jpg")
facecrop("3.jpg")
facecrop("a.png")
facecrop("b.png")
facecrop("c.png")
facecrop("d.png")
facecrop("e.png")
