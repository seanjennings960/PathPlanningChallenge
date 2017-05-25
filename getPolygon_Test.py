import numpy as np
import matplotlib.pyplot as plt
from func.CurveObst import *
import math


def func1(x):
    return 1/3*x**2+3

def func2(x):
    return math.sin(x)-3

x = np.linspace(-2*math.pi,2*math.pi)

curveObst1 = CurveObst(func1,func2,x)


x = np.linspace(10,16)

def func1(x):
    return 8

def func2(x):
    return math.sqrt(9-(x-13)**2)

O2 = CurveObst(func1,func2,x)

def func1(x):
    return 40
def func2(x):
    return -x+math.sin(x)+25
x = np.linspace(-10,10)
O3 = CurveObst(func1,func2,x)

def func1(x):
    return math.sqrt(9-x**2)+15
def func2(x):
    return -math.sqrt(9-x**2)+15
x = np.linspace(-3,3)
O4 = CurveObst(func1,func2,x)


##curveObst1.evalYvals()
##(i_change,concaveUp,allZero) = concavityChange(curveObst1.x,curveObst1.y2)
##for i in range(len(i_change)):
##    if concaveUp[i]:
##        plt.plot(curveObst1.x[i_change[i]],curveObst1.y2[i_change[i]],'x')
##    else:
##        plt.plot(curveObst1.x[i_change[i]],curveObst1.y2[i_change[i]],'o')

P = getPolygon(curveObst1,3)
plt.plot(P[:,0],P[:,1],'k')
curveObst1.plot()

P = getPolygon(O2,3)
plt.plot(P[:,0],P[:,1],'k')
O2.plot()

P = getPolygon(O3,3)
plt.plot(P[:,0],P[:,1],'k')
O3.plot()

P = getPolygon(O4,3)
plt.plot(P[:,0],P[:,1],'k')
O4.plot()
plt.show()
