# Creacion del algoritmo E0 para crear la clave cifrante del mensaje
# Damos por hecho que los valores Hexadecimales son strings en mayuscula 
class E0 (object):
  # BD_BDDR es la direccion en formato binario/decimal
  # CLK es el valor del reloj en bits/decimal
  # CK es el valor de la clave en bits/decimal
  # mac es el valor de la direccion en formato hex
  # LAP valor del LAP en hex
  # UAP valor del UAP en hex
  # NAP valor del NAP en hex 


  def __init__ (self):
    self.BD_BDDR = 0 
    self.CLK = 0     
    self.CK = 0      
    self.LFSR0 = 0
    self.LFSR1 = 0
    self.LFSR2 = 0
    self.LFSR3 = 0
    self.c=0
    self.c_next=0
    self.c_prev=0
    self.vector_0 = self.init_vector_LFSR0()
    self.vector_1 = self.init_vector_LFSR1()



  def init_vector_LFSR0 (self):
    input_vector=0

    # ADR[2]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[4])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[5])
    input_vector = input_vector | bit

    # CLK[1]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[2])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[3])
    input_vector = input_vector | bit

    # KC[12]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[24])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[25])
    input_vector = input_vector | bit

    # KC[8]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[16])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[17])
    input_vector = input_vector | bit

    # KC[4]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[8])
    input_vector = input_vector | bit
    
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[9])
    input_vector = input_vector | bit

    # KC[0]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[0])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[1])
    input_vector = input_vector | bit

    # CL24
    input_vector = input_vector << 1
    bit = self.get_bit_value(self.hex_to_bit(self.CLK[6]),3)
    input_vector = input_vector | bit

    return input_vector

  def init_vector_LFSR1 (self):
    input_vector=0

    # AD[3]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[6])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[7])
    input_vector = input_vector | bit

    # AD[0]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[0])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[1])
    input_vector = input_vector | bit

    # KC[13]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[26])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[27])
    input_vector = input_vector | bit

    # KC[9]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[18])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[19])
    input_vector = input_vector | bit

    # KC[5]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[10])
    input_vector = input_vector | bit
    
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[11])
    input_vector = input_vector | bit

    # KC[1]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[2])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[3])
    input_vector = input_vector | bit

    # CLK[0]L = [3,2,1,0]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[0])
    input_vector = input_vector | bit

    # CTES 001
    input_vector = input_vector << 3
    bit = self.get_bit_value(1,1)
    input_vector = input_vector | bit

    return input_vector

  def init_vector_LFSR2 (self):
    input_vector=0

    # AD[4]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[8])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[9])
    input_vector = input_vector | bit

    # CLK[2]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[4])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[5])
    input_vector = input_vector | bit

    # KC[14]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[28])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[29])
    input_vector = input_vector | bit

    # KC[10]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[20])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[21])
    input_vector = input_vector | bit

    # KC[6]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[12])
    input_vector = input_vector | bit
    
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[13])
    input_vector = input_vector | bit

    # KC[2]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[4])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[5])
    input_vector = input_vector | bit

    # CL25
    input_vector = input_vector << 1
    bit = self.get_bit_value(self.hex_to_bit(self.CLK[6]),2)
    input_vector = input_vector | bit

    return input_vector

  def init_vector_LFSR3 (self):
    input_vector=0

    # AD[5]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[10])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[11])
    input_vector = input_vector | bit

    # AD[1]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[2])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[3])
    input_vector = input_vector | bit

    # KC[15]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[30])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[31])
    input_vector = input_vector | bit

    # KC[11]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[22])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[23])
    input_vector = input_vector | bit

    # KC[7]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[14])
    input_vector = input_vector | bit
    
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[15])
    input_vector = input_vector | bit

    # KC[3]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[6])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[7])
    input_vector = input_vector | bit

    # CLK[0]U = [7,6,5,4]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[1])
    input_vector = input_vector | bit

    # CTES 111
    input_vector = input_vector << 3
    bit = 7
    input_vector = input_vector | bit

    return input_vector

    
  # Este metodo le indicaremos un valor numerico y la posicion del byte que nos interesa
  def get_byte_value(self,valor,byte):
    Byte = 15
    Byte = Byte << (byte * 4)
    resultado = valor & Byte
    resultado = resultado >> (byte * 4)
    return resultado
# metodo que dado un byte, y una posicion dentro del mismo, nos retorna el valor del bit en esa posicion
  def get_bit_value(self,valor,bit):
    Bit = 1
    Bit = Bit << bit
    resultado = valor & Bit
    resultado = resultado >> bit
    return resultado

  # Guardamos el valor del reloj, hasta 26b  
  def set_clk (self,clk):
    self.CLK = clk

  # Guardamos el valor de una lcave de la comunicacion, hasta 128b
  def set_Ck (self,ck):
    self.CK = ck

  # Recibiremos una MAC con el siguiente formato : AA:AA:AA:AA:AA:AA
  # En mayuscula y separado por puntos
  def set_mac (self,mac):
    self.mac = mac.replace(':','')
    self.NAP=self.mac[:4]
    self.UAP=self.mac[4:6]
    self.LAP=self.mac[6:12]

    for hexa in self.mac:
      self.BD_BDDR = self.BD_BDDR << 4
      bit = self.hex_to_bit(hexa)
      self.BD_BDDR =self.BD_BDDR | bit 

    # print("{0:b}".format(self.BD_BDDR))
    # print(self.mac)
    # print(self.LAP)
    # print(self.UAP)
    # print(self.NAP)
  
  # Este metodo recibira un valor hexadecimal y devolvera el entero que representa su valor en bits
  def hex_to_bit (self,hex):
    resultado=0
    if hex == '0':
      resultado=0
      a="{0:b}".format(resultado)
    
    if hex == '1':
      resultado=1
      a="{0:b}".format(resultado)

    if hex == '2':
      resultado = 2
      a="{0:b}".format(resultado)
    
    if hex == '3':
      resultado = 3
      a="{0:b}".format(resultado)

    if hex == '4':
      resultado = 4
      a="{0:b}".format(resultado) 
    
    if hex == '5':
      resultado = 5
      a="{0:b}".format(resultado)
      
    if hex == '6':
      resultado = 6
      a="{0:b}".format(resultado)

    if hex == '7':
      resultado = 7
      a="{0:b}".format(resultado)

    if hex == '8':
      resultado = 8
      a="{0:b}".format(resultado)

    if hex == '9':
      resultado = 9
      a="{0:b}".format(resultado)

    if hex == 'A':
      resultado = 10
      a="{0:b}".format(resultado)

    if hex == 'B':
      resultado = 11
      a="{0:b}".format(resultado)

    if hex == 'C':
      resultado = 12
      a="{0:b}".format(resultado)

    if hex == 'D':
      resultado = 13
      a="{0:b}".format(resultado)

    if hex == 'E':
      resultado = 14
      a="{0:b}".format(resultado)

    if hex == 'F':
      resultado = 15
      a="{0:b}".format(resultado)
    
    # print(a)
    return resultado

hola = E0()
hola.set_mac("AA:BB:CC:DD:EE:FF")
# tmp = hola.get_byte_value(131241234,2)
# tmp = hola.get_bit_value(131241234,4)
# print("{0:b}".format(tmp))
# hola.hex_to_bit("F")
hola.set_clk("AABBCCDD")
hola.set_Ck("00112233445566778899AABBCCDDEEFF")
