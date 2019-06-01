import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
import math
import lmfit

# data after the first mirror
dist  = np.array([220,437,518,600,641])
waist = np.array([850,1060,1148,1047,1167])

# data after second mirror
dist2 = np.array([437,518,600,641])
w2 =  np.array([1060,1148,1047,1167])

# average waists
avg_w = np.average(waist)
avg_w_sim = np.average(w2)

print(avg_w)
print(avg_w_sim)
plt.plot(dist,waist,'r.')
plt.show()


def fcn2min(w_0,z,z_R,lbda):
    """ 
    Params:
    _________

    w_0: minimum waist
    z:   distance along the beam path
    z_R: pi*w_0**2/lambda
    
    """
    z_R = np.pi*w_0**2/(lbda)
    return w_0*np.sqrt(1+(z/z_R)**2)


    
    


    





