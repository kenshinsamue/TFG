import os
from pyparsing import match_previous_literal
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import pandas as pd
import numpy as np
from matplotlib import pyplot
def cargar_datos(numero):
  pd.set_option('display.max_columns',None)
  muestra = pd.read_csv("ML/diccionario/partes_original/muestra{}.csv".format(numero))

  muestras_objetivo = muestra.copy()
  max=int(0)
  for x in muestra["Z"]:
    x_ = int(x)
    if(x_>=max):
      max = x_
  datos =[]
  for x in muestra["Z"]:
    x_ = float(x)
    datos.append(x_/max)
  muestra["Z"] = tf.cast(datos,dtype=tf.float64)

  muestras_objetivo = muestra.copy()

  muestra["BDADDR"] = muestra["BDADDR"] / muestra["BDADDR"].max()
  muestra["CLK"] = muestra["CLK"] / muestra["CLK"].max()

  muestras_objetivo.pop("BDADDR")
  muestras_objetivo.pop("CLK")
  muestra.pop("Z")

  muestra["CLK"] = tf.constant(muestra["CLK"],dtype=tf.uint64)
  muestra["BDADDR"] = tf.constant(muestra["BDADDR"],dtype=tf.uint64)

  return [muestra,muestras_objetivo]





modelo = tf.keras.Sequential([
    tf.keras.layers.Dense(10),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(2)
])

informacion = cargar_datos(1)
muestra_entrenamiento = informacion[0]
objetivo = informacion[1]

modelo.compile(loss='mean_squared_error',optimizer= tf.optimizers.Adam(clipnorm=0.001),metrics=['accuracy'])
history = modelo.fit(muestra_entrenamiento,objetivo,epochs=1,validation_split=0.30,batch_size=32)

informacion = cargar_datos(2)
muestra_entrenamiento = informacion[0]
objetivo = informacion[1]

pyplot.title('Loss / Mean Squared Error')
pyplot.plot(history.history['loss'],label='train')
pyplot.plot(history.history['val_loss'],label='test')
pyplot.legend()
pyplot.show()
modelo.summary()
print("-------------")
print(modelo.layers[0].weights)
# modelo.save_weights("./guardados/save1")


