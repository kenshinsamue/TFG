BCE

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

# model = model.cuda()
# #  ------ Loss y optimizer --------

learning_rate =0.01
funcion_loss = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(),lr=learning_rate)

epoch: 50, loss = 0.693426, validation_loss = 0.693151
epoch: 100, loss = 0.693235, validation_loss = 0.693150
epoch: 150, loss = 0.693182, validation_loss = 0.693151
epoch: 200, loss = 0.693162, validation_loss = 0.693154
epoch: 250, loss = 0.693144, validation_loss = 0.693158
epoch: 300, loss = 0.693135, validation_loss = 0.693164
epoch: 350, loss = 0.693123, validation_loss = 0.693169
epoch: 400, loss = 0.693117, validation_loss = 0.693174
epoch: 450, loss = 0.693113, validation_loss = 0.693177
epoch: 500, loss = 0.693106, validation_loss = 0.693180
epoch: 550, loss = 0.693101, validation_loss = 0.693182
epoch: 600, loss = 0.693099, validation_loss = 0.693184
epoch: 650, loss = 0.693097, validation_loss = 0.693186
epoch: 700, loss = 0.693093, validation_loss = 0.693188
epoch: 750, loss = 0.693093, validation_loss = 0.693189
epoch: 800, loss = 0.693091, validation_loss = 0.693191
epoch: 850, loss = 0.693087, validation_loss = 0.693191
epoch: 900, loss = 0.693090, validation_loss = 0.693194
epoch: 950, loss = 0.693084, validation_loss = 0.693193
epoch: 1000, loss = 0.693083, validation_loss = 0.693193

----------------------------------------------

epoch: 50, loss = 55.431416, validation_loss = 55.451210
epoch: 100, loss = 55.430714, validation_loss = 55.451263
epoch: 150, loss = 55.430283, validation_loss = 55.451527
epoch: 200, loss = 55.430035, validation_loss = 55.451687
epoch: 250, loss = 55.429913, validation_loss = 55.451763
epoch: 300, loss = 55.429779, validation_loss = 55.451824
epoch: 350, loss = 55.429729, validation_loss = 55.451866
epoch: 400, loss = 55.429668, validation_loss = 55.451923
epoch: 450, loss = 55.429630, validation_loss = 55.451939
epoch: 500, loss = 55.429585, validation_loss = 55.451962
epoch: 550, loss = 55.429558, validation_loss = 55.452015
epoch: 600, loss = 55.429543, validation_loss = 55.452084
epoch: 650, loss = 55.429462, validation_loss = 55.452106
epoch: 700, loss = 55.429344, validation_loss = 55.452141
epoch: 750, loss = 55.429317, validation_loss = 55.452213
epoch: 800, loss = 55.429199, validation_loss = 55.452225
epoch: 850, loss = 55.429199, validation_loss = 55.452259
epoch: 900, loss = 55.429058, validation_loss = 55.452324
epoch: 950, loss = 55.429089, validation_loss = 55.452324
epoch: 1000, loss = 55.428921, validation_loss = 55.452385