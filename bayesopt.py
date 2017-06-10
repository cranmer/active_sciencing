import numpy as np
from skopt import Optimizer
from skopt.learning import GaussianProcessRegressor
from skopt.learning.gaussian_process.kernels import ConstantKernel
from skopt.learning.gaussian_process.kernels import Matern, WhiteKernel

NRANDOM = 3
NTOTAL = 10

#cov_amplitude = ConstantKernel(1.0, (0.01, 5.0))
cov_amplitude = ConstantKernel(1.0, "fixed")

other_kernel = Matern(
    length_scale=np.ones(1),
    length_scale_bounds=[(0.3, 10)],
    nu=2.5)

white_kernel = WhiteKernel()

gp = GaussianProcessRegressor(
    kernel=cov_amplitude * other_kernel + white_kernel,
    normalize_y=True, alpha=0.0, noise=10e-7,
    n_restarts_optimizer=2)


def get_optimizer(range,nrandom):
    return Optimizer(dimensions=[range],
                    base_estimator=gp,
                    n_random_starts=nrandom)
