import numpy as np
import matplotlib.pyplot as plt

def plotSegment(p1,p2,color=None):
    '''
    Plots a segment between p1 and p2
    Inputs: p1 and p2 as numpy arrays
            color (optional) as input to plot function
    Output: None
    '''
    if color is None:
        plt.plot([p1[0],p2[0]],[p1[1],p2[1]])
    else:
        plt.plot([p1[0],p2[0]],[p1[1],p2[1]],color)

def plotVisGraph(V,E):
    '''
    Plots segments between all the nodes which are visible
    Inputs: V is a 2D numpy array with V = [[x0,y0],[x1,y1],...,[xn,yn]]
            where [xi,yi] are the x and y coordinates of node i
            E is an adjacency dictionary E where E[i] is a list of node indices [j,k,...] connected to node i
    Output: None
    '''
    
    n = np.size(V,axis=0) #number of convex nodes
    for i in range(n):
        node1 = V[i,:]
        visEdges = E[i]             #list of visible edges
        for j in visEdges:
            if j>i:                 #each edge is listed twice
                node2 = V[j,:]      #only plot the first time
                plotSegment(node1,node2,'r')



def plotAll(ObstacleList,pos_start,pos_goal,path):
    '''
    Plots obstacles, start and goal positions, and path
    Inputs: ObstacleList is a list of polygons [P1,P2,...] where each polygon P is a 2D array of vertices in CCW order
            pos_start is a 1d array of the x and y coordinates of the start position
            pos_goal is a 1d array of the x and y coordinates of the goal position
            path is a 2d array which is a list of the points between the start and the goal
    ''' 

    #plot start and end positions
    start = plt.plot(pos_start[0],pos_start[1],'rx')
    goal = plt.plot(pos_goal[0],pos_goal[1],'ro')
    #plot path if path is not empty
    if np.size(path)>0: 
        plt.plot(path[:,0],path[:,1],'k')
    plotObstacles(ObstacleList)
    plt.legend(['Start Position','Goal Position'],loc=4)
    plt.show()



def plotObstacles(ObstacleList):
    '''
    Plots all obstacles in ObstacleList
    Inputs: ObstacleList is a list of polygons [P1,P2,...] where each polygon P is a 2D array of vertices in CCW order
    '''

    n = len(ObstacleList)
    for i in range(n):
        P = ObstacleList[i]
        plt.fill(P[:,0],P[:,1],'b')


def plotAll_wCurves(ObstacleList,CurveObstList,posStart,posGoal,path):
    '''
    Plots obstacles, start and goal positions, and path
    Inputs: ObstacleList is a list of polygons [P1,P2,...] where each polygon P is a 2D array of vertices in CCW order
            pos_start is a 1d array of the x and y coordinates of the start position
            pos_goal is a 1d array of the x and y coordinates of the goal position
            path is a 2d array which is a list of the points between the start and the goal
    ''' 

    #plot start and end positions
    plt.plot(posStart[0],posStart[1],'bx')
    plt.plot(posGoal[0],posGoal[1],'ro')
    #plot path if path is not empty
    if np.size(path)>0: 
        plt.plot(path[:,0],path[:,1],'b')
    plotObstacles(ObstacleList)
    for curveObst in CurveObstList:
        curveObst.plot()
        
    plt.show()
