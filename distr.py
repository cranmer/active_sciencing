from scipy.stats import entropy, gaussian_kde
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin


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
        self._approx_pdf=None
        if samples is None:
            self.samples = np.random.uniform(range[0], range[1], size=10000)
        else:
            self.samples = samples

    def map(self,bins = 20, use_kde=True):
        """Calculate maximum a posterior estimate"""
        if use_kde:
            approx_pdf = self.approx_pdf()
            return fmin(lambda x: -approx_pdf(x),x0=np.mean(self.samples), disp=False)[0]
        else:
            prob, edges = np.histogram(self.samples, range=self.range, bins=bins)
            bin_widths = edges[1:] - edges[:-1]
            prob = prob.clip(min=0.0000000001)
            max_index = np.argmax(prob)
            return edges[max_index]+bin_widths[max_index]/2.

    def entropy(self):
        """Compute Shannon entropy of this distribution"""
        approx_pdf = self.approx_pdf()
        prob = approx_pdf(np.linspace(self.range[0],self.range[1],100))
        return entropy(prob)

    def hist(self,ax = plt, **kwargs):
        """Plot distribution samples as histogram"""
        ax.hist(self.samples, range=self.range, **kwargs)

    def plot(self,ax = plt, *args,**kwargs):
        """Draw distribution using KDE"""
        xs = np.linspace(*self.range, num = 100)
        approx_pdf = self.approx_pdf()
        ax.plot(xs, approx_pdf(xs))

    def pdf(self, theta):
        approx_pdf = self.approx_pdf()
        return approx_pdf(theta)

    def approx_pdf(self,bw = 0.1, mirror = False, mirror_shifts = None):
        if self._approx_pdf != None:
            return self._approx_pdf

        if mirror:
            data = np.concatenate([
                (mirror_shifts[0]-self.samples),
                self.samples,
                (mirror_shifts[1]-self.samples)]
            )
        else:
            data = self.samples

        kernel = gaussian_kde(data) 
        if mirror:
            return lambda x: 3*kernel.pdf(x)
        else:
            return lambda x: kernel.pdf(x)

    def approx_logpdf(self,bw = 0.1, mirror = False, mirror_shifts = None):
        approx_pdf = self.approx_pdf()
        return lambda x: np.log(approx_pdf(x))
