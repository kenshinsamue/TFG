import sys
import platform
import os
import re
from metodos import *
import UbertoothSniff as Ubertooth
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

def ComprobarMac(MAC):
  # MAC: AA:BB:CC:DD:EE:FF
  # 2 5 8 11 14
  comprobado =  False
  repetir = False
  caracteres_permitidos = ["0","1","2","3","4","5","6","7","8","9","A","a","B","b","C","c","D","d","E","e","F","f",":"]
  while comprobado == False:
    repetir = False
    if len(MAC) != 17 :
      print ("la direccion es erronea, recuerde que el formato es el siguiente: \nMAC: AA:BB:CC:DD:EE:FF\n\tPruebe de nuevo")
      repetir = True
    else:
      if not (MAC[2]==":" and MAC[5]==":" and MAC[8]==":" and MAC[11]==":" and MAC[14] ==":") : 
        print ("la direccion es erronea, recuerde que el formato es el siguiente: \nMAC: AA:BB:CC:DD:EE:FF\n\tPruebe de nuevo")
        repetir = True
      else:
        for caracter in MAC:
          if caracter  not in caracteres_permitidos:
            print("la direccion contiene caracteres no validos\nrecuerde que el formato es el siguiente: \nMAC: AA:BB:CC:DD:EE:FF\n\tPruebe de nuevo")  
            repetir = True    
        
    if repetir == False:
        comprobado = True  
    if repetir == True:
      input()
      os.system("clear")
      print("Introduzca la direccion MAC objetivo: ")
      MAC = input()
  
  return MAC
# menu en el cual podemos elegir que hacer
def Menu():
  print("Elija una opcion a realizar: ")
  print("1) Escanear Dispositivos por HCI")
  print("2) Introducir Bluetooth MAC para empezar el SNIFF")
  opcion = input()
  if(1 == int(opcion)):
    os.system('clear')
    iface = SetearBT()
    dispositivo = Escanear(iface)
  if(2 == int(opcion)):
    os.system('clear')
    print("Introduzca la direccion MAC objetivo: ")
    MAC = input()
    MAC = ComprobarMac(MAC)
    os.system("clear")
    print("Estamos analizando el trafico de paquetes, mantengase a la espera")
    datos = Ubertooth.main(MAC)
    DeepLearning(MAC,datos)

#metodo que se encarga de recoger los datos necesarios para ejecutar los procesos de deep learning, transformar los datos de entero/hex a binario y viceversa para ver el resultado
def DeepLearning( MAC, datos):
  # modificar datos en binario

  # cargar el modelo

  # predecir 

  # transformar datos en hex 
  pass
# main, punto de inicio    
def main() -> None:
  if sys.platform not in PLATAFORMAS_PERMITIDAS:
    raise RuntimeError("Error,Plataforma no compatible")
# si ejecutamos sin comandos 
  if len(sys.argv) == 1:
    Menu()
# En el caso de que establezcamos parametros
  else:
    LeerConsola()

if __name__ =="__main__":
  main()