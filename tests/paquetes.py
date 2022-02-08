from dataclasses import dataclass
from re import sub
from tokenize import Pointfloat
from unittest import result
from xml.etree.ElementInclude import include
import pyshark
from pyshark.capture.pipe_capture import PipeCapture

FIFO = 'informacion.pcap'
LOG = 'registros.log'

global RegistroLog
global data
data =[]
def leerLog():
  logFinal=[]
  with open(LOG) as log:
    lineas = log.readlines()
    log.close()
    for x in lineas:
      if x[0:8] == "systime=":
        logFinal.append(x)
  return logFinal

def obtener_raw_data (vector_datos):
  datos = ""
  for x in vector_datos[22::]:
    datos+=x
  return datos

def get_cln(registro):
  clkn_index = registro.index("clkn=")
  clk_offset_index = registro.index("clk_offset=")
  clkn_value = registro[(clkn_index+5):(clk_offset_index-1)]
  return clkn_value

def Obtener_registro(registros,ch,err,s,n):
  resultado=[]
  
  ch_index=0
  ch_value=""
  err_index=0
  err_value=""
  s_index=0
  s_value=""
  n_index=0
  n_value="" 
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

def print_callback(pkt):
  sub_data=[]

  ch =0
  err=0
  s=0
  n=0
  vacio = True
  tiempo = pkt.sniff_time
  datos= ""
  datos = obtener_raw_data(pkt.get_packet_raw())
  
  ch = pkt['BTBREDR_RF'].rf_channel
  err = pkt['BTBREDR_RF'].access_address_offenses
  s = pkt['BTBREDR_RF'].signal_power
  n = pkt['BTBREDR_RF'].noise_power

  registro = Obtener_registro(RegistroLog,ch,err,s,n)

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

      sub_data.append(registro)
      sub_data.append(datos)
      data.append(sub_data)
      
RegistroLog = leerLog()

with open(FIFO) as fifo:
  capture = PipeCapture(pipe=fifo,use_json=True,include_raw=True)
  capture.apply_on_packets(print_callback)



