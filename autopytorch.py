from pickletools import optimize
import torch
import torch.utils.data as data
import torch.nn as nn
import numpy as np
import csv
from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split

from autoPyTorch.api.tabular_classification import TabularClassificationTask

import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics





path = "diccionarios/partes/muestra1_hex_.csv"
dataset = pd.read_csv(path,skiprows=0,dtype=np.float32)

# *------------- Separacion entre los datasets de inputs/outputs ------------------*
headers = []
for x in range(32):
  headers.append("Z{}".format(x))

resultados=[]
for x in headers:
  resultados.append(dataset.pop(x)) 
result = pd.concat(resultados,axis=1,keys=headers)
# *------------- /Separacion entre los datasets de inputs/outputs ------------------*
# *------------- Conversion a un dataset de pytorch ------------------*
x = pd.DataFrame(dataset).to_numpy(dtype=np.float32)
y = pd.DataFrame(result).to_numpy(dtype=np.float32)


del(headers)
del(resultados)
del(result)


# x = torch.from_numpy(x)
# y = torch.from_numpy(y)
# *------------- /Conversion a un dataset de pytorch ------------------*
# *------------- Normalizacion ------------------*
# x_mean = torch.mean(x,dim=0)
# x_data_var = torch.var(x,dim=0)

# y_mean = torch.mean(y,dim=0)
# y_data_var = torch.var(y,dim=0)

# x = (x+x_data_var)+x_mean
# y = (y+y_data_var)+y_mean

# *------------- /Normalizacion ------------------*
# *------------- Separacion de datos en entrenamiento y prueba ------------------*
X_train, X_test, y_train, y_test =train_test_split(x,y,test_size=0.2, train_size=0.8,random_state=1)

n_samples,n_inputs = X_train.shape
n_outputs = y_train.shape[1]
# *------------- /Separacion de datos en entrenamiento y prueba ------------------*

del(x)
del(y)


api = TabularClassificationTask()

api.search(
    X_train=X_train,
    y_train=y_train,
    X_test=X_test,
    y_test=y_test,
    optimize_metric='accuracy',
    total_walltime_limit=300,
    func_eval_time_limit_secs=50
)
y_pred = api.predict(X_test)
score = api.score(y_pred, y_test)
print("Accuracy score", score)
print(api.show_models())
