
import csv
import pathlib


PATH = "ML/diccionario/muestras/"



def modificarcsv():

  for i in range(34,FICHEROS+1):
    with open("{}muestra{}.csv".format(PATH,i),'r') as source:
      reader = csv.reader(source)
      
      with open("{}muestra_{}.csv".format(PATH,i),'w') as result:
        writter = csv.writer(result)

        for r in reader:
          print("estamos en parte {}".format(i))
          print("linea : {}".format(r))
          
          linea = []
          for x in range(0,336):
              if x < 48 or x > 175:
                  linea.append(r[x])

          writter.writerow(linea)
        result.close()
      source.close()
        # print("linea: {}".format(r))
 
  # for x in range(5,FICHEROS):
  #   with open("{}parte{}.csv".format(PATH,x),'r') as source:
  #     reader = csv.reader(source)

  #     with open("{}parte{}_nuevo.csv".format(PATH,x),'w') as result:
  #       writer = csv.writer(result)

  #       for r in reader:
  #         print("estamos en parte {}".format(x))
  #         print("linea : {}".format(r))
  #         writer.writerow((r[0],r[2],r[3]))

  #       result.close()
  #     source.close()






count=0
for path in pathlib.Path(PATH).iterdir():
  if path.is_file():
    count+=1

FICHEROS = count

modificarcsv()