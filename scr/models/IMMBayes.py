'''
Created on 10.03.2017

@author: Hsuan-Yu Lin
'''
import IMM
import numpy

class IMMBayes(IMM.IMM):
    '''
    classdocs
    '''

    def __init__(self, b = .15, a = .21, s = 7.7, kappa = 7.19):
        '''
        Constructor
        '''
        super(IMMBayes, self).__init__(b = b, a = a, s = s, kappa = kappa)
        self.model_name_prefix = 'Interference Measurement Model with Bayes'
        
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1

        self.model_name = self.updateModelName()
        
        
    def getInitialParameters(self):
        return [.05, .21, .5, 7.19]
    
    def getPRecall(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)
        
        C = self._getActivationC(trial)
        
        p_recall = self._getPred(A + B + C)
        
        return p_recall
        
    def getPrediction(self, trial):
        p_recall = self.getPRecall(trial)

        P_S1 = self._getPS1(trial)
        d = self._getD(trial, self.kappa, P_S1)
        
        p_change = numpy.sum((d > 0) * p_recall)
        
        
        return p_change
        
    def _getPS1(self, trial):
        weighting = numpy.zeros(trial.set_size)
        for i, stimulus in enumerate(trial.stimuli):
            weighting[i] = self._getWeighting(trial.probe.location, stimulus.location) + self.a
            
        weighting /= (numpy.sum(weighting) + self.b * trial.set_size)
        return weighting[trial.serial_position]
        
    def _getD(self, trial, kappa, P_S1):
        act = self._getActivation(trial.probe.color, kappa)
        
        return -numpy.log(2.0 * numpy.pi * (P_S1 * act + (1-P_S1) / (2.0*numpy.pi)))