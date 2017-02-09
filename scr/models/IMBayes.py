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


    def __init__(self, b = .05, a = .21, s = 2.0, kappa = 7.19, kappa_f = 40.14, r = 0.12):
        '''
        Constructor
        '''
        super(IMBayes, self).__init__(b = b, a = a, s = s, kappa = kappa, kappa_f = kappa_f, r = r)
        self.model_name = 'Interference Model with Bayes'
        
        
    def getInitialParameters(self):
        return [.05, .21, 7.7, 7.19, 40.14, 0.12]
        
    def getPrediction(self, trial):
        p_recall = super(IMBayes, self).getPrediction(trial)
        
        P_S1 = self._getPS1(trial)
        d_f = self._getD(trial, self.kappa_f, P_S1)
        d_no_f = self._getD(trial, self.kappa, P_S1)
            
        n_change = trial.getPFocus() * numpy.sum((d_f > 0) * p_recall) + (1.0-trial.getPFocus()) * numpy.sum((d_no_f > 0) * p_recall)
        p_change = n_change
        
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
    t0 = time.time()
    imbayes = IMBayes()
    for trial in participants[5].trials:
        imbayes.getPrediction(trial)
#         print(trial)
#         print(imbayes.getPrediction(trial))

    print(time.time()-t0)
    
if __name__ == '__main__':
    
    import sys
    sys.path.insert(0, '../')
    import Parser
    import time

    _test()
    pass