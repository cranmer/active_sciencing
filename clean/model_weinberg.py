import weinberg
import  math

PHI_RANGE     = [40.,50.]
THETA_RANGE   = [0.5,1.5]
DATA_RANGE    = [-1,1] 
THE_SIMULATOR = weinberg.simulator

model_details_shifts = [-2.,2.]
model_details_mirror = True
model_details_lnlike_nsim = 1000
model_details_map_bins = 20

intro_theta_nom = 1.0
intro_phi_noms  = 43,47
intro_binning   = 21

example_phi = 47.
example_theta = 1.0
example_ndata = 100


liklihood_settings_1 = dict(
               simulator = THE_SIMULATOR,
       simulation_kwargs = {'n_samples': model_details_lnlike_nsim},
            distr_kwargs = {'range': DATA_RANGE},
           logpdf_kwargs = {'mirror': model_details_mirror, 'mirror_shifts': model_details_shifts}
)


liklihood_settings_2 = dict(simulator = THE_SIMULATOR,
       simulation_kwargs = {'n_samples': 3000},
            distr_kwargs = {'range': DATA_RANGE},
           logpdf_kwargs = {'mirror': model_details_mirror, 'mirror_shifts': model_details_shifts}
)