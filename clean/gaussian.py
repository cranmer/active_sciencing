import numpy as np
def simulator(theta,phi,n_samples):
    samples =  np.random.normal(loc = theta, scale = 2+np.cos(phi), size = n_samples)
    return samples
