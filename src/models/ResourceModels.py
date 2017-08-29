import numpy
import scipy.stats
import time

class SlotAveraging(object):

    def __init__(self, k = 2.2, kappa = 7.2):
        self.k = k
        self.kappa = kappa

        self.model_name_prefix = 'Slot averaging Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 3
        self.model_name = self.updateModelName()
        self.n_parameters = 2

        self.description = 'This is the vanilla IM model.'

        self.xmax = [8.0, 100.0]
        self.xmin = [0.0, 0.0]

    def updateModelName(self):
        self.model_name = self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)
        return self.model_name

    def getInitialParameters(self):
        return [2.2, 7.2]

    def getParametersAsVector(self):
        return [self.k, self.kappa]

    def updateParameters(self, x):
        self.k = x[0]
        self.kappa = x[1]

    def getPRecall(self, trial):
        kappa = self._getKappa(trial)
        pm = self._getPMemory(trial)
        pred = self._getPred(trial, kappa, pm)

        return pred

    def _getKappa(self, trial):
        if trial.set_size >= self.k:
            return self.kappa
        
        k_sz_ratio = self.k / trial.set_size
        lower_slot_number = numpy.floor(k_sz_ratio)
        higher_slot_number = lower_slot_number + 1
        higher_slot_precentage = k_sz_ratio - lower_slot_number
        lower_slot_precentage = 1 - higher_slot_precentage

        return self.kappa/numpy.sqrt(lower_slot_number) * lower_slot_precentage + self.kappa/numpy.sqrt(higher_slot_number) * higher_slot_precentage

    def _getPMemory(self, trial):
        if self.k >= trial.set_size:
            return 1.0

        return self.k / trial.set_size

    def _getEmptyActivation(self):
        return numpy.zeros((1, 360))

    def _getActivation(self, mu, kappa):
        # if self.reset_activation:
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180.0

        rads_mu = mu * numpy.pi / 180.0
        diff = rads - rads_mu
        
        return scipy.stats.vonmises(kappa).pdf(diff)

    def _getPred(self, trial, kappa, pm):
        activation = self._getActivation(trial.target.color, kappa)
        activation /= numpy.sum(activation)
        activation = activation * pm + (1.0-pm) * (1.0 / 360.0)

        return activation

class VariablePrecision(object):
    def __init__(self, J1 = 60.0, tau = 44.47, alpha = 0.7386):
        self.J1 = J1
        self.tau = tau
        self.alpha = alpha

        self.model_name_prefix = 'Variable precision Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 3
        self.model_name = self.updateModelName()
        self.n_parameters = 3

        self.description = 'This is the vanilla IM model.'

        self.xmax = [100.0, 100.0, 1.0]
        self.xmin = [0.0, 0.0, 0.0]

        self.updating_distribution = True
        self.n_sim = 5000
        self.max_set_size = 8

    def updateModelName(self):
        self.model_name = self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)
        return self.model_name

    def getInitialParameters(self):
        return [60.0, 44.47, 0.7386]

    def getParametersAsVector(self):
        return [self.J1, self.tau, self.alpha]

    def updateParameters(self, x):
        self.J1 = x[0]
        self.tau = x[1]
        self.alpha = x[2]

        self.updating_distribution = True

    def getPRecall(self, trial):
        pred = self._getActivation(trial.target.color, trial.set_size)
        pred /= numpy.sum(pred)

        return pred

    def _getActivation(self, mu, set_size):
        if self.updating_distribution:
            self._resimulate_distribution()

        x_ind = numpy.arange(360) - mu
        return self.distribution[set_size, x_ind]

        
    def _resimulate_distribution(self):
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180.0

        self.distribution = numpy.zeros((self.max_set_size, 360))
        for sz in range(self.max_set_size):
            J = self.J1 / ((sz+1) ** self.alpha)
            for iteration in range(self.n_sim):
                kappa = numpy.random.gamma(J/self.tau, self.tau)
                self.distribution[sz] += scipy.stats.vonmises(kappa).pdf(rads)
            self.distribution[sz] /= self.n_sim

        self.updating_distribution = False
