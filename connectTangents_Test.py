import numpy as np
import matplotlib.pyplot as plt
from func.CurveObst import *
import math


    #Test Case 1: Parabola

x = np.linspace(-5,5)
n = len(x)
y = np.zeros(n)
for i in range(n):
    y[i] = -x[i]**2+15

plt.figure(1)
plt.fill(x,y)


P = connectTangents(x,y,3)
##print(P)
plt.plot(P[:,0],P[:,1],'r')


    #Test Case 2: Circle

x = np.linspace(-5,5,300)
n = len(x)
y1 = np.zeros(n)
y2 = np.zeros(n)
for i in range(n):
    y1[i] = math.sqrt(25-x[i]**2)
    y2[i] = -math.sqrt(25-x[i]**2)

plt.figure(2)

num_div = 3
i_start = 0
i_end = 3
P1 = connectTangents(x[::-1],y1[::-1],num_div)
P2 = connectTangents(x,y2,num_div)
P = np.append(P1,P2,axis=0)
##print('This is P from connnect Tangents: ',P)
##print('P is done')
plt.fill(P[:,0],P[:,1])
plt.plot(x,y1,'r',x,y2,'r')


num_div = 3
P1 = connectDirect(x,y2,num_div)
P2 = connectDirect(x[::-1],y1[::-1],num_div)
P = np.append(P1,P2,axis=0)
plt.fill(P[:,0],P[:,1],'k')


plt.show()
