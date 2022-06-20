
# Librerias
import os
from dbus import Interface
from numpy import interp 
import pyshark
from pyshark.capture.pipe_capture import PipeCapture
# 50:8e:49:df:03:9f

# Apartado de valores constantes 
# Establecemos el nombre del fichero creado
FILE_PCAP = 'Sniffing/informacion.pcap'
SCRIPT = "Sniffing/iniciar.sh"
LOG = 'Sniffing/registros.log'


def main (MAC) :
  valores = parsearMAC(MAC)
  #  Iniciamos la ejecucion por parte de ubertooth para capturar los paquetes y los logs de los mismos
  ejecutarComando(valores)
  #  creamos variables globales para guardar informacion
  global RegistroLog
  global Data
  Data = []
  RegistroLog = leerLog()
  # Abrimos el fichero .pcap que es el que contiene la informacion relativa a los paquetes capturados
  with open(FILE_PCAP) as pcap:
    capture = PipeCapture(pipe=pcap,use_json=True,include_raw=True)
    capture.apply_on_packets(registro_callback)
  # print(Data)
  return Data


# Metodo que obtiene una direccion mac en su formato hexadecimal y lo pone sin puntos y en minuscula 
def parsearMAC(MAC):
  MAC = MAC.replace(":","")
  MAC= MAC.lower()
  # 508e49df039f
  valores = [MAC[4:6],MAC[6::]]
  return valores

# Metodo que ejecuta el script de ubertooth
def ejecutarComando(valores): 
  os.system('bash {} -u {} -l {} -f {} -t {} -r {}'.format(SCRIPT,valores[0],valores[1],FILE_PCAP,60,LOG))

# metodo que se encarga de leer todos los mensajes de ubertooth y filtrar solo los que empiezen por "systime="
def leerLog():
  logFinal=[]
  with open(LOG) as log:
    lineas = log.readlines()
    log.close()
    for x in lineas:
      if x[0:8] == "systime=":
        logFinal.append(x)
  return logFinal

# Metodo que se encargar de realizar las siguientes operaciones al encontrar un paquete dentro de fichero pcap:
  # 1. obtener el canal de comunicacion,access address offences, signal power y noise power
  # 2. Obtener el campo de datos encriptados que es a partir del 11 avo byte
  # 3. obtener el registro proporcionado por ubertooth que corresponda al paquete en funcion de lo obtenido en (1)
  # 4. analizamos si el paquete tiene datos, en caso de tenerlos detectar si esta corrupto o no 
  # 4. De (4) nos quedamos con los paquetes que estan integros y tienen datos y los guardamos en un array que contendra los registros relacionados al paquete en conjunto con los datos encriptados
def registro_callback(pkt):
  sub_data=[] 
  ch =0
  err=0
  s=0
  n=0
  vacio = True
  datos= ""
  # guarda el paquete entero en formato raw (hex)
  datos = obtener_raw_data(pkt.get_packet_raw())

  ch = pkt['BTBREDR_RF'].rf_channel
  err = pkt['BTBREDR_RF'].access_address_offenses
  s = pkt['BTBREDR_RF'].signal_power
  n = pkt['BTBREDR_RF'].noise_power

  registro = Obtener_registro(RegistroLog,ch,err,s,n)
  clkn = get_clkn(registro)
  if datos == "":
    pass
  else:
    for x in datos:
      if x != '0':
        vacio = False
        break
    if vacio == True:
      pass
    else:
      sub_data.append(clkn)
      sub_data.append(datos)
      Data.append(sub_data)

#  Metodo que se encarga de obtener los datos encriptados del paquete
def obtener_raw_data (vector_datos):
  datos = ""
  for x in vector_datos[22::]:
    datos+=x
  return datos

# Metodo que busca el registro que tiene valores comunes con los registrados dentro del paquete
def Obtener_registro(registros,ch,err,s,n):
  resultado=[]

  for x in registros:
    ch_index = x.index("ch=")
    err_index = x.index("err=")
    s_index = x.index("s=")
    n_index = x.index(" n=")
    
    ch_value = x[(ch_index+3):ch_index+5]
    err_value = x[(err_index+4):(err_index+5)]
    s_value = x[(s_index+2):(s_index+5)]
    n_value = x[(n_index+3):(n_index+6)]

    if ch_value[0]==" ":
      ch_value = ch_value[1]

    if (ch == ch_value and err == err_value and s == s_value and n == n_value):
      resultado.append(x)

    else:
      pass

  return resultado

# Metodo que se encarga de buscar el valor del registro del reloj del adaptador maestro de la comunicacion
def get_clkn(registro):
  registro_nuevo=[]
  for x in registro:  
    clkn_index = x.index("clkn=")
    clk_offset_index = x.index("clk_offset=")
    valor = x[(clkn_index+5):(clk_offset_index-1)]
    registro_nuevo.append(valor)
  return registro_nuevo


if __name__ == "__main__":
  main()