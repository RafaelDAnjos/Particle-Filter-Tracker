import random
import decimal
import math
import matplotlib.pyplot as plt
import cv2
import numpy as np
import imutils



numero_de_Particulas = 10
velocidadeInicialX = 20
velocidadeInicialY = 20
numero_de_frames = 30




class Particula():
    # Construtor do no
    def __init__(self):
        self.x = 0
        self.y = 0
        self.peso = 0
        self.vX = 0
        self.vy = 0
    # Método usado na comparação de dois nós
    # def __eq__(self, outroNo): 
    #     return self.posicao == outroNo.posicao

def velocidades(particulas):
    for i in range(len(particulas)):
        particulas[i].vX = decimal.Decimal(random.randrange(0, velocidadeInicialX*10))/10
        particulas[i].vY = decimal.Decimal(random.randrange(0, velocidadeInicialY*10))/10
    return particulas

def geraParticulas():
    particulas = []
    for i in range(numero_de_Particulas):
        particula = Particula()
        particulas.append(particula)
    return particulas

#seta todos as particulas no centro de massa do objeto inicialmente
def updateParticulasCM(centro,particulas):
    particlas_novas = []
    for i in range(len(particulas)):
        particulas[i].x = centro[0]
        particulas[i].y = centro[1]
        particlas_novas.append(particulas[i])
    return particlas_novas

def predict(particulas_atuais,particulas_antigas):
    ruido = 0.5
    for i in range(len(particulas_antigas)):
        particulas_atuais[i].x = particulas_antigas[i].x + particulas_antigas[i].x * particulas_antigas[i].vX * (1/30)
        particulas_atuais[i].y = particulas_antigas[i].y + particulas_antigas[i].y * particulas_antigas[i].vY * (1/30)
        particulas_atuais.vX = particulas_antigas.vX + ruido
        particulas_atuais.vY = particulas_antigas.vY + ruido
    return particulas_atuais

def correcao(xCenter,yCenter,particulas):
    
    for i in range(len(particulas)):
        dist = math.sqrt((particulas[i].x-xCenter) ** 2 + (particulas[i].y-yCenter) ** 2)
        particulas.peso = math.log(-(dist))

    return particulas

def mediaPesos(particulas):
    media_pesos = 0
    for i in range(len(particulas)):
        media_pesos += particulas[i].peso

    return media_pesos/len(particulas)

#Inicialmente, o algoritmo cria uma lista de tamanho igual à soma dos pesos das partículas 
def resorteio(particulas,particulas_antigas):
    media_pesos = mediaPesos(particulas)

    return particulas

def imprimeParticulas(frame,particulas):
    for i in range(len(particulas)):
        cv2.circle(frame,(int(particulas[i].y),int(particulas[i].x)), 3, (255,0,0), -1)

#main
def main():

    curFrame = 0
    cap = cv2.VideoCapture('ball_bouscing.mp4')
    ret, frame = cap.read()
    newx = len(frame[0])//2
    newy = len(frame)//2
    frame = cv2.resize(frame,(newx,newy))

    particulas_antigas = []
    particulas_atuais = []

    particulas_antigas = geraParticulas()
    particulas_antigas = updateParticulasCM([6,3],particulas_antigas)
    particulas_antigas = velocidades(particulas_antigas)


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
            posX = int(M["m10"] / M["m00"])
            posY = int(M["m01"] / M["m00"])
            if posX == 0:
                posX +=1
            if posY == 0:
                posY +=1
            center = [posX,posY]
            # draw the contour and center of the shape on the image
            cv2.circle(frame, (posX, posY), 7, (255, 255, 255), -1)
            cv2.putText(frame, "center", (posX - 20, posY - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


            # particulas_atuais = resorteio(particulas_atuais,particulas_antigas)
            
            particulas_antigas = particulas_atuais.copy()
            #ler outro frame

            particulas_atuais = updateParticulasCM(center,particulas_antigas)

        else:
        # show the image
            cv2.imshow("Image", frame)



        # cv2.imshow('mask',mask)
        imprimeParticulas(frame,particulas_antigas)
        cv2.imshow("Image", frame)

        # cv2.imshow('res',res)
        k = cv2.waitKey(10) & 0xFF
        if k == 27:
            break
    # cv2.imshow('Visão',thresh5)








main()