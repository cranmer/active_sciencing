import math
import yadage_sim_local

name = 'weinberg'

phi_range     = [40.,50.]
theta_range   = [0.5,1.5]
data_range    = [-1,1] 
simulator     = yadage_sim_local.simulator

details_shifts = [-2.,2.]
details_mirror = True
details_lnlike_nsim = 1000
details_map_bins = 20
details_likelihood_settings = {
    'simulator': simulator,
    'simulation_kwargs': {'n_samples': 200},
    'distr_kwargs': {'range': data_range},
    'logpdf_kwargs': {'mirror': details_mirror, 'mirror_shifts': details_shifts}
}

intro_theta_nom = 1.0
intro_phi_noms  = 43,47
intro_binning   = 21

example_phi = 47.
example_theta = 1.0
example_ndata = 100


