
import numpy as np

def addStartAndGoalToGraph(posStart,posGoal,V,E,w,ObstacleList):
    '''
    adds start and end positions to visibility graph G=(V,E,w)
    Inputs: posStart and posGoal are 1d arrays containing start and goal coordinates
            V is a 2D numpy array with V = [[x0,y0],[x1,y1],...,[xn,yn]]
            where [xi,yi] are the x and y coordinates of node i
            E is an adjacency dictionary E where E[i] is a list of node indices [j,k,...] connected to node i
            w is a dictionary with the keys as tuples of node indices: (i,j)
            and values w_ij corresponding to the distance between node i and node j so w[(i,j)]=w_ij
            ObstacleList is the list of polygonal obstacles P with vertices listed in CCW order
    Output: V with posStart and posGoal added

    Note: E and w objects themselves are modified so don't require output
    '''

    n = np.size(V,axis=0)
    V = np.append(V,[posStart],axis=0)
    V = np.append(V,[posGoal],axis=0)
    for i in range(n):          #for each convex vertex
        v = V[i]
        if visible(posStart,v,ObstacleList):        #if node i is visible
            addToEdgeList(n,i,E)                    #add to edge and weight list 
            addToEdgeList(i,n,E)                    
            dist = np.linalg.norm(posStart-v)
            w[(i,n)] = dist
            
        if visible(posGoal,v,ObstacleList):
            addToEdgeList(n+1,i,E)
            addToEdgeList(i,n+1,E)
            dist = np.linalg.norm(posGoal-v)
            w[(i,n+1)] = dist
            
    if visible(posStart,posGoal,ObstacleList):
        addToEdgeList(n,n+1,E)
        addToEdgeList(n+1,n,E)
        dist = np.linalg.norm(posStart-posGoal)
        w[(n,n+1)] = dist
    return V



def extractVisGraph(ObstacleList):
    '''
    returns visibility graph G=(V,E,w) of all obstacle vertices which can be connected with an unobstructed line 
    Input: ObstacleList: list of polygonal obstacles with vertices listed in CCW order
    Output: visibility graph G=(V,E,w) with node list V, edge list E, and weights w
           V is a 2D numpy array with V = [[x0,y0],[x1,y1],...,[xn,yn]]
           where [xi,yi] are the x and y coordinates of node i
           E is an adjacency dictionary E where E[i] is a list of node indices [j,k,...] connected to node i
           w is a dictionary with the keys as tuples of node indices: (i,j)
           and values w_ij corresponding to the distance between node i and node j so w[(i,j)]=w_ij
    '''
    
    n_conv = 0              #tracks number of convex vertices
    E = {}
    w = {}
    # First, add all convex vertices to node list V
    for P in ObstacleList:
        n = np.shape(P)[0] # number of vertices
        for i in range(n):
            if convex(P,i):
                if n_conv==0:
                    V = np.array([P[i,:]])
                else:
                    V = np.append(V,[P[i,:]],axis=0)
                n_conv += 1

    #Next, check the visibility between every node
    #If they are visible, add vertices to the edge list and distance to weight list
    for i in range(n_conv):
        for j in range(i+1,n_conv):
            u = V[i]
            v = V[j]
            if visible(u,v,ObstacleList):       #if nodes u and v can see each other
                addToEdgeList(i,j,E)
                addToEdgeList(j,i,E)
                dist = np.linalg.norm(u-v)
                w[(i,j)]=dist
                
            
    


    return (V,E,w)





def convex(P,i):
    '''
    Checks convexity of ith vertex of polygon P
    Input: P is polygon with vertices listed in CCW order, i is index of vertex to check
    Output: True if P[i,:] is a convex vertex, false if not
    '''
    
    n = np.size(P,axis=0)
    if i == 0:
        prevVertex = P[n-1,:]
        nextVertex = P[1,:]
    elif i==n-1:
        prevVertex = P[n-2,:]
        nextVertex = P[0,:]
    else:
        prevVertex = P[i-1,:]
        nextVertex = P[i+1,:]

    v1 = prevVertex-P[i,:]
    v2 = nextVertex-P[i,:]
##    print(i,v1,v2)
    if np.cross(v1,v2)<0:
        return True
    else:
        return False
    
def addToEdgeList(sourceNode,targetNode,E):
    '''
    adds targetNode to the list of nodes connected to sourceNode in edge list E
    '''

    if E.get(sourceNode) is None:
        E[sourceNode] = [targetNode]
    else:
        E[sourceNode].append(targetNode)

def visible(u,v,ObstacleList):
    '''
    returns true if coordinates u and v are visible; returns false otherwise
    u and v are visible iff they are not obstructed by an obstacle in ObstacleList
    Inputs:  u and v are coordinates associated with the two nodes being checked
             ObstacleList is the list of Obstacles
    Outputs: True or False
    '''

    for P in ObstacleList:
        n = np.size(P,axis=0)
        # if u and v are both vertices on P, make sure line doesn't go through object interior

        u_in_P=False
        v_in_P=False
        for i in range(n):
            if (u==P[i,:]).all():       #if both entries of u equal P[i,:]
                u_in_P = True           #then u is a vertex of P
            if (v==P[i,:]).all():   
                v_in_P = True

        if  u_in_P and v_in_P:
