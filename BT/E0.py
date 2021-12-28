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
    self.vector_z=[]
    self.bloqueo = False
              

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
    print ("Inicializando mac")
    print ("Binario: {0:b}".format(self.BD_BDDR))
    print ("Hexadecimal: {}".format(self.mac))
    print ("  LAP  UAP NAP\n{} {} {}".format(self.LAP,self.UAP,self.NAP))
    
  

########### Inicializacion de los LFSR #####################

  def init_vectores (self) :
    self.vector_0 = self.init_vector_LFSR0()
    self.vector_1 = self.init_vector_LFSR1()
    self.vector_2 = self.init_vector_LFSR2()
    self.vector_3 = self.init_vector_LFSR3() 

    print ("\n\n Inicializacion de Vectores: \n     LFSR1            LFSR2              LFSR3           LFSR4 \n{}  {}  {}  {}".format(hex(self.vector_0),hex(self.vector_1),hex(self.vector_2),hex(self.vector_3)))
    print ("\n\n")

  def init_LFSR (self):
    print("\n\n##############Iteraciones iniciales#####################")
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

        #LFSR 1
        resultado = self.shift_LFSR_accarreado(self.LFSR1,self.vector_1,1)
        self.LFSR1 = resultado[0]
        self.vector_1 = resultado[1]        
        self.x[1] = resultado[2]

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

        #LFSR 1
        resultado = self.shift_LFSR_accarreado(self.LFSR1,self.vector_1,1)
        self.LFSR1 = resultado[0]
        self.vector_1 = resultado[1]        
        self.x[1] = resultado[2]

        #LFSR 0
        resultado = self.shift_LFSR_accarreado(self.LFSR2,self.vector_2,2)
        self.LFSR2 = resultado[0]
        self.vector_2 = resultado[1]        
        self.x[2] = resultado[2]
        

        #LFSR3
        resultado = self.shift_LFSR(self.LFSR3,self.vector_3)
        self.LFSR3 = resultado[0]
        self.vector_3 = resultado[1]
      print("\n t: {}".format(x+1))
      print("LFSR0 {}".format(hex(self.LFSR0)))
      print("LFSR1 {}".format(hex(self.LFSR1)))
      print("LFSR2 {}".format(hex(self.LFSR2)))
      print("LFSR3 {}".format(hex(self.LFSR3)))
      print("X: {} {} {} {}".format(self.x[0],self.x[1],self.x[2],self.x[3]))


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
      
  def shift_LFSR_accarreado_final(self,LFSR,vector,indice):
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
    
    mascara = bit << self.size[indice]
    mascara = mascara -1
    
    # introducimos el proximo bit
    LFSR = LFSR & mascara
    LFSR = LFSR<< 1
    LFSR = LFSR | acarreado
    return LFSR,vector,sobrante
