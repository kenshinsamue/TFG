from BT.Adaptador.Adaptador import *
from BT.Adaptador.Dispositivo import *
from gi.repository import GLib
import scapy.all as scapy
from scapy.layers import bluetooth
import os
import signal
import re
import keyboard
class Sniffer(object):
  def __init__(self,adaptador):
    self.registro = list()
    self.adaptador_local= adaptador
    self.interfaz = adaptador.GetAdaptadorBT()
    self.interfaz.SetDiscoveryFilter({"Transport": pydbus.Variant("s","auto")})
    self.interfaz.StartDiscovery()

  def run (self):
    self.adaptador_local.EliminarDispositivos()     # eliminamos los dispositivos registrados previamente
    self.CrearSignals()
    loop = GLib.MainLoop()
    try:
      loop.run()
    except KeyboardInterrupt:
      loop.quit()
    # contador = 0
    self.eleccion = self.ElegirInterfaz()
    # for device in self.registro:
    #   if contador == destino:
    #     resultado = device
    #   contador = contador +1
    # print ("el resultado es : {}".format(resultado))
    # return resultado

  def GetDispositivoElegido(self):
    return self.registro[self.eleccion]

    
  def ElegirInterfaz(self):
    opcion =0
    while opcion<=0 or opcion> len(self.registro):
      self.MostrarDispositivosEncontrados()
      print("Eliga el dispositivo al que quiere connectar")
      opcion = int(input())
    return opcion-1 

  #metodo para gestionar las senales 
  def CrearSignals(self):
    BUS_DEL_SISTEMA.subscribe(
      sender=SERVICIO_BLUEZ,
      iface=CONTROLADOR_DE_OBJETOS,
      signal="InterfacesAdded",
      signal_fired= self.AgregarInterfaz
    )
    BUS_DEL_SISTEMA.subscribe(
      sender=SERVICIO_BLUEZ,
      iface=CONTROLADOR_DE_OBJETOS,
      signal="InterfacesRemoved",
      signal_fired=self.EliminarInterfaz
    )
    BUS_DEL_SISTEMA.subscribe(
      sender = SERVICIO_BLUEZ,
      iface= CONTROLADOR_DE_OBJETOS,
      signal="PropertiesChanged",
      arg0=INTERFAZ_DE_DISPOSITIVO,
      signal_fired = self.CambiarPropiedad
    )

  def CambiarPropiedad(self,sender,obj,iface,signal,params):
    print("{}".format(obj))
    if INTERFAZ_DE_DISPOSITIVO in params:
      device = EncontrarDispositivoPath(obj)
      if device is not None:
        print ("un dispositivo cambio")
  # si se detecta un nuevo dispositivo 
  def AgregarInterfaz(self,sender,obj,iface,signal,params):
    (path,interfaces) = params
    if INTERFAZ_DE_DISPOSITIVO in interfaces:
      self.RegistrarDispositivo(Dispositivo.CrearInstancia(path,interfaces[INTERFAZ_DE_DISPOSITIVO]))
      self.ProbarScapy()

  def ProbarScapy(self):
    bt = scapy.BluetoothHCISocket(0)
    # paquetes =bt.sniff(prn=process_packet)


  def EliminarInterfaz(self,sender,obj,iface,signal,params):
    (path,interfaces) = params
    if INTERFAZ_DE_DISPOSITIVO in interfaces:
      device = self.EncontrarDispositivoPath(path)
      self.registro.remove(device)
    self.MostrarDispositivosEncontrados()

  def EncontrarDispositivoPath(self,path):
    for device in self.registro:
      if device.path==path:
        return device

  #registramos y guardamos el dispositivo
  def RegistrarDispositivo(self,dispositivo):
    remoto = self.EncontrarDispositivo(dispositivo)
    if remoto is None:
      self.registro.append(dispositivo)
    self.MostrarDispositivosEncontrados()

  def EncontrarDispositivo(self,dispositivo):
    for remoto in self.registro:
      if dispositivo == remoto:
        return remoto
    return None

  def MostrarDispositivosEncontrados(self):
    os.system('clear')
    print("BID\t\t BD_ADDR\t    rssi")
    numero =1
    for device in self.registro:
      print("{}) {}".format(numero,device))
      numero = numero+1