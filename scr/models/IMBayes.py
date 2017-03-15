'''
Created on 06.02.2017

@author: Hsuan-Yu Lin
'''
import IM
import numpy



class IMBayes(IM.IM):
    '''
    classdocs
    '''


    def __init__(self, b = .05, a = .01, s = 2.5, kappa = 7.19, kappa_f = 40.14, r = 0.12):
        '''
        Constructor
        '''
        super(IMBayes, self).__init__(b = b, a = a, s = s, kappa = kappa, kappa_f = kappa_f, r = r)
        self.model_name_prefix = 'Interference Model with Bayes'
        
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1

        self.model_name = self.updateModelName()
        
        
    def getInitialParameters(self):
        return [.05, .21, .5, 7.19, 40.14, 0.12]
    
    def getPRecall(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)
        
        C = self._getActivationC(trial)
        C_f = self._getActivationC_f(trial)
        
        p_recall_no_f = self._getPred(A + B + C)
        p_recall_f = self._getPred((A+B) * self.r + C_f)
        
        return (p_recall_f, p_recall_no_f)
        
    def getPrediction(self, trial):
        p_recall_f, p_recall_no_f = self.getPRecall(trial)

        P_S1_f = self._getPS(trial, self.r)
        P_S1_no_f = self._getPS(trial, 0)
        d_f = self._getD(trial, self.kappa_f, P_S1_f)
        d_no_f = self._getD(trial, self.kappa, P_S1_no_f)
        
        p_change = trial.getPFocus() * numpy.sum((d_f > 0) * p_recall_f) + (1.0-trial.getPFocus()) * numpy.sum((d_no_f > 0) * p_recall_no_f)
#         p_change = numpy.sum((d_no_f > 0) * p_recall_no_f)
        
        if p_change >= 1.0:
            print('warning, p > 1.0')
            p_change = 0.999999999
        elif p_change <= 0.0:
            print('warning, p < 0')
            p_change = 0.000000001
        return p_change
        
    def _getPS(self, trial, r):
        weighting = numpy.zeros(trial.set_size)
        for i, stimulus in enumerate(trial.stimuli):
            weighting[i] = self._getWeighting(trial.probe.location, stimulus.location) + (self.a * r)
            
        weighting /= (numpy.sum(weighting) + self.b * trial.set_size * r)
        return weighting[trial.serial_position]
        
    def _getD(self, trial, kappa, P_S):
        act = self._getActivation(trial.probe.color, kappa)
        
        return -numpy.log(2.0 * numpy.pi * (P_S * act + (1-P_S) / (2.0*numpy.pi)))
    
class IMBayesKappaD(IMBayes):
    '''
    The IMBayes model with separate precision for decision rule. 
    '''
    
    def __init__(self, b = .05, a = .01, s = 2.5, kappa = 7.19, kappa_f = 40.14, kappa_d = 7.19, r = 0.12):

        super(IMBayesKappaD, self).__init__(b = b, a = a, s = s, kappa = kappa, kappa_f = kappa_f, r = r)
        self.kappa_d = kappa_d
        
        self.model_name_prefix = 'Interference Model with additional precision for Bayes'
        self.n_parameters = 7
        
        self.xmax = [1.0, 1.0, 20.0, 100.0, 100.0, 100.0, 1.0]
        self.xmin = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
    def getInitialParameters(self):
        return [.05, .21, .5, 7.19, 40.14, 7.19, 0.12]
    
    def getParametersAsVector(self):
        return [self.b, self.a, self.s, self.kappa, self.kappa_f, self.kappa_d, self.r]
    
    def updateParameters(self, x):
        self.b = x[0]
        self.a = x[1]
        self.s = x[2]
        self.kappa = x[3]
        self.kappa_f = x[4]
        self.kappa_d = x[5]
        self.r= x[6]
        
    def getPrediction(self, trial):
        p_recall_f, p_recall_no_f = self.getPRecall(trial)

        P_S1_f = self._getPS(trial, self.r)
        P_S1_no_f = self._getPS(trial, 0)
        d_f = self._getD(trial, self.kappa_d, P_S1_f)
        d_no_f = self._getD(trial, self.kappa_d, P_S1_no_f)
        
        p_change = trial.getPFocus() * numpy.sum((d_f > 0) * p_recall_f) + (1.0-trial.getPFocus()) * numpy.sum((d_no_f > 0) * p_recall_no_f)
#         p_change = numpy.sum((d_no_f > 0) * p_recall_no_f)
        
        if p_change >= 1.0:
            print('warning, p > 1.0')
            p_change = 0.999999999
        elif p_change <= 0.0:
            print('warning, p < 0')
            p_change = 0.000000001
        return p_change
        
        
