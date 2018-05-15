'''
Created on Jan 4, 2017

@author: user
'''

import numpy
import scipy.stats
# 
# import sys
# sys.path.insert(0, '../')
# import figures

class IMM(object):
    '''
    The full model of IMM.
    '''


    def __init__(self, b = .15, a = .21, s = 7.7, kappa = 7.19):
        '''
        The default parameter values is the mean estimated value from Colorwheel experiment 1. 
        '''
        self.b = b
        self.a = a
        self.s = s
        self.kappa = kappa
        
        self.c = 1.0 # fixed
        
        self.model_name_prefix = 'Interference Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1
        self.model_name = self.updateModelName()
        self.n_parameters = 4
        
        self.description = 'This is the vanilla IMM Bayes model.'

        
        self.xmax = [1.0, 1.0, 20.0, 100.0]
        self.xmin = [0.0, 0.0, 0.0, 0.0]
        
    def getInitialParameters(self):
        return [.15, .21, 7.7, 7.19]
    
    def getParametersAsVector(self):
        return [self.b, self.a, self.s, self.kappa]
        
    def getPrediction(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)
        
        C = self._getActivationC(trial)
        
        activation = A + B + C
        
        pred = self._getPred(activation)
        return numpy.squeeze(pred)
    
    def updateParameters(self, x):
        self.b = x[0]
        self.a = x[1]
        self.s = x[2]
        self.kappa = x[3]
        
    def updateModelName(self):
        return self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)
        
    def _getEmptyActivation(self):
        return numpy.zeros((1, 360))
    
    def _getActivation(self, mu, kappa):
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180.0
        
        mu_rads = mu * numpy.pi / 180.0
        
        difference = rads - mu_rads
        pdf = scipy.stats.vonmises(kappa).pdf(difference)
#         pdf = pdf/numpy.sum(pdf)
        
        return numpy.squeeze(pdf)

        
    def _getDistance(self, location1, location2):
        dist = abs(location1 - location2)
        if dist >= 7:
            dist = 13-dist
            
        return dist
        
    def _getActivationA(self, trial):
        activation_A = self._getEmptyActivation()
        for stimulus in trial.stimuli:
            activation_A += self._getActivation(stimulus.color, self.kappa)
            
        return numpy.squeeze(activation_A * self.a)
    
    def _getActivationB(self, trial):
        activation_B = self._getEmptyActivation()
        activation_B += trial.set_size / len(activation_B)

        return numpy.squeeze(activation_B * self.b)
    
    def _getWeighting(self, location1, location2, max_distance = 7.0):
        dist = self._getDistance(location1, location2) * 7.0 / max_distance
        
        return numpy.exp(-dist*self.s)
    
    def _getMaxDistance(self, trial):
        max_distance = 1.0
        for stimulus1 in trial.stimuli:
            for stimulus2 in trial.stimuli:
                dist = self._getDistance(stimulus1.location, stimulus2.location)
                if dist > max_distance:
                    max_distance = dist
                    
        return max_distance
    
    def _getActivationC(self, trial):
        activation_C = self._getEmptyActivation()
        max_distance = self._getMaxDistance(trial)
        for stimulus in trial.stimuli:
            weighting = self._getWeighting(trial.probe.location, stimulus.location, 7)
            activation_C += self._getActivation(stimulus.color, self.kappa) * weighting
            
        return numpy.squeeze(activation_C * self.c)
    
    def _getPred(self, activation):
        return activation / numpy.sum(activation)
#     
# def test():
#     im = IM()
#     data = {'mu = 180, kappa = 40':im._getActivation(180, 40)}
#     line_figure = figures.LineFigure(data)
#     line_figure.show()
#     
if __name__ == '__main__':
#     test()
    pass
