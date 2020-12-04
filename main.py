import sys
import os
import re
from BT.Adaptador.Adaptador import *
from BT.src.adaptador import *
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


def main() -> None:
  if sys.platform not in PLATAFORMAS_PERMITIDAS:
    raise RuntimeError("Error,Plataforma no compatible")
  interfaces = ObtenerInterfacesSistema()
  if (len(interfaces)>0):
    MostrarInterfacesBT()
    opcion = input()
    while (int(opcion)>=len(interfaces)):
      os.system('clear')
      print("Opcion no valida, elija una interfaz disponible")
      MostrarInterfacesBT()
      opcion = input()
    sniffear(interfaces[int(opcion)])
  else:
    print("No hay adaptadores conectados al sistema")

if __name__ =="__main__":
  main()