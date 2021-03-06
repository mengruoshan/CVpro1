import cv2
import numpy
import math
from PIL import Image

imgNum = 35
numEigValue = 300


#mean adjustment for a 1d array
def mean_adjustment(array_1d):
	mean = array_1d.mean()
	for x in range(0, len(array_1d)):
		temp = array_1d[x] - mean
		array_1d[x] = temp
	return array_1d


#normalise the vector in a 1d array and return the array
def normalised_vector(array_1d):
	total = 0
	for x in range(0, len(array_1d)):
		total = total + array_1d[x]*array_1d[x]

	total = math.sqrt(total)
	for x in range(0, len(array_1d)):
		array_1d[x] = array_1d[x] / total
	return array_1d


#convert string to complex 
def convertComplex(complex_number):
	
	complex_number = complex_number.replace("+-", "-")
	t = complex(complex_number)
	#result = (t.real*t.real + t.imag*t.imag)**(1.0/2)
	return t


#Ini func that create and return the mean adjusted database matrix
def ini_img_base():
	#Create the base 100*10000 matrix
	baseMatrix = numpy.zeros((imgNum,10000))
	array_int = numpy.zeros(10000)

	for x in range(0, imgNum):
		img = Image.open('cap/%s.jpg' % x).convert('L')  #import the image base
		img_arr_2d = numpy.asarray(img)              #convert the image to 2d array
		img_arr_1d = img_arr_2d.flatten()			 #convert the image 2d array to 1d array
		for y in range(0, len(img_arr_1d)):
			array_int[y] =  img_arr_1d[y]          
		#array_int = mean_adjustment(array_int)     #perform the mean adjustment for teh 1d array
		baseMatrix[x,:] = array_int[:]              #save the mean adjusted array in the the base matrix
	return baseMatrix,imgNum,numEigValue


#import eigenFaces(imgNum*200) generated by create_eigFaces.py
def eigenFacesImport():
	
	eigenFaces = numpy.empty((imgNum,numEigValue),complex)
	filepath = 'eigFaces'  
	with open(filepath) as fp:  
		vec1 = fp.readline()
		vec = convertComplex(vec1)
		print numpy.iscomplexobj(vec)
		print vec
		row = 1

		while row <=imgNum:
			col = 1
	   		while col<=numEigValue:

				eigenFaces[row-1,col-1] = vec
				vec1 = fp.readline()
				col += 1
			row +=1

	print ("eigenFaces:",eigenFaces.shape)
	return eigenFaces


#import eigenVector
def eigenVectorImport():

	eigVector = numpy.empty((10000*numEigValue,1),complex)
	filepath2 = 'eignevector'  

	with open(filepath2) as fp:  
		vec = fp.readline()
		cnt = 1

		while cnt <=10000*numEigValue: #pick eigenvectors with top 200~300 largest eigenvalue
			cmpl = convertComplex(vec)
			eigVector[cnt-1] = cmpl
			vec = fp.readline()
			cnt += 1

		eigVec = numpy.resize(eigVector,(10000,numEigValue))

	eigVectorT = eigVec.transpose()		
	print ("eigenVectorT:",eigVectorT.shape)
	return eigVectorT


#calculate eigenFaces
def calcEigFaces():
	baseMatrix,imgNum,numEigValue = ini_img_base()    #35*10000
	baseMatrixT = baseMatrix.transpose()   #10000*35
	print baseMatrixT.shape

	face_avg = numpy.empty((1,10000),float)            #1*10000
	face_avg = baseMatrix.sum(axis = 0)/imgNum
	avgMatrix = numpy.empty((imgNum,10000),float)      #35*10000
	for cnt in range (0,imgNum):

		avgMatrix[cnt]=baseMatrix[cnt] - face_avg

	transMatrix=avgMatrix.transpose()               #10000*35

	eigenVector = eigenVectorImport()   #300*10000
	eigFaces = numpy.empty((numEigValue,imgNum),complex)       #300*35
	number = 0
	#img = Image.open('cap/0.jpg')
	eigFaces = numpy.dot(eigenVector,transMatrix)
	eigFacesT = eigFaces.transpose() 
	return eigFacesT

#calcualte average face
def avgMatrix():
	baseMatrix,imgNum,numEigValue = ini_img_base()    #35*10000
	baseMatrixT = baseMatrix.transpose()   #10000*35
	face_avg = numpy.empty((1,10000),float)            #1*10000
	face_avg = baseMatrix.sum(axis = 0)/imgNum
	return face_avg