import gaussian
import math

PHI_RANGE     = [ 0.,6.]
THETA_RANGE   = [-2.,2.]
DATA_RANGE    = [-5.,5.] 
THE_SIMULATOR = gaussian.simulator


model_details_shifts = [-10.,10.]
model_details_mirror = False
model_details_lnlike_nsim = 1000
model_details_map_bins = 20

intro_theta_nom = 0.0
intro_phi_noms  = math.pi,math.pi/2.
intro_binning   = 51

example_phi = math.pi/2.
example_theta = 1.
example_ndata = 100


model_details_likelihood_settings = {
    'simulator': THE_SIMULATOR,
    'simulation_kwargs': {'n_samples': 200},
    'distr_kwargs': {'range': DATA_RANGE},
    'logpdf_kwargs': {'mirror': model_details_mirror, 'mirror_shifts': model_details_shifts}
}
