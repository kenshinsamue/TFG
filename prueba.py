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

device = torch.cuda.device(0)
path = "diccionario/prueba.csv"
dataset = pd.read_csv(path,skiprows=0,dtype=np.float32)

resultados = dataset.pop('e')

x = pd.DataFrame(dataset).to_numpy(dtype=np.float32)
y = pd.DataFrame(resultados).to_numpy(dtype=np.float32)

x = torch.from_numpy(x)
y = torch.from_numpy(y)

x = x.cuda()
y = y.cuda()


X_train, X_test, y_train, y_test =train_test_split(x,y,test_size=0.2, train_size=0.8,random_state=1)

n_samples,n_inputs = X_train.shape
n_outputs = y_train.shape[1]

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

model = model.cuda()

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
  print("calculando error")
  loss = funcion_loss(y_predicted,y_train)
  # back propagation 
  print("back propagation")
  loss.backward()
  # # actualizacion
  optimizer.step()
  print ("actualizacion")
  optimizer.zero_grad()
  print("evaluando")
  model.eval()
  target = model(X_test)
  loss_t = funcion_loss(target,y_test)
  loss_array.append(loss.item())
  val_loss_array.append(loss_t.item())
  model.train()

  if(epoch+1)%50 == 0:
    print(f'epoch: {epoch+1}, loss = {loss.item():.6f}, validation_loss = {loss_t.item():.6f}')
