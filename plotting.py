import sys
import scipy
import numpy as np
import matplotlib.pyplot as plt
import math


dist  = np.array([220,437,518,600,641])
dist2 = np.array([437,518,600,641])

waist = np.array([850,1060,1148,1047,1167])
w2 =  np.array([1060,1148,1047,1167])

avg_w = np.average(waist)
avg_w_sim = np.average(w2)

print(avg_w)
print(avg_w_sim)
plt.plot(dist,waist,'r.')
plt.show()
