from parallelGameOfLife import ParalellGameOfLife
from secuentialGameOfLife import SecuentialGameOfLife
import time
from numba import set_num_threads
from timeit import default_timer as timer


if __name__ == '__main__':
    
    num_threads = input(f'Enter max number of cores to use: ')

    set_num_threads(int(num_threads))   
    
    # Parámetros del Tablero:
    
    #Tamaño de la ventana del tablero 
    width = 800
    height = 800
    
    #Número de celdas en el eje X
    nxC = 100
    #Número de celdas en el eje Y
    nyC = 100

    epochs = 20
    
    #Empezamos el juego Paralelo
    juego = SecuentialGameOfLife()
    start = timer()
    juego.start(width=width, height=height, nxC=nxC, nyC=nyC, epochs=epochs)
    end = timer()
    print("Tiempo Secuencial: [{0}]".format(end-start))
    
    #Empezamos el juego Paralelo
    juego = ParalellGameOfLife()
    start = timer()
    juego.start(width=width, height=height, nxC=nxC, nyC=nyC, epochs=epochs)
    end = timer()
    print("Tiempo Paralelo: [{0}]".format(end-start))
    
