#example1

# import matplotlib.pyplot as plt
#
# import arviz as az
#
# az.style.use("arviz-darkgrid")
#
# data = az.load_arviz_data("centered_eight")
# az.plot_autocorr(data, var_names=("tau", "mu"))
#
# plt.show()


from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import pymc3 as pm

import sys
from io import StringIO

from scipy.stats import norm, multivariate_normal, beta, binom, stats
from scipy.stats import t as stats_t
from scipy.special import beta as beta_func
from scipy.special import binom as special_binom
from scipy.special import betaln as special_betaln
from scipy.optimize import fmin
from scipy.interpolate import spline
from mpl_toolkits.mplot3d.axes3d import Axes3D
import arviz as az
# x = np.linspace(-2, 2, 40)
# y = x**2
#
# plt.figure(figsize=(16, 6))
# plt.plot(x, y)
# plt.show()


def main(argv=None):
    RANDOM_SEED = 8927
    np.random.seed(RANDOM_SEED)
    az.style.use("arviz-darkgrid")
    T = 10000
    y = np.zeros((T,))
    # true stationarity:
    true_theta = 0.95
    # true variance of the innovation:
    true_tau = 1.0
    # true process mean:
    true_center = 0.0

    for t in range(1, T):
        y[t] = true_theta * y[t - 1] + np.random.normal(loc=true_center, scale=true_tau)

    y = y[-5000:]
    # 取-5000到最后一个数
    plt.plot(y, alpha=0.8)
    plt.xlabel("Timestep")
    plt.ylabel("$y$")
    # plt.show()
    # print(y)
    with pm.Model() as ar1:
        # assumes 95% of prob mass is between -2 and 2
        theta = pm.Normal("theta", 0.0, 1.0)
        # variance of the innovation term
        tau = pm.Exponential("tau", 0.5)
        # process mean
        center = pm.Normal("center", mu=0.0, sigma=1.0)

        likelihood = pm.AR1("y", k=theta, tau_e=tau, observed=y - center)

        trace = pm.sample(2000, tune=2000, init="advi+adapt_diag", random_seed=RANDOM_SEED)
        idata = az.from_pymc3(trace)
        az.plot_trace(
            idata,
            lines=[
                ("theta", {}, true_theta),
                ("tau", {}, true_tau),
                ("center", {}, true_center),
            ],
        )
        plt.show()

if __name__ == '__main__':
     sys.exit(main())