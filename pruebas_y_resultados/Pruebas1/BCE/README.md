Figure_1

model = nn.Sequential(
  nn.Linear(n_inputs,100),
  nn.ReLU(),
  nn.Dropout(p=0.1),
  nn.Linear(100,n_outputs),
  nn.Sigmoid()
)

epoch: 50, loss = 0.693150, validation_loss = 0.693151
epoch: 100, loss = 0.693147, validation_loss = 0.693147
epoch: 150, loss = 0.693146, validation_loss = 0.693147
epoch: 200, loss = 0.693147, validation_loss = 0.693147
epoch: 250, loss = 0.693146, validation_loss = 0.693147
epoch: 300, loss = 0.693146, validation_loss = 0.693147
epoch: 350, loss = 0.693146, validation_loss = 0.693147
epoch: 400, loss = 0.693146, validation_loss = 0.693147
epoch: 450, loss = 0.693146, validation_loss = 0.693147
epoch: 500, loss = 0.693146, validation_loss = 0.693147
epoch: 550, loss = 0.693146, validation_loss = 0.693147
epoch: 600, loss = 0.693146, validation_loss = 0.693147
epoch: 650, loss = 0.693145, validation_loss = 0.693147
epoch: 700, loss = 0.693144, validation_loss = 0.693148
epoch: 750, loss = 0.693143, validation_loss = 0.693148
epoch: 800, loss = 0.693143, validation_loss = 0.693148
epoch: 850, loss = 0.693142, validation_loss = 0.693149
epoch: 900, loss = 0.693142, validation_loss = 0.693150
epoch: 950, loss = 0.693142, validation_loss = 0.693150
epoch: 1000, loss = 0.693141, validation_loss = 0.693150

-----------------------------------------------------------

Figure_2

model = nn.Sequential(
  nn.Linear(n_inputs,100),
  nn.Dropout(p=0.1),
  nn.Linear(100,n_outputs),
  nn.Sigmoid()
)

epoch: 50, loss = 0.693492, validation_loss = 0.693362
epoch: 100, loss = 0.693219, validation_loss = 0.693225
epoch: 150, loss = 0.693173, validation_loss = 0.693219
epoch: 200, loss = 0.693142, validation_loss = 0.693220
epoch: 250, loss = 0.693122, validation_loss = 0.693222
epoch: 300, loss = 0.693109, validation_loss = 0.693223
epoch: 350, loss = 0.693095, validation_loss = 0.693225
epoch: 400, loss = 0.693090, validation_loss = 0.693226
epoch: 450, loss = 0.693081, validation_loss = 0.693227
epoch: 500, loss = 0.693077, validation_loss = 0.693228
epoch: 550, loss = 0.693070, validation_loss = 0.693228
epoch: 600, loss = 0.693067, validation_loss = 0.693229
epoch: 650, loss = 0.693066, validation_loss = 0.693230
epoch: 700, loss = 0.693065, validation_loss = 0.693231
epoch: 750, loss = 0.693064, validation_loss = 0.693231
epoch: 800, loss = 0.693061, validation_loss = 0.693231
epoch: 850, loss = 0.693060, validation_loss = 0.693231
epoch: 900, loss = 0.693058, validation_loss = 0.693232
epoch: 950, loss = 0.693059, validation_loss = 0.693232
epoch: 1000, loss = 0.693058, validation_loss = 0.693232
------------------------------------------------------------
Figure_3


model = nn.Sequential(
  nn.Linear(n_inputs,100),
  nn.Linear(100,100),
  nn.Dropout(p=0.2),
  nn.Linear(100,n_outputs),
  nn.Sigmoid()
)

