import unittest
import re
from BT.Dispositivo.Dispositivo import *
class TestAdaptador(unittest.TestCase):
  def test_getadaptador(self):
    dispositivo = Adaptador("hci0")
    self.assertEqual(str(dispositivo),
    "Dispositivo: hci0, Address: DC:8B:28:83:D6:8B, Nombre: parrot, Discoverable: False por 60s")
    

if __name__ == "__main__":
  unittest.main()