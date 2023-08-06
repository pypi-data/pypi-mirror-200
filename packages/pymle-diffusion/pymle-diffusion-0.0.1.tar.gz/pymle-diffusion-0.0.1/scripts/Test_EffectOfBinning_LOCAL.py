from pymle.ctmc.StateSpace import StateSpace
from pymle.ctmc.utility.test_utils import *
from pymle.ctmc.utility.plot_utils import *
from pymle.core.TransitionDensity import *
from pymle.fit.AnalyticalMLE import AnalyticalMLE
import seaborn as sns

sns.set_style('whitegrid')

T = 5  # num years
freq = 250  # observations per year
dt = 1. / freq
M = T * freq

N_states = 300  # Number of ctmc states

#################
# Choose which model  (test case)
#################
model_id = 1

seed = None #  CIR = 343

model, is_positive, S0, params, bounds, params0, simulator = get_test_case(M=M, dt=dt, model_id=model_id, seed=seed)
generator = get_generator_for_test(model_id=model_id, params=params)

# =========================
# Simulate the sample path
# =========================
path = simulator.sim_path()

print(f"Freq = {freq}")
print(f"N = {len(path) - 1}")

# =========================
# Construct State-Space
# =========================
state_space = StateSpace.from_sample(sample=path, is_positive=is_positive, N_states=N_states,
                                     bump=0.1)

binned_path, state_index = state_space.bin_path(path)

# =========================
# Plot the sample vs Binned Sample
# =========================
plot_sample = False
if plot_sample:
    plot_CTMC_sample_vs_binned(path=path, binned_path=binned_path)

# =========================
# Estimate Parameters
# =========================
generator.states = state_space.states

estimator_exact = AnalyticalMLE(sample=path, dt=dt,
                                density=ExactDensity(model=generator.model), param_bounds=bounds)

estimator_binned = AnalyticalMLE(sample=binned_path, dt=dt,
                                density=ExactDensity(model=generator.model), param_bounds=bounds)


plot_Exact_Likelihood_binning_one_param(model_id=model_id, params=params,
                                        estimator_binned=estimator_binned,
                                        estimator_exact=estimator_exact)


