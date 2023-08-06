from pymle.ctmc.StateSpace import StateSpace
from pymle.ctmc.AdaptiveCTMC import AdaptiveCTMC
from pymle.ctmc.utility.test_utils import *
from pymle.ctmc.utility.plot_utils import *
from pymle.core.TransitionDensity import *
from pymle.fit.AnalyticalMLE import AnalyticalMLE
import seaborn as sns
import time

sns.set_style('whitegrid')

T = 5  # num years
freq = 250  # observations per year
dt = 1. / freq
M = T * freq

N_states = 300  # Number of ctmc states

#################
# Choose which model  (test case)
#################
model_id = 4

seed = None #  CIR = 343

model, is_positive, S0, params, bounds, params0, simulator = get_test_case(M=M, dt=dt, model_id=model_id, seed=seed)
generator = get_generator_for_test(model_id=model_id, params=params)

# =========================
# Simulate the sample path
# =========================
path = simulator.sim_path()
x = 2
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
plot_sample = True
if plot_sample:
    plot_CTMC_sample_vs_binned(path=path, binned_path=binned_path)

# =========================
# Estimate Parameters
# =========================
generator.states = state_space.states

estimator = CTMCEstimator(binned_sample=binned_path, s_index=state_index,
                          dt=dt, generator=generator, param_bounds=bounds)
estimator_exact = AnalyticalMLE(sample=path, dt=dt,
                                density=ExactDensity(model=generator.model), param_bounds=bounds)

plot_counts = True
if plot_counts:
    plot_CTMC_Counts_C_Matrix(estimator=estimator)

plot_likelihood = False
if plot_likelihood:
    plot_CTMC_vs_Exact_Likelihood_one_param(model_id=model_id, params=params,
                                            estimator=estimator,
                                            estimator_exact=estimator_exact,
                                            do_psuedo=True,
                                            do_shoji_ozaki=True,
                                            do_kessler=True,
                                            do_elerian=False)


#################################
# Optimize
#################################
do_exact_mle = True

if do_exact_mle and generator.model.has_exact_density:
    print("\nRunning EXACT MLE: ")
    t = time.time()
    params_exact = estimator_exact.estimate_params(params0=params0).params
    print(f"Time: {time.time() - t}")
    error = np.sqrt(np.sum(np.power(params_exact - params, 2)))
    print(f"Exact Mle Error: {error}")

print("\n Running CTMC MLE: ")

t = time.time()
params_opt = estimator.estimate_params(params0=params0).params
print(f"Time: {time.time() - t}")
error = np.sqrt(np.sum(np.power(params_opt - params, 2)))
print(f"CTMC Mle Error: {error}")

do_adaptive = False
if do_adaptive:
    print("\n Running Adaptive CTMC MLE: ")
    estimator = AdaptiveCTMC(sample=path,
                             dt=dt, generator=generator, param_bounds=bounds)

    t = time.time()
    params_opt, _ = estimator.estimate_params(params0=params0)
    print(f"Time: {time.time() - t}")
    error = np.sqrt(np.sum(np.power(params_opt - params, 2)))
    print(f"CTMC Mle Error: {error}")

# =========================
# Plot Estimated Densities
# =========================
plot_est = False
if plot_est:
    plot_CTMC_estimated_density(params=params, params_est=params_opt, dt=dt, generator=generator)


# =========================
# Plot Estimated Path
# =========================
plot_path_vs_est = False

if plot_path_vs_est:

    plt.plot(path, label='Original Path', linestyle='solid')
    plt.xlabel('time index', fontsize=12)
    plt.ylabel('process', fontsize=12)

    simulator.model.params = params_opt
    simulator.set_seed(seed=seed)
    path_est = simulator.sim_path()

    plt.plot(path_est, label='Estimated Path', linestyle='dashed')
    plt.legend()
    plt.show()
