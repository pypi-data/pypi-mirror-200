# ===============================================
# Real FX Rate Data Examples
# ===============================================
import pandas as pd
import matplotlib.pyplot as plt
from pymle.models.CIR import CIR
from pymle.core.TransitionDensity import *
import seaborn as sns
import matplotlib.dates as mdates
import datetime

sns.set_style('whitegrid')
# As a first step, we read the data into a pandas ‘DataFrame’ from the data directory:
df = pd.read_csv("../data/FX_USD_EUR.csv")
df.columns = ['Date', 'Rate']
df['Rate'] = df['Rate']

# To generate Figure 4 with properly formatted dates, we run the following:
skip = 20  # Change to sample time series at a different freq
dt = skip / 252.
sample = df['Rate'].values[:-1:skip]
df['Date'] = [datetime.datetime.strptime(d, "%m/%d/%Y").date() for d in df['Date']]
fig, ax = plt.subplots()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

ax.plot(df['Date'].values, df['Rate'].values)
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
fig.autofmt_xdate()
plt.show()

# We then initialize the CIR model as follows, and supply an initial guess and parameter bounds
# for the fit
model = CIR()
guess = np.asarray([.24, 1.0, 0.1])  # kappa, mu, sigma
param_bounds = [(0.01, 5), (0.01, 2), (0.01, 0.9)]

from pymle.fit.AnalyticalMLE import AnalyticalMLE
from pymle.core.TransitionDensity import *

euler_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=EulerDensity(model)).estimate_params(guess)
print('\nEuler: --------------------')
print(euler_est)

exact_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=ExactDensity(model)).estimate_params(guess)

print('\nExact MLE: --------------------')
print(exact_est)

ozaki_est = AnalyticalMLE(sample, param_bounds, dt,
                          density=OzakiDensity(model)).estimate_params(guess)

print('\nOzaki: --------------------')
print(ozaki_est)

shoji_ozaki_est = AnalyticalMLE(sample, param_bounds, dt,
                                density=ShojiOzakiDensity(model)).estimate_params(guess)

print('\nShoji-Ozaki: --------------------')
print(shoji_ozaki_est)

kessler_est = AnalyticalMLE(sample, param_bounds, dt,
                            density=KesslerDensity(model)).estimate_params(guess)

print('\nKessler: --------------------')
print(kessler_est)

AitSahalia_est = AnalyticalMLE(sample, param_bounds, dt,
                               density=AitSahaliaDensity(model)).estimate_params(guess)
print('\nAit-Sahalia: --------------------')
print(AitSahalia_est)
