from func.extractVisGraph import *
from func.Dijkstra import Dijkstra

def findPath(ObstacleList,posStart,posGoal):
    '''
    Finds shortest path and path distance of given environment
    Inputs: ObstacleList is list of polygonal obstacles [P1,P2,...]
            with Pi a 2d array of vertices coordinates in CCW order
            posStart and posGoal are 1d arrays with x and y coordinates of start and goal positions
    Output: path is 2d array [[x0,y0],[x1,y1],...] of order coordinates in shortest path
            pathDist is the total distance of the path
    '''
    
    (V,E,w) = extractVisGraph(ObstacleList)

    V = addStartAndGoalToGraph(posStart,posGoal,V,E,w,ObstacleList)

    (path,pathDist) = Dijkstra(V,E,w)
    return (path,pathDist)

