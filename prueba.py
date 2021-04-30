from pyubertooth.ubertooth import *


ut = Ubertooth()
for data in ut.rx_stream(count=5):
    print (data)
ut.close()