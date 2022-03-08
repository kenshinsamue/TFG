import os
from tabnanny import verbose
from pyparsing import match_previous_literal
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import pandas as pd
import numpy as np
from matplotlib import pyplot
from autokeras import StructuredDataRegressor
from sklearn.model_selection import train_test_split

def cargar_datos(numero):
  pd.set_option('display.max_columns',None)
  muestra = pd.read_csv("ML/diccionario/partes_original/muestra{}.csv".format(numero))
  valores_max=[]
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
  print(len(muestra))

  muestras_objetivo = muestra.copy()
  mac_max = muestra["BDADDR"].max()
  clk_max = muestra["CLK"].max()
  muestra["BDADDR"] = muestra["BDADDR"] / mac_max
  muestra["CLK"] = muestra["CLK"] / clk_max

  muestras_objetivo.pop("BDADDR")
  muestras_objetivo.pop("CLK")
  muestra.pop("Z")

  muestra["CLK"] = tf.constant(muestra["CLK"],dtype=tf.uint64)
  muestra["BDADDR"] = tf.constant(muestra["BDADDR"],dtype=tf.uint64)
  valores_max = [mac_max,clk_max,max]
  return [muestra,muestras_objetivo,valores_max]




informacion = cargar_datos(1)
muestra_entrenamiento = informacion[0]
objetivo = informacion[1]

# 4075/31711
# 26426/26426

# print (muestra_entrenamiento.shape(),objetivo.shape())
X_train, X_test, y_train, y_test =train_test_split(muestra_entrenamiento,objetivo,test_size=0.1,random_state=1)
search = StructuredDataRegressor(max_trials=15,loss='binary_crossentropy',optimizer='adam',metrics=['mse'])
model=search.export_model()

history = model.fit(x=X_train,y=y_train,epochs=10,batch_size=32,validation_data=(X_test,y_test))

# tf.keras.utils.plot_model(model,to_file="tmp.png",show_shapes=True,show_layer_names=True,show_layer_activations=True)


# pyplot.title('Loss / Mean Squared Error')
# pyplot.plot(history.history['loss'],label='train')
# pyplot.plot(history.history['val_loss'],label='test')
# pyplot.legend()
# pyplot.show()
# model.save('./guardados/save.tf')
# model.summary()
# search.fit()
# modelo.save_weights(".


