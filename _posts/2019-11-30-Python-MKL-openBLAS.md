---
layout: post
title: Speed-up numpy with Intel's Math Kernel Library (MKL)
comments: true
---

The [numpy](https://numpy.org/) package is at the core of scientific computing
in python. It is the go-to tool for implementing any numerically intensive
tasks. The popular [pandas](https://pandas.pydata.org/about.html) package is
also built on top of the capabilities of numpy.

Vectorising computationally intensive code in numpy allows you to reach near-C
speeds, all from the comfort of python. See, for example, [this previous
post]({{ site.baseurl }}{% link
_posts/2018-08-27-Efficient-effective-sample-size-python.md %}) in which I speed
up a function provided by the [PyMC3](https://docs.pymc.io/) project by _over
500_ times.

Numpy really is a great tool to use right out of the box. However, it's also
possible to squeeze even more performance out of numpy with [Intel's Math Kernel
Library](https://software.intel.com/en-us/mkl) (MKL). In this post I will
introduce [Basic Linear Algebra
Subprograms](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms)
(BLAS) and see how choosing a different BLAS implementation can lead to free
speed-ups for your numpy code.

# Basic Linear Algebra Subprograms

Basic linear algebra subprograms are low level implementations of common and
fundamental linear algebra operations. They are intended to provide portable and
high-performance routines for common operations such as vector addition, scalar
multiplication, dot products and matrix multiplications. Examples of BLAS
libraries include [OpenBLAS](https://www.openblas.net/),
[ATLAS](http://math-atlas.sourceforge.net/) and [Intel Math Kernel
Library](https://software.intel.com/en-us/mkl). 

# Numpy and BLAS

I've found that whatever machine I `pip install numpy` on, it always manages to
find an OpenBLAS implementation to link against. This is great, with no extra
steps compiling numpy from source and manually linking against a BLAS library,
we get the benefits of BLAS, all for free.

However, it's also possible to link numpy against different BLAS
implementations, which may or may not perform better on our particular CPUs.
There are lots of different BLAS implementations out there, however here I'm
going to focus on Intel's Math Kernel Library, which is specifically designed
for optimum performance on Intel chipsets.
 
## Numpy and Intel's Math Kernel Library

So, firstly, I should mention that [Intel provide a python
distribution](https://software.intel.com/en-us/distribution-for-python)
explicitly intended to speed up computation on Intel CPUs. However, it is also
possible to install select Intel-accelerated packages into a regular python
distribution.  In practice I prefer this latter method, finding it quicker to
set up on a new system and giving me the illusion of more control.

To get an install of numpy compiled against Intel MKL it's simple enough to `pip
install intel-numpy`. If you use [scipy](https://www.scipy.org/about.html) or
[scikit-learn](https://scikit-learn.org/stable/), it would be worthwhile to also
`pip install intel-scipy intel-scikit-learn`. If you already have a numpy
install, you should first `pip uninstall numpy`, to avoid any conflicts (and
similarly for scipy and scikit-learn, if you already have either of these
installed).

## Speed comparison

Okay, great, so we can install select packages which are intended to perform
better on Intel CPUs, but do they actually outperform OpenBLAS on your
particularly system?  Naturally, it's time for a benchmark.

I've included all the code necessary to perform this benchmark on your machine
[here](/assets/posts/BLAS/intel_v_openblas.tar.gz). To run these tests you'll
need [virtualenv](https://virtualenv.pypa.io/en/latest/) and bash (and
python...).  Give it a go and find out how Intel MKL performs on your machine.
The comparison is made by computing a
[speed-up](https://en.wikipedia.org/wiki/Speedup#Examples) factor.

First, let's take a look at how Intel MKL performs on some basic linear algebra
operations. From the graph below we see that Intel MKL has outperformed OpenBLAS
for the functions we tested. In fact, computing the inverse and determinant of a
matrix is over twice as fast with Intel. Neat. And recall that we haven't had to
change any of our python code to get these speed-ups. These speed-ups are, for
all intents and purposes, free.

![](/assets/posts/BLAS/np_linalg.png)

Next in line for inspection are numpy's fast fourier transform functions. I was
really impressed with the performance of Intel MKL on these functions:
`np.fft.fftn` was a huge _7x faster_ than the OpenBLAS linked numpy. If you're
regularly using numpy to perform fast fourier transforms you'd really feel the
benefit here.

![](/assets/posts/BLAS/np_fft.png)

Finally, it was the go of random number generation. These were the results that
surprised me the most. All the distributions I tested were actually _slower_
with Intel. This I certainly did not expect. The only redeeming factor for Intel
here is when looking at the _efficiency_ of the random number generation; Intel
used half the amount of CPU OpenBLAS did. However, since resources are not an
issue for this test on my machine, OpenBLAS performs better here.

![](/assets/posts/BLAS/np_rand.png)

## Conclusion

BLAS libraries are a great way to squeeze extra performance from numerically
intensive schemes. However, which BLAS library you choose can affect the
performance of your code.  In this post we compare the speed of numpy with
OpenBLAS and numpy with Intel MKL.  The code I used for benchmarking is provided
[here](/assets/posts/BLAS/intel_v_openblas.tar.gz), and so the reader is
encouraged to run these same tests on their machine, to assess performance on
their exact setup. On my machine, at least, I found that Intel outperformed
OpenBLAS on the fft tests _and_ the linear algebra tests, but lagged behind on
the random number generation.

### Post-script

The results shown in the post were generated on my laptop, which has the
following stats:

```
Kernel Version: 5.3.0-22-generic
OS Type: 64-bit
Processors: 4 × Intel® Core™ i7-7500U CPU @ 2.70GHz
Memory: 7.7 GiB of RAM
```
