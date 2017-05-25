from func.extractVisGraph import checkSegmentIntersect
import numpy as np
import matplotlib.pyplot as plt

def plotSegment(p1,p2):
    plt.plot([p1[0],p2[0]],[p1[1],p2[1]])

def printSegmentIntersection(p1,p2,p3,p4):
    if checkSegmentIntersect(p1,p2,p3,p4):
        print('Segment {} to {} intersects Segment {} to {}: True'.format(p1,p2,p3,p4))
    else:
        print('Segment {} to {} intersects Segment {} to {}: False'.format(p1,p2,p3,p4))
        

p1 = np.array([1,1])
p2 = np.array([2,2])
p3 = np.array([0,0])
p4 = np.array([2,0])
p5 = np.array([0,-1])
p6 = np.array([2,1])
p7 = np.array([0,0])
p8 = np.array([0,3])


plotSegment(p1,p2)
plotSegment(p3,p4)
plotSegment(p5,p6)
plotSegment(p7,p8)
printSegmentIntersection(p1,p2,p3,p4)
printSegmentIntersection(p1,p2,p5,p6)
printSegmentIntersection(p3,p4,p5,p6)
printSegmentIntersection(p3,p4,p7,p8)

plt.show()
