#! /usr/bin/env python3
""" Compare the speed of mine and PyMC's computation of Gelman et. al's effective sample size. """

import matplotlib.pyplot as plt
plt.style.use('seaborn')
import numpy as np
from scipy.stats import norm

from IPython import get_ipython
ipython = get_ipython()

def my_ESS(x):
    """ Compute the effective sample size of estimand of interest. Vectorised implementation. """
    m_chains, n_iters = x.shape

    variogram = lambda t: ((x[:, t:] - x[:, :(n_iters - t)])**2).sum() / (m_chains * (n_iters - t))

    post_var = my_gelman_rubin(x)

    t = 1
    rho = np.ones(n_iters)
    negative_autocorr = False

    # Iterate until the sum of consecutive estimates of autocorrelation is negative
    while not negative_autocorr and (t < n_iters):
        rho[t] = 1 - variogram(t) / (2 * post_var)

        if not t % 2:
            negative_autocorr = sum(rho[t-1:t+1]) < 0

        t += 1

    return int(m_chains*n_iters / (1 + 2*rho[1:t].sum()))

def my_gelman_rubin(x):
    """ Estimate the marginal posterior variance. Vectorised implementation. """
    m_chains, n_iters = x.shape

    # Calculate between-chain variance
    B_over_n = ((np.mean(x, axis=1) - np.mean(x))**2).sum() / (m_chains - 1)

    # Calculate within-chain variances
    W = ((x - x.mean(axis=1, keepdims=True))**2).sum() / (m_chains*(n_iters - 1))

    # (over) estimate of variance
    s2 = W * (n_iters - 1) / n_iters + B_over_n

    return s2

def ESS(x):
    """ Compute the effective sample size of estimand of interest. PyMC's implementation. """
    m_chains, n_iters = x.shape

    variogram = lambda t: (sum(sum((x[j][i] - x[j][i-t])**2 for i in range(t, n_iters)) for j in
                               range(m_chains)) / (m_chains * (n_iters - t)))

    post_var = gelman_rubin(x)

    t = 1
    rho = np.ones(n_iters)
    negative_autocorr = False

    # Iterate until the sum of consecutive estimates of autocorrelation is negative
    while not negative_autocorr and (t < n_iters):
        rho[t] = 1 - variogram(t) / (2 * post_var)

        if not t % 2:
            negative_autocorr = sum(rho[t-1:t+1]) < 0

        t += 1

    return int(m_chains * n_iters / (1 + 2*rho[1:t].sum()))

def gelman_rubin(x):
    """ Estimate the marginal posterior variance. PyMC's implementation. """
    m_chains, n = x.shape

    # Calculate between-chain variance
    B_over_n = ((np.mean(x, axis=1) - np.mean(x))**2).sum() / (m_chains - 1)

    # Calculate within-chain variances
    W = np.sum([(x[i] - xbar) ** 2 for i, xbar in enumerate(np.mean(x, 1))]) / (m_chains * (n - 1))

    # (over) estimate of variance
    s2 = W * (n - 1) / n + B_over_n

    return s2

if __name__ == "__main__":
    # Observed data
    data = np.zeros(2)

    # Number of iterations and number of runs to make
    iters = 10000
    runs = 4

    # Initial values
    mu_cur = np.array([[2.5, 2.5], [2.5, -2.5], [-2.5, 2.5], [-2.5, -2.5]])

    # Array to store output in
    output = np.zeros([runs, 2, iters])
    output[:, :, 0] = mu_cur
    # Innovation size
    rw_cov = np.eye(2)

    for j in range(runs):
        ll_cur = norm.logpdf(data, mu_cur[j], 1).sum()
        accept = 0

        for i in range(1, iters):
            # Propose new values
            mu_prop = np.random.multivariate_normal(mu_cur[j], rw_cov)
            # Compute log-likelihood of proposed values
            ll_prop = norm.logpdf(data, mu_prop, 1).sum()

            # Accept or reject proposal
            if ll_prop - ll_cur > np.log(np.random.uniform()):
                mu_cur[j] = mu_prop.copy()
                ll_cur = ll_prop
                accept += 1

            # Record current state of chain
            output[j, :, i] = mu_cur[j]

        print("Chain {} acceptance rate was: {:.2f}%".format(j, accept / (iters - 1) * 100))

    # Plot walk around parameter space
    fig, ax = plt.subplots(1, 1)
    for j in range(runs):
        ax.plot(output[j, 0, :], output[j, 1, :])

    ax.set_aspect('equal')
    ax.set_xlabel(r'$\mu_1$')
    ax.set_ylabel(r'$\mu_2$')
    fig.tight_layout()

    # Plot trajectories of chains
    fig, ax = plt.subplots(1, 2)

    for i in range(2):
        for j in range(runs):
            ax[i].plot(np.r_[:iters], output[j, i, :])

        ax[i].set_xlabel('Iteration')
        ax[i].set_ylabel(r'$\mu_{}$'.format(i+1))

        ax[i].set_xticks((0, iters))
        ax[i].set_xticklabels((0, r'$10\,000$'))
        ax[i].set_xlim((0, iters))

    fig.tight_layout()

    ipython.magic('timeit ESS(output[:, 0, :])')
    ipython.magic('timeit my_ESS(output[:, 0, :])')
