from BT.Adaptador.Adaptador import *
from BT.src.dbus_bluez import *
from BT.Escaner import *


#metodo que se encarga de obtener una lista con las interfaces disponibles
def ObtenerInterfacesSistema():
  objetos = GetObjectManager()
  llaves = objetos.keys()
  dispositivos=list()
  for path in llaves:
    result = re.match(r'/org/bluez/hci[0-1]*$',path)
    if result:
      dispositivos.append(path.replace("/org/bluez/",""))
  return dispositivos

def MostrarInterfacesBT():
  print("Opcion\tInterfaz")
  print("------------------")
  i=0
  for iface in ObtenerInterfacesSistema():
    print(str(i)+"\t"+iface)

def Escanear(interfaz):
  adaptador1= Adaptador(interfaz)
  mi_sniffer = Sniffer(adaptador1)
  mi_sniffer.run()
  resultado =mi_sniffer.GetDispositivoElegido()

def SetearBT():
  interfaces = ObtenerInterfacesSistema()
  if (len(interfaces)>0):
    MostrarInterfacesBT()
    opcion = input()
    while (int(opcion)>=len(interfaces)):
      os.system('clear')
      print("Opcion no valida, elija una interfaz disponible")
      MostrarInterfacesBT()
      opcion = input()
    os.system('clear')
    print("Mostrando interfaces detectados en la zona: ")
    return interfaces[int(opcion)]
  else:
    print("No hay adaptadores conectados al sistema")

