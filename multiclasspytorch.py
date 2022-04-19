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


path = "diccionarios/partes/binario/muestra1_bin_.csv"
dataset = pd.read_csv(path,skiprows=0,dtype=np.float32)
# aux_ds = pd.read_csv("diccionarios/partes/binario/muestra2_bin_.csv",skiprows=0,dtype=np.float32)
# dataset = dataset.append(aux_ds)
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


x = torch.from_numpy(x)
y = torch.from_numpy(y)
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


# #  ---------- Modelo --------------

model = nn.Sequential(
  nn.Linear(n_inputs,100),
  nn.Tanh(),
  nn.Dropout(p=0.5),
  nn.Linear(100,100),
  nn.Tanh(),
  nn.Dropout(p=0.2),
  nn.Linear(100,200),
  nn.Tanh(),
  nn.Dropout(p=0.2),
  nn.Linear(200,n_outputs),
  nn.Sigmoid()
)

# #  ------ Loss y optimizer --------

learning_rate =0.01
funcion_loss = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

num_epoch = 1000

valid_loss =0.0
val_loss_array=[]
loss_array=[]

for epoch in range(num_epoch):
  # fordward y calcula el loss
  y_predicted = model(X_train)
  loss = funcion_loss(y_predicted,y_train)
  # back propagation 
  loss.backward()
  # # actualizacion
  optimizer.step()
  # optimizer.zero_grad()
  
#   model.eval()
#   target = model(X_test)
#   loss_t = funcion_loss(target,y_test)
#   loss_array.append(loss.item())
#   val_loss_array.append(loss_t.item())
#   model.train()

#   if(epoch+1)%50 == 0:
#     print(f'epoch: {epoch+1}, loss = {loss.item():.6f}, validation_loss = {loss_t.item():.6f}')


# # MAC0,MAC1,MAC2,MAC3,MAC4,MAC5,MAC6,MAC7,MAC8,MAC9,MAC10,MAC11,CLK0,CLK1,CLK2,CLK3,CLK4,CLK5,CLK6,CLK7,Z0,Z1,Z2,Z3,Z4,Z5,Z6,Z7,Z8,Z9,Z10,Z11,Z12,Z13,Z14,Z15,Z16,Z17,Z18,Z19,Z20,Z21,Z22,Z23,Z24,Z25,Z26,Z27,Z28,Z29,Z30,Z31
# # 4   ,5   ,0   ,15  ,4   ,6   ,9   ,8   ,14  ,4   ,14   ,3    ,11  ,4   ,7   ,0   ,4   ,5   ,1   ,2   ,7,8,5,14,9,4,10,7,2,15,6,3,2,8,5,6,2,11,0,5,5,6,12,11,9,15,9,7,11,14,0,3

# # inputs_ = torch.tensor([4   ,5   ,0   ,15  ,4   ,6   ,9   ,8   ,14  ,4   ,14   ,3    ,11  ,4   ,7   ,0   ,4   ,5   ,1   ,2 ],dtype=torch.float32)
# # resultados = torch.tensor([7,8,5,14,9,4,10,7,2,15,6,3,2,8,5,6,2,11,0,5,5,6,12,11,9,15,9,7,11,14,0,3],dtype=torch.float32)

# # estimados = model(inputs_)

# # print (estimados)
# # print(resultados)
# plt.title('Loss / MSE')
# plt.plot(loss_array,label='train')
# plt.plot(val_loss_array,label='test')
# plt.legend()
# plt.show()