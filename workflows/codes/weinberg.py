import numpy as np
import sys

def a_fb(sqrtshalf,gf):
    MZ = 90
    GFNom = 1.0

    sqrts = sqrtshalf*2.
    A_FB_EN = np.tanh((sqrts-MZ)/MZ*10)
    A_FB_GF = gf/GFNom
    return 2*A_FB_EN*A_FB_GF
    
def diffxsec(costheta,sqrtshalf,gf):
    norm = 2.*((1.+1./3.))
    return ((1+costheta**2)+a_fb(sqrtshalf,gf)*costheta)/norm

def rej_sample_costheta(nsamples,sqrtshalf,gf):
    ntrials = 0
    samples = []
    x = np.linspace(-1,1,num = 1000)
    maxval = np.max(diffxsec(x,sqrtshalf,gf))
    while len(samples) < nsamples:
        ntrials = ntrials+1
        xprop  = np.random.uniform(-1,1)
        ycut = np.random.random()
        yprop = diffxsec(xprop,sqrtshalf,gf)/maxval
        if yprop/maxval < ycut:
            continue
        samples.append(xprop)
    return np.array(samples)

def simulator(theta,phi,n_samples):
    sys.stdout.write('.')
    samples =  rej_sample_costheta(n_samples,phi,theta)
    return samples


