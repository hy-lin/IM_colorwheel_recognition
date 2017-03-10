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

        P_S1_f = self._getPS1(trial, self.r)
        P_S1_no_f = self._getPS1(trial, 0)
        d_f = self._getD(trial, self.kappa_f, P_S1_f)
        d_no_f = self._getD(trial, self.kappa, P_S1_no_f)
        
        # p_change = trial.getPFocus() * numpy.sum((d_f > 0) * p_recall_f) + (1.0-trial.getPFocus()) * numpy.sum((d_no_f > 0) * p_recall_no_f)
        p_change = numpy.sum((d_no_f > 0) * p_recall_no_f)
        
        return p_change
        
    def _getPS1(self, trial, r):
        weighting = numpy.zeros(trial.set_size)
        for i, stimulus in enumerate(trial.stimuli):
            weighting[i] = self._getWeighting(trial.probe.location, stimulus.location) + (self.a * r)
            
        weighting /= (numpy.sum(weighting) + self.b * trial.set_size * r)
        return weighting[trial.serial_position]
        
    def _getD(self, trial, kappa, P_S1):
        act = self._getActivation(trial.probe.color, kappa)
        
        return -numpy.log(2.0 * numpy.pi * (P_S1 * act + (1-P_S1) / (2.0*numpy.pi)))
    
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
        
        P_S1_rec = self._getPS1(trial)
        d_f_rec = self._getD(trial, self.kappa_f, P_S1_rec)
        d_no_f_rec = self._getD(trial, self.kappa, P_S1_rec)
        
        d_f = numpy.sum(((self.w * d_f_rec + (1-self.w) * d_f_fam) > 0) * p_recall_f)
        d_no_f = numpy.sum(((self.w * d_no_f_rec + (1-self.w) * d_no_f_fam) > 0) * p_recall_no_f)
        
        p_change = trial.getPFocus() * d_f + (1-trial.getPFocus()) * d_no_f
        
        return p_change
        
    def _getPS1(self, trial):
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
