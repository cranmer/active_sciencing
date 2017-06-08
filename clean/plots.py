import matplotlib.pyplot as plt
import numpy as np

def plot_simple_grid(res, ax = plt):
    ax.plot(res[1],res[2])
    ax.axvline(res[0], c = 'r')

def plot_bayes(res,phi_range, ax=plt):
    smooth_phi = np.linspace(*phi_range,num = 200).reshape(-1,1)
    y,std = res[0].models[-1].predict(smooth_phi, return_std = True)
    y,std = -y,-std
    ax.plot(smooth_phi[:,0],y, c = 'k')
    ax.plot(smooth_phi[:,0],y+std, c = 'k', linestyle = 'dashed')
    ax.plot(smooth_phi[:,0],y-std, c = 'k', linestyle = 'dashed')
    ax.fill_between(smooth_phi[:,0],y-std,y+std, color = 'k', alpha = 0.2)
    ax.scatter(res[0].x_iters,-res[0].func_vals, marker = '.', s = 200, color = 'k')
    ax.axvline(res[0].x, c = 'r')

def plot_data(data, data_range, ax = plt):
    bins = np.linspace(*data_range, num = 11)
    ax.hist(data, bins = bins)

def plot_posterior(prior,posterior, best_theta, true_theta, theta_range, map_bins = 20, ax = plt):
    xs = np.linspace(*theta_range,num = map_bins)
    logpdf_prior = prior.approx_logpdf()
    logpdf_postr = posterior.approx_logpdf()
    ax.plot(xs,np.exp(logpdf_prior(xs)))
    ax.plot(xs,np.exp(logpdf_postr(xs)))
    ax.axvline(best_theta, c = 'k')
    ax.axvline(true_theta, c = 'grey')


def summary_plot(data,prior,posterior,best_theta,true_theta,res,expected_posterior = None,res_type = 'simple'):
    fig,axarr = plt.subplots(1,4 if expected_posterior else 3)
    fig.set_size_inches(20,4)
    bins = np.linspace(*DATA_RANGE, num = 11)
    axarr[0].hist(data, bins = bins)
    axarr[0].set_title('data')


    xs = np.linspace(*THETA_RANGE,num = model_details_map_bins)
    logpdf_prior = prior.approx_logpdf()
    logpdf_postr = posterior.approx_logpdf()
    axarr[1].plot(xs,np.exp(logpdf_prior(xs)))
    axarr[1].plot(xs,np.exp(logpdf_postr(xs)))
    axarr[1].axvline(best_theta, c = 'k')
    axarr[1].axvline(true_theta, c = 'grey')
    axarr[1].set_title('prior and posterior of parameter of interest')
    
    if res_type=='simple':
        plot_simple_grid(res,ax = axarr[2])
    else:
        plot_bayes(res,ax = axarr[2])
    axarr[2].set_title('expected information gain - next expt')


    if expected_posterior:
        logpdf_prior = prior.approx_logpdf()
        logpdf_postr = posterior.approx_logpdf()
        axarr[3].plot(xs,np.exp(logpdf_prior(xs)))
        axarr[3].plot(xs,np.exp(logpdf_postr(xs)))

        logpdf_exp_postr = expected_posterior.approx_logpdf()
        axarr[3].plot(xs,np.exp(logpdf_exp_postr(xs)))
        axarr[3].set_title('expected posterior after next exp')