########### Ultima Iteracion ###############################

  def llenarLFSR(self):
    
    ############ LFSR1 ############
    # z[12]_0
    self.LFSR0 = 0
    mascara = 1
    self.LFSR0 = mascara & self.vector_z[25]
    
    # z[8]
    tmp = self.vector_z[16]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[17]
    self.LFSR0 = self.LFSR0 << 8
    self.LFSR0 = self.LFSR0 | tmp

    # z[4]
    tmp = self.vector_z[8]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[9]
    self.LFSR0 = self.LFSR0 << 8
    self.LFSR0 = self.LFSR0 | tmp
    # z[0]
    tmp = self.vector_z[0]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[1]
    self.LFSR0 = self.LFSR0 << 8
    self.LFSR0 = self.LFSR0 | tmp
    mascara = 33554432-1
    self.LFSR0 = self.LFSR0 & mascara
    # print("LFSR1 :{}".format(hex(self.LFSR0)))

    ########### LFSR2 ###########
    self.LFSR1 = 0
    mascara = 14
    # z[12](7-1)
    self.LFSR1 = self.vector_z[24]
    self.LFSR1 = self.LFSR1 << 4
    tmp = self.vector_z[25] & mascara
    self.LFSR1 = self.LFSR1 | tmp
    self.LFSR1 = self.LFSR1 >> 1

    # z[9]
    tmp = self.vector_z[18]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[19]
    self.LFSR1 = self.LFSR1 << 8
    self.LFSR1 = self.LFSR1 | tmp
    # z[5]
    tmp = self.vector_z[10]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[11]
    self.LFSR1 = self.LFSR1 << 8
    self.LFSR1 = self.LFSR1 | tmp

    tmp = self.vector_z[2]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[3]
    self.LFSR1 = self.LFSR1 << 8
    self.LFSR1 = self.LFSR1 | tmp
    
    # print("LFSR2 :{}".format(hex(self.LFSR1)))

    ############### LFSR3 ###############
    self.LFSR2 = 0
    # z[15]_0
    self.LFSR2 = self.vector_z[31] & 1

    # z[13]
    tmp = self.vector_z[26]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[27]
    self.LFSR2 = self.LFSR2 << 8
    self.LFSR2 = self.LFSR2 | tmp

    # z[10]
    tmp = self.vector_z[20]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[21]
    self.LFSR2 = self.LFSR2 << 8
    self.LFSR2 = self.LFSR2 | tmp

    # z[6]
    tmp = self.vector_z[12]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[13]
    self.LFSR2 = self.LFSR2 << 8
    self.LFSR2 = self.LFSR2 | tmp

    #z[2] 
    tmp = self.vector_z[4]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[5]
    self.LFSR2 = self.LFSR2 << 8
    self.LFSR2 = self.LFSR2 | tmp
   
    # print("LFSR3 :{}".format(hex(self.LFSR2)))
    
    ############ LFSR4 ############
    self.LFSR3 = 0
    mascara = 14
    # z[15](7-1)
    self.LFSR3 = self.vector_z[30]
    self.LFSR3 = self.LFSR3 << 4
    tmp = self.vector_z[31] & mascara
    self.LFSR3 = self.LFSR3 | tmp
    self.LFSR3 = self.LFSR3 >> 1

    # z[14]
    tmp = self.vector_z[28]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[29]
    self.LFSR3 = self.LFSR3 << 8
    self.LFSR3 = self.LFSR3 | tmp
    
    # z[11]
    tmp = self.vector_z[22]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[23]
    self.LFSR3 = self.LFSR3 << 8
    self.LFSR3 = self.LFSR3 | tmp
    
    # z[7]
    tmp = self.vector_z[14]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[15]
    self.LFSR3 = self.LFSR3 << 8
    self.LFSR3 = self.LFSR3 | tmp

    # z[3]
    tmp = self.vector_z[6]
    tmp = tmp << 4
    tmp = tmp | self.vector_z[7]
    self.LFSR3 = self.LFSR3 << 8
    self.LFSR3 = self.LFSR3 | tmp
   
    # print("LFSR4 :{}".format(hex(self.LFSR3)))    

  def IteracionFinal(self):
    self.bloqueo = False
    self.z = 0
    cuenta = 0
    print("\n\n Ultima iteracion de combinacion de bits")
    for x in range(125):
      print("\n t: {}".format(x+1))
      print("LFSR0 {}".format(hex(self.LFSR0)))
      print("LFSR1 {}".format(hex(self.LFSR1)))
      print("LFSR2 {}".format(hex(self.LFSR2)))
      print("LFSR3 {}".format(hex(self.LFSR3)))
      #LFSR 0
      resultado = self.shift_LFSR_accarreado_final(self.LFSR0,self.vector_0,0)
      self.LFSR0 = resultado[0]
      self.vector_0 = resultado[1]        
      self.x[0] = resultado[2]

      #LFSR 1
      resultado = self.shift_LFSR_accarreado_final(self.LFSR1,self.vector_1,1)
      self.LFSR1 = resultado[0]
      self.vector_1 = resultado[1]        
      self.x[1] = resultado[2]

      #LFSR 2
      resultado = self.shift_LFSR_accarreado_final(self.LFSR2,self.vector_2,2)
      self.LFSR2 = resultado[0]
      self.vector_2 = resultado[1]        
      self.x[2] = resultado[2]
      
      #LFSR3
      resultado = self.shift_LFSR_accarreado_final(self.LFSR3,self.vector_3,3)
      self.LFSR3 = resultado[0]
      self.vector_3 = resultado[1]        
      self.x[3] = resultado[2]

      
      c = self.blend()
      XResultantes = 0
      
      for y in self.x:
        XResultantes = XResultantes^y
      
      salida = c ^ XResultantes       
      print("Salida: {0:b}".format(salida))
      
      print("X: {} {} {} {}".format(self.x[0],self.x[1],self.x[2],self.x[3]))
      cuenta = cuenta + 1
      self.z = self.z << 1
      self.z = self.z | salida
      print("Z:") 
      print("{0:b}".format(self.z))
      
    
