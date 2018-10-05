'''
Created on 15.05.2018

@author: Hsuan-Yu Lin
'''
import MixtureModels
import numpy

class MixtureModelsBayes(MixtureModels.MixtureModel):

    def __init__(self, kappa = 8.0, p_guess = 0.1, p_swap = 0.0):
        super(MixtureModelsBayes, self).__init__(kappa = kappa, p_guess = p_guess, p_swap = p_swap)

        self.model_name_prefix = 'Mixture model  with Bayes'
        
        self.major_version = 1
        self.middle_version = 2
        self.minor_version = 1

        ## 1.1.1: 2 parameters
        ## 1.2.1: 3 parameters

        self.model_name = self.updateModelName()

    def getPRecall(self, trial):
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

        return numpy.squeeze(p_recall)

    def getPrediction(self, trial):
        p_recall = self.getPRecall(trial)

        P_S1 = self._getPS1(trial)
        d = self._getD(trial, self.kappa, P_S1)
        
        p_change = numpy.sum((d > 0) * p_recall)
        # # print(p_change)
        # if p_change <= 0:
        #     print(p_recall, p_change)
        #     p_change = 0.0000000000000000001
        # if p_change >= 1:
        #     print(p_recall, p_change)
        #     p_change = 0.9999999999999999999
        
        return p_change
        
    def _getPS1(self, trial):
        return 1.0 - self.p_guess - self.p_swap
        
    def _getD(self, trial, kappa, P_S1):
        act = self._getActivation(trial.probe.color)
        
        return -numpy.log(2.0 * numpy.pi * (P_S1 * act + (1-P_S1) / (2.0*numpy.pi)))

class MixtureModelsBayesBias(MixtureModels.MixtureModel):

    def __init__(self, kappa = 8.0, p_guess = 0.1, p_swap = 0.0, bias = 0.0):
        super(MixtureModelsBayesBias, self).__init__(kappa = kappa, p_guess = p_guess, p_swap = p_swap)

        self.bias = bias

        self.model_name_prefix = 'Mixture model with Bayes and bias'
        
        self.major_version = 1
        self.middle_version = 2
        self.minor_version = 1
        ## 1.1.1: 2 parameters
        ## 1.2.1: 3 parameters

        self.n_parameters = 4

        self.model_name = self.updateModelName()

        self.xmax = [100.0, 1.0, 1.0, 25.0]
        self.xmin = [0.0, 0.0, 0.0, -25.0]

    def getInitialParameters(self):
        return [8.0, 0.1, 0.0, 0.0]
    
    def getParametersAsVector(self):
        return [self.kappa, self.p_guess, self.p_swap, self.bias]

    def updateParameters(self, x):
        self.kappa = x[0]
        self.p_guess = x[1]
        self.p_swap = (1.0-x[1]) * x[2]
        self.bias = x[3]

    def getPRecall(self, trial):
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
        # print(p_recall)

        return numpy.squeeze(p_recall)

    def getPrediction(self, trial):
        p_recall = self.getPRecall(trial)

        P_S1 = self._getPS1(trial)
        d = self._getD(trial, self.kappa, P_S1)
        
        p_change = numpy.sum((d > self.bias) * p_recall)

        return p_change
        
    def _getPS1(self, trial):
        return 1.0 - self.p_guess - self.p_swap
        
    def _getD(self, trial, kappa, P_S1):
        act = self._getActivation(trial.probe.color)
        
        return -numpy.log(2.0 * numpy.pi * (P_S1 * act + (1-P_S1) / (2.0*numpy.pi)))