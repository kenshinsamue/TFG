from BT.Adaptador.Adaptador import *
from BT.Adaptador.Dispositivo import *
from gi.repository import GLib
import scapy.all as scapy
from scapy.layers import bluetooth
import os
import signal
import re
import keyboard

# Clase de escaner mediante la libreria bluez y pydbus
class Escaner(object):
  # Constructor del objeto, le especificamos que queremos que realize una busqueda para ambos protocolos tanto bd/edr como LE
  def __init__(self,adaptador):
    self.registro = list()
    self.adaptador_local= adaptador
    self.interfaz = adaptador.GetAdaptadorBT()
    self.interfaz.SetDiscoveryFilter({"Transport": pydbus.Variant("s","auto")})
    self.interfaz.StartDiscovery()

  def run (self,retornar=False):
    self.adaptador_local.EliminarDispositivos()     # eliminamos los dispositivos registrados previamente
    self.CrearSignals()
    loop = GLib.MainLoop()
    try:
      loop.run()
    except KeyboardInterrupt:
      loop.quit()
    if(retornar == True):
      self.eleccion = self.ElegirInterfaz()


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

  def AgregarInterfaz(self,sender,obj,iface,signal,params):
    (path,interfaces) = params
    if INTERFAZ_DE_DISPOSITIVO in interfaces:
      self.RegistrarDispositivo(Dispositivo.CrearInstancia(path,interfaces[INTERFAZ_DE_DISPOSITIVO]))
      


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