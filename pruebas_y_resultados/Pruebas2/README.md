
1 dataset
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

epoch: 50, loss = 0.693386, validation_loss = 0.693150
epoch: 100, loss = 0.693216, validation_loss = 0.693148
epoch: 150, loss = 0.693174, validation_loss = 0.693150
epoch: 200, loss = 0.693157, validation_loss = 0.693153
epoch: 250, loss = 0.693142, validation_loss = 0.693155
epoch: 300, loss = 0.693131, validation_loss = 0.693159
epoch: 350, loss = 0.693122, validation_loss = 0.693163
epoch: 400, loss = 0.693117, validation_loss = 0.693167
epoch: 450, loss = 0.693112, validation_loss = 0.693169
epoch: 500, loss = 0.693107, validation_loss = 0.693171
epoch: 550, loss = 0.693105, validation_loss = 0.693175
epoch: 600, loss = 0.693101, validation_loss = 0.693176
epoch: 650, loss = 0.693099, validation_loss = 0.693178
epoch: 700, loss = 0.693099, validation_loss = 0.693179
epoch: 750, loss = 0.693095, validation_loss = 0.693179
epoch: 800, loss = 0.693095, validation_loss = 0.693181
epoch: 850, loss = 0.693094, validation_loss = 0.693182
epoch: 900, loss = 0.693093, validation_loss = 0.693184
epoch: 950, loss = 0.693091, validation_loss = 0.693183
epoch: 1000, loss = 0.693088, validation_loss = 0.693185

---------------------------------------------------------

