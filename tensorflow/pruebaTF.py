import os
from pyparsing import match_previous_literal
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from autokeras import StructuredDataRegressor
import tensorflow as tf
import pandas as pd
import numpy as np
from matplotlib import pyplot
from keras.models import load_model
from sklearn.model_selection import train_test_split

def cargar_datos(numero):
  pd.set_option('display.max_columns',None)
  muestra = pd.read_csv("ML/diccionario/partes_original/muestra1.csv")
  for x in range (2,numero+1):
    muestra_aux = pd.read_csv("ML/diccionario/partes_original/muestra{}.csv".format(x))
    muestra = muestra.append(muestra_aux)
  
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
    tf.keras.layers.InputLayer(input_shape=(2)),
    tf.keras.layers.LayerNormalization(axis=1),
    tf.keras.layers.Dense(512,activation="linear"),
    tf.keras.layers.BatchNormalization(axis=-1,center=True,epsilon=0.000001,momentum=0.80),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(0.8),
    tf.keras.layers.Dense(512,activation='linear'),
    tf.keras.layers.BatchNormalization(epsilon=0.01,momentum=0.70),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(32,activation='linear'),
    tf.keras.layers.BatchNormalization(epsilon=0.01,momentum=0.70),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1,activation='sigmoid'),
])

informacion = cargar_datos(1)
muestra_entrenamiento = informacion[0]
objetivo = informacion[1]

X_train, X_test, y_train, y_test =train_test_split(muestra_entrenamiento,objetivo,test_size=0.1,random_state=1)
modelo.compile(loss='binary_crossentropy',optimizer= tf.optimizers.Adam(clipnorm=0.001))
history = modelo.fit(x=X_train,y=y_train,validation_data=(X_test,y_test),epochs=10,batch_size=10)
tf.keras.utils.plot_model(modelo,to_file="tmp1.png",show_shapes=True,show_layer_names=True,show_layer_activations=True)

pyplot.title('Loss / Mean Squared Error')
pyplot.plot(history.history['loss'],label='train')
pyplot.plot(history.history['val_loss'],label='test')
pyplot.legend()
pyplot.show()
modelo.summary()
scores = modelo.evaluate(X_train, y_train)
print("%s: %.2f%%" % (modelo.metrics_names[1], scores[1]*100))
# model.save('./guardados/save.tf')
# print("-------------")
# print(modelo.layers[0].weights)
# modelo.save_weights("./guardados/save1")


