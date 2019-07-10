import numpy
import numpy.random
import scipy.stats
import time

n_test = 50000

angs = numpy.arange(0, 360)
rads = angs * numpy.pi / 180.0

t0 = time.time()
for i in range(n_test):
    kappa = numpy.random.rand() * 30
    distribution = scipy.stats.vonmises(kappa).pdf(rads)

t1 = time.time()

for i in range(n_test):
    target_val = numpy.random.randint(0, 360)
    x_ind = numpy.arange(360) - target_val
    new_distribution = distribution[x_ind]

t2 = time.time()

print('call scipy: {}'.format(t1-t0))
print('wrap: {}'.format(t2-t1))