epoch: 50, loss = 0.693467, validation_loss = 0.693357
epoch: 100, loss = 0.693238, validation_loss = 0.693214
epoch: 150, loss = 0.693181, validation_loss = 0.693199
epoch: 200, loss = 0.693145, validation_loss = 0.693197
epoch: 250, loss = 0.693127, validation_loss = 0.693199
epoch: 300, loss = 0.693113, validation_loss = 0.693201
epoch: 350, loss = 0.693099, validation_loss = 0.693204
epoch: 400, loss = 0.693090, validation_loss = 0.693207
epoch: 450, loss = 0.693087, validation_loss = 0.693210
epoch: 500, loss = 0.693082, validation_loss = 0.693213
epoch: 550, loss = 0.693074, validation_loss = 0.693216
epoch: 600, loss = 0.693074, validation_loss = 0.693218
epoch: 650, loss = 0.693074, validation_loss = 0.693220
epoch: 700, loss = 0.693069, validation_loss = 0.693221
epoch: 750, loss = 0.693069, validation_loss = 0.693221
epoch: 800, loss = 0.693066, validation_loss = 0.693222
epoch: 850, loss = 0.693067, validation_loss = 0.693224
epoch: 900, loss = 0.693065, validation_loss = 0.693224
epoch: 950, loss = 0.693063, validation_loss = 0.693223
epoch: 1000, loss = 0.693061, validation_loss = 0.693225
------------------------------------------------------------

model = nn.Sequential(
  nn.Linear(n_inputs,200),
  nn.ReLU(),
  nn.Dropout(p=0.2),
  nn.Linear(200,n_outputs),
  nn.Sigmoid()
)

epoch: 50, loss = 0.693825, validation_loss = 0.693595
epoch: 100, loss = 0.693329, validation_loss = 0.693258
epoch: 150, loss = 0.693275, validation_loss = 0.693235
epoch: 200, loss = 0.693241, validation_loss = 0.693233
epoch: 250, loss = 0.693212, validation_loss = 0.693232
epoch: 300, loss = 0.693187, validation_loss = 0.693232
epoch: 350, loss = 0.693175, validation_loss = 0.693233
epoch: 400, loss = 0.693157, validation_loss = 0.693232
epoch: 450, loss = 0.693147, validation_loss = 0.693233
epoch: 500, loss = 0.693129, validation_loss = 0.693232
epoch: 550, loss = 0.693120, validation_loss = 0.693233
epoch: 600, loss = 0.693108, validation_loss = 0.693233
epoch: 650, loss = 0.693103, validation_loss = 0.693233
epoch: 700, loss = 0.693100, validation_loss = 0.693233
epoch: 750, loss = 0.693090, validation_loss = 0.693233
epoch: 800, loss = 0.693085, validation_loss = 0.693234
epoch: 850, loss = 0.693079, validation_loss = 0.693233
epoch: 900, loss = 0.693079, validation_loss = 0.693233
epoch: 950, loss = 0.693075, validation_loss = 0.693234
epoch: 1000, loss = 0.693071, validation_loss = 0.693234

vs 

model = nn.Sequential(
  nn.Linear(n_inputs,200),
  nn.Tanh(),
  nn.Dropout(p=0.2),
  nn.Linear(200,n_outputs),
  nn.Sigmoid()
)
epoch: 50, loss = 0.694138, validation_loss = 0.693427
epoch: 100, loss = 0.693354, validation_loss = 0.693224
epoch: 150, loss = 0.693215, validation_loss = 0.693221
epoch: 200, loss = 0.693164, validation_loss = 0.693222
epoch: 250, loss = 0.693124, validation_loss = 0.693222
epoch: 300, loss = 0.693108, validation_loss = 0.693222
epoch: 350, loss = 0.693091, validation_loss = 0.693224
epoch: 400, loss = 0.693081, validation_loss = 0.693224
epoch: 450, loss = 0.693075, validation_loss = 0.693225
epoch: 500, loss = 0.693070, validation_loss = 0.693225
epoch: 550, loss = 0.693068, validation_loss = 0.693226
epoch: 600, loss = 0.693066, validation_loss = 0.693226
epoch: 650, loss = 0.693062, validation_loss = 0.693227
epoch: 700, loss = 0.693060, validation_loss = 0.693227
epoch: 750, loss = 0.693061, validation_loss = 0.693227
epoch: 800, loss = 0.693060, validation_loss = 0.693228
epoch: 850, loss = 0.693059, validation_loss = 0.693229
epoch: 900, loss = 0.693059, validation_loss = 0.693228
epoch: 950, loss = 0.693059, validation_loss = 0.693228
epoch: 1000, loss = 0.693059, validation_loss = 0.693230

------------------------------------------------