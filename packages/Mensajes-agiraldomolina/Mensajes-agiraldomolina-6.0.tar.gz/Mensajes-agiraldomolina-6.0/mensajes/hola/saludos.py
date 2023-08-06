import numpy as np

def saludar():
    print('Hola, te saludo desde saludos.saludar()')


def prueba():
    print('Esto es una nueva prueba de la nueva versión 6.0')

def generar_array(numeros):
    return np.arange(numeros)

class Saludo:
    def __init__(self):
        print('Hola te saludo desde Saludo.__init__')


# Con este código se evita ejecutar esta parte desde donde es llamado
# solo se corre cuando se ejecuta desde el propio módulo
if __name__ =='__main__':    #__name__ toma el nombre de saludos  y __main__ toma el nombre desde donde es llamado

    print(generar_array(5))