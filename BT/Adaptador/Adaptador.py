from BT.src.adaptador import *
import re
class Adaptador(object):
  def __init__(self,identificador):
    try:
      self.id = identificador
      self.ruta= "/org/bluez/"+self.id
      self.adaptador = GetAdaptador(self.ruta)
      self.CrearAtributos(self.adaptador)
    except:
      print("Error al intentar obtener el adaptador")

  def GetAdaptadorBT(self):
    return BUS_DEL_SISTEMA.get(SERVICIO_BLUEZ,self.ruta)[INTERFAZ_DE_ADAPTADOR]
  
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