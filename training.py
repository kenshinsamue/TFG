
import csv
import pathlib

PATH = "ML/diccionario/partes/"
FICHEROS = 0
def modificarcsv():

  for x in range(5,FICHEROS):
    with open("{}parte{}.csv".format(PATH,x),'r') as source:
      reader = csv.reader(source)

      with open("{}parte{}_nuevo.csv".format(PATH,x),'w') as result:
        writer = csv.writer(result)

        for r in reader:
          print("estamos en parte {}".format(x))
          print("linea : {}".format(r))
          writer.writerow((r[0],r[2],r[3]))

        result.close()
      source.close()
count=0
for path in pathlib.Path("ML/diccionario/partes/").iterdir():
  if path.is_file():
    count+=1
FICHEROS = count    
modificarcsv()
