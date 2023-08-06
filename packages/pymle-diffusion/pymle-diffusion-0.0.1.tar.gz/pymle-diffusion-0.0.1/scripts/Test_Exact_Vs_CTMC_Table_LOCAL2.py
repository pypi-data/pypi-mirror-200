from pymle.ctmc.StateSpace import StateSpace
from pymle.ctmc.utility.test_utils import *
from pymle.ctmc.CTMCEstimator import CTMCEstimator
from pymle.core.TransitionDensity import *
from pymle.fit.AnalyticalMLE import AnalyticalMLE
import pandas as pd
import time
import seaborn as sns

sns.set_style('whitegrid')

T = 5  # num years
# freq = 12
freq = 24
#freq = 52  # observations per year
#freq = 250  # observations per year
#freq = 1000
dt = 1. / freq
M = T * freq

N_states = 300  # Number of ctmc states

N_trials = 500

#################
# Choose which model  (test case)
#################
model_id = 8

model, is_positive, S0, params, bounds, params0, simulator = get_test_case(M=M, dt=dt, model_id=model_id)
generator = get_generator_for_test(model_id=model_id, params=params)

print(f"Freq = {freq}")
print(f"N = {T * freq}")
print(f"S_0 = {S0}")

param_ctmc_ests = []
param_exact_ests = []
params_kessler_ests = []
params_osaki_ests = []
params_euler_ests = []

version = 2   # 1) CTMC, Exact
              # 2) CTMC, Kessler, Osaki

do_CTMC = True

do_exact = False
do_kessler = False
do_shoji_ozaki = False
do_euler = False

if version == 1:
    do_exact = True
elif version == 2:
    do_shoji_ozaki = True
    do_kessler = True
    # do_euler = True

estimator_names = []

for n in range(N_trials):
    print(f"------------ Trial {n + 1} of {N_trials} ------------------ \n")
    # =========================
    # Simulate the sample path
    # =========================
    path = simulator.sim_path()

    if do_CTMC:
        print("\n Running CTMC MLE: ")
        estimator_names.append("CTMC")
        t = time.time()
        state_space = StateSpace.from_sample(sample=path, is_positive=is_positive, N_states=N_states,
                                             bump=0.1)
        binned_path, state_index = state_space.bin_path(path)

        generator.states = state_space.states

        estimator = CTMCEstimator(binned_sample=binned_path, s_index=state_index,
                                  dt=dt, generator=generator, param_bounds=bounds)
        params_ctmc = estimator.estimate_params(params0=params0).params
        param_ctmc_ests.append(params_ctmc)
        print(f'TIME: {time.time() - t}\n')

    if do_exact:
        print("Running EXACT MLE: ")
        estimator_names.append("EXACT")
        t = time.time()
        estimator_exact = AnalyticalMLE(sample=path, dt=dt, density=ExactDensity(model=generator.model), param_bounds=bounds)
        params_exact = estimator_exact.estimate_params(params0=params0).params
        # params_exact = params
        param_exact_ests.append(params_exact)
        print(f'TIME: {time.time() - t}\n')

    if do_kessler:
        print("Running Kessler: ")
        estimator_names.append("Kessler")
        t = time.time()
        estimator = AnalyticalMLE(sample=path, dt=dt, density=KesslerDensity(model=generator.model), param_bounds=bounds)
        params_kessler = estimator.estimate_params(params0=params0).params
        params_kessler_ests.append(params_kessler)
        print(f'TIME: {time.time() - t}\n')

    if do_shoji_ozaki:
        print("Running Shoji-Ozaki: ")
        estimator_names.append("Shoji-Ozaki")
        t = time.time()
        estimator = AnalyticalMLE(sample=path, dt=dt,
                                  density=ShojiOzakiDensity(model=generator.model), param_bounds=bounds)
        params_ozaki = estimator.estimate_params(params0=params0).params
        params_osaki_ests.append(params_ozaki)
        print(f'TIME: {time.time() - t}\n')

    if do_euler:
        print("Running Euler: ")
        estimator_names.append("Euler")
        t = time.time()
        estimator = AnalyticalMLE(sample=path, dt=dt, density=EulerDensity(model=generator.model), param_bounds=bounds)
        params_euler = estimator.estimate_params(params0=params0).params
        params_euler_ests.append(params_euler)
        print(f'TIME: {time.time() - t}\n')


def get_stats(params_true: np.ndarray, params_est: List):
    cols = [f"Param{i}" for i in range(1, len(params_true) + 1)]
    ests = pd.DataFrame(data=np.vstack(params_est), columns=cols)

    means = ests.mean(axis=0)
    stds = ests.std(axis=0)

    errs = means-params_true
    means = np.round(means, 4)
    stds = np.round(stds, 4)

    return means, errs, stds


N = freq * T

print("Stats: \n -----------------------------------")

if version == 1:
    means_c, errs_c, stds_c = get_stats(params, params_est=param_ctmc_ests)
    means_e, errs_e, stds_e = get_stats(params, params_est=param_exact_ests)

    for i in range(len(params)):
        if i == 0:
            fprintf(f" %.0f & %.0f & $=%.3f$", N, freq, params[i])
        else:
            fprintf(f"  & & $=%.3f$ ", params[i])

        fprintf(f"  & %.3f & %.3f & %.3f", means_c[i], errs_c[i], stds_c[i])
        fprintf(f"  & %.3f & %.3f & %.3f ", means_e[i], errs_e[i], stds_e[i])

        fprintf(" \\\\ \n")

else:
    means_c, errs_c, stds_c = get_stats(params, params_est=param_ctmc_ests)
    means_e, errs_e, stds_e = get_stats(params, params_est=params_kessler_ests)
    #means_e, errs_e, stds_e = get_stats(params, params_est=params_euler_ests)
    means_s, errs_s, stds_s = get_stats(params, params_est=params_osaki_ests)

    for i in range(len(params)):
        if i == 0:
            fprintf(f" %.0f & %.0f & $=%.3f$", N, freq, params[i])
        else:
            fprintf(f"  & & $=%.3f$ ", params[i])

        fprintf(f"  &  %.3f & %.3f", errs_c[i], stds_c[i])
        fprintf(f"  &  %.3f & %.3f ", errs_e[i], stds_e[i])
        fprintf(f"  &  %.3f & %.3f ", errs_s[i], stds_s[i])

        fprintf(" \\\\ \n")
x = 2
