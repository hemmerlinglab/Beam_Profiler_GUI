import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
import math
import lmfit
from lmfit import Minimizer, Parameters, report_fit



""" This code was used to determine incoming beam waist for the cavity
"""

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

        fac = 1

        z_plot = np.linspace(np.min(z), np.max(z), 100)
        #z_plot = np.linspace(-fac*z_R + z_offset, +fac*z_R + z_offset, 500)
        model = w_0*np.sqrt(1+( (z_plot-z_offset)/z_R)**2)
        return (z_plot, model)

def fitting(z, w):

    vary_all = True

    # giving values to the params defined in previous function
    params = Parameters()
    params.add('min_waist',value=0.5*300e-6, min=5.0e-6, max=10000e-6, vary=vary_all)
    params.add('z_offset',value=-10e-2, min=-80e-2,max=80e-2, vary = vary_all)
    params.add('lbda',  value = 523e-9, vary = False)
    
    # do the fit here, least sq model
    # put in x and y data here
    minner = Minimizer(fcn2min,params,fcn_args=(z, w))
    result = minner.minimize()

    return result

def main():

    # data after the first mirror

    data = np.genfromtxt('waist.csv')

    z  = data[:, 0] * 2.54e-2
    wx  = 0.5 * data[:, 1] * 1e-6
    wy  = 0.5 * data[:, 2] * 1e-6

    


    plt.plot(z/1e-2, wx/1e-6, 'r.')

    plt.xlabel('Position (cm)')
    plt.ylabel('Beam waist (radius) (um)')

    result = fitting(z, wx)
    print(result.params)
    
    (fit_x, fit_y) = fcn2min(result.params, z, None, do_fit = False)
    
    plt.plot(fit_x/1e-2, fit_y/1e-6, '-')

    print('Waist = ' + str(result.params['min_waist']/1e-6) + ' um')
    print('Waist_pos = ' + str(result.params['z_offset']/1e-2) + ' cm')

    plt.show()

if __name__=="__main__":
    main()
    


    

