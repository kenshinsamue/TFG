from BT.Adaptador.Adaptador import *
from scapy.layers.bluetooth import *
from scapy.all import *

class Sniffer(object):

  def __init__ (self,adaptador,remoto):
    self.AdaptadorLocal = Adaptador(adaptador)
    self.AdaptadorLocal.SetAdaptadorPropiedad("Discoverable","True")
  
  def ReceptorPaquete(selfpkt):
    pkt.show()

  def start (self):
    bt = BluetoothHCISocket(0)
    bt.sniff(prn=ReceptorPaquete)
  
