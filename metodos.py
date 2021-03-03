from BT.Adaptador.Adaptador import *
from BT.src.dbus_bluez import *
from BT.Escaner import *
from BT.Sniffer import *

# metodo que se encarga de obtener una lista con las interfaces de los controladores locales disponibles
def ObtenerInterfacesSistema():
  objetos = GetObjectManager()
  llaves = objetos.keys()
  dispositivos=list()
  for path in llaves:
    result = re.match(r'/org/bluez/hci[0-1]*$',path)
    if result:
      dispositivos.append(path.replace("/org/bluez/",""))
  return dispositivos

# Metodo que como su nombre indica lista las diferentes interfaces del controlador local
def MostrarInterfacesBT():
  print("Opcion\tInterfaz")
  print("------------------")
  i=0
  for iface in ObtenerInterfacesSistema():
    print(str(i)+"\t"+iface)

# Metodo que configura la interfaz a utilizar para un determinado proposito
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


# Metodo que permite mostrar los diferentes controladores o dispositivos en un area cercana 

def Escanear(interfaz,retornar_opcion=False):
  adaptador1= Adaptador(interfaz)
  mi_escaner = Escaner(adaptador1)
  mi_escaner.run(retornar_opcion)
  return mi_escaner

# Metodo que busca sniffear mediante un controlador bluetooth generico atraves de scapy
def Sniffear(interfaz):
  escaner = Escanear(interfaz,True)
  remoto = escaner.GetDispositivoElegido()
  mi_sniffer =  Sniffer(interfaz,remoto)
  mi_sniffer.start()




  



