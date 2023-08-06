
# ===============================================
# CTMC Examples
# ===============================================
from pymle.sim.Simulator1D import Simulator1D
from pymle.models import OrnsteinUhlenbeck
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

S0 = 0.2  # initial value of process
kappa = 4  # rate of mean reversion
mu = 0.2  # long term level of process
sigma = 0.4  # volatility

T = 5  # num years of the sample
freq = 250  # observations per year
dt = 1. / freq  # time step (constant for the example)
seed = 123  # random seed: set to None to get new results each time

model = OrnsteinUhlenbeck()
model.params = np.array([kappa, mu, sigma])

simulator = Simulator1D(S0, T * freq, dt, model).set_seed(seed)
sample = simulator.sim_path()

model = OrnsteinUhlenbeck()
model.params = np.array([kappa, mu, sigma])

from pymle.ctmc.StateSpace import StateSpace

N_states = 30  # Set low just to illustrate the binning
state_space = StateSpace.from_sample(sample, is_positive=True, N_states=30)
binned_path, state_index = state_space.bin_path(sample)

from pymle.ctmc.Generator1D import Generator1D
from pymle.ctmc.CTMCEstimator import CTMCEstimator

generator = Generator1D(model)
generator.states = state_space.states

param_bounds = [(0, 10), (0, 4), (0.01, 1)]  # kappa, mu, sigma
guess = np.array([1, 0.1, 0.4])

ctmc_estimator = CTMCEstimator(binned_path, state_index, dt, generator,
                               param_bounds)
ctmc_est = ctmc_estimator.estimate_params(guess)

sns.set_style('whitegrid')


def plot_CTMC_sample_vs_binned(path: np.ndarray, binned_path: np.ndarray):
    plt.plot(path, label='Original Path', linestyle='solid')
    plt.xlabel('time index', fontsize=12)
    plt.ylabel('process', fontsize=12)
    plt.plot(binned_path, label='Binned Path', linestyle='dashed')
    plt.legend()
    plt.show()


plot_CTMC_sample_vs_binned(path=sample, binned_path=binned_path)


def plot_CTMC_Counts_C_Matrix(estimator: CTMCEstimator):
    C = pd.DataFrame(estimator.transition_counts)
    ax = sns.heatmap(C, cmap=sns.color_palette("Blues", as_cmap=True),
                     linewidths=.5, yticklabels=False, xticklabels=5)
    plt.xlabel('state')
    plt.show()


plot_CTMC_Counts_C_Matrix(estimator=ctmc_estimator)
