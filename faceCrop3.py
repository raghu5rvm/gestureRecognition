import cv2
import os
import glob


def faceCrop(imagePattern,boxScale=1):
    # Select one of the haarcascade files:
    #   haarcascade_frontalface_alt.xml  <-- Best one?
    #   haarcascade_frontalface_alt2.xml
    #   haarcascade_frontalface_alt_tree.xml
    #   haarcascade_frontalface_default.xml
    #   haarcascade_profileface.xml
    imgList=glob.glob(imagePattern)
    if len(imgList)<=0:
        print 'No Images Found'
        return
    i=0
    for img in imgList:
        facecrop(img,str(i))
        i=i+1
"""        pil_im=Image.open(img)
        cv_im=pil2cvGrey(pil_im)
        faces=DetectFace(cv_im,faceCascade)
        if faces:
            n=1
            for face in faces:
                croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
                fname,ext=os.path.splitext(img)
                croppedImage.save(fname+'_crop'+str(n)+ext)
                n+=1
        else:
            print 'No faces found:', img
"""
def facecrop(image,i):
	facedata = "haarcascade_frontalface_alt.xml"
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
		cv2.imwrite("anxiousC/"+i+"_c"+ext, sub_face)
	return


faceCrop('anxious/*.png',boxScale=1)
