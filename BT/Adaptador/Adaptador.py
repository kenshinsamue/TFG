from BT.src.dbus_bluez import *
import re
from gi.repository import GLib

# Clase del adaptador local 
class Adaptador(object):
  # Constructor, inicializa multiples atributos del controlador:
  ## El identificador { hci0, hci1 ...}
  ## La ruta dentro del bus del servicio bluez { /org/bluez/hci0 }
  ## El adaptador interno del controlador dentro del sistema
  def __init__(self,identificador):
    try:
      self.id = identificador
      self.ruta= "/org/bluez/"+self.id
      self.adaptador = GetAdaptador(self.ruta)
      self.CrearAtributos(self.adaptador)
    except:
      print("Error al intentar obtener el adaptador")
  
  ## Getters 
  def getid(self):
    return self.id
  
  def GetAdaptadorBT(self):
    return BUS_DEL_SISTEMA.get(SERVICIO_BLUEZ,self.ruta)[INTERFAZ_DE_ADAPTADOR]
  
  def SetAdaptadorPropiedad(self,propiedad,valor):
    propiedad_bus = BUS_DEL_SISTEMA.get(SERVICIO_BLUEZ,self.ruta)[PROPERTIES_INTERFACE]
    variant = GLib.Variant('b',valor)
    # print("{}".format(propiedad_bus.Get(INTERFAZ_DE_ADAPTADOR,propiedad)))
    propiedad_bus.Set(INTERFAZ_DE_ADAPTADOR,propiedad,variant)
    # print("{}".format(propiedad_bus.Get(INTERFAZ_DE_ADAPTADOR,propiedad)))  

  ## Metodo que permite eliminar la "cache" de los dispositivos previamente encontrados 
  def EliminarDispositivos(self):
    prueba = GetObjectManager()
    interfaz = self.GetAdaptadorBT()
    for path in prueba:
      result = re.match(r'/org/bluez/hci[0-1]*/',path)
      if result:
        interfaz.RemoveDevice(path)


  def CrearAtributos(self,adaptador_link):
    self.address = adaptador_link['Address']
    self.nombre = adaptador_link['Name']
    self.reconocible = adaptador_link['Discoverable']
    self.tiempo_reconocible = adaptador_link['DiscoverableTimeout']
    self.servicios = adaptador_link['UUIDs']
    
  #metodo que devuelve una descripcion del objeto en formato string
  def __str__(self)-> str:
    return("Dispositivo: {}, Address: {}, Nombre: {}, Discoverable: {} por {}s"
    .format(self.id,self.address,self.nombre,self.reconocible,self.tiempo_reconocible))