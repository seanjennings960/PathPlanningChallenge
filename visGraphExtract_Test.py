import numpy as np
import matplotlib.pyplot as plt
from func.extractVisGraph import *
from func.plotting import *

def convex_Test(P):
    n = np.size(P,axis=0)
    for i in range(n):
        c = convex(P,i)
        if c:
            print('Point ({},{}) is convex'.format(P[i,0],P[i,1]))
        else:
            print('Point ({},{}) is not convex'.format(P[i,0],P[i,1]))


P1 = np.array([[0,0],[0,-1],[1,0],[.9,.25],[0.5,1],[-1,0]])
P2 = np.array([[2,3],[2,2],[3,3]])
P3 = np.array([[3,0],[4,0],[4,1],[3,1]])
ObstacleList = [P1,P2,P3]
plotObstacles(ObstacleList)

convex_Test(P1)
point1 = np.array([-1,0])
point2 = np.array([0.5,1])
plt.plot(point1[0],point1[1],'rx')
plt.plot(point2[0],point2[1],'rx')
vis = visible(point1,point2,ObstacleList)
if vis:
    plotSegment(point1,point2,'r')
    print('Points are visible')
else:
    print('Points are not visible')


(V,E,w) = extractVisGraph(ObstacleList)
print(V)

plotVisGraph(V,E)


plt.show()
