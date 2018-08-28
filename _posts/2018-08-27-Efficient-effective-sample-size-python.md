---
layout: post
title: Speeding up Python code with Numpy&#58; an example case
image: https://jwalton3141.github.io/assets/ESS/Astro-ML.png
mathjax: true
---

In this post I shall introduce the defintion of the effective sample size (ESS) as given by Gelman *et. al* in their book [Bayesian Data Analysis 3](http://www.stat.columbia.edu/~gelman/book/). Afterwards I shall review [PyMC](https://pymc-devs.github.io/pymc/README.html#purpose)'s computation of the ESS. PyMC's implementation provides a perfect example case of how we can speed up code with [Numpy](https://docs.scipy.org/doc/numpy/user/whatisnumpy.html#what-is-numpy). I show how we can do so and compute the ESS over *500x faster* than PyMC. I've posted the full example code and speed comparison used in this post [here](https://github.com/jwalton3141/jwalton3141.github.io/blob/master/assets/ESS/rwmh.py).

## Effective sample size

The statistican is often interested in drawing random samples from probability distributions. For nice, well-behaved distributions they can do this easily, and the draws made are all independent of one another. However, it is often of interest to draw from some nasty intractable distributions, from which we cannot easily sample. MCMC provides a way of making draws from these complex distributions. However, the samples made are not independent. 

The effective sample size (ESS) is introduced as a notion to assess the `size' of a sample when the samples are correlated. As such, the ESS provides the practitioner a way to assess the output and efficiency of their MCMC scheme.

## Definition

I've tried to keep this defintion as concise as possible. If you'd like more details and justification, see section 11.5 of BDA3. In contrast, if you're not interested in the maths, feel free to skip ahead and see how I improved PyMC's computation of the ESS in python.

Consider that we have \\( m \\) chains of length \\( n\\), which target some estimand of interest \\( \psi \\), where we label the simulations as \\( \psi\_{i, j}\\) \\( (i=1,\ldots,n;j=1,\ldots,m) \\). If the \\( n \\) simulation draws are all independent within each chain, then the between sequence variance \\( B \\) is an unbiased estimator of \\( \textrm{var}( \psi \mid y ) \\), and we have realised \\( mn \\) independent samples. Often, though, each sequence is autocorrelated and so we see that the between sequence variance \\( B \\) is greater than the posterior variance \\( \textrm{var}( \psi \mid y ) \\).

In computing the ESS, we shall need to estimate a sum of the correlations \\( \rho \\). We can compute the correlations by first computing the variogram
\\[ 
	V_t = \frac{1}{m(n-t)} \sum\_{j=1}^m \sum\_{i=t+1}^{n} (\psi\_{i,j} - \psi\_{i-t,j})^2.
\\]
We shall also require an estimate of the marginal posterior variance \\( \widehat{\text{var}}^+ \\), which can be computed as a weighted sum of the between-sequence variance \\( B \\), and within-sequence variance \\( W \\):

\\[
	\widehat{\text{var}}^+(\psi \mid y) = \frac{n-1}{n} W + \frac{1}{n} B,
\\]

where the within-sequence variance can be realised as

\\[
	W = \frac{1}{m} \sum\_{j=1}^m s\_j^2, \quad \text{and} \quad s\_j^2 = \frac{1}{n-1}\sum_{i=1}^{n}(\psi\_{ij} - \bar{\psi}\_{. j})^2,
\\]

and the between-sequence variance can be computed:

\\[
	B = \frac{n}{m - 1} \sum\_{j=1}^m (\bar{\psi}\_{. j} - \bar{\psi}\_{..} )^2 \quad \text{where} \quad \bar{\psi}\_{.j} = \frac{1}{n} \sum\_{i=1}^{n} \psi\_{ij}, \quad \bar{\psi}_{..} = \frac{1}{m} \sum\_{j=1}^m \bar{\psi}\_{.j}.
\\]

Putting this together we have our estimate of the correlations as:

\\[
	\hat{\rho}\_t = 1 - \frac{V\_t}{2\widehat{\text{var}}^+},
\\]

and finally, we can realise the estimate of the effective sample size

\\[
	\hat{n}\_{\text{eff}} = \frac{mn}{1+ 2\sum\_{t=1}^{T}\hat{\rho}\_t},
\\]

where \\( T \\) is the first odd positive integer for which \\( \hat{\rho}\_{T+1} + \hat{\rho}\_{T+2} \\) is negative.

## Improving performance with Numpy

In wishing to compute the ESS of some MCMC scheme output in python, I had a look around to try and find existing python implementations. I was surprised to find only [one implementation](https://github.com/pymc-devs/pymc/blob/14d8e9fc03bf9be1c3508b8b4563561480f0b358/pymc/diagnostics.py#L497), by PyMC. The author's compute the ESS as defined by Gelman *et. al* (above). However, inspecting the source code revealed warning signs of inefficiencies.

A big red efficiency flag when reading python code is seeing an abundance of for loops. Python is very flexible, and allows users to combine any types of objects in the same list. As such, whenever operating on any element of a list there is a lot of overhead in type checking . Because of this overhead python's for loops are notoriously slow (see [this link](https://jakevdp.github.io/blog/2014/05/09/why-python-is-slow/) for a more thorough and accurate explanation of why python is slow).

However, we can often use [Numpy](https://docs.scipy.org/doc/numpy/user/whatisnumpy.html#what-is-numpy) to vectorise our code and push these for loops down into C, where the implementation will happen at near-C speed. This is possible as Numpy is more strict as to what an array can contain. Whereas a python list can contain any sequence of objects, Numpy upcasts objects to ensure that all elements are of the same type, allowing for more efficient manipulation and storage of data.

Of particular concern to me was the PyMC computation of the variogram, which was done so using a generator expression and two nested for loops:

```py
# Nested for loops make me slow
variogram = lambda t: (sum(sum((x[j][i] - x[j][i-t])**2 for i in range(t,n)) for j in range(m)) 
/ (m*(n - t)))
```

The code is readable (if you're familiar with [generators](https://wiki.python.org/moin/Generators)) and reads like the mathematical definition of the variogram given above. However, this implementation will be slow because of the nested for loops, which to make matters worse is called inside a third loop:

```py
negative_autocorr = False
t = 1
rho = np.ones(n)

# And another loop!
while not negative_autocorr and (t < n):
	rho[t] = 1 - variogram(t) / (2 * s2)
	if not t % 2:
		negative_autocorr = sum(rho[t-1:t+1]) < 0
	t += 1
```

The outmost loop seems unavoidable, but we can vectorise the computation of the variogram easily, pushing both the for loops down into C:

```py
# Look mum, no loops!
my_variogram = lambda t: ((x[:, t:] - x[:, :(n - t)])**2).sum() / (m*(n - t))
```

Another improvement we can make is in the computation of the within-chain variance. The source code implementation makes use of for loops:

```py
# PyMC's computation of within-chain variance
W = np.sum([(x[i] - xbar) ** 2 for i, xbar in enumerate(np.mean(x, 1))]) / (m * (n - 1))
```

But again, we can push this for loop down into C with a neat one-liner:

```py
# Computing within-chain variance with Numpy
my_W = ((x - x.mean(axis=1, keepdims=True))**2).sum() / (m*(n - 1))
```

Putting this altogether we can improve PyMC's computation of the ESS. All that is left to do is assess the performance of our implementation. We shall keep PyMC's function defined as ```effective_n(x)```, and shall define our improved implementation as ```my_effective_n(x)```.

## Assessing speed up

To assess how our vectorisation improves the performance of the computation we need a simple example and some MCMC output to assess.

Here I shall consider that we wish to infer the location parameters \\( (\mu\_1, \mu\_2)^T \\) of a bivariate normal distribution with covariance given by the identity matrix, and observations \\( (x, y) \\). We shall simulate a random walk [Metropolis--Hastings algorithm](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm#Formal_derivation). For this simple example a Metropolis--Hastings algorithm is overkill --- but it provides us a quick way to get our hands on some correlated samples. The code below will simulate 4 separate chains, each with different initialisations and each chain making 10,000 iterations of the MH algorithm.

```py
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
```

Now that we have some output we can go ahead and assess the performance of our new vectorised function. We shall use this function to compute the number of effective samples of \\( \mu\_1 \\) which we've made. Ipython's magic command ```%timeit``` is perfect for making speed-up comparisons. Performing the test on my work machine I find:

```py
%timeit effective_n(output[:, 0, :])
1.88 s ± 128 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%timeit my_effective_n(output[:, 0, :])
3.18 ms ± 427 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

So we see, vectorising two lines of python code with Numpy has taken the run time down from 1.88 seconds to 3.18 milliseconds. This is almost a *600 time* speed-up over the PyMC implementation!

## Summary

As we have seen, with a little Numpy know-how we can make very significant performace improvements with little alteration to our code. We explored a real-world example case where we were able to improve the performance of a function by over 500 times by altering two lines of code. So next time you hit a bottleneck in your code, see which for loops you can shed with the help of Numpy.
