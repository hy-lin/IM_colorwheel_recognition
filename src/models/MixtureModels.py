'''
Created on Jan 4, 2017

@author: Hsuan-Yu Lin
'''

import numpy
import scipy.stats

class MixtureModel(object):
    def __init__(self, kappa = 8.0, p_guess = 0.1):
        self.kappa = kappa
        self.p_guess = p_guess
        # self.p_swap = p_swap

        self.model_name_prefix = 'Mixture Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1
        self.model_name = self.updateModelName()
        self.n_parameters = 4
        
        self.description = 'This is the mixture model'

        self.xmax = [100.0, 1.0]
        self.xmin = [0.0, 0.0]

    def getInitialParameters(self):
        return [8.0, 0.1]
    
    def getParametersAsVector(self):
        return [self.kappa, self.p_guess]

    def updateParameters(self, x):
        self.kappa = x[0]
        self.p_guess = x[1]
        
    def updateModelName(self):
        return self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)

    def getPrediction(self, trial):
        pdf = self._getActivation(trial.target.color)
        pdf = pdf/numpy.sum(pdf)
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