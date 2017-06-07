import distr
import numpy as np
import emcee
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

def lnprob(theta, x, prior, phi, lnlike_kwargs):
    lp = lnprior(theta, prior)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta, x, phi,**lnlike_kwargs)

def collect_data(phi, simulator, theta_nature, n_samples = 500):
    return simulator(theta_nature,phi,n_samples)


def calculate_posterior(prior, data, phi, n_walkers = 10, n_warmup = 10, n_chainlen = 20, lnprob_args = None):
    """Compute samples from the posterior"""
    ndim, n_walkers = 1, n_walkers
    # initialise walkers from the MAP + noise
    # XXX alternatively sample a point from the KDE without adding noise?
    # XXX not sure if the noise takes us into a region where the prior is zero?
    pos = [prior.map() + 1e-1*np.random.randn(ndim) for i in range(n_walkers)]
    
    sampler = emcee.EnsembleSampler(
    	n_walkers, 1, lnprob,
    	args=(data,prior,phi,lnprob_args)
   	)
    pos, prob, state = sampler.run_mcmc(pos, n_warmup)
    
    sampler.reset()
    pos, prob, state = sampler.run_mcmc(pos, n_chainlen)
    return distr.Distribution(prior.name, prior.range, sampler.flatchain[:,0])