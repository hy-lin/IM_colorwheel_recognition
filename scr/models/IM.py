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

class IM(object):
    '''
    This is the core IM model. 
    '''


    def __init__(self, b = .15, a = .21, s = 7.7, kappa = 7.19, kappa_f = 40.14, r = 0.12):
        '''
        The default parameter values is the mean estimated value from Colorwheel experiment 1. 
        '''
        self.b = b
        self.a = a
        self.s = s
        self.kappa = kappa
        self.kappa_f = kappa_f
        self.r = r
        
        self.c = 1.0 # fixed
        
        self.model_name = 'Interference Model'
        self.n_parameters = 6
        
    def getPrediction(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)
        
        C = self._getActivationC(trial)
        C_f = self._getActivationC_f(trial)
        
        p_focus = trial.getPFocus()
        
        activation = (A + B + C) * (1-p_focus) + ((A+B) * self.r + C_f) * p_focus
        
        pred = self._getPred(activation)
        
        return pred
        
    def _getEmptyActivation(self):
        return numpy.zeros((1, 360))
    
    def _getActivation(self, mu, kappa):
        angs = numpy.arange(1, 360)
        rads = angs * numpy.pi / 180.0
        
        mu_rads = mu * numpy.pi / 180.0
        
        difference = rads - mu_rads
        pdf = scipy.stats.vonmises(kappa).pdf(difference)
        pdf = pdf/numpy.sum(pdf)
        
        return pdf

        
    def _getDistance(self, location1, location2):
        dist = abs(location1 - location2)
        if dist >= 7:
            dist = 13-dist
            
        return dist
        
    def _getActivationA(self, trial):
        activation_A = self._getEmptyActivation()
        
        for stimulus in trial.stimuli:
            activation_A += self._getActivation(stimulus.color, self.kappa)
        
        return activation_A * self.a
    
    def _getActivationB(self, trial):
        activation_B = self._getEmptyActivation()
        activation_B += trial.set_size / len(activation_B)

        return activation_B * self.b
    
    def _getWeighting(self, location1, location2):
        dist = self._getDistance(location1, location2)
        
        return numpy.exp(-dist*self.s)
    
    def _getActivationC(self, trial):
        activation_C = self._getEmptyActivation()
        for stimulus in trial.stimuli:
            weighting = self._getWeighting(trial.probe.location, stimulus.location)
            activation_C += self._getActivation(stimulus.color, self.kappa) * weighting
            
        return activation_C * self.c
    
    def _getActivationC_f(self, trial):
        activation_C_f = self._getActivation(trial.target.color, self.kappa_f)
        
        return activation_C_f * self.c
    
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