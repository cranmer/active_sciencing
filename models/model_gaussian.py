import math
import gaussian

name = 'gaussian'

phi_range     = [ 0.,6.]
theta_range   = [-2.,2.]
data_range    = [-5.,5.] 
simulator     = gaussian.simulator

details_shifts = [-10.,10.]
details_mirror = False
details_lnlike_nsim = 1000
details_map_bins = 20
details_likelihood_settings = {
    'simulator': simulator,
    'simulation_kwargs': {'n_samples': 200},
    'distr_kwargs': {'range': data_range},
    'logpdf_kwargs': {'mirror': details_mirror, 'mirror_shifts': details_shifts}
}

intro_theta_nom = 0.0
intro_phi_noms  = math.pi,math.pi/2.
intro_binning   = 51

example_phi = math.pi/2.
example_theta = 1.
example_ndata = 100


