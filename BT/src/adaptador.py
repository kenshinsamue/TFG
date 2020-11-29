
import pydbus
from typing import *
BUS_DEL_SISTEMA = pydbus.SystemBus() # obtenemos el bus del sistema
SERVICIO_BLUEZ = "org.bluez"      ## el servicio sobre el que se basara la aplicacion sera bluez, este es el dominio de dicho servicio
CONTROLADOR_DE_OBJETOS= "org.freedesktop.DBus.ObjectManager"    ## El controlador del objeto que nos devolvera toda la informacion de una interfaz
INTERFAZ_DE_ADAPTADOR="{}.Adapter1".format(SERVICIO_BLUEZ)      ## Obtenemos el primer adaptador de dispositivo
INTERFAZ_DE_DISPOSITIVO="{}.Device1".format(SERVICIO_BLUEZ)
GATT_SERVICE_INTERFACE = "{}.GattService1".format(SERVICIO_BLUEZ)
GATT_DESCRIPTOR_INTERFACE = "{}.GattDescriptor1".format(SERVICIO_BLUEZ)
GATT_CHARACTERISTIC_INTERFACE = "{}.GattCharacteristic1".format(SERVICIO_BLUEZ)
PROPERTIES_INTERFACE = "org.freedesktop.DBus.Properties"
class BlueZDBusException(Exception):
    pass

# Este metodo nos devuelve una estructura json con un conjunto de direcciones que representan diferentes ojetos dentro de la api,
  # el ejemplo encontrable en .tmp/objeto.bluez.txt
def GetObjectManager():
  controlador = BUS_DEL_SISTEMA.get(SERVICIO_BLUEZ, "/")[CONTROLADOR_DE_OBJETOS]
  return controlador.GetManagedObjects()


# Este metodo sirve para obtener los diferentes adaptadores dentro del sistema
  # para ello buscara dentro del bus cuales estan registrados dentro de las direcciones y retornara el primero
def GetAdaptador(pattern=None):
  objetos = GetObjectManager()
  for path, ifaces in objetos.items():
    adaptador = ifaces.get(INTERFAZ_DE_ADAPTADOR)
    if adaptador is not None:
      if pattern is None:
        return BUS_DEL_SISTEMA.get(SERVICIO_BLUEZ,path)[INTERFAZ_DE_ADAPTADOR]
  else:
    raise BlueZDBusException("Adaptador bluetooth no encontrado")

def GetDispositivos():
  objetos = GetObjectManager()
  for path, ifaces in objetos.items():
    if INTERFAZ_DE_DISPOSITIVO in ifaces.keys():
      yield(path,ifaces[GATT_SERVICE_INTERFACE])