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

        v 1.1.2: nothing changed, except adding the getPRecall function for getting the
        recall probability. 
        '''
        self.b = b
        self.a = a
        self.s = s
        self.kappa = kappa
        self.kappa_f = kappa_f
        self.r = r
        
        self.c = 1.0 # fixed
        self.max_setsize = 6
        
        self.model_name_prefix = 'Interference Model'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 4
        # self.model_name = self.updateModelName()
        self.n_parameters = 6

        self.description = 'This is the vanilla IM model.'
        
        self.xmax = [1.0, 1.0, 20.0, 100.0, 100.0, 1.0]
        self.xmin = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        self.inference_knowledge = ['focus', 'trial_specific']

        # self.reset_activation = True
        
    def getInitialParameters(self):
        return [.15, .21, 7.7, 7.19, 40.14, 0.12]
    
    def getParametersAsVector(self):
        return [self.b, self.a, self.s, self.kappa, self.kappa_f, self.r]

    def getPRecall(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)
        
        C = self._getActivationC(trial)
        C_f = self._getActivationC_f(trial)
        
        p_focus = trial.getPFocus()
        
        activation = (A + B + C) * (1-p_focus) + ((A+B) * self.r + C_f) * p_focus
        
        pred = self._getPred(activation)
        return numpy.squeeze(pred)
        
    def getPrediction(self, trial):
        return self.getPRecall(trial)

    def getRTPrediction(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)
        
        C = self._getActivationC(trial)
        C_f = self._getActivationC_f(trial)
        
        p_focus = trial.getPFocus()

        activation_no_f = A + B + C
        activation_f = (A+B) * self.r + C_f 
    
    def updateParameters(self, x):
        self.b = x[0]
        self.a = x[1]
        self.s = x[2]
        self.kappa = x[3]
        self.kappa_f = x[4]
        self.r= x[5]

        # self.reset_activation = True
        
    def updateModelName(self):
        self.model_name =  self.model_name_prefix + ' v{}.{:02d}.{:02d}'.format(self.major_version, self.middle_version, self.minor_version)
        return self.model_name
        
    def _getEmptyActivation(self):
        return numpy.zeros((1, 360))
    
    def _getActivation(self, mu, kappa):
        # if self.reset_activation:
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180.0

        rads_mu = mu * numpy.pi / 180.0
        diff = rads - rads_mu
        
        return scipy.stats.vonmises(kappa).pdf(diff)
        # self.activation = scipy.stats.vonmises(self.kappa).pdf(rads)
        # self.activation_f = scipy.stats.vonmises(self.kappa_f).pdf(rads)

        # x_ind = numpy.arange(360) - mu
        # if kappa == self.kappa:
        #     return self.activation[x_ind]
        # elif kappa == self.kappa_f:
        #     return self.activation_f[x_ind]

        
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
            weighting = self._getWeighting(trial.probe.location, stimulus.location)
            activation_C += self._getActivation(stimulus.color, self.kappa) * weighting
            
        return numpy.squeeze(activation_C * self.c)
    
    def _getActivationC_f(self, trial):
        activation_C_f = self._getActivation(trial.target.color, self.kappa_f)
        
        return numpy.squeeze(activation_C_f * self.c)
    
    def _getPred(self, activation):
        return activation / numpy.sum(activation)

class IMEta(IM):
    def __init__(self, b = .15, a = .21, s = 7.7, kappa = 7.19, kappa_f = 40.14, r = 0.12, p = 0.8):
        super(IMEta, self).__init__(b, a, s, kappa, kappa_f, r)
        self.p = p

        self.model_name_prefix = 'Interference Model'
        self.major_version = 3
        self.middle_version = 1
        self.minor_version = 1
        self.model_name = self.updateModelName()
        self.n_parameters = 6

        self.description = 'This is the IM model with encoding strength. Currently the encoding strength only works on C component.'
        
        self.xmax = [1.0, 1.0, 20.0, 100.0, 100.0, 1.0, 1.0]
        self.xmin = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

    def _getEta(self, set_size, serial_position):
        sp = numpy.arange(set_size)
        etas = numpy.power(self.p, sp) + numpy.power(self.p, set_size - sp - 1)
        etas /= numpy.sum(etas) * set_size

        return etas[serial_position]

    def _getActivationA(self, trial):
        activation_A = self._getEmptyActivation()
        for serial_position, stimulus in enumerate(trial.stimuli):
            # eta = self._getEta(serial_position+1)
            activation_A += self._getActivation(stimulus.color, self.kappa) * 1.0
            
        return numpy.squeeze(activation_A * self.a)
    
    def _getActivationB(self, trial):
        activation_B = self._getEmptyActivation()
        for serial_position in range(trial.set_size):
            # activation_B += self._getEta(serial_position+1) / len(activation_B)
            activation_B += 1.0 / len(activation_B)

        return numpy.squeeze(activation_B * self.b)

    def _getActivationC(self, trial):
        activation_C = self._getEmptyActivation()
        max_distance = self._getMaxDistance(trial)
        for serial_position, stimulus in enumerate(trial.stimuli):
            weighting = self._getWeighting(trial.probe.location, stimulus.location, max_distance)
            activation_C += self._getActivation(stimulus.color, self.kappa) * weighting * self._getEta(trial.set_size, serial_position)
            
        return numpy.squeeze(activation_C * self.c)

#     
# def _test():
#     im = IM()
#     data = {'mu = 180, kappa = 40':im._getActivation(180, 40)}
#     line_figure = figures.LineFigure(data)
#     line_figure.show()
#     
if __name__ == '__main__':
#     _test()
    pass
