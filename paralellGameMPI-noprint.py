from mpi4py import MPI
import numpy as np
import time
from timeit import default_timer as timer

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

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

def updateGameState():
    global gameState, nxC, tmpGame,comm
    #Creamos una varible temporal que almacene el estado temporal de juego actual
    tmpGame = np.copy(gameState)
    # Recorremos las celdas en verticalmente
    my_rank = comm.Get_rank()
    world_size = comm.Get_size()

    ## Actualizar GameState Global
    if my_rank == 0:
        gameState = comm.bcast(gameState, root=0)
        
    #### Paralelizar------------------
    for y in range(0, nxC): 
        # Recorremos las celdas en horizontal
        #### Paralizar------------------
        tmpGame = vertical(y, tmpGame)     
        #### ------------------        
    #### ------------------ 
    ## Juntamos el tablero en uno y guardamos cuando sea root 0 
    
    # send results to rank 0
    try:
        if my_rank != 0:
            resultsLen = [*range(my_rank,nxC, world_size)]
            comm.Send(tmpGame[resultsLen], dest=0, tag=11)  # send results to process 0
        else:
            resultsLen= [*range(my_rank,nxC, world_size)]
            final_result = np.zeros((nxC,nxC), dtype=int)  # create empty array to receive results
            final_result[resultsLen] = tmpGame[resultsLen]
            for i in range(1, world_size):  # determine the size of the array to be received from each process
                tmpValues = [*range (i,nxC, world_size)]
                comm.Recv(final_result[tmpValues], source=i, tag=11)  # receive results from the process
                
            tmpGame = final_result  
            gameState = tmpGame
            
    except Exception as e:
        print("[WARNING] Fail " % e)

                
def vertical(y, tmpGame):
    global nxC, nyC, pauseExect,gameState, screen, comm
    # Dividimos en rangos
    my_rank = comm.Get_rank()
    world_size = comm.Get_size()
    for x in range (my_rank, nyC, world_size):
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
            # Envio el valor actualizado de TMPGAME A TODOS
            #paint(poly,tmpGame[x,y])
                 
    return tmpGame    


if __name__ == '__main__':
    
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    # Parámetros del Tablero:
    
    #Tamaño de la ventana del tablero 
    width = 800
    height = 800
    
    #Número de celdas en el eje X
    nxC = 50
    #Número de celdas en el eje Y
    nyC = 50

    epochs = 100
    
    if rank == 0:
        start = timer()

    # Empezamos el juego
    startGame(w=width, h=height, nx=nxC, ny=nyC, epoch=epochs)
    
    if rank == 0:
        end = timer()
        finalTime = end-start
        print("Tiempo Paralelo: [{0}]".format(finalTime))
        