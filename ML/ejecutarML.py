
import os
import sys


layout = sys.argv[1]
comando = "./a.out -C diccionario/partes/"
configuracion = sys.argv[2]

for x in range(1,10):
    os.system("./a.out -C diccionario/partes/parte{}_nuevo.csv -t -c {} -l {}".format(x,configuracion,layout))

