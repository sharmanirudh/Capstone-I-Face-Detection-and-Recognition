import os
from PIL import Image, ImageDraw
import face_recognition

def detectFaces(image):
	# Load the jpg file into a numpy array
	image = face_recognition.load_image_file(image)

	# Find all the faces in the image using the default HOG-based model.
	# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
	# See also: find_faces_in_picture_cnn.py
	face_locations = face_recognition.face_locations(image)

	# Find all the faces in the image using a pre-trained convolutional neural network.
	# This method is more accurate than the default HOG model, but it's slower
	# unless you have an nvidia GPU and dlib compiled with CUDA extensions. But if you do,
	# this will use GPU acceleration and perform well.
	# See also: find_faces_in_picture.py
	# face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

	print("I found {} face(s) in this photograph.".format(len(face_locations)))

	# Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
	# See http://pillow.readthedocs.io/ for more about PIL/Pillow
	pil_image = Image.fromarray(image)
	# Create a Pillow ImageDraw Draw instance to draw with
	draw = ImageDraw.Draw(pil_image)

	for face_location in face_locations:
	    # Print the location of each face in this image
	    top, right, bottom, left = face_location
	    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

	    # You can access the actual face itself like this:
	    # face_image = image[top:bottom, left:right]
	    # pil_image = Image.fromarray(face_image)
	    
	    # Draw a box around the face using the Pillow module
	    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255), width=0)

	    # image_path = os.path.join(app.root_path, 'static/user_images/', image_fn)
	    # output_size = (500, 500)
	    # i = Image.open(pil_image)
	    # i.thumbnail(output_size)
	    # i.save(image_path)

	# Remove the drawing library from memory as per the Pillow docs
	del draw

	# Display the resulting image
	# pil_image.show()
	return pil_image


# detectFaces('static/unknown/03.jpg', '03.jpg')
