
from typing import *



class GATTServicio(object):
  def __init__(self,uuid:str,primary:bool):
    self.uuid = uuid
    self.primary = primary
    



class Dispositivo(object):
  @classmethod
  def CrearInstancia(cls,path:str,data:Dict[str,Any]) -> "Dispositivo":
    return cls(
      path,
      data["Address"], data["Paired"],data["Connected"],data["ServicesResolved"],
      data.get("Name",None),data.get("Class",None),data.get("Appearance",None),data.get("UUIDs",list()),
      data.get("RSSI",None), data.get("TxPower",None),data.get("ManufacturerData",dict()),data.get("ServiceData",dict())
    )

  def __init__(self,path:str,address:str,paired:bool,connected:bool,
              services_resolved:bool,name:Optional[str] = None,device_class:Optional[int]=None,
              appearance:Optional[int]=None,uuids:Sequence[int]=None,
              rssi:int = None,tx_power:int = None,
              manufacturer_data: Dict[int,Sequence[int]]=None,
              service_data: Dict[str,Sequence[int]]=None)->None:
    self.activo = True
    self.path = path
    self.direccion = address
    self.enlazado = paired
    self.conectado = connected
    self.servicios = service_data
    self.nombre= name
    self.dispositivo_clase = device_class
    self.appearance=appearance
    self.uuids = set(uuids)
    self.rssis = [rssi]
    self.tx_power = tx_power
  
  def MostrarDispositivo(self):
    print("{}".format(self))

  def __str__ (self) -> str:
    name = self.nombre if self.nombre is not None else "Desconocido\t"
    rssi = self.rssis[-1] if len(self.rssis) > 0 else -120
    return "{} {} {}dBa {}".format(name[0:16],self.direccion,rssi,self.conectado)