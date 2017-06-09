import numpy as np
import sys
import time
import random

def simulator(theta,phi,n_samples, widget = None, delay = False):
    samples =  np.random.normal(loc = theta, scale = 2+np.cos(phi), size = n_samples)
    if delay:
		for i in range(widget.max):
		    time.sleep(random.random())
		    widget.value = widget.value + 1    		
    return samples
