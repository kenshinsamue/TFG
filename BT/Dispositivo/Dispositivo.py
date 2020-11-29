from BT.src.adaptador import *
class Dispositivo(object):
  def __init__(self):
    try:
      self.adaptador = GetAdaptador()
    except:
      print("Error al intentar obtener el adaptador")

  def GetAdaptadorBT(self):
    return self.adaptador