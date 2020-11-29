import unittest
import re
from BT.Dispositivo.Dispositivo import *
class TestAdaptador(unittest.TestCase):
  def test_ObjectManager(self):
    tmp = GetObjectManager()
    keys = tmp.keys()

    

    for path in keys:

      result = re.match(r'/org/bluez/hci[0-1]*$',path)
      if result:
        print(path)

    
    pass
  #self.assertEqual(GetAdaptador().path,"")

if __name__ == "__main__":
  unittest.main()