########### Acarreo de 200 iteraciones #####################
  def CorregirBits(self):
    print("\n\n ########## Carga paralela de los bits ##########")
    
    vector_z = self.z
    Bytes_resultantes = []
    hexa_1 = 240 
    hexa_2 = 15 
    mascara = 255

    for x in range(16) :
      mascara_aux = mascara << 120-(x*8)
      resultado = vector_z & mascara_aux
      resultado = resultado >> 120-(x*8)
      primero = resultado & hexa_2
      segundo = resultado & hexa_1
      segundo = segundo >> 4
      Bytes_resultantes.append(primero)
      Bytes_resultantes.append(segundo)
    
    for x in range(32):

      prueba = Bytes_resultantes[x]
      final = 0
      mascara = 1
      for y in range(4):
        tmp = prueba & mascara
        prueba = prueba >> 1
        final = final | tmp
        if y != 3:
          final = final << 1
        
      Bytes_resultantes[x]= final
    self.vector_z = Bytes_resultantes
    print ("Z : ")
    for x in self.vector_z:
      print("{}".format(hex(x)))
      

  def clocking(self):
    cuenta = 0
    print("\n\n ############# Clocking ############")
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
      if x== 199:
        self.bloqueo = True
      c = self.blend()
      XResultantes = 0
      
      for y in self.x:
        XResultantes = XResultantes^y
      
      salida = c ^ XResultantes       
      if x > 71:
        cuenta = cuenta + 1
        self.z = self.z << 1
        self.z = self.z | salida 
        # print("{0:b}".format(self.z))
      print("\n t: {}".format(x+1))
      print("LFSR0 {}".format(hex(self.LFSR0)))
      print("LFSR1 {}".format(hex(self.LFSR1)))
      print("LFSR2 {}".format(hex(self.LFSR2)))
      print("LFSR3 {}".format(hex(self.LFSR3)))
      print("X: {} {} {} {}".format(self.x[0],self.x[1],self.x[2],self.x[3]))
      print("Z: {}".format(salida))
    # self.z=0
    # print ("{}".format(hex(self.z)))
    # print ("{0:b}".format(self.z))
  
    self.CorregirBits()
    self.llenarLFSR()
    self.IteracionFinal()

  def blend(self):
    suma = 0
    # print("{} -- {}".format(self.z_1, self.z_2))
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
    if self.bloqueo == False:
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

def GetHEx (valor):
  if valor == 0:
    return "0"
  elif valor == 1:
    return "1"
  elif valor == 2:
    return "2"
  elif valor == 3:
    return "3"
  elif valor == 4:
    return "4"
  elif valor == 5:
    return "5"
  elif valor == 6:
    return "6"
  elif valor == 7:
    return "7"
  elif valor == 8:
    return "8"
  elif valor == 9:
    return "9"
  elif valor == 10:
    return "A"
  elif valor == 11:
    return "B"
  elif valor == 12:
    return "C"
  elif valor == 13:
    return "D"
  elif valor == 14:
    return "E"
  elif valor == 15:
    return "F"


def To_MAC(valor):
  mac = ""
  mascara = 15
  mascara = mascara << 44
  
  tmp = valor & mascara
  tmp = tmp >>44
  hexadecimal = GetHEx(tmp)
  
  mac = mac + hexadecimal
  mascara = mascara>>4

  tmp = valor & mascara
  tmp = tmp >>40
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mac = mac+":"
  mascara = mascara>>4

  tmp = valor & mascara
  tmp = tmp >>36
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mascara = mascara>>4

  tmp = valor & mascara
  tmp = tmp >>32
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mac = mac+":"
  mascara = mascara>>4
  tmp = valor & mascara
  tmp = tmp >>28
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mascara = mascara>>4

  tmp = valor & mascara
  tmp = tmp >>24
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mac = mac+":"
  mascara = mascara>>4

  tmp = valor & mascara
  tmp = tmp >>20
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mascara = mascara>>4

  tmp = valor & mascara
  tmp = tmp >>16
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mac = mac+":"
  mascara = mascara>>4

  tmp = valor & mascara
  tmp = tmp >>12
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mascara = mascara>>4

  tmp = valor & mascara
  tmp = tmp >>8
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mac = mac+":"
  mascara = mascara>>4


  tmp = valor & mascara
  tmp = tmp >>4
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mascara = mascara>>4

  tmp = valor & mascara
  hexadecimal = GetHEx(tmp)
  mac = mac + hexadecimal
  mascara = mascara>>4
  return mac

def To_Hex(valor,size):
  Hex = ""
  size_t = size - 4
  while size_t != -4:
    mascara = 15 << size_t
    tmp = valor & mascara
    tmp = tmp >>size_t
    Hex = Hex + GetHEx(tmp)
    size_t = size_t - 4
  return Hex

fichero = open("diccionario.txt","w")

valor_mac_max = pow(2,48)
valor_ck_max = pow(2,128)
valor_clk_max = pow(2,32)

linea = ""
for x in range(pow(2,48)):
  for y in range(pow(2,128)):
    for z in range(pow(2,32)):
      mac = To_MAC(x)
      ck = To_Hex(y,128)
      clk = To_Hex(z,32)
      linea =mac +" "+ ck +" "+ clk
      print(linea)
      
      fichero.write(linea+"\n")

# protocolo = E0()


# hola = E0()
# hola.set_mac("1B:0F:56:94:7F:2C")


# hola.set_clk("02001A5F")
# hola.set_Ck("633A15E0534C0D78D03190BA4AF08721")
# hola.init_vectores()
# hola.init_LFSR()
# hola.clocking()


