import numpy as np
import sys

def simulator(theta,phi,n_samples):
    sys.stdout.write('.')
    samples =  np.random.normal(loc = theta, scale = 2+np.cos(phi), size = n_samples)
    return samples
