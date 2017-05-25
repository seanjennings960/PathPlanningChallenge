import numpy as np
from func.extractVisGraph import throughInterior
import matplotlib.pyplot as plt

P = np.array([[0,0],[1,0],[2,1],[3,0],[3,4],[1.5,4],[1.5,2]])
plt.fill(P[:,0],P[:,1])
u = P[5,:]
v = P[0,:]
plt.plot([u[0],v[0]],[u[1],v[1]],'r')
print(throughInterior(u,v,P))


plt.show()
