import random
import decimal

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

numero_de_Particulas = 10
velocidadeInicialX = 20
velocidadeInicialY = 20
numero_de_frames = 30

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

def correcao():
    
#main
def main():
    particulas_antigas = []
    particulas_antigas = geraParticulas()
    particulas_atuais = geraParticulas()
    particulas_antigas = updateParticulasCM([6,3],particulas_antigas)
    particulas_antigas = velocidades(particulas_antigas)


    for i in range(numero_de_frames):

main()