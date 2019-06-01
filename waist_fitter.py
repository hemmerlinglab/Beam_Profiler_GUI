import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
import math
import lmfit

""" Questions on lmfit/beam-waist stuff:
    1. How to come up with could values to input in the params function for offsets  
"""



def fcn2min(params,x,data):
    """ 
    Params:
    _________

    w_0: minimum waist
    z:   distance along the beam path
    z_R: pi*w_0**2/lambda
    
    """

    # giving names to the set params
    w_0 = params['min_waist']
    lbda = params['lambda']
    z_offset = params['z_offset'] # waist isnt centered at zero
    
    z_R = np.pi*w_0**2/(lbda)
    return w_0*np.sqrt(1+(z/z_R)**2)

def fitting(w,z):
    # giving values to the params defined in previous function
    params = Parameters()
    params.add('min_waist',value=(np.max(w)-np.min(w))/2.0, min=10.0, max=2000)
    params.add('z_offset',value=np.mean(z), min=-1000,max=500)

    # do the fit here, least sq model
    # put in x and y data here
    minner = Minimizer(fcn2min,params,fcn_args=(somex,somey))
    result = minner.minimize()


def main():

    # data after the first mirror
    dist  = np.array([-424,80,127,228,437,518,634,685])
    waist = np.array([302,748,741,850,1060,1148,1047,1167])

    plt.plot(dist,waist,'r.')
    plt.show()

if __name__=="__main__":
    main()
    


    





