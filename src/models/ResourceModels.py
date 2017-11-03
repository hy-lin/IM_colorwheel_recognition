import numpy
import scipy.stats
import scipy.special
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

        sigma = numpy.sqrt(1.0/self.kappa)
        
        k_sz_ratio = self.k / trial.set_size
        lower_slot_number = numpy.floor(k_sz_ratio)
        higher_slot_number = lower_slot_number + 1
        higher_slot_precentage = k_sz_ratio - lower_slot_number
        lower_slot_precentage = 1 - higher_slot_precentage

        sigma_sz = sigma/numpy.sqrt(lower_slot_number) * lower_slot_precentage + sigma/numpy.sqrt(higher_slot_number) * higher_slot_precentage

        return 1.0/(sigma**2)

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

class SlogAveragingBinding(SlotAveraging):
    def __init__(self, k = 2.2, kappa = 7.2, b = .1):
        super(SlogAveragingBinding, self).__init__(k, kappa)
        self.b = b

        self.model_name_prefix = 'Slot Averaging Model with Binding errors'

        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 3

        self.model_name = self.updateModelName()

        self.xmax = [8.0, 100.0, 1.0]
        self.xmin = [0.0, 0.0, .0]

    def getInitialParameters(self):
        return [2.2, 7.2, .6]

    def getParametersAsVector(self):
        return [self.k, self.kappa, self.b]

    def updateParameters(self, x):
        self.k = x[0]
        self.kappa = x[1]
        self.b = x[2]

    def _getPred(self, trial, kappa, pm):
        activation = self._getActivation(trial.target.color, kappa) * pm * (1.0-self.b * (trial.set_size-1))

        for stimulus in trial.stimuli:
            if stimulus != trial.target:
                activation += self._getActivation(stimulus.color, kappa) * pm * self.b

        activation /= numpy.sum(activation)

        pred = activation * pm + (1.0-pm) * (1.0 / 360.0)
        return pred

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
        self.xmin = [0.0, 0.000001, 0.0]

        self.updating_distribution = True
        self.n_sim = 5000
        self.max_set_size = 6

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
        return self.distribution[set_size-1, x_ind]

        
    def _resimulate_distribution(self):
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180.0

        self.distribution = numpy.zeros((self.max_set_size, 360))
        for sz in range(self.max_set_size):
            J = self.J1 / ((sz+1) ** self.alpha)
            for iteration in range(self.n_sim):
                kappa = numpy.random.gamma(J/self.tau, self.tau)
                if kappa >= 650:
                    kappa = 650
                distribution = scipy.stats.vonmises(kappa).pdf(rads)
                self.distribution[sz] += distribution

            self.distribution[sz] /= self.n_sim

        self.updating_distribution = False

class VariablePrecisionBinding(VariablePrecision):
    def __init__(self, J1 = 60.0, tau = 44.47, alpha = 0.7386, kappa_s_scaling = 0.05):
        super(VariablePrecisionSwap, self).__init__(J1, tau, alpha)
        self.kappa_s_scaling = kappa_s_scaling

        self.model_name_prefix = 'Variable Precision Binding Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1
        self.model_name = self.updateModelName()
        self.n_parameters = 4

        self.n_spatial_locations = 13
        self.max_spatial_distance = numpy.ceil(self.n_spatial_locations / 2)

        self.description = 'This is the VP with binding model in IM paper'

        self.xmax = [100.0, 100.0, 1.0, 5.0]
        self.xmin = [0.0, 0.000001, 0.0, 0.0]


    def getInitialParameters(self):
        return [60.0, 44.47, 0.7386, 0.05]

    def getParametersAsVector(self):
        return [self.J1, self.tau, self.alpha, self.J_s_scaling]

    def updateParameters(self, x):
        self.J1 = x[0]
        self.tau = x[1]
        self.alpha = x[2]
        self.J_s_scaling = x[3]

        self.updating_distribution = True

    def _getSpatialActivation(location, target_location, set_size):
        if self.updating_distribution:
            self._resimulate_distribution()

        dist = numpy.abs(target_location - location)
        if dist > self.max_spatial_distance:
            dist = self.n_spatial_locations - dist

        dist_ind = dist * 360 / (self.max_spatial_distance * 2)

        return self.spatial_distribution[set_size-1, dist_ind]

    def _resimulate_distribution(self):
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180.0

        self.distribution = numpy.zeros((self.max_set_size, 360))
        self.spatial_distribution = numpy.zeros((self.max_set_size, 360))
        for sz in range(self.max_set_size):
            J = self.J1 / ((sz+1) ** self.alpha)
            for iteration in range(self.n_sim):
                kappa = numpy.random.gamma(J/self.tau, self.tau)
                kappa_s = kappa * kappa_s_scaling
                if kappa >= 650:
                    kappa = 650
                if kappa_s >= 650:
                    kappa_s = 650

                distribution = scipy.stats.vonmises(kappa).pdf(rads)
                self.distribution[sz] += distribution
                distribution = scipy.stats.vonmises(kappa_s).pdf(rads)
                self.spatial_distribution[sz] += distribution

            self.distribution[sz] /= self.n_sim
            self.spatial_distribution[sz] /= self.n_sim

        self.updating_distribution = False

    def getPRecall(self, trial):
        act = self._getEmptyActivation()
        for stimulus in trial.stimuli:
            act += self._getActivation(trial.target.color, trial.set_size) *  \
                self._getSpatialActivation(stimulus.location, trial.target.location, trial.set_size)
        pred = act / numpy.sum(act)

        return pred

    def getPM(self, trial):
        numerator = self._getSpatialActivation(0, 0, trial.set_size)
        denominator = 0
        for stimulus in trial.stimulus:
            denominator += self._getSpatialActivation(
                stimulus.location,
                trial.target.location,
                trial.set_size
            )
        
        return numerator / denominator


