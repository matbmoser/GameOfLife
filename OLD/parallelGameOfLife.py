
# to measure exec time
from numba import njit, prange, set_num_threads, jit,int32, float32, boolean   # import the types
from numba.experimental import jitclass
from numba.np.ufunc import parallel
import pygame
import numpy as np
import time
        

background = (25, 25, 25) # Color de fondo
screen = None
gameState = None

def clear_display():
    global screen
    global background
    screen.fill(background) 
    
spec1 = [
    ('width',int32),
    ('height',int32),    
    ('nxC',int32),   # a simple scalar field
    ('nyC',int32),   
    ('dimCW',int32),   
    ('dimCH', int32)
]
@jitclass(spec1)
class Tablero():
    def __init__ (self):
        
        # Atributos definidos por defecto para tablero
        self.width = 0
        self.height = 0

        # Personalizamos la ventana 
        pygame.display.set_caption("Horton's Game of Life: Mathias Moser y Rafael Camarero")
        
        
        # Atributos de celdas
        self.nxC = 0
        self.nyC = 0
        self.dimCW = 0
        self.dimCH = 0
       
    def open_display(self,width=400,height=400,nxC=60,nyC=60):
        global background
        global screen
        global gameState
        #Definimos los parámetros para el display
        self.width = width
        self.height = height
        screen = pygame.display.set_mode((height, width))
        screen.fill(background)
        
        
        #Numero de Celdas en cada eje
        self.nxC, self.nyC = nxC, nyC
        
        # Estado de las celdas. Viva = 1 / Muerta = 0 Generamos un tablero aleatório
        gameState = self.generate_random_board()
        
        #Dimención de cada celda
        self.dimCW = self.width / self.nxC
        self.dimCH = self.height / self.nyC

    
    # Genera un tablero aleatório de unos y ceros    
    def generate_random_board(self):
        return np.random.randint(2, size=(self.nxC, self.nyC))
     
    def calculate_neighbours(self, x, y):
        global gameState
        # Calcula el número de elementos alrededor sumando las posiciones
        return gameState[(x - 1) % self.nxC, (x - 1)  % self.nyC] + \
                gameState[(x)     % self.nxC, (x - 1)  % self.nyC] + \
                gameState[(x + 1) % self.nxC, (x - 1)  % self.nyC] + \
                gameState[(x - 1) % self.nxC, (x)      % self.nyC] + \
                gameState[(x + 1) % self.nxC, (x)      % self.nyC] + \
                gameState[(x - 1) % self.nxC, (x + 1)  % self.nyC] + \
                gameState[(x)     % self.nxC, (x + 1)  % self.nyC] + \
                gameState[(x + 1) % self.nxC, (x + 1)  % self.nyC]
    
    def getPolygon(self,x,y):
        # Calculamos el polígono que forma la celda.
        return [((x)*self.dimCW, y*self.dimCH),((x+1)*self.dimCW,y*self.dimCH),((x+1)*self.dimCW, (y+1)*self.dimCH), ((x)*self.dimCW, (y+1) * self.dimCH)]  
    
    def colorCell(self,x,y,state):
        global screen
        # Calculamos el polígono que forma la celda.
        poly = self.getPolygon(x,y)
        
        # Si la celda está "muerta" pintamos un recuadro con borde gris
        if state == 0:
            pygame.draw.polygon(screen, (40, 40, 40), poly, 1)
            return
        
        # Si la celda está "viva" pintamos un recuadro relleno de color
        pygame.draw.polygon(screen, (255, 200, 100), poly, 0)
    

    def applyRules(self, x,y, state):
        global gameState
        # Calculamos el número de vecinos cercanos.
        num_neighbours = self.calculate_neighbours(x,y,state)
        
        
        # Regla #1 : Una celda muerta con exactamente 3 vecinas vivas, "revive".
        if gameState[x,y] == 0 and num_neighbours == 3:
            return 1
        # Regla #2 : Una celda viva con menos de 2 o 3 vecinas vinas, "muere".
        if gameState[x,y] == 1 and (num_neighbours < 2 or num_neighbours > 3):
            return 0 
        
        return None #En el caso que no se aplique reglas dejamos como está
    


