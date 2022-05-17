import torch
import torch.nn as nn

model = torch.load("modelo.pth")
print (model)

for param in model.parameters():
  print(param.data)