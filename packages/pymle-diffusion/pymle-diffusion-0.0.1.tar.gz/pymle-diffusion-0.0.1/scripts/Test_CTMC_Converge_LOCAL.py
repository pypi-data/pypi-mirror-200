from pymle.ctmc.StateSpace import StateSpace
from pymle.ctmc.utility.test_utils import *
from pymle.ctmc.utility.plot_utils import *
import seaborn as sns
from pymle.core.TransitionDensity import *
from pymle.fit.AnalyticalMLE import AnalyticalMLE

sns.set_style('whitegrid')

T = 5  # num years
freq = 250  # observations per year
dt = 1. / freq
M = T * freq

#################
# Choose which model  (test case)
#################
model_id = 1

model, is_positive, S0, params, bounds, params0, simulator = get_test_case(M=M, dt=dt, model_id=model_id)

# =========================
# Simulate the sample path
# =========================

# state_sizes = [20, 40, 80, 160, 320]
N_trials = 1
# state_sizes = [10, 20, 40, 80, 160, 320]
# state_sizes = [10, 20, 40, 80, 160]
state_sizes = [10, 20, 40, 60,  100, 160, 320, 400]
# state_sizes = [10, 20, 40]

errors_trials = []
errors_exact_trials = []

for n in range(N_trials):
    errors = []
    path = simulator.sim_path()

    for N_states in state_sizes:
        state_space = StateSpace.from_sample(sample=path, is_positive=is_positive, N_states=N_states,
                                             bump=0.05)

        binned_path, state_index = state_space.bin_path(path)

        generator = get_generator_for_test(model_id=model_id, params=params)
        generator.states = state_space.states

        estimator = CTMCEstimator(binned_sample=binned_path, s_index=state_index,
                                  dt=dt, generator=generator, param_bounds=bounds)

        if N_states == state_sizes[-1]:
            estimator_exact = AnalyticalMLE(sample=path, dt=dt,
                                            density=ExactDensity(model=generator.model), param_bounds=bounds)
            params_exact = estimator_exact.estimate_params(params0=params0).params

            err = np.sqrt(np.sum(np.power(params_exact - params, 2)))
            errors_exact_trials.append(err)

        params_opt, _ = estimator.estimate_params(params0=params0)
        err = np.sqrt(np.sum(np.power(params_opt - params, 2)))
        errors.append(err)
        print(f'Sates: {N_states}, Err: {err} \n')

    errors_trials.append(errors)

errors_trials = np.vstack(errors_trials)
errors = np.mean(errors_trials, axis=0)

err_exact = np.mean(np.asarray(errors_exact_trials))

plt.plot(state_sizes, errors, label='CTMC MLE')
plt.plot(state_sizes, err_exact * np.ones_like(state_sizes), label='Exact MLE', linestyle='dashed')

plt.xlabel(r'$m$', fontsize=12)
plt.ylabel(r'$||\theta - \hat \theta_{N,m}||$', fontsize=12)
plt.legend()
plt.show()
plt.loglog(state_sizes, errors)
plt.show()
