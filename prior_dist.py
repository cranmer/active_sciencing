from scipy.stats import entropy, gaussian_kde
import numpy as np
import matplotlib.pyplot as plt


class Distribution:
    '''
    member vars
        variable names
        ranges  (for use with george)
    methods
        density estimate (KDE or histogram) (for use with emcee)
        MAP (for saddle point approximation)
    '''
    def __init__(self, name, range, samples=None):
        self.range = range
        self.name = name
        if samples is None:
            self.samples = np.random.uniform(range[0], range[1], size=10000)
        else:
            self.samples = samples

    def map(self,bins = 100):
        """Calculate maximum a posterior estimate"""
        prob, edges = np.histogram(self.samples, range=self.range, bins=bins)
        bin_widths = edges[1:] - edges[:-1]
#        print prob
#        plt.p
        prob = prob.clip(min=0.0000000001)
        max_index = np.argmax(prob)
        return edges[max_index]+bin_widths[max_index]/2.

    def entropy(self):
        """Compute Shannon entropy of this distribution"""
        prob, edges = np.histogram(self.samples, range=self.range, bins=100)
        prob = prob.clip(min=0.0000000001)
        return entropy(prob)

    def hist(self,bins = 100,normed = False):
        """Plot distribution samples as histogram"""
        plt.hist(self.samples, range=self.range, bins=bins, histtype='step',normed = True)

    def plot(self):
        """Draw distribution using KDE"""
        xs = np.linspace(*self.range, num = 100)
        kernel = gaussian_kde(self.samples[~np.isnan(self.samples)])
        plt.plot(xs, [kernel(x) for x in xs])

    def pdf(self, theta):
        kernel = gaussian_kde(self.samples[~np.isnan(self.samples)])
        return kernel(theta)
