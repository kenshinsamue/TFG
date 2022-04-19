Pruebas de MSE 

Figure_1 

model = nn.Sequential(
  nn.Linear(n_inputs,100),
  nn.ReLU(),
  nn.Dropout(p=0.2),
  nn.Linear(100,n_outputs),
  nn.ReLU()
)

resultados :

epoch: 50, loss = 40.9088, validation_loss = 24.9788
epoch: 100, loss = 34.9772, validation_loss = 22.7380
epoch: 150, loss = 33.4483, validation_loss = 22.4822
epoch: 200, loss = 32.8654, validation_loss = 22.3980
epoch: 250, loss = 32.6454, validation_loss = 22.3569
epoch: 300, loss = 32.5020, validation_loss = 22.3629
epoch: 350, loss = 32.4345, validation_loss = 22.3350
epoch: 400, loss = 32.3826, validation_loss = 22.3357
epoch: 450, loss = 32.3143, validation_loss = 22.3217
epoch: 500, loss = 32.2270, validation_loss = 22.3098
epoch: 550, loss = 32.1899, validation_loss = 22.3339
epoch: 600, loss = 32.1242, validation_loss = 22.3185
epoch: 650, loss = 32.0358, validation_loss = 22.2897
epoch: 700, loss = 31.9505, validation_loss = 22.2749
epoch: 750, loss = 31.8995, validation_loss = 22.2800
epoch: 800, loss = 31.8478, validation_loss = 22.2728
epoch: 850, loss = 31.7363, validation_loss = 22.2644
epoch: 900, loss = 31.6664, validation_loss = 22.2423
epoch: 950, loss = 31.5782, validation_loss = 22.2267
epoch: 1000, loss = 31.5199, validation_loss = 22.2405




----------------------------------------------------------

Figure_2

model = nn.Sequential(
  nn.Linear(n_inputs,500),
  nn.ReLU(),
  nn.Dropout(p=0.2),
  nn.Linear(500,n_outputs),
  nn.ReLU()
)

epoch: 50, loss = 28.4592, validation_loss = 22.9237
epoch: 100, loss = 26.7790, validation_loss = 22.4231
epoch: 150, loss = 26.2564, validation_loss = 22.3296
epoch: 200, loss = 26.6128, validation_loss = 22.5104
epoch: 250, loss = 25.8510, validation_loss = 22.3075
epoch: 300, loss = 26.2741, validation_loss = 23.5247
epoch: 350, loss = 25.6637, validation_loss = 22.3087
epoch: 400, loss = 25.5987, validation_loss = 22.2830
epoch: 450, loss = 25.9617, validation_loss = 22.7147
epoch: 500, loss = 25.5134, validation_loss = 22.2514
epoch: 550, loss = 25.4920, validation_loss = 22.2617
epoch: 600, loss = 25.6116, validation_loss = 22.5309
epoch: 650, loss = 25.4411, validation_loss = 22.2731
epoch: 700, loss = 26.6564, validation_loss = 23.7320
epoch: 750, loss = 25.3791, validation_loss = 22.2279
epoch: 800, loss = 25.3671, validation_loss = 22.2218
epoch: 850, loss = 25.6915, validation_loss = 22.2760
epoch: 900, loss = 25.2939, validation_loss = 22.2234
epoch: 950, loss = 26.8962, validation_loss = 22.8048
epoch: 1000, loss = 25.2595, validation_loss = 22.2041


------------------------------------------------------
Figure 3

model = nn.Sequential(
  nn.Linear(n_inputs,250),
  nn.ReLU(),
  nn.Dropout(p=0.2),
  nn.Linear(250,250),
  nn.ReLU(),
  nn.Dropout(p=0.2),
  nn.Linear(250,n_outputs),
  nn.ReLU()
)
epoch: 50, loss = 41.5841, validation_loss = 23.8710
epoch: 100, loss = 37.7526, validation_loss = 22.5480
epoch: 150, loss = 36.6879, validation_loss = 22.3906
epoch: 200, loss = 37.3478, validation_loss = 25.3995
epoch: 250, loss = 35.0604, validation_loss = 22.4842
epoch: 300, loss = 34.8556, validation_loss = 23.2263
epoch: 350, loss = 39.0951, validation_loss = 30.4782
epoch: 400, loss = 38.1783, validation_loss = 31.8069
epoch: 450, loss = 33.7314, validation_loss = 24.9506
epoch: 500, loss = 32.6984, validation_loss = 22.9188
epoch: 550, loss = 32.1513, validation_loss = 26.9953
epoch: 600, loss = 30.9146, validation_loss = 24.2991
epoch: 650, loss = 30.8296, validation_loss = 23.1460
epoch: 700, loss = 30.1805, validation_loss = 25.9194
epoch: 750, loss = 30.0104, validation_loss = 25.9754
epoch: 800, loss = 29.8616, validation_loss = 25.8603
epoch: 850, loss = 30.0012, validation_loss = 28.2938
epoch: 900, loss = 29.6365, validation_loss = 25.4281
epoch: 950, loss = 29.5788, validation_loss = 24.9391
epoch: 1000, loss = 29.4905, validation_loss = 27.3784

-----------------------------------------------------

Figura 4

model = nn.Sequential(
  nn.Linear(n_inputs,50),
  nn.ReLU(),
  nn.Dropout(p=0.2),
  nn.Linear(50,50),
  nn.ReLU(),
  nn.Dropout(p=0.2),
  nn.Linear(50,n_outputs),
  nn.ReLU()
)

epoch: 50, loss = 56.0074, validation_loss = 28.3822
epoch: 100, loss = 43.8924, validation_loss = 43.5664
epoch: 150, loss = 38.8531, validation_loss = 55.2165
epoch: 200, loss = 35.8038, validation_loss = 58.6808
epoch: 250, loss = 34.1330, validation_loss = 55.2884
epoch: 300, loss = 33.3347, validation_loss = 58.4775
epoch: 350, loss = 33.7245, validation_loss = 72.2404
epoch: 400, loss = 31.9681, validation_loss = 59.8823
epoch: 450, loss = 31.5992, validation_loss = 58.5228
epoch: 500, loss = 31.9935, validation_loss = 52.7426
epoch: 550, loss = 31.0615, validation_loss = 59.2857
epoch: 600, loss = 31.4746, validation_loss = 64.0645
epoch: 650, loss = 30.6441, validation_loss = 60.0802
epoch: 700, loss = 30.8779, validation_loss = 50.4674
epoch: 750, loss = 30.3965, validation_loss = 61.3812
epoch: 800, loss = 30.2426, validation_loss = 61.2737
epoch: 850, loss = 30.2604, validation_loss = 53.8787
epoch: 900, loss = 30.0503, validation_loss = 56.0366
epoch: 950, loss = 29.9187, validation_loss = 55.5170
epoch: 1000, loss = 30.8079, validation_loss = 65.4861