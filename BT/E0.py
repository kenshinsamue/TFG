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
    self.size = [24,30,32,38]
    self.z_1=0
    self.z_2=0
    self.c=0
    self.feedback = [[0,5,13,17],
                     [0,7,15,19],
                     [0,5,9,29 ],
                     [0,3,11,35]]
    self.x = [0,0,0,0]
    self.clave=0
    self.z = 0
              

############################ setter ##################################

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
  

########### Inicializacion de los LFSR #####################

  def init_vectores (self) :
    self.vector_0 = self.init_vector_LFSR0()
    self.vector_1 = self.init_vector_LFSR1()
    self.vector_2 = self.init_vector_LFSR2()
    self.vector_3 = self.init_vector_LFSR3() 

  def init_LFSR (self):
    for x in range(39):
      if x < 25 :
        #LFSR0
        resultado = self.shift_LFSR(self.LFSR0,self.vector_0)
        self.LFSR0 = resultado[0]
        self.vector_0 = resultado[1]

        #LFSR1
        resultado = self.shift_LFSR(self.LFSR1,self.vector_1)
        self.LFSR1 = resultado[0]
        self.vector_1 = resultado[1]

        #LFSR2
        resultado = self.shift_LFSR(self.LFSR2,self.vector_2)
        self.LFSR2 = resultado[0]
        self.vector_2 = resultado[1]

        #LFSR3
        resultado = self.shift_LFSR(self.LFSR3,self.vector_3)
        self.LFSR3 = resultado[0]
        self.vector_3 = resultado[1]

      if x < 31 and x >= 25:
        #LFSR 0
        resultado = self.shift_LFSR_accarreado(self.LFSR0,self.vector_0,0)
        self.LFSR0 = resultado[0]
        self.vector_0 = resultado[1]        
        self.x[0] = resultado[2]
        # print("el vector es: {}".format(hex(self.LFSR0)))

        #LFSR1
        resultado = self.shift_LFSR(self.LFSR1,self.vector_1)
        self.LFSR1 = resultado[0]
        self.vector_1 = resultado[1]

        #LFSR2
        resultado = self.shift_LFSR(self.LFSR2,self.vector_2)
        self.LFSR2 = resultado[0]
        self.vector_2 = resultado[1]

        #LFSR3
        resultado = self.shift_LFSR(self.LFSR3,self.vector_3)
        self.LFSR3 = resultado[0]
        self.vector_3 = resultado[1]

      if x < 33 and x >= 31:

        #LFSR 0
        resultado = self.shift_LFSR_accarreado(self.LFSR0,self.vector_0,0)
        self.LFSR0 = resultado[0]
        self.vector_0 = resultado[1]        
        self.x[0] = resultado[2]
        #print("el vector es: {}".format(hex(self.LFSR0)))

        #LFSR 1
        resultado = self.shift_LFSR_accarreado(self.LFSR1,self.vector_1,1)
        self.LFSR1 = resultado[0]
        self.vector_1 = resultado[1]        
        self.x[1] = resultado[2]
        #print("el vector es: {}".format(hex(self.LFSR1)))

        #LFSR2
        resultado = self.shift_LFSR(self.LFSR2,self.vector_2)
        self.LFSR2 = resultado[0]
        self.vector_2 = resultado[1]

        #LFSR3
        resultado = self.shift_LFSR(self.LFSR3,self.vector_3)
        self.LFSR3 = resultado[0]
        self.vector_3 = resultado[1]

      if x >= 33:
        #LFSR 0
        resultado = self.shift_LFSR_accarreado(self.LFSR0,self.vector_0,0)
        self.LFSR0 = resultado[0]
        self.vector_0 = resultado[1]        
        self.x[0] = resultado[2]
        #print("el vector es: {}".format(hex(self.LFSR0)))

        #LFSR 1
        resultado = self.shift_LFSR_accarreado(self.LFSR1,self.vector_1,1)
        self.LFSR1 = resultado[0]
        self.vector_1 = resultado[1]        
        self.x[1] = resultado[2]
        #print("el vector es: {}".format(hex(self.LFSR1)))

        #LFSR 0
        resultado = self.shift_LFSR_accarreado(self.LFSR2,self.vector_2,2)
        self.LFSR2 = resultado[0]
        self.vector_2 = resultado[1]        
        self.x[2] = resultado[2]
        #print("el vector es: {}".format(hex(self.LFSR2)))
        

        #LFSR3
        resultado = self.shift_LFSR(self.LFSR3,self.vector_3)
        self.LFSR3 = resultado[0]
        self.vector_3 = resultado[1]

  def shift_LFSR(self,LFSR,vector):
    
    bit = 1
    valor = vector & bit
    vector = vector >> 1
    LFSR = LFSR << 1
    LFSR = LFSR | valor
    return LFSR, vector

  def shift_LFSR_accarreado(self,LFSR,vector,indice):
    bit = 1
    acarreado = vector & bit
    vector = vector >> 1
    for x in self.feedback[indice]: # obtenemos el valor acarreado
        
      tmp_bit = 1
      tmp_bit = tmp_bit << (self.size[indice]-x)
      resultado = tmp_bit & LFSR   # usamos AND porque queremos obtener el primer valor descrito 
                                    # por el polinomio
      resultado = resultado >> (self.size[indice]-x)    
      acarreado = acarreado ^ resultado                         

    # creamos la mascara para guardar el bit sobrante y acarrear
    
   
    mascara = bit << self.size[indice]
    # sobrante = LFSR & mascara
    # sobrante = sobrante >> self.size[indice]
    mascara = mascara -1
    
    # introducimos el proximo bit
    LFSR = LFSR & mascara
    LFSR = LFSR<< 1
    LFSR = LFSR | acarreado

    if(indice == 0):
      bit_x = 1
      bit_x = bit_x<<23
      sobrante = LFSR & bit_x
      sobrante = sobrante>>23
    elif (indice == 1):
      bit_x = 1
      bit_x = bit_x<<23
      sobrante = LFSR & bit_x
      sobrante = sobrante>>23
    elif (indice == 2):
      bit_x = 1
      bit_x = bit_x<<31
      sobrante = LFSR & bit_x
      sobrante = sobrante>>31
    elif (indice == 3):
      bit_x = 1
      bit_x = bit_x<<31
      sobrante = LFSR & bit_x
      sobrante = sobrante>>31

    return LFSR,vector,sobrante
      

