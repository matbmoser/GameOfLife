
# to measure exec time
import numpy as np
from timeit import default_timer as timer


## Global Shared Atributes
background = (25, 25, 25) # Color de fondo
screen = None
gameState = None
tmpGame = None
finish = False
#Indica si el juego esta pausado
pauseExect = False
epochs = 0
counter = 0
# Atributos definidos por defecto para tablero
width = 0
height = 0
# Atributos de celdas
nxC = 0
nyC = 0
dimCW = 0
dimCH = 0


def open_display(w=400,h=400,nx=60,ny=60):
    
    global background,gameState,screen
    global width,height,dimCW,dimCH
    #Definimos los parámetros para el display
    width = w
    height = h
    
    #Numero de Celdas en cada eje
    nxC, nyC = nx, ny
    
    # Estado de las celdas. Viva = 1 / Muerta = 0 Generamos un tablero aleatório
    gameState = generate_random_board()
    
    #Dimención de cada celda
    dimCW = width / nxC
    dimCH = height / nyC


# Genera un tablero aleatório de unos y ceros    
def generate_random_board():
    global nxC, nyC
    return np.random.randint(2, size=(nxC, nyC))

def calculate_neighbours(x, y):
    global gameState,nxC, nyC
    # Calcula el número de elementos alrededor sumando las posiciones
    return gameState[(x - 1) % nxC, (y - 1)  % nyC] + \
            gameState[(x)     % nxC, (y - 1)  % nyC] + \
            gameState[(x + 1) % nxC, (y - 1)  % nyC] + \
            gameState[(x - 1) % nxC, (y)      % nyC] + \
            gameState[(x + 1) % nxC, (y)      % nyC] + \
            gameState[(x - 1) % nxC, (y + 1)  % nyC] + \
            gameState[(x)     % nxC, (y + 1)  % nyC] + \
            gameState[(x + 1) % nxC, (y + 1)  % nyC]


def startGame(w, h, nx, ny, epoch=0):
    #pygame.init()
    global gameState, epochs, counter
    # Pasamos los parámetros al tablero para abrir
    epochs = epoch
    open_display(w=w,h=h,nx=nx,ny=ny)
    counter = 0
    
    while(True):
        
        
        checkStatus()
        
        #Si precionamos el botón de cerrar o CTRL-Z
        if(finish):
            break
        
        updateGameState()

         
def checkStatus():
    global finish, pauseExect, counter, epochs
    if counter >= epochs:
        finish = True
        return
        
    counter+=1

def updateGameState():
    global gameState, nxC, tmpGame
    #Creamos una varible temporal que almacene el estado temporal de juego actual
    tmpGame = np.copy(gameState)

    # Recorremos las celdas en verticalmente
    #### Paralelizar------------------
    for y in range(0, nxC): 
        # Recorremos las celdas en horizontalemente
        #### Paralizar------------------
        tmpGame = vertical(y, tmpGame)
        #### ------------------        
    #### ------------------  
    
    gameState = tmpGame
                

def vertical(y, tmpGame):
    global nyC, pauseExect,gameState, screen
    for x in range (0, nyC):
                
            #Si el juego no esta en pausa
            if not pauseExect:    
                                
                ### APLICAMOS LAS REGLAS A UNA CELDA
                
                # Calculamos el número de vecinos cercanos.
                num_neighbours = calculate_neighbours(x,y)
                
                
                # Regla #1 : Una celda muerta con exactamente 3 vecinas vivas, "revive".
                if gameState[x,y] == 0 and num_neighbours == 3:
                    tmpGame[x,y] =  1
                # Regla #2 : Una celda viva con menos de 2 o 3 vecinas vinas, "muere".
                if gameState[x,y] == 1 and (num_neighbours < 2 or num_neighbours > 3):
                    tmpGame[x,y] = 0 

            # Calculamos el polígono que forma la celda.
                
    return tmpGame    

if __name__ == '__main__':

    # Parámetros del Tablero:
    
    #Tamaño de la ventana del tablero 
    width = 800
    height = 800
    
    #Número de celdas en el eje X
    nxC = 100
    #Número de celdas en el eje Y
    nyC = 100

    epochs = 250
    

    #Empezamos el juego Secuencial
    start = timer()
    startGame(w=width, h=height, nx=nxC, ny=nyC, epoch=epochs)
    end = timer()
    print("Tiempo Secuencial: [{0}]".format(end-start))
    

