import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
import math
import lmfit
from lmfit import Minimizer, Parameters, report_fit


""" Questions on lmfit/beam-waist stuff:
    1. How to come up with could values to input in the params function for offsets  
"""



def fcn2min(params,z,data, do_fit = True):
    """ 
    Params:
    _________

    w_0: minimum waist
    z:   distance along the beam path
    z_R: pi*w_0**2/lambda
    
    """

    # giving names to the set params
    w_0 = params['min_waist']
    lbda = params['lbda']
    z_offset = params['z_offset'] # waist isnt centered at zero
    
    z_R = np.pi*w_0**2/(lbda)

    if do_fit:
        model = w_0*np.sqrt(1+( (z-z_offset)/z_R )**2)
        return model - data
    else:
        z_plot = np.linspace(np.min(z), np.max(z), 100)
        model = w_0*np.sqrt(1+( (z_plot-z_offset)/z_R)**2)
        return (z_plot, model)

def fitting(z,w):

    # giving values to the params defined in previous function
    params = Parameters()
    params.add('min_waist',value=(np.max(w)-np.min(w))/2.0, min=10.0e-6, max=2000e-6)
    params.add('z_offset',value=np.mean(z), min=-3,max=3)
    params.add('lbda',  value = 780e-9, vary = False)
    
    # do the fit here, least sq model
    # put in x and y data here
    minner = Minimizer(fcn2min,params,fcn_args=(z,w))
    result = minner.minimize()

    return result

def main():

    # data after the first mirror

    z  = np.array([-424,80,127,228,437,518,634,685]) * 1e-3
    w  = np.array([302,748,741,850,1060,1148,1047,1167]) * 1e-6
    plt.plot(z,w/1e-6,'r.')
    result = fitting(z,w)
    
    (fit_x,fit_y) = fcn2min(result.params,z,None, do_fit = False)
    plt.plot(fit_x,fit_y/1e-6, '-')

    print('Waist = ' + str(result.params['min_waist']/1e-6) + ' um')
    print('Waist_pos = ' + str(result.params['z_offset']/1e-3) + ' mm')

    plt.show()

if __name__=="__main__":
    main()
    


    





