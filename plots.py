import matplotlib.pyplot as plt
import numpy as np

def plot_bayes(res,phi_range, ax=plt):
    smooth_phi = np.linspace(*phi_range,num = 200).reshape(-1,1)
    try:
        y,std = res.models[-1].predict(smooth_phi, return_std = True)
        y,std = -y,-std
        ax.plot(smooth_phi[:,0],y, c = 'k')
        ax.plot(smooth_phi[:,0],y+std, c = 'k', linestyle = 'dashed')
        ax.plot(smooth_phi[:,0],y-std, c = 'k', linestyle = 'dashed')
        ax.fill_between(smooth_phi[:,0],y-std,y+std, color = 'k', alpha = 0.2)
    except IndexError:
        pass
    ax.scatter(res.x_iters,-res.func_vals, marker = '.', s = 100, color = 'k')
    ax.axvline(res.x_iters[-1],color = 'b')
    ax.axvline(res.x, c = 'r')
    ax.set_xlim(*phi_range)

def plot_data(data, data_range, ax = plt):
    bins = np.linspace(*data_range, num = 11)
    ax.hist(data, bins = bins)

def plot_posterior(prior,posterior, best_theta, true_theta, theta_range, map_bins = 20, ax = plt):
    xs = np.linspace(*theta_range,num = map_bins)
    ax.plot(xs,prior.pdf(xs))
    ax.plot(xs,posterior.pdf(xs))
    ax.axvline(best_theta, c = 'k')
    ax.axvline(true_theta, c = 'grey')

