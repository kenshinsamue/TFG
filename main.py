import sys
from subprocess import Popen
import platform
import os
import re
import multiprocessing
import asyncio
from BT.Adaptador.Adaptador import *
from BT.src.dbus_bluez import *
from BT.Sniffer import *
#creamos una lista de plataformas permitidas
PLATAFORMAS_PERMITIDAS = {'linux'}

#metodo que se encarga de obtener una lista con las interfaces disponibles
def ObtenerInterfacesSistema():
  objetos = GetObjectManager()
  llaves = objetos.keys()
  dispositivos=list()
  for path in llaves:
    result = re.match(r'/org/bluez/hci[0-1]*$',path)
    if result:
      dispositivos.append(path.replace("/org/bluez/",""))
  return dispositivos


def MostrarInterfacesBT():
  print("Opcion\tInterfaz")
  print("------------------")
  i=0
  for iface in ObtenerInterfacesSistema():
    print(str(i)+"\t"+iface)

def sniffear(interfaz):
  adaptador1= Adaptador(interfaz)
  mi_sniffer = Sniffer(adaptador1)
  mi_sniffer.run()
  resultado =mi_sniffer.GetDispositivoElegido()
  


def LeerConsola():
  if(sys.argv[1]=='--sniff' or sys.argv[1]=='-s'):
    sniffear(sys.argv[2])

def SetearBT():
  interfaces = ObtenerInterfacesSistema()
  if (len(interfaces)>0):
    MostrarInterfacesBT()
    opcion = input()
    while (int(opcion)>=len(interfaces)):
      os.system('clear')
      print("Opcion no valida, elija una interfaz disponible")
      MostrarInterfacesBT()
      opcion = input()
    os.system('clear')
    print("Mostrando interfaces detectados en la zona: ")
    return interfaces[int(opcion)]
  else:
    print("No hay adaptadores conectados al sistema")

def Menu():
  print("Elija una opcion a realizar: ")
  print("1) Sniffear Dispositivos")
  opcion = input()
  if(1 == int(opcion)):
    os.system('clear')
    iface = SetearBT()
    dispositivo = sniffear(iface)
    
def main() -> None:
  if sys.platform not in PLATAFORMAS_PERMITIDAS:
    raise RuntimeError("Error,Plataforma no compatible")
  if len(sys.argv) == 1:
    Menu()
   
  else:
    LeerConsola()

if __name__ =="__main__":
  main()