########### Ultima Iteracion ###############################

  def IteracionFinal(self):
    #LFSR 0
    resultado = self.shift_LFSR_accarreado(self.LFSR0,self.vector_0,0)
    self.LFSR0 = resultado[0]
    self.vector_0 = resultado[1]        
    self.x[0] = resultado[2]

    #LFSR 1
    resultado = self.shift_LFSR_accarreado(self.LFSR1,self.vector_1,1)
    self.LFSR1 = resultado[0]
    self.vector_1 = resultado[1]        
    self.x[1] = resultado[2]

    #LFSR 2
    resultado = self.shift_LFSR_accarreado(self.LFSR2,self.vector_2,2)
    self.LFSR2 = resultado[0]
    self.vector_2 = resultado[1]        
    self.x[2] = resultado[2]
    

    #LFSR3
    resultado = self.shift_LFSR_accarreado(self.LFSR3,self.vector_3,3)
    self.LFSR3 = resultado[0]
    self.vector_3 = resultado[1]        
    self.x[3] = resultado[2]

    print ("resultado {}".format(hex(self.z)))
    print ("LFSR1: {}".format(hex(self.LFSR0)))
    print ("LFSR2: {}".format(hex(self.LFSR1)))
    print ("LFSR3: {}".format(hex(self.LFSR2)))
    print ("LFSR4: {}".format(hex(self.LFSR3)))

########### Acarreo de 200 iteraciones #####################

  def clocking(self):
    result =0
    cuenta = 0
    for x in range(200):
      #LFSR 0
      resultado = self.shift_LFSR_accarreado(self.LFSR0,self.vector_0,0)
      self.LFSR0 = resultado[0]
      self.vector_0 = resultado[1]        
      self.x[0] = resultado[2]

      #LFSR 1
      resultado = self.shift_LFSR_accarreado(self.LFSR1,self.vector_1,1)
      self.LFSR1 = resultado[0]
      self.vector_1 = resultado[1]        
      self.x[1] = resultado[2]

      #LFSR 2
      resultado = self.shift_LFSR_accarreado(self.LFSR2,self.vector_2,2)
      self.LFSR2 = resultado[0]
      self.vector_2 = resultado[1]        
      self.x[2] = resultado[2]
      
      #LFSR3
      resultado = self.shift_LFSR_accarreado(self.LFSR3,self.vector_3,3)
      self.LFSR3 = resultado[0]
      self.vector_3 = resultado[1]        
      self.x[3] = resultado[2]

      c = self.blend()
<<<<<<< HEAD
      print("El blend es : {}".format(c))
      XResultantes = 0
      for x in self.x:
        # print(x)
        XResultantes = XResultantes^x
      # print(XResultantes)
      
      result = result << 1
      result = result  | (c^XResultantes)
      salida = c ^ XResultantes
      self.z = self.z << 1
      self.z = self.z | salida 
      print("{0:b}".format(self.z))
    # print("\n\n\n{}".format(hex(result)))
    print ("resultado {}".format(hex(result)))
  # a5 1f 39 be 88 14 83 d4 0d fc 8d e6 4b f4 65 f8 9d 67 21 c2 e0 1b 78 e7 c3
