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
        result = scipy.optimize.differential_evolution(self._wrapper, bounds = bnds)
        result.model_description = self.model.description
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
    imbayesswap = IMBayes.IMBayesSwap()
    imbayesswap.major_version = 1
    imbayesswap.middle_version = 1
    imbayesswap.minor_version = 1
    imbayesswap.updateModelName()
    imbayesswap.description = 'Vanilla IMBaysSwap, the probability of swapping is considered in the "change"'
    
    wrapper = Wrapper(participant, imbayesswap)
    wrapper.fit()
    
    file_path = 'Data/fitting result/tmp/'
    file_name = '{}fitting_result_{}.dat'.format(file_path, participant.pID)
    d = shelve.open(file_name)
    d['participant'] = participant
    d.close()
    
def loadTmpData():
    file_path = 'Data/fitting result/tmp/'
    pID_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    participants ={}
    
    for pID in pID_list:
        file_name = '{}fitting_result_{}.dat'.format(file_path, pID)
        fitting_result = shelve.open(file_name)
        participants[pID] = fitting_result['participant']
        fitting_result.close()
        
    return participants

def loadSimulationData():
    file_path = 'Data/fitting result/Exp1/'
    file_name = '{}fitting_results.dat'.format(file_path)
    fitting_results = shelve.open(file_name)
    participants = fitting_results['participants']
    fitting_results.close()

    return participants
    
def merge(simulationData, tmpData):
    for pID in simulationData.keys():
        for model in tmpData[pID].fitting_result.keys():
            simulationData[pID].fitting_result[model] = tmpData[pID].fitting_result[model]
            
            for i, trial in enumerate(simulationData[pID].trials):
                trial.simulation[model] = tmpData[pID].trials[i].simulation[model]
                
    return simulationData


def fitExp1():
    participants = loadExp1()
    fit(participants[1])
#     
#     with Pool(1) as p:
#         p.map(fit, [participants[pID] for pID in participants.keys()])
#     
    participants = merge(loadSimulationData(), loadTmpData())
    
    d = shelve.open('Data/fitting result/Exp1/fitting_results.dat')
    d['participants'] = participants
    d.close()
    
if __name__ == '__main__':
    fitExp1()
    pass
