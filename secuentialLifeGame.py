import pygame
import numpy as np
import time


class Tablero():
    def __init__ (self):
        #Valores definidos por defecto
        self.width = 400
        self.height = 400
        self.background = (25, 25, 25) # Color de fondo
        self.screen = None
        self.gameState = None
        self.display = pygame.display
        self.game = pygame
        self.nxC = 120
        self.nyC = 120
        self.dimCW = 400/60
        self.dimCH = 400/60
    
        
    def open_display(self,width=400,height=400,nxC=60,nyC=60):
        
        self.width = width
        self.height = height
        self.screen = self.display.set_mode((height, width))
        self.screen.fill(self.background)
        
        #Numero de Celdas en cada eje
        self.nxC, self.nyC = nxC, nyC
        
        # Estado de las celdas. Viva = 1 / Muerta = 0 Generamos un tablero aleatório
        self.gameState = self.generate_random_board()

        #Dimención de cada celda
        self.dimCW = self.width / self.nxC
        self.dimCH = self.height / self.nyC
    
    # Genera un tablero aleatório de unos y ceros    
    def generate_random_board(self):
        return np.random.randint(2, size=(self.nxC, self.nyC))
     
    def calculate_neighbours(self, x, y):
        # Calcula el número de elementos alrededor sumando las posiciones
        return self.gameState[(x - 1) % self.nxC, (y - 1)  % self.nyC] + \
                self.gameState[(x)     % self.nxC, (y - 1)  % self.nyC] + \
                self.gameState[(x + 1) % self.nxC, (y - 1)  % self.nyC] + \
                self.gameState[(x - 1) % self.nxC, (y)      % self.nyC] + \
                self.gameState[(x + 1) % self.nxC, (y)      % self.nyC] + \
                self.gameState[(x - 1) % self.nxC, (y + 1)  % self.nyC] + \
                self.gameState[(x)     % self.nxC, (y + 1)  % self.nyC] + \
                self.gameState[(x + 1) % self.nxC, (y + 1)  % self.nyC]
    
    def getPolygon(self,x,y):
        # Calculamos el polígono que forma la celda.
        return [((x)*self.dimCW, y*self.dimCH),((x+1)*self.dimCW,y*self.dimCH),((x+1)*self.dimCW, (y+1)*self.dimCH), ((x)*self.dimCW, (y+1) * self.dimCH)]
    
    def colorCell(self,x,y, state):
        # Calculamos el polígono que forma la celda.
        poly = self.getPolygon(x,y)
        
        # Si la celda está "muerta" pintamos un recuadro con borde gris
        if state == 0:
            self.game.draw.polygon(self.screen, (40, 40, 40), poly, 1)
            return
        
        # Si la celda está "viva" pintamos un recuadro relleno de color
        self.game.draw.polygon(self.screen, (255, 200, 100), poly, 0)
        
    def applyRules(self, x, y):
        # Calculamos el número de vecinos cercanos.
        num_neighbours = self.calculate_neighbours(x, y)
        
        # Regla #1 : Una celda muerta con exactamente 3 vecinas vivas, "revive".
        if self.gameState[x, y] == 0 and num_neighbours == 3:
            return 1
        # Regla #2 : Una celda viva con menos de 2 o 3 vecinas vinas, "muere".
        if self.gameState[x, y] == 1 and (num_neighbours < 2 or num_neighbours > 3):
            return 0 
        
        return None

class GameOfLife():
    def __init__ (self):
        #Almacena los datos del tablero
        self.tablero = Tablero() 
        #Indica si el juego esta pausado
        self.pauseExect = False
        self.finish = False
    
    def start(self, width, height, nxC, nyC):
        
        self.tablero.open_display(width=width,height=height,nxC=nxC,nyC=nyC)
        
        while(True):
            # Copiamos la matriz del estado anterior
            # #para representar la matriz en el nuevo estado
            # Ralentizamos la ejecución a 0.1 segundos
            time.sleep(0.1)
            # Limpiamos la pantalla
            self.tablero.screen.fill(self.tablero.background) 
            
            self.checkStatus()
            
            if(self.finish):
                break
            
            self.tablero.gameState = self.actualizateGameState()
            
            # Mostramos el resultado
            self.tablero.display.flip()   

    def checkStatus(self):
        # Registramos eventos de teclado y ratón.
        ev = self.tablero.game.event.get()
       
        for event in ev:
            
            #Si damos a cerrar se cierra el tablero
            if event.type == self.tablero.game.QUIT:
                print("GameOfLife Closed!")
                self.finish = True
                return
            
            # Detectamos si se presiona una tecla.
            if event.type == self.tablero.game.KEYDOWN:
                
                #En el caso de que la tecla sea escape o ESC pausamos el juego
                if event.key == self.tablero.game.K_ESCAPE or event.key == self.tablero.game.K_SPACE:
                    self.pauseExect = not self.pauseExect

                #En el caso que ta tecla sea CTL + Z cerramos el juego
                elif event.key == self.tablero.game.K_z:
                    mods = self.tablero.game.key.get_mods()
                    if mods & self.tablero.game.KMOD_CTRL:
                        print("GameOfLife Closed!")
                        self.finish = True
            

    def actualizateGameState(self):
        
         #Creamos una varible temporal que almacene el estado temporal de juego actual
        tmpGameState = np.copy(self.tablero.gameState)
        
        # Recorremos las celdas en verticalmente
        #### Paralelizar------------------
        for y in range(0, self.tablero.nxC): 
            # Recorremos las celdas en horizontalemente
            #### Paralizar------------------
            for x in range (0, self.tablero.nyC):
                
                #Si el juego no esta en pausa
                if not self.pauseExect:    
                                    
                    ### APLICAMOS LAS REGLAS
                    
                    state = self.tablero.applyRules(x,y)
                    if (state != None):
                        tmpGameState[x,y] = state
                
                #Coloreamos la celda    
                self.tablero.colorCell(x, y, tmpGameState[x,y])
           
            #### ------------------        
        #### ------------------  
                    
        return np.copy(tmpGameState)

class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = None
        
    

if __name__ == '__main__':
    
    juego = GameOfLife()
    
    # Parámetros del Tablero:
    
    #Tamaño de la ventana del tablero 
    width = 800
    height = 800
    
    #Número de celdas en el eje X
    nxC = 100
    #Número de celdas en el eje Y
    nyC = 100
    
    #Empezamos el juego
    juego.start(width=width, height=height, nxC=nxC, nyC=nyC)
    


