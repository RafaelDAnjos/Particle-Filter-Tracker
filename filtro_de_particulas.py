
import math
import random
import matplotlib.pyplot as plt
import cv2
import numpy as np
import imutils


# simulation constants
FPS = 10
B_SIZE = 20
P_SIZE = 6
R_SIZE = 20
numero_particulas = 50
R_WALK_MAX = 10
ESTIMATE_RADIUS = 10
R_WALK_FREQUENposY = 5
JUMP_DISTANCE = 40

movedX = 0
movedY = 0
estimateX = 0
estimateY = 0
estimateWX = 0
estimateWY = 0

curFrame = -1


def distance(x1, y1, x2, y2):
    distX = x1-x2
    distY = y1-y2
    return  int(math.sqrt(distX*distX + distY*distY))

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

def imprimeParticulas(frame,particulas):
    for i in range(len(particulas)):
        cv2.circle(frame,(int(particulas[i][1]),int(particulas[i][0])), 3, (255,0,0), -1)


def geraParticulas(frame):
    lista_pos = []
    for i in range(numero_particulas):
        k =  random.randint(1,len(frame)-1)
        j =  random.randint(1,len(frame[0])-1)
        w = 1
        lista_pos.append([k,j,w])
    return lista_pos


def getWeight(robotDistToBeacon, particleDistToBeacon,maxDist):
    diff = abs(robotDistToBeacon - particleDistToBeacon)

    return (maxDist - diff) / maxDist


def degrade (particle, weight):
    particle[2] = particle[2] * weight

    return particle


def normalize (particula,maxWeight):
    if(maxWeight == 0):
        return particula
    
    particula[2] = particula[2] / maxWeight

    return particula


def filtro_particulas(particles,movedX,movedY,beacons,maxDist,curFrame):

    totalX = 0
    totalY = 0
    totalWX = 0
    totalWY = 0
    totalW = 0

    for i in range(len(particles)):
        totalX += particles[i][0]
        totalY += particles[i][1]
        weight = "%.2f" % particles[i][2]
        totalWX += (float(weight) * particles[i][0])
        totalWY += (float(weight) * particles[i][1])
        totalW += float(weight)
    
    estimateX = int(totalX / len(particles))
    estimateY = int(totalY / len(particles))
    estimateWX = totalWX / totalW
    estimateWY = totalWY / totalW


    # 1. if mouse moved (i.e. the "agent" moved), update all particles
    if movedX != 0 or movedY != 0:
        for i in range(len(particles)):
            particles[i][0] += movedX
            particles[i][1] += movedY


    # 2. do a random walk if on random walk frame
    if(R_WALK_FREQUENposY != 0 ) and ((curFrame % R_WALK_FREQUENposY) == 0):
        for i in range(len(particles)):
            dX = int(random.randint(1,R_WALK_MAX+1) - R_WALK_MAX/2)
            dY = int(random.randint(1,R_WALK_MAX+1) - R_WALK_MAX/2)
            particles[i][0] += dX
            particles[i][1] += dY


    # 3. estimate weights of every particle
    maxWeight = 0
    for i in range(len(particles)-1):
        weightSum = 0
        for j in range(len(beacons)-1):
        # // get distance to beacon of both the particle and the robot
            robotDistToBeacon = distance(movedX, movedY, beacons[j][0], beacons[j][1])
            particleDistToBeacon = distance(particles[i][0], particles[i][1], beacons[j][0], beacons[j][1])
            weightSum += getWeight(robotDistToBeacon, particleDistToBeacon,maxDist)
        weight = weightSum / len(beacons)
        particles[i] = degrade(particles[i],weight)
        if (weight > maxWeight):
            maxWeight = weight


    # 4. normalize weights
    weightSum = 0;
    goodParticles = []
    badParticles = []
    for i in range(len(particles)-1):
        particles[i] = normalize(particles[i],maxWeight)
        weightSum += particles[i][2]


    # 5. resample: pick each particle based on probability
    newParticles = []
    numParticles = len(particles)
    for i in range(numParticles-1):
        choice = weightSum
        index = -1
        while(choice > 0):
            index +=1
            choice -= particles[index][2]
        newParticles.append(particles[index])
    particles = newParticles


    movedX = 0
    movedY = 0


    return particles

def main():
    curFrame = 0
    cap = cv2.VideoCapture('ball_bouscing.mp4')
    ret, frame = cap.read()
    newx = len(frame[0])//2
    newy = len(frame)//2
    frame = cv2.resize(frame,(newx,newy))
    particulas = geraParticulas(frame)
    maxDist = int(math.sqrt(newx*newx + newy*newy))
    beacons = []
    beacons.append([20, 20])
    beacons.append([newx/2, 20])
    beacons.append([newx-20, 20])
    beacons.append([20, newy-20])
    beacons.append([newx/2, newy-20])
    beacons.append([newx-20, newy-20])

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
            curFrame += 1
            particulas = filtro_particulas(particulas,center[0],center[1],beacons,maxDist,curFrame)
        else:
        # show the image
            cv2.imshow("Image", frame)



        # cv2.imshow('mask',mask)
        print(particulas)
        imprimeParticulas(frame,particulas)
        cv2.imshow("Image", frame)

        # cv2.imshow('res',res)
        k = cv2.waitKey(200) & 0xFF
        if k == 27:
            break
    # cv2.imshow('Visão',thresh5)




if __name__ == "__main__":
    main()


