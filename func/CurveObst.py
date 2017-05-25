import numpy as np
import matplotlib.pyplot as plt


def plotCurveObstList(curveObstList):
    for curveObst in curveObstList:
        curveObst.plot()


class CurveObst:
    
    def __init__(self,func1,func2,x):
        self.func1 = func1      #function of upper bound
        self.func2 = func2      #function of lower bound
        self.x = x    #list of x values where funcs are evaluated
        self.y1 = np.zeros(len(x))
        self.y2 = np.zeros(len(x))

    def plot(self):
        self.evalYvals()
        plt.fill_between(self.x,self.y1,self.y2)

    def evalYvals(self):
        n = len(self.x)
        for i in range(n):
            self.y1[i] = self.func1(self.x[i])
            self.y2[i] = self.func2(self.x[i])
            if self.y1[i]<self.y2[i]:
                raise ValueError('Func1 must be greater than Func2 for all values in x')
        

def getPolygon(curveObst,num_div):
    '''
    Returns bounding polygon in which curveObst fits in entirely
    Inputs: num_div is an integer that represents the number of divisions in each concave region
    Output: 2d array polygon that slightly overestimates the area of curveObst
    Finds the points where the concavity changes. Based on the concavity and whether it is the upper or lower bound function,
    either 1. picks vertices along the curve or 2. extends tangent lines and takes vertices at the tangent line intersections.
    This ensures that the curve obstacle is completely contained by the polygon
    '''
    curveObst.evalYvals()
    x = curveObst.x
    y1 = curveObst.y1
    y2 = curveObst.y2
    
    #start with the lower bound
    P1 = fitCurveOneSided(x,y2,num_div,False)
    P2 = fitCurveOneSided(x,y1,num_div,True)
    P2 = P2[::-1,:]                         #flip P
    P = np.append(P1,P2,axis=0)
    
    return P




def fitCurveOneSided(x,y,num_div,upper):
    '''
    fits curve with line segments that are either all above or below curve
    Inputs: x and y - 1d arrays representing curve
            num_div - number of divisions of each concavity region
            upper - True if the curve represents the upper region of polygon
                    False if the curve represents the lower region of polygon
    '''
    (i_change,concaveUp,allZero) = concavityChange(x,y)
    if allZero:
        n = len(x)
        P = np.array([[x[0],y[0]],[x[n-1],y[n-1]]])
        return P
    for j in range(len(i_change)-1):     # for all the points where concavity changes
        i_start = i_change[j]
        i_end = i_change[j+1]
        if concaveUp[j] ^ upper:
            P_new = connectTangents(x[i_start:i_end],y[i_start:i_end],num_div)
        else:
            P_new = connectDirect(x[i_start:i_end],y[i_start:i_end],num_div)
            

        if j==0:
            P = np.array(P_new)
        else:
            P = np.append(P,P_new,axis=0)

    P = np.append(P,[[x[-1],y[-1]]],axis=0)
    return P

    

    

def connectDirect(x,y,num_div):
    '''
    returns a set of (num_div+2) points evenly spaced along the curve (x,y)
    Inputs: x - numpy array of x coordinates of curve
            y - numpy array of y coordinates of curve
            num_div - the number of additional points the tangent is assessed at; evenly spaced along x-axis between endpoints
            If num_div=0, only endpoints are used
    Outputs: P - 2d array list of points along curve (x,y)
             Starting endpoint [x[0],[y[0]] is included in list P
    '''
    n = len(x)
    connect_indeces = np.linspace(0,n-1,num_div+2,dtype=int)
    connect_indeces = removeRepeats(connect_indeces)            #If the number of division is more than the number of interior points, there will be indentical vertices
                                                                #Remove repeats to remove identical vertices 
    P = np.array([[x[0],y[0]]])
    for i in connect_indeces[1:-1]:
        P = np.append(P,[[x[i],y[i]]],axis=0)
    return P


    

