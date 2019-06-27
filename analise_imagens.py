import cv2
import numpy as np
import imutils
import random


cap = cv2.VideoCapture('ball_bouscing.mp4')
velocidade = 0.7
numero_particulas = 100

ret, frame = cap.read()
newx = len(frame[0])//2
newy = len(frame)//2
frame = cv2.resize(frame,(newx,newy))
# particulas = geraParticulas(frame)


def setParams():
	numero_particulas = int(input("Informe a quantidade de particulas: "))


def predict(particles, velocidade):
    new_lst = []
    for i in particles:
        new_x = int(i[0] + i[0] * velocidade)
        new_y = int(i[1] + i[1] * velocidade)
        new_lst.append([new_x,new_y])
  
    return new_lst


def filtroRGB(src,r,g,b):
    if r == 0:
        src[:,:,2] = 0    #elimina o vermelho
    if g == 0:
        src[:,:,1] = 0    #elimina o verde
    if b == 0:
        src[:,:,0] = 0    #elimina o azul

def geraParticulas(frame):
	lista_pos = []
	for i in range(numero_particulas):
		k =  random.randint(1,len(frame)-1)
		j =  random.randint(1,len(frame[0])-1)
		lista_pos.append([k,j])
	return lista_pos

def imprimeParticulas(frame,particulas):
	for i in range(len(particulas)):
		cv2.circle(frame,(particulas[i][1],particulas[i][0]), 3, (255,0,0), -1)





while True:
	ret, frame = cap.read()
	newx = len(frame[0])//2
	newy = len(frame)//2
	frame = cv2.resize(frame,(newx,newy))
	# Convert BGR to HSV

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Threshold the HSV image to get only colors in parameters 1,2
	mask = cv2.inRange(hsv, (10, 42, 82), (18, 255, 255))
	mask = cv2.bitwise_not(mask)

	M = cv2.moments(mask)
	if M["m00"] != 0:
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
		center = [cX,cY]
		# draw the contour and center of the shape on the image
		cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
		cv2.putText(frame, "center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	else:
	# show the image
		cv2.imshow("Image", frame)

	# particulas = calcula_dist(center)


	



	# cv2.imshow('mask',mask)
	# imprimeParticulas(frame,particulas)
	cv2.imshow("Image", frame)

	# cv2.imshow('res',res)
	k = cv2.waitKey(15) & 0xFF
	if k == 27:
	    break
	# cv2.imshow('Visão',thresh5)