class IMBayesSwap(IMBayes):
    
    def __init__(self, b = .05, a = .01, s = 2.5, kappa = 7.19, kappa_f = 40.14, r = 0.12):
        '''
        Constructor
        '''
        super(IMBayesSwap, self).__init__(b = b, a = a, s = s, kappa = kappa, kappa_f = kappa_f, r = r)
        self.model_name_prefix = 'Interference Model with Bayes and Swap'
        
    def _getPS(self, trial, r):
        weighting = numpy.zeros(trial.set_size)
        for i, stimulus in enumerate(trial.stimuli):
            weighting[i] = self._getWeighting(trial.probe.location, stimulus.location) + (self.a * r)
            
        weighting /= (numpy.sum(weighting) + self.b * trial.set_size * r)
        return weighting
    
    def _getD(self, trial, kappa, P_S):
        act = self._getActivation(trial.probe.color, kappa)
        
        if len(P_S) == 1:
            D = -numpy.log(2.0 * numpy.pi * (P_S[0] * act + (1-P_S[0]) / (2.0*numpy.pi)))
        else:
            numerator = 0
            for i in range(1, len(P_S)):
                numerator += (P_S[i] * act + (1-P_S[i]) / (2.0*numpy.pi))
            
            numerator /= (trial.set_size-1)
            
            numerator += 1.0/(2.0*numpy.pi)
            
            numerator /= 2.0
            
            D = numpy.log(numerator) - numpy.log(P_S[0] * act + (1-P_S[0]) / (2.0*numpy.pi))
            
        return D
        
        
        return -numpy.log(2.0 * numpy.pi * (P_S * act + (1-P_S) / (2.0*numpy.pi)))
    
class IMBayesDual(IM.IM):
    '''
    This is the dual process version of IMBayes, unfortunately the IMBayes doesn't work well.
    '''
    def __init__(self, b = .05, a = .21, s = 2.0, kappa = 7.19, kappa_f = 40.14, r = 0.12, w = .5):
        '''
        Constructor
        '''
        super(IMBayesDual, self).__init__(b = b, a = a, s = s, kappa = kappa, kappa_f = kappa_f, r = r)
        
        self.w = w
        
        self.xmax = [1.0, 1.0, 20.0, 100.0, 100.0, 1.0, 1.0]
        self.xmin = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        self.model_name_prefix = 'Interference Model with Bayes Dual Process'
        self.n_parameters = 7
        
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1

        self.model_name = self.updateModelName()
        
    def getInitialParameters(self):
        return [.05, .21, 2.0, 7.19, 40.14, 0.12, .5]
    
    def getPRecall(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)
        
        C = self._getActivationC(trial)
        C_f = self._getActivationC_f(trial)
        
        p_recall_no_f = self._getPred(A + B + C)
        p_recall_f = self._getPred((A+B) * self.r + C_f)
        
        return (p_recall_f, p_recall_no_f)
    
    def getPrediction(self, trial):
        p_recall_f, p_recall_no_f = self.getPRecall(trial)

        P_S1_fam = 1.0 / trial.set_size
        d_f_fam = self._getD(trial, self.kappa_f, P_S1_fam)
        d_no_f_fam = self._getD(trial, self.kappa, P_S1_fam)
        
        P_S1_rec = self._getPS(trial)
        d_f_rec = self._getD(trial, self.kappa_f, P_S1_rec)
        d_no_f_rec = self._getD(trial, self.kappa, P_S1_rec)
        
        d_f = numpy.sum(((self.w * d_f_rec + (1-self.w) * d_f_fam) > 0) * p_recall_f)
        d_no_f = numpy.sum(((self.w * d_no_f_rec + (1-self.w) * d_no_f_fam) > 0) * p_recall_no_f)
        
        p_change = trial.getPFocus() * d_f + (1-trial.getPFocus()) * d_no_f
        
        return p_change
        
    def _getPS(self, trial):
        weighting = numpy.zeros(trial.set_size)
        for i, stimulus in enumerate(trial.stimuli):
            weighting[i] = self._getWeighting(trial.probe.location, stimulus.location)
            
        weighting /= numpy.sum(weighting)
        return weighting[trial.serial_position]
        
    def _getD(self, trial, kappa, P_S1):
        act = self._getActivation(trial.probe.color, kappa)
        
        return -numpy.log(2.0 * numpy.pi * (P_S1 * act + (1-P_S1) / (2.0*numpy.pi)))

def _test():
    data_file = open('..\\Data\\colorwheelr1.dat')
    data_format = Parser.BasicDataFormat()
    parser = Parser.BasicParser(data_file, data_format)
    
    participants = parser.parse()
    
    data_file.close()
    imbayes = IMBayesDual()
    t0 = time.time()

    for trial in participants[5].trials:
        imbayes.getPrediction(trial)
        print(trial, imbayes.getPrediction(trial))

    print(time.time()-t0)
    
if __name__ == '__main__':
    
    import sys
    sys.path.insert(0, '../')
    import Parser
    import time

    _test()
    pass
