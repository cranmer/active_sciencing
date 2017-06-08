
# coding: utf-8

# In[1]:

import math
import numpy as np
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt

# In[2]:


import distr
import common
import multiprocessing


# In[3]:


import gaussian


# In[4]:


PHI_RANGE     = [ 0.,6.]
THETA_RANGE   = [-2.,2.]
DATA_RANGE    = [-5.,5.] 
THE_SIMULATOR = gaussian.simulator
MODEL_NAME = 'gaussian'


# In[5]:


model_details_shifts = [-10.,10.]
model_details_mirror = False
model_details_lnlike_nsim = 1000
model_details_map_bins = 20


# In[6]:


intro_theta_nom = 0.0
intro_phi_noms  = math.pi,math.pi/2.
intro_binning   = 51

example_phi = math.pi/2.
example_theta = 1.
example_ndata = 100


# # Introducing the Model p(x|$\theta$,$\Phi$)

# In[7]:


cm = plt.get_cmap('copper')
fig,axarr = plt.subplots(1,3)
fig.set_size_inches(20,5)
bins = np.linspace(*DATA_RANGE, num = intro_binning)

nsteps_phi, theta_nom = 6, intro_theta_nom
for i,phi in enumerate(np.linspace(*PHI_RANGE,num = nsteps_phi)):
    _=axarr[0].hist(THE_SIMULATOR(theta_nom,phi,10000), bins = bins, color = cm(i/float(nsteps_phi)), alpha = 0.5, histtype='step')

nsteps_theta, phi_nom = 6, intro_phi_noms[0]
for i,theta in enumerate(np.linspace(*THETA_RANGE,num = nsteps_theta)):
    _=axarr[1].hist(THE_SIMULATOR(theta,phi_nom,10000), bins = bins, color = cm(i/float(nsteps_phi)), alpha = 0.5, histtype='step')
    
nsteps_theta, phi_nom = 6, intro_phi_noms[1]
for i,theta in enumerate(np.linspace(*THETA_RANGE,num = nsteps_theta)):
    _=axarr[2].hist(THE_SIMULATOR(theta,phi_nom,10000), bins = bins, color = cm(i/float(nsteps_phi)), alpha = 0.5, histtype='step')
    
plt.savefig('{}_intro.pdf'.format(MODEL_NAME))
plt.savefig('{}_intro.pdf'.format(MODEL_NAME))


# # An Example Experiment
# ## Taking Data

# In[8]:


fig,axarr = plt.subplots(1,2)
fig.set_size_inches(20,5)


bins = np.linspace(*DATA_RANGE, num = 11)
example_data = common.collect_data(example_phi,THE_SIMULATOR, theta_nature=example_theta, n_samples = example_ndata)
datacounts,bins = np.histogram(example_data,bins = bins)
centers = bins[:-1] + (bins[1:]-bins[:-1])/2.
axarr[0].errorbar(centers,datacounts,fmt = 'o',xerr = (bins[1:]-bins[:-1])/2.,yerr = np.sqrt(datacounts), c = 'k')

n_mc = 10000
mc = THE_SIMULATOR(example_theta,example_phi,n_mc) #simulate much more than data
mccounts,_,_ = axarr[0].hist(mc,weights = [float(example_ndata)/float(n_mc)]*n_mc, bins = bins)

####

samples = THE_SIMULATOR(example_theta,example_phi,n_mc)
p = distr.Distribution(
    name = 'example_simulation',
    samples = samples,
    range = DATA_RANGE)

p.hist(bins = 10, normed = True,ax = axarr[1])

xs = np.linspace(*DATA_RANGE,num = 21)
logpdf_nomirr = p.approx_logpdf()
logpdf_mirror = p.approx_logpdf(mirror = True, mirror_shifts=model_details_shifts)

axarr[1].plot(xs,np.exp(logpdf_nomirr(xs)))
axarr[1].plot(xs,np.exp(logpdf_mirror(xs)))

plt.savefig('{}_data.pdf'.format(MODEL_NAME))
plt.savefig('{}_data.pdf'.format(MODEL_NAME))


# ## The likelihood $p(x|\theta,\Phi)$ and the prior $p(\theta|\Phi)$

# In[11]:


test_thetas = np.linspace(*THETA_RANGE,num = 6)
pool = multiprocessing.Pool(4)


nll = [pool.apply_async(common.lnlike,
                        args = (theta_test,example_data,example_phi),
                        kwds = dict(
                         simulator=THE_SIMULATOR,
                         simulation_kwargs = {'n_samples': model_details_lnlike_nsim},
                         distr_kwargs =  {'range': DATA_RANGE},
                         logpdf_kwargs = {'mirror': model_details_mirror, 'mirror_shifts': model_details_shifts}
                        )
                       ) for theta_test in test_thetas]
[r.ready() for r in nll]
pool.close()
pool.join()

nll = [r.get() for r in nll]

fig,axarr = plt.subplots(1,2)
fig.set_size_inches(20,5)

axarr[0].plot(test_thetas,nll)
axarr[0].axvline(example_theta, c = 'grey') #truth
axarr[0].axvline(test_thetas[np.argmax(nll)], c = 'r') #max NLL


example_prior = distr.Distribution('prior',range = THETA_RANGE)
xs = np.linspace(*THETA_RANGE,num = 21)
logpdf = example_prior.approx_logpdf()
axarr[1].plot(xs,np.exp(logpdf(xs)))


plt.savefig('{}_likli.pdf'.format(MODEL_NAME))
plt.savefig('{}_likli.pdf'.format(MODEL_NAME))


# ## The posterior $p(\theta|x,\Phi)$

# In[12]:


example_posterior = common.calculate_posterior(
    example_prior,example_data,example_phi,
    lnprob_args = dict(simulator = THE_SIMULATOR,
                       simulation_kwargs = {'n_samples': model_details_lnlike_nsim},
                       distr_kwargs =  {'range': DATA_RANGE},
                       logpdf_kwargs = {'mirror': model_details_mirror, 'mirror_shifts': model_details_shifts}
                  ),
    n_chainlen = 50
)


# In[13]:


xs = np.linspace(*THETA_RANGE,num = model_details_map_bins+1)
example_posterior.hist(bins = model_details_map_bins,normed = True)
example_prior.plot()
example_posterior.plot()
example_best_theta = example_posterior.map(bins = model_details_map_bins)
plt.axvline(example_best_theta, c = 'k')

plt.savefig('{}_post.pdf'.format(MODEL_NAME))
plt.savefig('{}_post.pdf'.format(MODEL_NAME))







