import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
import math
import lmfit

# data after the first mirror
dist  = np.array([-424,80,127,228,437,518,634,685])
waist = np.array([302,748,741,850,1060,1148,1047,1167])

# average waist
avg_w = np.average(waist)

print(avg_w)
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


    
    


    





