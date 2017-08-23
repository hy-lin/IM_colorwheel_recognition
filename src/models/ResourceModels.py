import numpy
import scipy.stats

class SlotAveraging(object):

    def __init__(self, k = 2.2, kappa = 7.2):
        self.k = k
        self.kappa = kappa

        self.model_name_prefix = 'Interference Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 3
        self.model_name = self.updateModelName()
        self.n_parameters = 6

        self.description = 'This is the vanilla IM model.'

        self.xmax = [8.0, 100.0]
        self.xmin = [0.0, 0.0]

    def updateModelName(self):
        self.model_name =  self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)
        return self.model_name

    def getInitialParameters(self):
        return [2.2, 7.2]

    def getParametersAsVector(self):
        return [self.k, self.kappa]

    def getPRecall(self, trial):
        kappa = self._getKappa(trial)
        pm = self._getPMemory(trial)
        pred = self._getPred(trial, kappa, pm)

        return pred

    def updateParameters(self, x):
        self.k = x[0]
        self.kappa = x[1]

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