class Cell():
    def __init__(self, x, y, state, dimCW, dimCH):
        # Atributos de una celda
        self.x = x
        self.y = y
        self.state = state #Viva o Muerta
        self.dimCW = dimCW
        self.dimCH = dimCH
    
    # Devuelve el eje
    def axis(self):
        return self.x, self.y
    
    def getPolygon(self):
        # Calculamos el polígono que forma la celda.
        return [((self.x)*self.dimCW, self.y*self.dimCH),((self.x+1)*self.dimCW,self.y*self.dimCH),((self.x+1)*self.dimCW, (y+1)*self.dimCH), ((self.x)*self.dimCW, (self.y+1) * self.dimCH)]  


spec = [
    ('tablero', Tablero.class_type.instance_type),               # a simple scalar field
    ('pauseExect', boolean),
    ('finish',boolean),
    ('epochs',int32),
    ('counter',int32)# an array field
]

@jitclass(spec)
class ParalellGameOfLife():
    def __init__ (self):
        #Almacena los datos del tablero
        self.tablero = Tablero() 
        #Indica si el juego esta pausado
        self.pauseExect = False
        #Indica cuando el juego debe cerrarse
        self.finish = False
        
        self.epochs = 0
        self.counter = 0

    def start(self, width, height, nxC, nyC, epochs=0):
        
        # Pasamos los parámetros al tablero para abrir
        self.epochs = epochs
        self.tablero.open_display(width=width,height=height,nxC=nxC,nyC=nyC)
        self.counter = 0
        
        while(True):
            
            # Limpiamos la pantalla
            clear_display()
            
            self.checkStatus()
            
            #Si precionamos el botón de cerrar o CTRL-Z
            if(self.finish):
                break
            
            self.tablero.gameState = self.updateGameState()
            
            # Mostramos el resultado
            self.tablero.display.flip()   

    def checkStatus(self):
        
        if self.counter >= self.epochs:
            self.finish = True
            return
            
        self.counter+=1
        # Registramos eventos de teclado y ratón.
        ev = pygame.event.get()
    
        # PARALELIZAR -----------------------------
        for event in ev:
            
            #Si damos a cerrar se cierra el tablero
            if event.type == pygame.QUIT:
                print("GameOfLife Closed!")
                self.finish = True
                return
            
            # Detectamos si se presiona una tecla.
            if event.type == pygame.KEYDOWN:
                
                #En el caso de que la tecla sea escape o ESC pausamos el juego
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    self.pauseExect = not self.pauseExect

                #En el caso que ta tecla sea CTRL + Z cerramos el juego
                elif event.key == pygame.K_z:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        print("GameOfLife Closed!")
                        self.finish = True
            

    def updateGameState(self):
        global gameState
        #Creamos una varible temporal que almacene el estado temporal de juego actual
        tmpGameState = np.copy(gameState)

        # Recorremos las celdas en verticalmente
        #### Paralelizar------------------
        for y in range(0, self.tablero.nxC): 
            # Recorremos las celdas en horizontalemente
            #### Paralizar------------------
                tmpGameState = self.vertical(y,tmpGameState)
            #### ------------------        
        #### ------------------  
                    
        return np.copy(tmpGameState) #Devolvemos el nuevo estado del juego
    
    @jit(parallel=True)
    def vertical(self, y, tmpGameState):

        for x in prange (0, self.tablero.nyC):
                    
                #Si el juego no esta en pausa
                if not self.pauseExect:    
                                    
                    ### APLICAMOS LAS REGLAS A UNA CELDA
                    
                    state = self.tablero.applyRules(x,y, tmpGameState[x,y])
                    
                    # Si tenemos que actualizar el estado
                    if (state != None):
                        tmpGameState[x,y] = state
                        
                
                #Coloreamos la celda en el tablero    
                self.tablero.colorCell(x, y, tmpGameState[x,y])
        return tmpGameState
  


