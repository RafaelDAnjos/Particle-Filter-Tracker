import random
import decimal
import math
import matplotlib.pyplot as plt
import cv2
import numpy as np


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
        particulas[i].vX = float(decimal.Decimal(random.randrange(0, velocidadeInicialX*10))/10)
        particulas[i].vY = float(decimal.Decimal(random.randrange(0, velocidadeInicialY*10))/10)
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
    ruido = np.random.uniform(low=0, high=20, size=len(particulas_antigas))
    for i in range(len(particulas_antigas)):
        particulas_atuais[i].x = particulas_antigas[i].x + particulas_antigas[i].x * particulas_antigas[i].vX * (1/30)
        particulas_atuais[i].y = particulas_antigas[i].y + particulas_antigas[i].y * particulas_antigas[i].vY * (1/30)
        particulas_atuais[i].vX = particulas_antigas[i].vX + ruido[i]
        particulas_atuais[i].vY = particulas_antigas[i].vY + ruido[i]

    return particulas_atuais

def encontraCentro(frame,M):
    posX = int(M["m10"] / M["m00"])
    posY = int(M["m01"] / M["m00"])
    if posX == 0:
        posX +=1
    if posY == 0:
        posY +=1
    center = [posX,posY]
    cv2.circle(frame, (center[0], center[1]), 7, (255, 255, 255), -1)
    cv2.putText(frame, "center", (center[0] - 20, center[1] - 20),
    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    return center


def correcao(xCenter,yCenter,particulas):
    soma = 0
    for i in range(len(particulas)):
        dist = math.sqrt((particulas[i].x-xCenter) ** 2 + (particulas[i].y-yCenter) ** 2)
        particulas.peso = math.log(-(dist))
        soma += particulas.peso
    for i in range(len(particulas)):
        particulas[i].peso = particulas[i].peso/soma

    return particulas


def mediaPesos(particulas):
    media_pesos = 0
    for i in range(len(particulas)):
        media_pesos += particulas[i].peso
        print(media_pesos)
    return media_pesos/len(particulas)


#Inicialmente, o algoritmo cria uma lista de tamanho igual à soma dos pesos das partículas 
def resorteio(particulas,particulas_antigas):
    media_pesos = mediaPesos(particulas_antigas)
    n = decimal.Decimal(random.randrange(0,1))/10
    

    return particulas_antigas


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
    particulas_atuais= geraParticulas()
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
            center = encontraCentro(frame,M)
            
            # draw the contour and center of the shape on the image
            particulas_atuais = predict(particulas_atuais,particulas_antigas)
            particulas_atuais = resorteio(particulas_atuais,particulas_antigas)
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
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
    # cv2.imshow('Visão',thresh5)


main()