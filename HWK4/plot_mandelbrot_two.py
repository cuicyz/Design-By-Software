import numpy as np
import matplotlib.pyplot as plt
def bounded_box(c):
	return ((-2.0 < c.real <2.0) and (-2.0 < c.imag < 2.0))

def bounded_circle(c):
	return abs(c) < 2.0

def mandelbrot(c,maxiteration=12,boundedfcn=bounded_box):
    z,count=0,0
    while boundedfcn(z) and count<maxiteration:
        z = z*z + c
        count += 1
    return count

X = Y = np.r_[-2.1:2.1:1001j]

XX,YY = np.meshgrid(X,X)
Z = XX+1j*YY

array_mandelbrot = np.vectorize(mandelbrot)

M = array_mandelbrot(Z)
plt.imshow(M, interpolation='nearest', cmap='jet')
plt.axis('off')       
plt.show()
