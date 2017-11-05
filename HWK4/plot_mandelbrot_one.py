# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:52:11 2016

@author: richardbrower

Documentation
"""
import numpy as np, matplotlib.pyplot as plt
max_iterations = 32
x_min, x_max = -2.5, 1.5
y_min, y_max = -1.5, 1.5
ds = 0.002

X = np.arange(x_min, x_max + ds, ds)
Y = np.arange(y_min, y_max + ds, ds)
data = np.zeros(  (X.size, Y.size), dtype='uint')

for i in range(X.size):
    for j in range(Y.size):
        x0, y0 = X[i], Y[j]
        x, y = x0, y0
        count = 0
        while count < max_iterations:
            x, y = (x0 + x*x - y*y, y0 + 2*x*y)
            if (x*x + y*y) > 4.0: break
            count += 1
        data[i, j] = max_iterations - count
 
plt.imshow(data.transpose(), interpolation='nearest', cmap='jet')
plt.axis('off')       
plt.show()
