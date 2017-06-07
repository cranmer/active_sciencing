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

from multiprocessing import Pool

def info_gain(p1, p2):
    return p1.entropy() - p2.entropy()

def _simulate(args):
    theta_map, phi, prior, emcee_kwargs = args
    print 'simulating with ',theta_map, phi
    # external workflow provides simulated data
    sim_data = emcee_kwargs['lnprob_args']['simulator'](theta_map, phi, n_samples = 1000)

    #external workflow uses simulator to provide likelihood 
    sim_posterior = calculate_posterior(prior, sim_data, phi,**emcee_kwargs)
    return info_gain(prior, sim_posterior)

def expected_information_gain(phi, prior, emcee_kwargs, map_bins = 20):
    'calculate the expression above using workflow for simulations'
    print 'EIG',phi
    n_simulations = 4
    n_parallel = 4
    
    phi = phi[0]
    #need to pass in prior through some extra arguments
    
    # use saddle-point approximation
    theta_map = prior.map(bins = map_bins)

    # currently the MCMC sampler is the slower part, which already uses threads so we don't gain
    # this should change once we have a more realistic simulator that takes time to run
    pool = Pool(n_parallel)
    eig = pool.map(_simulate, [(theta_map, phi, prior,emcee_kwargs) for i in range(n_simulations)])
    pool.close()
    pool.join()
    return np.mean(eig)


def expected_information_gain_dummy(phi, prior, emcee_kwargs, map_bins = 20):
    'calculate the expression above using workflow for simulations'
    print 'EIG',phi
    n_simulations = 4
    n_parallel = 4
    
    phi = phi[0]

    # use saddle-point approximation
    theta_map = prior.map(bins = map_bins)

    return 1.0

from skopt import gp_minimize
def design_next_experiment(prior,phi_bounds, eig_kwargs, n_totalcalls=10, n_random_calls = 5):
    bounds = [phi_bounds]
    func = lambda p: -expected_information_gain_dummy(p, prior,**eig_kwargs)

    # five random points to initialise things, then five using the GP model
    # XXX Should we be reusing the random number generator? Means this call eseentially evaluates
    # XXX the same values of phi each science iteration
    opt_result = gp_minimize(func, bounds, n_random_starts=n_random_calls, n_calls=n_totalcalls, random_state=4)

    return opt_result, opt_result.x[0], opt_result.x_iters