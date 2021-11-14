
# to measure exec time
from numba import njit, prange, set_num_threads, jit,int32, float32, boolean   # import the types
from numba.experimental import jitclass
from numba.np.ufunc import parallel
import pygame
import numpy as np
from pygame import draw
import time
from numba import set_num_threads
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



def clear_display():
    global screen,background
    screen.fill(background) 
      

def open_display(w=400,h=400,nx=60,ny=60):
    
    global background,gameState,screen
    global width,height,dimCW,dimCH
    #Definimos los parámetros para el display
    width = w
    height = h
    #screen = pygame.display.set_mode((height, width))
    #screen.fill(background)
    
    # Personalizamos la ventana 
    #pygame.display.set_caption("Horton's Game of Life: Mathias Moser y Rafael Camarero")
    
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

def getPolygon(x,y):
    global dimCH, dimCW
    # Calculamos el polígono que forma la celda.
    return [((x)*dimCW, y*dimCH),((x+1)*dimCW,y*dimCH),((x+1)*dimCW, (y+1)*dimCH), ((x)*dimCW, (y+1) * dimCH)]   


def startGame(w, h, nx, ny, epoch=0):
    #pygame.init()
    global gameState, epochs, counter
    # Pasamos los parámetros al tablero para abrir
    epochs = epoch
    open_display(w=w,h=h,nx=nx,ny=ny)
    counter = 0
    
    while(True):
        
        
        # Limpiamos la pantalla
        #clear_display()
        
        checkStatus()
        
        #Si precionamos el botón de cerrar o CTRL-Z
        if(finish):
            break
        
        updateGameState()

        # Mostramos el resultado
        #pygame.display.flip()  
         
def checkStatus():
    global finish, pauseExect, counter, epochs
    if counter >= epochs:
        finish = True
        return
        
    counter+=1
    # Registramos eventos de teclado y ratón.
    """
    ev = pygame.event.get()

    # PARALELIZAR -----------------------------
    for event in ev:
        
        #Si damos a cerrar se cierra el tablero
        if event.type == pygame.QUIT:
            print("GameOfLife Closed!")
            finish = True
            return
        
        # Detectamos si se presiona una tecla.
        if event.type == pygame.KEYDOWN:
            
            #En el caso de que la tecla sea escape o ESC pausamos el juego
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                pauseExect = not pauseExect

            #En el caso que ta tecla sea CTRL + Z cerramos el juego
            elif event.key == pygame.K_z:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    print("GameOfLife Closed!")
                    finish = True
        """

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
            #poly = getPolygon(x,y)
            
            #paint(poly,tmpGame[x,y])
                
    return tmpGame    

def paint(poly, state):
    global screen
        # Si la celda está "muerta" pintamos un recuadro con borde gris
    if state == 0:
        #pygame.draw.polygon(screen, (40, 40, 40), poly, 1)
        return
    
    # Si la celda está "viva" pintamos un recuadro relleno de color
    #pygame.draw.polygon(screen, (255, 200, 100), poly, 0)  



if __name__ == '__main__':

    # Parámetros del Tablero:
    
    #Tamaño de la ventana del tablero 
    width = 800
    height = 800
    
    #Número de celdas en el eje X
    nxC = 100
    #Número de celdas en el eje Y
    nyC = 100

    epochs = 25
    

    #Empezamos el juego Paralelo
    start = timer()
    startGame(w=width, h=height, nx=nxC, ny=nyC, epoch=epochs)
    end = timer()
    print("Tiempo Secuencial: [{0}]".format(end-start))
    

