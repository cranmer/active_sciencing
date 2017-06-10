import distr
import numpy as np
import emcee
import datetime
from multiprocessing import Pool
from skopt import gp_minimize
import bayesopt
import plots

def lnprior(theta, prior):
    p = prior.pdf(theta)
    if p <= 1e-8:
        return -np.inf
    else:
        return np.log(p)

def lnlike(theta, x, phi,simulator, simulation_kwargs = dict(n_samples = 5000), distr_kwargs = {}, logpdf_kwargs = {}):
    mc = simulator(theta,phi, **simulation_kwargs)
    p = distr.Distribution(name = 'density', samples = mc, **distr_kwargs)
    logpdf = p.approx_logpdf(**logpdf_kwargs)
    return np.sum(logpdf(x))

def lnprob(theta, x, prior, phi, lnlike_kwargs):
    lp = lnprior(theta, prior)
    if not np.isfinite(lp):
        return -np.inf
    return lp + lnlike(theta, x, phi,**lnlike_kwargs)

def calculate_posterior(prior, data, phi, n_walkers = 10, n_warmup = 10, n_chainlen = 20, lnprob_args = None):
    """Compute samples from the posterior"""
    ndim, n_walkers = 1, n_walkers
    # initialise walkers from the MAP + noise
    # XXX alternatively sample a point from the KDE without adding noise?
    # XXX not sure if the noise takes us into a region where the prior is zero?
    pos = [prior.map() + 1e-1*np.random.randn(ndim) for i in range(n_walkers)]
    
    sampler = emcee.EnsembleSampler(
        n_walkers, 1, lnprob,
        args=(data,prior,phi,lnprob_args),
        # threads = n_walkers
    )
    pos, prob, state = sampler.run_mcmc(pos, n_warmup)
    
    sampler.reset()
    pos, prob, state = sampler.run_mcmc(pos, n_chainlen)
    return distr.Distribution(prior.name, prior.range, sampler.flatchain[:,0])


def info_gain(p1, p2):
    return p1.entropy() - p2.entropy()

def _simulate(args):
    theta_map, phi, prior, sim_n_data, emcee_kwargs = args
    # external workflow provides simulated data
    sim_data = emcee_kwargs['lnprob_args']['simulator'](theta_map, phi, n_samples = 1000)

    #external workflow uses simulator to provide likelihood 
    sim_posterior = calculate_posterior(prior, sim_data, phi,**emcee_kwargs)
    return info_gain(prior, sim_posterior)

def expected_information_gain(phi, prior, emcee_kwargs, sim_n_data , map_bins):
    'calculate the expression above using workflow for simulations'
    n_simulations = 4
    n_parallel = 4
    
    phi = phi[0]
    #need to pass in prior through some extra arguments
    
    # use saddle-point approximation
    theta_map = prior.map(bins = map_bins)

    print str(datetime.datetime.now()),'EIG via 4 parallel experiments with [theta,phi]',theta_map,phi

    # currently the MCMC sampler is the slower part, which already uses threads so we don't gain
    # this should change once we have a more realistic simulator that takes time to run
    pool = Pool(n_parallel)
    eig = pool.map(_simulate, [(theta_map, phi, prior,sim_n_data,emcee_kwargs) for i in range(n_simulations)])
    pool.close()
    pool.join()
    return np.mean(eig)


def design_next_experiment_bayesopt(prior,phi_bounds, eig_kwargs, n_totalcalls=10, n_random_calls = 5, ax = None, fig = None):


    opt  = bayesopt.get_optimizer(phi_bounds,n_random_calls)
    func = lambda p: -expected_information_gain(p, prior,**eig_kwargs)

    for i in range(n_totalcalls):
        # ask next x
        next_x = opt.ask()
        next_f = func(next_x)

        # tell a pair to the optimizer
        res = opt.tell(next_x, next_f)
        if ax:
            ax.clear()
            plots.plot_bayes(res, phi_range = phi_bounds, ax = ax)
            fig.canvas.draw()
    return res, res.x[0], res.x_iters






    # bounds = [phi_bounds]
    # func = lambda p: -expected_information_gain(p, prior,**eig_kwargs)

    # # five random points to initialise things, then five using the GP model
    # # XXX Should we be reusing the random number generator? Means this call eseentially evaluates
    # # XXX the same values of phi each science iteration
    # opt_result = gp_minimize(func, bounds, n_random_starts=n_random_calls, n_calls=n_totalcalls, random_state=4)

    # return opt_result, opt_result.x[0], opt_result.x_iters

def design_next_experiment_simplegrid(prior,phi_bounds, eig_kwargs, n_points=6):
    eig_test_phis = np.linspace(*phi_bounds, num = n_points)
    eig = []
    for x in eig_test_phis.reshape(-1,1):
        eig.append(expected_information_gain(x,prior,**eig_kwargs))
    eig = np.array(eig)
    next_phi = eig_test_phis[np.argmax(eig)]
    return next_phi, eig_test_phis, eig
