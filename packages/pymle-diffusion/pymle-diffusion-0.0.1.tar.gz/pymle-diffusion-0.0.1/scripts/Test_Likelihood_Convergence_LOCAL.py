from pymle.ctmc.StateSpace import StateSpace
from pymle.ctmc.utility.test_utils import *
from pymle.ctmc.utility.plot_utils import *
import seaborn as sns

sns.set_style('whitegrid')

T = 5  # num years
freq = 250  # observations per year
dt = 1. / freq
M = T * freq

#################
# Choose which model  (test case)
#################
model_id = 4

model, is_positive, S0, params, bounds, params0, simulator = get_test_case(M=M, dt=dt, model_id=model_id)

# =========================
# Simulate the sample path
# =========================

# state_sizes = [20, 40, 80, 160, 320]
N_trials = 1
# state_sizes = [10, 20, 40, 80, 160, 320]
# state_sizes = [10, 20, 40, 80, 160]
state_sizes = [150, 200, 300]
# state_sizes = [10, 20, 40]

path = simulator.sim_path()

for N_states in state_sizes:
    state_space = StateSpace.from_sample(sample=path, is_positive=is_positive, N_states=N_states,
                                         bump=0.1)

    binned_path, state_index = state_space.bin_path(path)

    generator = get_generator_for_test(model_id=model_id, params=params)
    generator.states = state_space.states

    estimator = CTMCEstimator(binned_sample=binned_path, s_index=state_index,
                              dt=dt, generator=generator, param_bounds=bounds)

    sigmas = np.linspace(0.3, 0.5, 35)
    kappa = params[0]
    mu = params[1]
    Ls = np.asarray([estimator.log_likelihood_negative(np.asarray([kappa, mu, sig])) for sig in sigmas])
    print(f"Minizer: {sigmas[np.nanargmin(Ls)]}")
    Ls = Ls - np.min(Ls)
    plt.plot(sigmas, Ls, label=r"CTMC Likelihood", linestyle='solid')

plt.show()