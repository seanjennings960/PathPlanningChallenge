import numpy as np

def Dijkstra(V,E,w):
    '''
    returns list of nodes which represent the shortest path through graph G=(V,E,w)

    Inputs: visibility graph G=(V,E,w) with node list V, edge list E, and weights w
            The start position is the (n-2)th element and the goal position is the (n-1)th element

           V is a 2D numpy array with V = [[x0,y0],[x1,y1],...,[xn,yn]]
           where [xi,yi] are the x and y coordinates of node i
           E is an adjacency dictionary E where E[i] is a list of node indices [j,k,...] connected to node i
           w is a dictionary with the keys as tuples of node indices: (i,j)
           and values w_ij corresponding to the distance between node i and node j so w[(i,j)]=w_ij

    Output: path, the 2d array of the node coordinates of the shortest path from start to goal
            distPath, the total distance of the path from start to goal
    '''

    n = np.size(V,axis=0)
    dist = np.full(n,float('inf'))      #dist is a list of the distances from the source node, all initially inf
    parent = np.full(n,None)            #the parent of each node
    dist[n-2] = 0
    Q = []                              
    for i in range(n):                  
        Q.append(i)                     #Queue is list with all node indeces initially added

    while len(Q)>0:                     #while queue is not empty
        i_min = 0
        min_dist = dist[0]
        for i in range(1,len(Q)):       #find the node in queue with the minimum distance to source node
            u = Q[i]                    #node index
            if dist[u]<min_dist:
                i_min = i
                min_dist = dist[u]

        u = Q.pop(i_min)                #take the vertex u with the minimum distance

        for v in E[u]:                  #for each node connected to u
            if u<v:
                w_edge = w[(u,v)]       #weight of edges are stored with the lower node index first
            else:
                w_edge = w[(v,u)]
            alt = dist[u]+w_edge        #the alternative distance is the distance
            if alt<dist[v]:
                dist[v]=alt
                parent[v] = u

    i = n-1                   #work backwards from the goal node
    path = [V[i,:]]
    while parent[i] is not None:  #while not at the start node
        i = parent[i]   #move to parent node
        path = np.concatenate(([V[i]],path),axis=0)

    distTotal = dist[n-1]
    return (path,distTotal)