=======
      XResultantes = 0
      
      for y in self.x:
        XResultantes = XResultantes^y
      
      result = result << 1
      result = result  | (c^XResultantes)
      salida = c ^ XResultantes       
      if x > 71:
        cuenta = cuenta + 1
        self.z = self.z << 1
        self.z = self.z | salida 
        # print("{0:b}".format(self.z))
      
    # self.z=0
    self.IteracionFinal()

>>>>>>> ML
  def blend(self):
    suma = 0
    for x in self.x:
      suma = suma + x
    suma = suma + self.z_1
    resultado = suma /2
    # print("{0:b}".format(tmp))
    t1= self.T1()
    t2 = self.T2()
    tmp = int(resultado) ^ t1 
    tmp = tmp ^ t2 
    bit = 1 
    c = bit&self.z_1
    self.z_2=self.z_1
    self.z_1= tmp
  
    return c

  def T1 (self):
    if self.z_1 ==0:
      return 0
    elif self.z_1 ==1:
      return 1
    elif self.z_1 == 2:
      return 2
    elif self.z_1 == 3:
      return 3

  def T2 (self):
    if self.z_2 ==0:
      return 0
    elif self.z_2 ==1:
      return 3
    elif self.z_2 == 2:
      return 1
    elif self.z_2 == 3:
      return 2

########### inicializacion de los vectores que se usaran para rellenar los LFSR ###############

  def init_vector_LFSR0 (self):
    input_vector=0

    # ADR[2]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[6])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[7])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # CLK[1]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[4])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[5])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[12]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[6])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[7])
    input_vector = input_vector | bit
    
    # print(hex(input_vector))

    # KC[8]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[14])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[15])
    input_vector = input_vector | bit
    
    # print(hex(input_vector))

    # KC[4]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[22])
    input_vector = input_vector | bit
    
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[23])
    input_vector = input_vector | bit

    # print(hex(input_vector))
    # KC[0]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[30])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[31])
    input_vector = input_vector | bit
    # print(hex(input_vector))
    # CL24
    input_vector = input_vector << 1
    bit = self.get_bit_value(self.hex_to_bit(self.CLK[1]),3)
    input_vector = input_vector | bit
    # print(hex(input_vector))
    return input_vector

  def init_vector_LFSR1 (self):
    input_vector=0

    # AD[3]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[4])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[5])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # AD[0]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[10])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[11])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[13]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[4])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[5])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[9]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[12])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[13])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[5]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[20])
    input_vector = input_vector | bit
    
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[21])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[1]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[28])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[29])
    input_vector = input_vector | bit
    
    # print(hex(input_vector))

    # CLK[0]L = [3,2,1,0]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[7])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # CTES 001
    input_vector = input_vector << 3
    input_vector = input_vector | 1

    # print(hex(input_vector))
    return input_vector

  def init_vector_LFSR2 (self):
    input_vector=0

    # AD[4]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[2])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[3])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # CLK[2]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[2])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[3])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[14]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[2])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[3])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[10]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[10])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[11])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[6]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[18])
    input_vector = input_vector | bit
    
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[19])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[2]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[26])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[27])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # CL25
    input_vector = input_vector << 1
    bit = self.get_bit_value(self.hex_to_bit(self.CLK[1]),1)
    input_vector = input_vector | bit

    # print(hex(input_vector))
    # print("{0:b}".format(input_vector))
    return input_vector

  def init_vector_LFSR3 (self):
    input_vector=0

    # AD[5]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[0])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[1])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # AD[1]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[8])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.mac[9])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[15]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[0])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[1])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[11]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[8])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[9])
    input_vector = input_vector | bit

    # print(hex(input_vector))

    # KC[7]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[16])
    input_vector = input_vector | bit
    
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[17])
    input_vector = input_vector | bit

    # print(hex(input_vector))
    # KC[3]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[24])
    input_vector = input_vector | bit

    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CK[25])
    input_vector = input_vector | bit

    # print(hex(input_vector))
    # CLK[0]U = [7,6,5,4]
    input_vector = input_vector << 4
    bit = self.hex_to_bit(self.CLK[6])
    input_vector = input_vector | bit

    # print(hex(input_vector))
    # CTES 111
    input_vector = input_vector << 3
    bit = 7
    input_vector = input_vector | bit

    return input_vector




########################## Bit y byte handlers ############################
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


############################################################################################################################



hola = E0()
hola.set_mac("1B:0F:56:94:7F:2C")
# tmp = hola.get_byte_value(131241234,2)
# tmp = hola.get_bit_value(131241234,4)
# print("{0:b}".format(tmp))
# hola.hex_to_bit("F")

hola.set_clk("02001A5F")
hola.set_Ck("633A15E0534C0D78D03190BA4AF08721")
hola.init_vectores()
hola.init_LFSR()
hola.clocking()



# LFSR0 = 0x845d1e
# LFSR1 = 0x4fe109b0
# LFSR2 = 0x10f8c325c
# LFSR3 = 0x7a520bcac6