# Tests plotting curve obstacles and derivative function


import numpy as np
import matplotlib.pyplot as plt
import math
from func.CurveObst import *


r = 1
x1 = -np.logspace(math.log(r+1,10),0)+r+1
x2 = np.logspace(0,math.log(r+1,10),endpoint=False)-r-1
x = np.concatenate((x2,x1))
def func1(x):
    return math.sqrt(r**2-x**2)

def func2(x):
    return -math.sqrt(r**2-x**2)

curveObst1 = CurveObst(func1,func2,x)


x = np.linspace(-10,10)
def func1(x):
    return -x+math.sin(x)-2

def func2(x):
    return -15
curveObst2 = CurveObst(func1,func2,x)


def func1(x):
    return 15

def func2(x):
    return -x+math.sin(x)+2

curveObst3 = CurveObst(func1,func2,x)
curveObstList = [curveObst2]
plt.figure(1)
plotCurveObstList(curveObstList)




    #Derivative Test on y=x**2:
    
x = np.linspace(-5,5)
n = len(x)
y = np.zeros(n)
for i in range(n):
    y[i] = -x[i]**2+15

y_prime = deriv(x,y)
y_prime2 = deriv(x,y_prime)

plt.figure(2)
##plt.plot(x,y,x,y_prime,x,y_prime2)
plt.plot(x,y)




plt.figure(3)
lines = plt.plot(x,y,x,y_prime,x,y_prime2)
labels = ['y','y_prime','y_prime2']
plt.legend(labels)





plt.show()

