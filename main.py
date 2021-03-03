import sys
import platform
import os
import re
from metodos import *

#creamos una lista de plataformas permitidas
PLATAFORMAS_PERMITIDAS = {'linux'}

# leemos comandos cortos desde consola
def LeerConsola():
  # ejecutamos el sniffer a travez de un controlador generico bluetooth (scapy)
  if(sys.argv[1]=='--sniff' or sys.argv[1]=='-S'):
    Sniffear(sys.argv[2])
    pass
  # escaneamos los dispositivos en el area (scapy,bluez)
  if(sys.argv[1]=='--scan' or sys.argv[1]=='-s'):
    Escanear(sys.argv[2])


# menu en el cual podemos elegir que hacer
def Menu():
  print("Elija una opcion a realizar: ")
  print("1) Escanear Dispositivos")
  opcion = input()
  if(1 == int(opcion)):
    os.system('clear')
    iface = SetearBT()
    dispositivo = Escanear(iface)
    
# main, punto de inicio    
def main() -> None:
  if sys.platform not in PLATAFORMAS_PERMITIDAS:
    raise RuntimeError("Error,Plataforma no compatible")
  if len(sys.argv) == 1:
    Menu()
   
  else:
    LeerConsola()

if __name__ =="__main__":
  main()