from concurrent.futures import thread
from unittest import result
# Thread 1:
  # 1. ejecutar ubertooth con exito 
  # 2. Guardar los paquetes dentro de un fichero 
  # 3.  
# Trhead 2: 
  # 1. Esperar la escritura dentro del fichero y 
  #     cuando este sea modificado extraer la informacion obtenida
  # 2. Procesar la informacion

# Librerias
import threading
import os
import signal
import sys

from dbus import Interface 
import pyshark

# Apartado de valores constantes 
# Establecemos el nombre del fichero creado
FIFO = '/tmp/pipe'
COMANDO = 'ubertooth-rx -q'
LAP = 'df039f'
UAP = '49'

def ejecutarComando():
  global terminal 
  terminal = os.popen("{} {} -l {} -u {}".format(COMANDO,FIFO,LAP,UAP))

def limpiar(sig, frame):
  terminar()

def terminar ():
  terminal.close()
  os.remove(FIFO)

def interpretar():
  print("entramos")

  with open(FIFO) as fifo:
    while True:
      print ("{}".format(fifo.readline()))

  # try: 
  #   cap = pyshark.LiveRingCapture(interface=FIFO)
  #   cap.sniff(timeout=100)
  
  # except:
  #   print (" Error")
  #   terminar()
  #   exit(0)
  pass


def main () :
  # Primero creamos la tuberia, que se encargara de enviar la informacion
  try:
    os.mkfifo(FIFO)
  except:
    print("el fichero {} ya existe, vamos a intentarlo de nuevo".format(FIFO))
    try:
      os.remove(FIFO) 
      os.mkfifo(FIFO)
    except:
      print("Ha habido un error al crear el fichero /tmp/pipe, no se ha podido solucionar internamente")
      exit(0)
  global lector
  global interprete
  # empezamos el trheat que inicia ubertooth
  lector = threading.Thread(target=ejecutarComando)
  lector.start()
  # empezamos thread que usa pyshark
  interprete = threading.Thread(target=interpretar)
  interprete.start()
  signal.signal(signal.SIGINT,limpiar)
  print(" pulse ctrl + c para seguir la ejecucion")
  signal.pause()

if __name__ == "__main__":
  main()