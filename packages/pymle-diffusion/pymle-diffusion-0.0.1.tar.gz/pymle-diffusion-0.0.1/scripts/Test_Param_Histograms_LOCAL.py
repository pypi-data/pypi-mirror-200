from pymle.ctmc.StateSpace import StateSpace
from pymle.ctmc.utility.test_utils import *
from pymle.ctmc.CTMCEstimator import CTMCEstimator
from pymle.core.TransitionDensity import *
from pymle.fit.AnalyticalMLE import AnalyticalMLE
import matplotlib.pyplot as plt
import pandas as pd
import time
import seaborn as sns

sns.set_style('whitegrid')

T = 5  # num years

# freq = 12
#freq = 52  # observations per year
# freq = 24
freq = 250  # observations per year
#freq = 1000

dt = 1. / freq
M = T * freq

N_states = 400  # Number of ctmc states

N_trials = 300

#################
# Choose which model  (test case)
#################
model_id = 1

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


do_CTMC = True

do_exact = True
do_kessler = False
do_shoji_ozaki = False
do_euler = False

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

xlabels = [r'$\mu$', r'$\sigma$']
for i in range(len(xlabels)):
    ps_exact = np.zeros(N_trials)
    ps_ctmc = np.zeros(N_trials)
    for n in range(N_trials):
        ps_exact[n] = param_exact_ests[n][i]
        # ps_ctmc[n] = param_exact_ests[n][i]
        ps_ctmc[n] = param_ctmc_ests[n][i]

    # f = plt.figure(figsize=(5,5), dpi=360)
    # np.histogram(ps, bins=10, range=None, normed=None, weights=None, density=None)
    plt.hist(ps_exact, bins=15, label='CTMC', density=True, alpha=0.5)
    plt.hist(ps_ctmc, bins=15, label='Exact', density=True, alpha=0.5)

    plt.legend()
    plt.ylabel('density')
    plt.xlabel(xlabels[i])

    #ax = plt.gca()
    #ax.set_rasterized(True)
    plt.show()
    plt.savefig(f'C:/temp/hist_param_{i}.png')


