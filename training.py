
import csv
import pathlib

from matplotlib.colors import hexColorPattern
PATH = "diccinario"
FICHEROS = 0


def BitArray(HEX):
  hexadecimal =[]
  for x in HEX:
    if x =="0":
      hexadecimal.append(0)
      hexadecimal.append(0)
      hexadecimal.append(0)
      hexadecimal.append(0)
    elif x =="1":
      hexadecimal.append(0)
      hexadecimal.append(0)
      hexadecimal.append(0)
      hexadecimal.append(1)
    elif x =="2":
      hexadecimal.append(0)
      hexadecimal.append(0)
      hexadecimal.append(1)
      hexadecimal.append(0)
    elif x =="3":
      hexadecimal.append(0)
      hexadecimal.append(0)
      hexadecimal.append(1)
      hexadecimal.append(1)
    elif x =="4":
      hexadecimal.append(0)
      hexadecimal.append(1)
      hexadecimal.append(0)
      hexadecimal.append(0)
    elif x =="5":
      hexadecimal.append(0)
      hexadecimal.append(1)
      hexadecimal.append(0)
      hexadecimal.append(1)
    elif x =="6":
      hexadecimal.append(0)
      hexadecimal.append(1)
      hexadecimal.append(1)
      hexadecimal.append(0)
    elif x =="7":
      hexadecimal.append(0)
      hexadecimal.append(1)
      hexadecimal.append(1)
      hexadecimal.append(1)
    elif x =="8":
      hexadecimal.append(1)
      hexadecimal.append(0)
      hexadecimal.append(0)
      hexadecimal.append(0)
    elif x =="9":
      hexadecimal.append(1)
      hexadecimal.append(0)
      hexadecimal.append(0)
      hexadecimal.append(1)
    elif x =="A" or x=="a":
      hexadecimal.append(1)
      hexadecimal.append(0)
      hexadecimal.append(1)
      hexadecimal.append(0)
    elif x =="B" or x=="b":
      hexadecimal.append(1)
      hexadecimal.append(0)
      hexadecimal.append(1)
      hexadecimal.append(1)
    elif x=="C" or x =="c":
      hexadecimal.append(1)
      hexadecimal.append(1)
      hexadecimal.append(0)
      hexadecimal.append(0)
    elif x =="D" or x=="d":
      hexadecimal.append(1)
      hexadecimal.append(1)
      hexadecimal.append(0)
      hexadecimal.append(1)
    elif x =="E" or x =="e":
      hexadecimal.append(1)
      hexadecimal.append(1)
      hexadecimal.append(1)
      hexadecimal.append(0)
    elif x =="F" or x=="f":
      hexadecimal.append(1)
      hexadecimal.append(1)
      hexadecimal.append(1)
      hexadecimal.append(1)
  return hexadecimal


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
  cabecera.append("MAC")
  cabecera.append("CLK")
  for x in range (0,2):
    cabecera.append("Z{}".format(x))

  for i in range(1,FICHEROS+1):
    with open("{}/original/muestra{}.csv".format(PATH,i),'r') as source:
      reader = csv.reader(source)
      
      with open("{}/binario/muestra{}_bin_.csv".format(PATH,i),'w') as result:
        writter = csv.writer(result)
        for r in reader:         
          if r == ['BDADDR','CK','CLK', 'Z']:
            cabecera = []
            for x in range(48):
              cabecera.append("MAC{}".format(x))
            for x in range(32):
              cabecera.append("CLK{}".format(x))
            for x in range (128):
              cabecera.append("Z{}".format(x))
            writter.writerow(cabecera)
          else:
            muestra = []
            MAC_= BitArray(ModificarMAC(r[0]))
            for x in MAC_:
              muestra.append(x)
            clk = BitArray(r[1])
            for x in clk:
              muestra.append(x)
            z = BitArray(r[2])
            for x in z:
              muestra.append(x)
            writter.writerow(muestra)
        result.close()
      source.close()


count=0
for path in pathlib.Path("{}/original/".format(PATH)).iterdir():
  if path.is_file():
    count+=1
FICHEROS = count
# resultado = ModificarMAC("AB:CD:DD")
# resultado = BitArray(ModificarMAC("01:23:45:67:89:AB"))
# print ("{}".format(resultado))    
modificarcsv()
