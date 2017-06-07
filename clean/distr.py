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
        prob = prob.clip(min=0.0000000001)
        max_index = np.argmax(prob)
        return edges[max_index]+bin_widths[max_index]/2.

    def entropy(self):
        """Compute Shannon entropy of this distribution"""
        prob, edges = np.histogram(self.samples, range=self.range, bins=100)
        prob = prob.clip(min=0.0000000001)
        return entropy(prob)

    def hist(self,**kwargs):
        """Plot distribution samples as histogram"""
        plt.hist(self.samples, range=self.range, **kwargs)

    def plot(self,*args,**kwargs):
        """Draw distribution using KDE"""
        xs = np.linspace(*self.range, num = 100)
        logpdf = self.approx_logpdf()
        plt.plot(xs, np.exp(logpdf(xs)))

    def pdf(self, theta):
        kernel = gaussian_kde(self.samples[~np.isnan(self.samples)])
        return kernel(theta)

    def approx_logpdf(self,bw = 0.1, mirror = False, mirror_shifts = None):
        if mirror:
            data = np.concatenate([
                (mirror_shifts[0]-self.samples),
                self.samples,
                (mirror_shifts[1]-self.samples)]
            )
        else:
            data = self.samples
        kernel = gaussian_kde(data, bw_method=bw)
        if mirror:
            return lambda x: np.log(3)+kernel.logpdf(x)
        else:
            return lambda x: kernel.logpdf(x)
