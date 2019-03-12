import cv2
import numpy as np
import eigenFacesImport as efi

#import cv2 Classifiers
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)
number = 0
eigenFaces = efi.eigenFacesImport()
eigenVector = efi.eigenVectorImport()

while(number<100):
    # Capture frame-by-frame
	ret, frame = video_capture.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(
	    gray,
	    scaleFactor=1.3,
	    minNeighbors=5
	)

	# Draw a rectangle around the faces and eyes
	for (x, y, w, h) in faces:

	    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
	    #crop the image, resize to 100*100
	    roi_gray = gray[y:y+h, x:x+w]
	    resized = cv2.resize(roi_gray,(100,100))
	    #save image in crop folder,required to create before running code
	    cv2.imwrite('temp/crop'+str(number)+'.jpg',resized)
	    number = number +1
	    cv2.waitKey(1500)

	# Display the resulting frame
	cv2.imshow('Video', frame)

	#calculate nearest eigenFace
	faceVec = np.resize(resized,(10000,1))
	RecEigenFace = np.dot(eigenVector,faceVec)
	print RecEigenFace.shape


	minDiff = 1000000000
	for i in range(0,40):
		tempFace = eigenFaces[i]
		result = np.absolute(np.array(RecEigenFace) - np.array(tempFace))
		diff = np.sum(result)
		#print diff
		if diff<minDiff:
			minDiff = diff 
			nearestFace = i

	print ("recognized as ", nearestFace)
	print ("minimun difference is ",minDiff)
	path = 'cap/'+str(i)+'.jpg'
	img = cv2.imread(path)
	cv2.imshow("recognation",img)


	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything is done, release the capture
#video_capture.release()
#cv2.destroyAllWindows()