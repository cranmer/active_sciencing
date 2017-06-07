import distr
import numpy as np
def lnprior(theta, prior):
    p = prior.pdf(theta)
    if p <= 1e-8:
        return -np.inf
    else:
        return np.log(p)

def lnlike(theta, x, phi,simulator, simulation_kwargs = dict(n_samples = 5000), distr_kwargs = {}, logpdf_kwargs = {}):
    mc = simulator(theta,phi, **simulation_kwargs)
    p = distr.Distribution(name = '', samples = mc, **distr_kwargs)
    logpdf = p.approx_logpdf(**logpdf_kwargs)
    return np.sum(logpdf(x))

def lnprob(theta, x, prior, phi, simulator, lnlike_kwargs):
    lp = lnprior(theta, prior)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta, x, phi, simulator,**lnlike_kwargs)

def collect_data(phi, simulator, theta_nature, n_samples = 500):
    return simulator(theta_nature,phi,n_samples)
