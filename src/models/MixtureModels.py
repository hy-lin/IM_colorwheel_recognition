'''
Created on Jan 4, 2017

@author: Hsuan-Yu Lin
'''

import numpy
import scipy.stats
import scipy.special

class MixtureModel(object):
    def __init__(self, kappa = 8.0, p_guess = 0.1, p_swap = 0.0):
        self.kappa = kappa
        self.p_guess = p_guess
        self.p_swap = p_swap

        self.model_name_prefix = 'Mixture Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 3
        self.model_name = self.updateModelName()
        self.n_parameters = 2
        
        self.description = 'This is the mixture model'

        self.xmax = [200.0, 1.0, 0.0]
        self.xmin = [0.0, 0.0, 0.0]

    def getInitialParameters(self):
        return [8.0, 0.1, 0.0]
    
    def getParametersAsVector(self):
        return [self.kappa, self.p_guess, self.p_swap]

    def updateParameters(self, x):
        self.kappa = x[0]
        self.p_guess = x[1]
        self.p_swap = (1.0-x[1]) * x[2]
        
    def updateModelName(self):
        return self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)

    def getPrediction(self, trial):
        pdf = self._getActivation(trial.target.color)
        pdf = pdf/numpy.sum(pdf)

        # non_target_pdf = numpy.zeros((1, 360))
        # for stimulus in trial.stimuli:
        #     if stimulus != trial.target:
        #         non_target_pdf += self._getActivation(stimulus.color)
        # if numpy.sum(non_target_pdf) != 0:
        #     # print(non_target_pdf)
        #     non_target_pdf = non_target_pdf/numpy.sum(non_target_pdf)

        p_recall = (1.0 - self.p_guess) * pdf + \
                   self.p_guess / 360.0

        return numpy.squeeze(p_recall)

    def _getActivation(self, mu):
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180.0
        
        mu_rads = mu * numpy.pi / 180.0
        
        difference = rads - mu_rads
        pdf = scipy.stats.vonmises(self.kappa).pdf(difference)
        # pdf = pdf/numpy.sum(pdf)
        
        return numpy.squeeze(pdf)

class MixtureModelBoundary(object):
    def __init__(self, kappa = 8.0, p_guess = 0.1, p_swap = 0.0, boundary = 30.0):
        self.kappa = kappa
        self.p_guess = p_guess
        self.boundary = boundary
        self.p_swap = p_swap

        self.model_name_prefix = 'Mixture Model Boundary'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1
        self.model_name = self.updateModelName()
        self.n_parameters = 3

        ## 1.1.1: 3 parameters
        ## 1.2.1: 4 parameters
        
        self.description = 'This is the mixture model'

        self.xmax = [200.0, 1.0, 0.0, 180]
        self.xmin = [0.0, 0.0, 0.0, 0]

    def getInitialParameters(self):
        return [8.0, 0.1, 0.0, 40]
    
    def getParametersAsVector(self):
        return [self.kappa, self.p_guess, self.p_swap, self.boundary]

    def updateParameters(self, x):
        self.kappa = x[0]
        self.p_guess = x[1]
        self.p_swap = (1.0-x[1]) * x[2]
        self.boundary = x[3]
        
    def updateModelName(self):
        return self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)

    def getPrediction(self, trial):
        pdf = self._getActivation(trial.target.color)
        pdf = pdf/numpy.sum(pdf)

        non_target_pdf = numpy.zeros((1, 360))
        for stimulus in trial.stimuli:
            if stimulus != trial.target:
                non_target_pdf += self._getActivation(stimulus.color)
        if numpy.sum(non_target_pdf) != 0:
            # print(non_target_pdf)
            non_target_pdf = non_target_pdf/numpy.sum(non_target_pdf)

        p_recall = (1.0 - self.p_guess - self.p_swap) * pdf + \
                   self.p_guess / 360.0 +\
                   self.p_swap * non_target_pdf

        dist = numpy.abs(numpy.arange(0, 360) - trial.probe.color)
        dist[dist>=180] = 360 - dist[dist>=180]

        d = dist > self.boundary
        p_change = numpy.sum(d * p_recall)

        return numpy.squeeze(p_change)

    def _getActivation(self, mu):
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180.0
        
        mu_rads = mu * numpy.pi / 180.0
        
        difference = rads - mu_rads
        pdf = scipy.stats.vonmises(self.kappa).pdf(difference)
        # pdf = pdf/numpy.sum(pdf)
        
        return numpy.squeeze(pdf)

class MurryERFC(object):
    def __init__(self, beta = 8.0, p_guess = 0.1, boundary = 20.0):
        self.beta = beta
        self.p_guess = p_guess
        self.boundary = boundary
        # self.p_swap = p_swap

        self.model_name_prefix = 'Murry Complementary Gaussian Error Function Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1
        self.model_name = self.updateModelName()
        self.n_parameters = 4
        
        self.description = 'Murry Complementary Gaussian Error Function Model'

        self.xmax = [100.0, 0.5, 180]
        self.xmin = [0.0, 0.0, 0]

    def getInitialParameters(self):
        return [5.0, 0.1, 45.0]
    
    def getParametersAsVector(self):
        return [self.beta, self.p_guess, self.boundary]

    def updateParameters(self, x):
        self.beta = x[0]
        self.p_guess = x[1]
        self.boundary = x[2]
        
    def updateModelName(self):
        return self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)

    def getPrediction(self, trial):
        dist = numpy.abs(trial.target.color - trial.probe.color)
        if dist >= 180:
            dist = 360 - dist
        x = -1 * dist + self.boundary

        p_change = 1.0 - (self.p_guess + (1.0-2.0*self.p_guess)/2.0 * scipy.special.erfc(-self.beta/numpy.sqrt(2)*x))

        return numpy.squeeze(p_change)
