import os
import numpy as np
import cv2 as cv

def detectFace(image_path, image_name):
	face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

	img = cv.imread(image_path)
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, w, h) in faces:
	    cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
	    roi_gray = gray[y:y + h, x:x + w]

	image_fn, f_ext = os.path.splitext(image_path)
	cv.imwrite(f"{image_fn}detected_face{f_ext}", img)

	image_fn, f_ext = os.path.splitext(image_name)
	return f"{image_fn}detected_face{f_ext}"