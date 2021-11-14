import pygame
import numpy as np
import time


class Tablero():
    def __init__ (self):
        
        # Atributos definidos por defecto para tablero
        self.width = 0
        self.height = 0
        self.background = (25, 25, 25) # Color de fondo
        
        # Atributos definidos para pintar la ventana
        self.screen = None
        self.display = pygame.display
        self.game = pygame
        
        # Personalizamos la ventana 
        self.display.set_caption("Horton's Game of Life: Mathias Moser y Rafael Camarero")
        
        # Atributo que almacena el estado del juego (La Matriz)
        self.gameState = None
        
        # Atributos de celdas
        self.nxC = 0
        self.nyC = 0
        self.dimCW = 0
        self.dimCH = 0
       
    def open_display(self,width=400,height=400,nxC=60,nyC=60):
        
        #Definimos los parámetros para el display
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
     
    def calculate_neighbours(self, cell):
        # Calcula el número de elementos alrededor sumando las posiciones
        return self.gameState[(cell.x - 1) % self.nxC, (cell.y - 1)  % self.nyC] + \
                self.gameState[(cell.x)     % self.nxC, (cell.y - 1)  % self.nyC] + \
                self.gameState[(cell.x + 1) % self.nxC, (cell.y - 1)  % self.nyC] + \
                self.gameState[(cell.x - 1) % self.nxC, (cell.y)      % self.nyC] + \
                self.gameState[(cell.x + 1) % self.nxC, (cell.y)      % self.nyC] + \
                self.gameState[(cell.x - 1) % self.nxC, (cell.y + 1)  % self.nyC] + \
                self.gameState[(cell.x)     % self.nxC, (cell.y + 1)  % self.nyC] + \
                self.gameState[(cell.x + 1) % self.nxC, (cell.y + 1)  % self.nyC]
    
    
    def colorCell(self,cell):
        # Calculamos el polígono que forma la celda.
        poly = cell.getPolygon()
        
        # Si la celda está "muerta" pintamos un recuadro con borde gris
        if cell.state == 0:
            self.game.draw.polygon(self.screen, (40, 40, 40), poly, 1)
            return
        
        # Si la celda está "viva" pintamos un recuadro relleno de color
        self.game.draw.polygon(self.screen, (255, 200, 100), poly, 0)
        
    def applyRules(self, cell):
        # Calculamos el número de vecinos cercanos.
        num_neighbours = self.calculate_neighbours(cell)
        
        # Recupero las coordenadas
        x,y = cell.axis()
        
        # Regla #1 : Una celda muerta con exactamente 3 vecinas vivas, "revive".
        if self.gameState[x,y] == 0 and num_neighbours == 3:
            return 1
        # Regla #2 : Una celda viva con menos de 2 o 3 vecinas vinas, "muere".
        if self.gameState[x,y] == 1 and (num_neighbours < 2 or num_neighbours > 3):
            return 0 
        
        return None #En el caso que no se aplique reglas dejamos como está
    
    def clear_display(self):
        self.screen.fill(self.background) 

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
        return [((self.x)*self.dimCW, self.y*self.dimCH),((self.x+1)*self.dimCW,self.y*self.dimCH),((self.x+1)*self.dimCW, (self.y+1)*self.dimCH), ((self.x)*self.dimCW, (self.y+1) * self.dimCH)]  

class SecuentialGameOfLife():
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
        pygame.init()
        # Pasamos los parámetros al tablero para abrir
        self.epochs = epochs
        self.tablero.open_display(width=width,height=height,nxC=nxC,nyC=nyC)
        self.counter = 0
        
        while(True):
            
            # Limpiamos la pantalla
            self.tablero.clear_display()
            
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
        ev = self.tablero.game.event.get()
    
        # PARALELIZAR -----------------------------
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

                #En el caso que ta tecla sea CTRL + Z cerramos el juego
                elif event.key == self.tablero.game.K_z:
                    mods = self.tablero.game.key.get_mods()
                    if mods & self.tablero.game.KMOD_CTRL:
                        print("GameOfLife Closed!")
                        self.finish = True
            

    def updateGameState(self):
        
        #Creamos una varible temporal que almacene el estado temporal de juego actual
        tmpGameState = np.copy(self.tablero.gameState)
        # Recogemos los valores de las dimensiones de cada celda
        dimCW, dimHW = self.tablero.dimCW, self.tablero.dimCH 
        # Recorremos las celdas en verticalmente
        #### Paralelizar------------------
        for y in range(0, self.tablero.nxC): 
            # Recorremos las celdas en horizontalemente
            #### Paralizar------------------
            for x in range (0, self.tablero.nyC):
                
                cell = Cell(x,y, tmpGameState[x,y], dimCW, dimHW) #Inicializamos la celda
                #Si el juego no esta en pausa
                if not self.pauseExect:    
                                    
                    ### APLICAMOS LAS REGLAS A UNA CELDA
                    
                    state = self.tablero.applyRules(cell)
                    
                    # Si tenemos que actualizar el estado
                    if (state != None):
                        tmpGameState[x,y] = state
                        cell.state = state # Actualizamos el estado
                
                #Coloreamos la celda en el tablero    
                self.tablero.colorCell(cell)
           
            #### ------------------        
        #### ------------------  
                    
        return np.copy(tmpGameState) #Devolvemos el nuevo estado del juego
  
        
    

