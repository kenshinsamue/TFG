
import csv
import pathlib

from matplotlib.colors import hexColorPattern

PATH = "ML/diccionario/partes_original/"
FICHEROS = 0

  
def HEXtoVector(HEX):
  valor =0
  hexadecimal =0
  for x in HEX:
    valor = valor << 4
    hexadecimal = 0
    if x =="0":
      pass
    elif x =="1":
      hexadecimal = 1
    elif x =="2":
      hexadecimal = 1
      hexadecimal = hexadecimal << 1
    elif x =="3":
      hexadecimal = 1
      hexadecimal = hexadecimal << 1
      hexadecimal = hexadecimal | 1
    elif x =="4":
      hexadecimal = 1
      hexadecimal = hexadecimal << 2      
    elif x =="5":
      hexadecimal = 1
      hexadecimal = hexadecimal << 2
      hexadecimal = hexadecimal | 1
    elif x =="6":
      hexadecimal = 1
      hexadecimal = hexadecimal << 1
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 1
    elif x =="7":
      hexadecimal = 1
      hexadecimal = hexadecimal << 1
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 1
      hexadecimal = hexadecimal | 1
    elif x =="8":
      hexadecimal = 1
      hexadecimal = hexadecimal <<3 
    elif x =="9":
      hexadecimal = 1
      hexadecimal = hexadecimal <<3
      hexadecimal = hexadecimal | 1 
    elif x =="A" or x=="a":
      hexadecimal = 1
      hexadecimal = hexadecimal << 2
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 1
    elif x =="B" or x=="b":
      hexadecimal = 1
      hexadecimal = hexadecimal << 2
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 1
      hexadecimal = hexadecimal | 1
    elif x=="C" or x =="c":
      hexadecimal = 1
      hexadecimal  = hexadecimal << 1
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 2
    elif x =="D" or x=="d":
      hexadecimal = 1
      hexadecimal  = hexadecimal << 1
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 2
      hexadecimal = hexadecimal | 1
    elif x =="E" or x =="e":
      hexadecimal = 1
      hexadecimal  = hexadecimal << 1
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 1
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 1
    elif x =="F" or x=="f":
      hexadecimal = 1
      hexadecimal  = hexadecimal << 1
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 1
      hexadecimal = hexadecimal | 1
      hexadecimal = hexadecimal << 1
      hexadecimal = hexadecimal | 1

    valor = valor | hexadecimal

  return valor

def ModificarMAC(MAC):
  tmp=""
  for x in MAC:
    if(x != ":"):
      tmp+=x
  return tmp

def modificarcsv():
  cabecera = []
  for x in range(0,48):

    cabecera.append("MAC{}".format(x))
  for x in range(0,128):
    cabecera.append("CK{}".format(x))
  for x in range (0,32):
    cabecera.append("CLK{}".format(x))
  for x in range (0,128):
    cabecera.append("Z{}".format(x))

  for i in range(1,FICHEROS+1):
    with open("{}parte{}.csv".format(PATH,i),'r') as source:
      reader = csv.reader(source)
      
      with open("{}muestra{}.csv".format(PATH,i),'w') as result:
        writter = csv.writer(result)
        for r in reader:
          print("estamos en parte {}".format(i))
          print("linea : {}".format(r))
          if r == ['BDADDR', 'CK', 'CLK', 'Z']:
            cabecera = ['BDADDR', 'CLK','Z']
            writter.writerow(cabecera)
          else:
            muestra = []
            muestra.append(HEXtoVector(ModificarMAC(r[0])))

            clk = HEXtoVector(r[2])
            muestra.append(clk)
            z = HEXtoVector(r[3])
            muestra.append(z)
            writter.writerow(muestra)
        result.close()
      source.close()


count=0
for path in pathlib.Path(PATH).iterdir():
  if path.is_file():
    count+=1
FICHEROS = count
# resultado = ModificarMAC("AB:CD:DD")
# resultado = HEXtoVector("ABCDEF0123456789")
# print ("{0:b}".format(resultado))    
modificarcsv()
