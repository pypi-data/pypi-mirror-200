# ===============================================
# Initial Examples
# ===============================================

from pymle.models import OrnsteinUhlenbeck
import numpy as np

S0 = 0.4  # initial value of process
kappa = 3  # rate of mean reversion
mu = 0.3  # long term level of process
sigma = 0.2  # volatility

model = OrnsteinUhlenbeck()
model.params = np.array([kappa, mu, sigma])

from pymle.sim.Simulator1D import Simulator1D

T = 5  # num years of the sample
freq = 250  # observations per year
dt = 1. / freq  # time step (constant for the example)
seed = 123  # random seed: set to None to get new results each time

simulator = Simulator1D(S0, T * freq, dt, model).set_seed(seed)
sample = simulator.sim_path()

import matplotlib.pyplot as plt

plt.plot(sample)
plt.xlabel('t')
plt.ylabel(r' $S_t$')
plt.show()

"""
To fit using any of the estimation procedures, we must specify the parameter bounds we wish
the optimizer to enforce during the fit, along with an initial guess for the parameters:
"""
param_bounds = [(0, 10), (0, 4), (0.01, 1)]  # kappa, mu, sigma
guess = np.array([1, 0.1, 0.4])

from pymle.fit.AnalyticalMLE import AnalyticalMLE
from pymle.core.TransitionDensity import EulerDensity

euler_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=EulerDensity(model)).estimate_params(guess)

from pymle.core.TransitionDensity import *

ozaki_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=OzakiDensity(model)).estimate_params(guess)
shoji_ozaki_est = AnalyticalMLE(sample, param_bounds, dt,
                                density=ShojiOzakiDensity(model)).estimate_params(guess)
kessler_est = AnalyticalMLE(sample, param_bounds, dt,
                            density=KesslerDensity(model)).estimate_params(guess)
AitSahalia_est = AnalyticalMLE(sample, param_bounds, dt,
                               density=AitSahaliaDensity(model)).estimate_params(guess)