##            print(u,v,P,sep='\n')
            if throughInterior(u,v,P):
                return False
        for i in range(n):
            if i==n-1:
                w = P[i,:]
                x = P[0,:]
            else:
                w = P[i,:]
                x = P[i+1,:]
            if segmentIntersect(u,v,w,x):
##                print('Intersects {} {}'.format(u,v))
                return False
            

    # if it reaches here, it does not intersect with any segment and does not go through object interior
    return True

def segmentIntersect(u,v,w,x):
    '''
    returns true if segment with endpoints u and v intersects segment with endpoints w and x
    Inputs: all are len=2 1d numpy arrays representing point coordinates
            u and v are endpoints of segment 1
            w and x are enpoints of segment 2
    Outputs: True or False
    '''

    #If the segments share one or both endpoints, return false
    #because visiblity segment doesn't intersect with segments
    #out of same vertices that you are checking for visibility
    if (u==w).all() or (u==x).all() or (v==w).all() or (v==x).all():
        return False

    (a1,b1,c1) = computeLineThroughTwoPoints(u,v)
    (a2,b2,c2) = computeLineThroughTwoPoints(w,x)
    A = np.array([[a1,b1],[a2,b2]])                 # use matrix equation Ax=b to solve for intersection
    b = np.array([[c1],[c2]])

    #Check det(A) to see i they are parallel or along same line
    if abs(np.linalg.det(A))<1e-9:                  #if determinate is close to 0
        return False                                
    inv = np.linalg.inv(A)
    intersect = np.matmul(inv,b)
    intersect = intersect.flatten()                 #flatten to 1d array to subtract with other points
    
    #If intersect is on segment, the vectors from intersect to endpoints
    #will be in opposite directions and the dot product will be negative
    onSeg1 = np.dot(u-intersect,v-intersect)
    onSeg2 = np.dot(w-intersect,x-intersect)
##    print(onSeg1,onSeg2)
    if onSeg1<=0 and onSeg2<=0:
        return True
    else:
        return False

def throughInterior(u,v,P):
    '''
    returns true if line between points u and v goes through the interior of polygon P
    returns false otherwise
    Inputs: points u and v are the coordinates of convex vertices of P
            P is a polygon with vertices listed in CCW order
    Output: True or False
    '''

    #First, find which vertex u is in P
    n = np.size(P,axis=0)
    for i in range(n):
        if (u==P[i,:]).all():       # u is vertex i of P
            if i == 0:
                prevVertex = P[n-1,:]
                nextVertex = P[1,:]
            elif i==n-1:
                prevVertex = P[n-2,:]
                nextVertex = P[0,:]
            else:
                prevVertex = P[i-1,:]
                nextVertex = P[i+1,:]
            u_index = i
            break
        if i==n-1:
            raise ValueError('u and v must be vertices of P')

    #Find vectors from u to prevVertex, nextVertex and v
    #Since u is a convex vertex and P's vertices are in CCW order,
    #if the u to v goes through the interior of the polygon then:
    #the cross product of the vector to v and the vector to prevVertex must be positive
    #and the cross product of the vector to v and the vector to nextVertex must be negative

    prevVector = prevVertex-u
    nextVector = nextVertex-u
    testVector = v-u
    if np.cross(testVector,prevVector)>0 and np.cross(testVector,nextVector)<0:
        return True
    
    #If the vector from u to v is in line with the previous vector and in the same direction
    #we need to check whether the previous vertex is convex to determine whether line is through the interior
    
    elif np.cross(testVector,prevVector)==0 and np.dot(testVector,prevVector)>0: #if inline and same direction as prevVector 
        if u_index==0:              #if prevVector is first
            prev_index = n-1        #prevIndex is last index
        else:
            prev_index = u_index-1
        return not convex(P,prev_index)          #if prevVertex is not convex,
                                        #then u to v is through interior

    #the same case for the next Vector
    elif np.cross(testVector,nextVector)==0 and np.dot(testVector,nextVector)>0: #if inline and same direction as nextVector
        if u_index==n-1:                  #if nextVector is the last
            next_index = 0                   #nextIndex is first
        else:
            next_index = u_index+1
        return not convex(P,next_index)          #if nextVertex is not convex

    else:                       #u to v is not between prev and next vectors
        return False            #so u to v is not through the interior


def computeLineThroughTwoPoints(p1,p2):
    '''
    returns equation of line between points p0 and p1
    Input: points p0 and p1 as 1d numpy array containing x and y coordinates of point
    Output: (a,b,c) that satisfies equation of the line ax+by=c between given points
    Values are normalized so [a,b] is normal unit vector
    '''

    d = np.linalg.norm(p1-p2)
    if d==0:
        a = 0
        b = 0
        c = 0
    else:
        a = (p1[1]-p2[1])/d
        b = (p2[0]-p1[0])/d                   #Rearrangement of Point-Slope formula for line
        c = ((p2[0]-p1[0])*p1[1]-(p2[1]-p1[1])*p1[0])/d
    return (a,b,c)
