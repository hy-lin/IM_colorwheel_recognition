'''
Created on 07.02.2017

@author: Hsuan-Yu Lin
'''
import Parser
import numpy
import scipy.optimize
from multiprocessing import Pool

import shelve
import time

import sys
sys.path.insert(0, 'models\\')
import IMBayes

def loadExp1():
    data_file = open('Data\\colorwheelr1.dat')
    data_format = Parser.BasicDataFormat()
    parser = Parser.BasicParser(data_file, data_format)
    
    participants = parser.parse()
    
    data_file.close()
    
    return participants


class Wrapper(object):
    def __init__(self, participant, model):
        self.participant = participant
        self.model = model
        
        self.t0 = time.time()
        
    def fit(self):
        bnds = [(self.model.xmin[i], self.model.xmax[i]) for i in range(len(self.model.xmax))]
#         result = scipy.optimize.minimize(self._wrapper, self.model.getInitialParameters(), bounds = bnds)
        result = scipy.optimize.differential_evolution(self._wrapper, bounds = bnds)
        self.participant.fitting_result[self.model.model_name] = result
    
    def _wrapper(self, x):
        
        self.t0 = time.time()
        self.model.updateParameters(x)
        self._simulate()
        ll = self._calculateLL()
        
        print('| {}, {}'.format(time.time()-self.t0, ll))
        
        return ll
    
    def _simulate(self):
        for trial in self.participant.trials:
            trial.simulation[self.model.model_name] = self.model.getPrediction(trial)
    
    def _calculateLL(self):
        ll = 0
        for trial in self.participant.trials:
            ll_t = numpy.log((trial.response==1) * trial.simulation[self.model.model_name] + \
                             (trial.response==2) * (1-trial.simulation[self.model.model_name]))
            ll -= ll_t
    
        if numpy.isnan(ll):
            ll = 999999999999.0
            
        if numpy.isinf(ll):
            ll = 888888888888.0
            
        print(self.model.getParametersAsVector())
    
        return ll + 2*self.model.n_parameters
    
def fit(participant):
    imbayes = IMBayes.IMBayesDual()
    wrapper = Wrapper(participant, imbayes)
    wrapper.fit()
    
    d = shelve.open('fitting_result_{}.dat'.format(participant.pID))
    d['participant'] = participant
    d.close()

def fitExp1():
    participants = loadExp1()
    
    with Pool(20) as p:
        p.map(fit, [participants[pID] for pID in participants.keys()])
    
#     imbayes = IMBayes.IMBayes()
#     
#     
#     for pID in participants.keys():
#         wrapper = Wrapper(participants[pID], imbayes)
#         wrapper.fit()
#         print(participants[pID].fitting_result)
#     
#     d = shelve.open('fitting_result_test.dat')
#     d['participants'] = participants
#     d.close()
if __name__ == '__main__':
    fitExp1()
    pass