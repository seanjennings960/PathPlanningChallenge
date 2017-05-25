import numpy as np
import matplotlib.pyplot as plt
import math
from func.CurveObst import *
from func.findPath_wCurves import *
from func.plotting import *
from func.extractVisGraph import *

def func1(x):                       #Define functions for Obstacle O1
    return -x+3*math.sin(2*x)-4
def func2(x):
    return -20
x = np.linspace(-10,10,100)
O1 = CurveObst(func1,func2,x)

def func1(x):                       #Define Function for Obstacle O2
    return 20
def func2(x):
    return -x+3*math.sin(2*x)+4
O2 = CurveObst(func1,func2,x)

def func1(x):                       #Defin Functions for Obstacle O3
    return math.sqrt(1-x**2)
def func2(x):
    return -math.sqrt(1-x**2)
x = np.linspace(-1,1)
O3 = CurveObst(func1,func2,x)



CurveObstList = [O1,O2,O3]


posStart = np.array([-15,20])
posGoal = np.array([20,-20])

(path,pathDist) = findPath_wCurves([],CurveObstList,posStart,posGoal)
plt.figure(1)
plotAll_wCurves([],CurveObstList,posStart,posGoal,path)

plt.show()
