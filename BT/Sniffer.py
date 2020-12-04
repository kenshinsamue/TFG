from BT.Adaptador.Adaptador import *
from BT.Adaptador.Dispositivo import *
from gi.repository import GLib
import os
import re
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
    loop.run()


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
    print("BID\t\t BD_ADDR\t\t   rssi")
    for device in self.registro:
      print("{}".format(device))