# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle

# import the necessary packages
from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2
import os

class Extract_encodings:
	# construct the argument parser and parse the arguments
	# ap = argparse.ArgumentParser()
	# ap.add_argument("-i", "--dataset", required=True,
	# 	help="path to input directory of faces + images")
	# ap.add_argument("-e", "--encodings", required=True,
	# 	help="path to serialized db of facial encodings")
	# ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	# 	help="face detection model to use: either `hog` or `cnn`")
	# args = vars(ap.parse_args())

	def __init__(self):
		print("[INFO] quantifying faces...")
		self.imagePaths = list(paths.list_images("dataset"))
		self.model_to_use = "cnn"
		self.encoding_file = "encodings.pickle"
		# grab the paths to the input images in our dataset

	def extract_encodings(self):
		knownEncodings = []
		knownNames = []


		# initialize the list of known encodings and known names


		# loop over the image paths
		for (i, imagePath) in enumerate(self.imagePaths):
			# extract the person name from the image path
			print("[INFO] processing image {}/{}".format(i + 1, len(self.imagePaths)))
			name = imagePath.split(os.path.sep)[-2]

			# load the input image and convert it from RGB (OpenCV ordering)
			# to dlib ordering (RGB)
			image = cv2.imread(imagePath)
			scale_percent = 50
			width = int(image.shape[1] * scale_percent / 100)
			height = int(image.shape[0] * scale_percent / 100)
			dim = (width, height)
			image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

			# detect the (x, y)-coordinates of the bounding boxes
			# corresponding to each face in the input image

			boxes = face_recognition.face_locations(rgb, number_of_times_to_upsample=0, model=self.model_to_use)


			# compute the facial embedding for the face
			encodings = face_recognition.face_encodings(rgb, boxes)

			# loop over the encodings
			for encoding in encodings:
				# add each encoding + name to our set of known names and
				# encodings
				knownEncodings.append(encoding)
				knownNames.append(name)

		# dump the facial encodings + names to disk
		print("[INFO] serializing encodings...")
		data = {"encodings": knownEncodings, "names": knownNames}
		f = open(self.encoding_file, "wb")
		f.write(pickle.dumps(data))
		f.close()
