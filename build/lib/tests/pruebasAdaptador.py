import unittest
from BT.Dispositivo.Dispositivo import *
class TestAdaptador(unittest.TestCase):
  def test_ObjectManager(self):
    
    self.assertEqual(GetAdaptador().address,"")

if __name__ == "__main__":
  unittest.main()