class VariablePrecisionSwap(VariablePrecision):
    def __init__(self, J1 = 60.0, tau = 44.47, alpha = 0.7386, p_swap = 0.05):
        super(VariablePrecisionSwap, self).__init__(J1, tau, alpha)
        self.p_swap = p_swap

        self.model_name_prefix = 'Variable Precision Swap Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 3
        self.model_name = self.updateModelName()
        self.n_parameters = 4

        self.description = 'This is the vanilla IM model.'

        self.xmax = [100.0, 100.0, 1.0, 0.18]
        self.xmin = [0.0, 0.000001, 0.0, 0.0]


    def getInitialParameters(self):
        return [60.0, 44.47, 0.7386, 0.05]

    def getParametersAsVector(self):
        return [self.J1, self.tau, self.alpha, self.p_swap]

    def updateParameters(self, x):
        self.J1 = x[0]
        self.tau = x[1]
        self.alpha = x[2]
        self.p_swap = x[3]

        self.updating_distribution = True

    def _getEmptyActivation(self):
        return numpy.zeros((1, 360))

    def getPRecall(self, trial):
        act = self._getEmptyActivation()
        pm = self.getPM(trial)
        act += self._getActivation(trial.target.color, trial.set_size) * pm
        for stimulus in trial.stimuli:
            if stimulus != trial.target:
                act += self._getActivation(stimulus.color, trial.set_size) * self.p_swap
        pred = act / numpy.sum(act)

        return pred

    def getPM(self, trial):
        pm = 1.0 - (trial.set_size-1) * self.p_swap
        return pm

class NeuronModel(object):
    def __init__(self, kappa_color=13.5, kappa_location=13.5, c=2.0):

        self.kappa_color = kappa_color
        self.kappa_location = kappa_location
        self.c = c

        self.n_color_nodes = 360
        self.n_location_nodes = 13
        self.neurons = numpy.zeros((self.n_color_nodes, self.n_location_nodes))

        self.model_name_prefix = 'Neuron Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1
        self.model_name = self.updateModelName()
        self.n_parameters = 3

        self.description = 'This is the simpified Neoron Model.'

        self.xmax = [100.0, 100.0, 100.0]
        self.xmin = [0.0, 0.0, 0.0]

    def updateModelName(self):
        self.model_name = self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)
        return self.model_name

    def getInitialParameters(self):
        return [2.2, 2.2, 7.2]

    def getParametersAsVector(self):
        return [self.k, self.kappa]

    def updateParameters(self, x):
        self.kappa_color = [0]
        self.kappa_location = x[1]
        self.c = x[2]

    def _getPChoise(self, activation):
        return numpy.exp(-self.c * activation)/sum(numpy.exp(-self.c * activation))

    def getPRecall(self, trial):
        self._setupNeurons(self, trial)
        
        probe_location_act = self._getActivation(trial.target.location, self.kappa_color, self.n_location_nodes)
        probe_location_retrieved = self._getPChoise(probe_location_act)

        retrieved_color = numpy.dot(self.neurons, probe_location_retrieved)

        return self._getPChoise(retrieved_color)


    def _getActivation(self, mu, kappa, n_response):
        angs = numpy.linspace(0, 360, n_response+1)
        angs = numpy.delete(angs, -1)
        rads = angs * numpy.pi / 180.0

        rads_mu = mu / n_response * 2 * numpy.pi
        diff = rads - rads_mu

        return numpy.exp(kappa * numpy.cos(diff))/scipy.special.iv(0, kappa)


    def _setupNeurons(self, trial):
        self.neurons = numpy.zeros((self.n_color_nodes, self.n_location_nodes))

        for stimulus in trial.stimuli:
            color_activation = self._getActivation(mu, self.kappa_color, self.n_color_nodes)
            location_activation = self._getActivation(mu, self.kappa_location, self.n_location_nodes)
            self.neurons += numpy.outer(color_activation, location_activation) / (trial.set_size * self.n_color_nodes * self.n_location_nodes)