def connectTangents(x,y,num_div):
    '''
    returns a set of points located at the intersection of the tangent lines of (x,y)
    Inputs: x - numpy array of x coordinates of curve
            y - numpy array of y coordinates of curve
            num_div - the number of additional points the tangent is assessed at; evenly spaced along x-axis between endpoints
            If num_div=0, only endpoints are used
    Outputs: P - 2d array list of points at the intersection of the tangent lines
             Starting endpoints [x[0],[y[0]] is included in list P
    '''

    n = len(x)
    P = np.array([[x[0],y[0]]])
    if n==1 or n==2:
        return P
    y_prime = deriv(x,y)
    #indeces of points to be chosen for tangents
    tangPoints = np.linspace(0,n-1,num_div+2,dtype=int)
    tangPoints = removeRepeats(tangPoints)          #remove repeat vertices for arrays shorter than num of divisions

    for i in range(len(tangPoints)-1):
        xi = x[tangPoints[i]]
        xip1 = x[tangPoints[i+1]]
        yi = y[tangPoints[i]]
        yip1 = y[tangPoints[i+1]]
        y_primei = y_prime[tangPoints[i]]
        y_primeip1 = y_prime[tangPoints[i+1]]

##        print('xi: ',xi)
##        print('xip1: ',xip1)
##        print('yi: ',yi)
##        print('yip1: ',yip1)
##        print('y_primei: ',y_primei)
##        print('y_primeip1: ',y_primeip1)

        
        if abs(y_prime[i]-y_prime[i+1])<1e-6:
            x_tang = x[i]
            y_tang = y[i]
        else:
            #Equation below is derived from the point-slope formula for consecutive tangent lines
            x_tang = ((yip1-yi)+y_primei*xi-y_primeip1*xip1)/(y_primei-y_primeip1)
            y_tang = y_primei*(x_tang-xi)+yi

        P = np.append(P,[[x_tang,y_tang]],axis=0)

    return P
    



def concavityChange(x,y,endpoints=True):
    '''
    returns the indices where the concavity changes
    Input: x,y - array of x and y values of function
           endpoints - if true, includes indeces and concavity of endpoints
    Output: i_change -  a list of the indeces where the concavity changes.
            All indeces of y = f(x) between i_change[j] and i_change[j+1]-1 have the same concavity
            ConcaveUp - a list of boolean values of the concavity of each region between i_change[j] and i_change[j+1]-1
                        True means concave up. False is concave down
    '''
    
    #keep track of where the 2nd derivative crosses zero
    n = len(y)
    y_prime = deriv(x,y)
    y_prime2 = deriv(x,y_prime)
    lastSign = y_prime2[0]>0         #True is positive
    i_change = []                   #List of vertices where concavity changes
    concaveUp = []
    allZero = True
    isZero = abs(y_prime2[0])<1e-9
    allZero = allZero and isZero
    for i in range(1,n):
        currentSign = y_prime2[i]>0
        if lastSign is not currentSign:
            i_change.append(i)
            concaveUp.append(currentSign)
        lastSign = currentSign
        isZero = abs(y_prime2[i])<1e-9
        allZero = allZero and isZero

    if endpoints:
        i_change.insert(0,0)
        concaveUp.insert(0,y_prime2[0]>0)
        i_change.append(n-1)
        concaveUp.append(y_prime2[n-1]>0)


    
    return (i_change,concaveUp,allZero)

def deriv(x,y):
    '''
    calculates the derivative of y(x) by numerical differention
    Inputs: x and y are lists of equal length
    Outputs: y_prime is a list of the derivative of y at all points x
    '''

    n = len(x)
    if type(y) is np.ndarray:       #if input is np array
        y_prime = np.zeros(n)       #output np array
    else:
        y_prime = [0]*n             #else output a list
        
    for i in range(n):
        if i==0:            #for first and last values use one sided difference
            h = x[1]-x[0]
            y_prime[i] = (y[1]-y[0])/h
        elif i==n-1:
            h = x[i]-x[i-1]
            y_prime[i] = (y[i]-y[i-1])/h
        else:
            h = x[i+1]-x[i-1]
            y_prime[i] = (y[i+1]-y[i-1])/h
    return y_prime

def removeRepeats(A):
    '''
    removes all repeat integers from a sorted list of integers
    Input: A - sorted 1d numpy array of integers
    Output: B - sorted list of integers with only one integer of each value
    '''
    n = len(A)
    B = np.array([A[0]])
    prevVal = A[0]
    for i in range(1,n):
        if prevVal != A[i]:
            B = np.append(B,[A[i]])
            prevVal = A[i]
    return B
