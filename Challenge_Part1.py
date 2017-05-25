import numpy as np
import matplotlib as plt
from func.findPath import findPath
from func.plotting import plotAll

P1 = np.array([[0,0],[0,-1],[2,-2],[.9,.25],[0.5,1],[-1,0]])
P2 = np.array([[2,3],[2,2],[3,3]])
P3 = np.array([[3,0],[4,0],[4,1],[3,1]])
P4 = np.array([[-4,-4],[6,-4],[6,3],[3.3,3],[3.3,1.5],[5,1.5],[5,-3],[-3,-3],[-3,4],[8,4],[8,5],[-4,5]])
ObstacleList = [P1,P2,P3,P4]
posStart = np.array([-1,-1])
posGoal = np.array([-5,-5])

plotAll(ObstacleList, posStart, posGoal,[])


(path,pathDist) = findPath(ObstacleList,posStart,posGoal)

print('Distance of path is: {}'.format(pathDist))
plotAll(ObstacleList, posStart, posGoal, path)


