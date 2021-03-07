from BT.Adaptador.Adaptador import *
from scapy.layers.bluetooth import *
from scapy.all import *
import pyshark

class Sniffer(object):

  def __init__ (self,adaptador,remoto):
    self.AdaptadorLocal = Adaptador(adaptador)
    self.AdaptadorLocal.SetAdaptadorPropiedad("Discoverable","True")
  
  def get_packet_layers(self,packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1

  def ReceptorPaquete(self,pkt):
    # pkt.show2()
    if pkt.getlayer(3) is not None: 
      pkt.show()
    # print ("Se ha encontrado un paquete del host: {}".format(pkt))
    # for layer in self.get_packet_layers(pkt):
    #   print("{}".format(pkt.getlayer(3)))
    #   pkt.show()
    #   print(layer.name)


  def start (self):
    # bt = BluetoothHCISocket(0)
    # bt.sniff(prn=self.ReceptorPaquete, count=0 )
    capture = pyshark.LiveCapture(interface='bluetooth0')
    while True:
      capture.sniff(packet_count=1)
      if capture[0].layers[2] is not None:
        print(capture[0].layers[2].name) 

