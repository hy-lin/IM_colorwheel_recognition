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
import IMMBayes
import MixtureModels
import MixtureModelsBayes

def loadExp1():
    data_file = open('Data\\colorwheelr1.dat')
    data_format = Parser.BasicDataFormat()
    parser = Parser.BasicParser(data_file, data_format, Parser.Exp1TrialFactory)
    
    participants = parser.parse()
    
    data_file.close()
    
    return participants

def loadExp2():
    data_file = open('Data\\Experiment2\\recognition2.dat')
    data_format = Parser.Exp2DataFormat()
    parser = Parser.BasicParser(data_file, data_format, Parser.Exp2TrialFactory)

    participants = parser.parse()
    
    data_file.close()
    
    return participants

def loadExp3():
    data_file = open('Data\\Experiment3\\recallNRecognition.dat')
    # data_format = BasicDataFormat()
    data_format = Parser.Exp3DataFormat()
    
    parser = Parser.BasicParser(data_file, data_format, Parser.Exp3TrialFactory)
    
    participants = parser.parse()
    
    data_file.close()
    
    return participants

class Wrapper(object):
    def __init__(self, participant, model, fit_mode = 'recognition'):
        self.participant = participant
        self.model = model
        self.fit_mode = fit_mode
        
        self.t0 = time.time()
        
    def fit(self):
        bnds = [(self.model.xmin[i], self.model.xmax[i]) for i in range(len(self.model.xmax))]
        
        xs = []
        fun = 0
        for set_size in [1, 2, 4, 6]:
            if self.fit_mode == 'recognition':
                self.active_trials = self.participant.getTrialsMetConstraints({'set_size': [set_size]})
            else:
                self.active_trials = self.participant.getTrialsMetConstraints({'set_size': [set_size]}, 'recall')
            result = scipy.optimize.differential_evolution(self._wrapper, bounds = bnds)
            fun += result.fun
            xs.append(result.x)
            
        result.model_description = self.model.description
        self.participant.fitting_result[self.model.model_name] = result
        self.participant.fitting_result[self.model.model_name].x = xs
        self.participant.fitting_result[self.model.model_name].fun = fun
    
    def _wrapper(self, x):
        
        self.t0 = time.time()
        self.model.updateParameters(x)
        self._simulate()
        ll = self._calculateLL()
        
        print('| {}, {}'.format(time.time()-self.t0, ll))
        
        return ll
    
    def _simulate(self):
        for trial in self.active_trials:
            trial.simulation[self.model.model_name] = self.model.getPrediction(trial)
    
    def _calculateLL(self):
        ll = 0
        if self.fit_mode == 'recognition':
            for trial in self.active_trials:
                ll_t = numpy.log((trial.response==1) * trial.simulation[self.model.model_name] + \
                                (trial.response!=1) * (1-trial.simulation[self.model.model_name]))
                if not numpy.isneginf(ll_t):
                    ll -= ll_t
                else:
                    ll += 99999999
        else:
            for trial in self.active_trials:
                ll_t = numpy.log(
                    trial.simulation[self.model.model_name][trial.response]
                )
                if not numpy.isneginf(ll_t):
                    ll -= ll_t
                else:
                    ll += 99999999

        if numpy.isnan(ll):
            ll = 999999999999.0
            
        if numpy.isinf(ll):
            ll = 888888888888.0
            
        print(self.model.getParametersAsVector())
    
        return ll + 2*self.model.n_parameters
    
def fit(participant, model, fit_mode = 'recognition'):
    # model = 'Murry'
    if model == 'IMM':
        immbayes = IMMBayes.IMMABBayes()
        immbayes.major_version = 1
        immbayes.middle_version = 1
        immbayes.minor_version = 1
        immbayes.updateModelName()
        immbayes.description = 'Vanilla immbayes AB'

        wrapper = Wrapper(participant, immbayes, fit_mode)

    if model == 'MMBayes':
        mixture_model = MixtureModelsBayes.MixtureModelsBayes()
        wrapper = Wrapper(participant, mixture_model, fit_mode)

    if model == 'MMBayesBias':
        mixture_model = MixtureModelsBayes.MixtureModelsBayesBias()
        wrapper = Wrapper(participant, mixture_model, fit_mode)

    if model == 'Murry':
        murry = MixtureModels.MurryERFC()
        wrapper = Wrapper(participant, murry, fit_mode)

    if model == 'MM':
        mixture_model = MixtureModels.MixtureModel()
        wrapper = Wrapper(participant, mixture_model, 'recall')

    if model == 'MMBoundary':
        mmb = MixtureModels.MixtureModelBoundary()
        wrapper = Wrapper(participant, mmb, fit_mode)

    wrapper.fit()
    
    file_path = 'Data/fitting result/tmp/'
    file_name = '{}fitting_result_{}.dat'.format(file_path, participant.pID)
    d = shelve.open(file_name)
    d['participant'] = participant
    d.close()
    
def loadTmpData():
    file_path = 'Data/fitting result/tmp/'
    pID_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    # pID_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

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

def loadExp2SimulationData():
    file_path = 'Data/fitting result/Exp2/'
    file_name = '{}fitting_results.dat'.format(file_path)
    fitting_results = shelve.open(file_name)
    participants = fitting_results['participants']
    fitting_results.close()

    return participants

def loadExp3SimulationData():
    file_path = 'Data/fitting result/Exp3/'
    file_name = '{}fitting_results.dat'.format(file_path)
    fitting_results = shelve.open(file_name)
    participants = fitting_results['participants']
    fitting_results.close()

    return participants

    
def merge(simulationData, tmpData):
    for pID in simulationData.keys():
        print('Merging: {}'.format(pID))
        for model in tmpData[pID].fitting_result.keys():
            simulationData[pID].fitting_result[model] = tmpData[pID].fitting_result[model]
            
            if 'trials' in tmpData[pID].__dict__.keys():
                try:
                    for i, trial in enumerate(simulationData[pID].trials):
                        trial.simulation[model] = tmpData[pID].trials[i].simulation[model]
                except:
                    pass
            try:
                if 'recall_trials' in tmpData[pID].__dict__.keys():
                    if 'recall_trials' in simulationData[pID].__dict__.keys():
                        for i, recall_trial in enumerate(simulationData[pID].recall_trials):
                            recall_trial.simulation[model] = tmpData[pID].recall_trials[i].simulation[model]
                    else:
                        simulationData[pID].recall_trials = tmpData[pID].recall_trials
            except:
                pass

    return simulationData


def fitExp1():
    participants = loadExp1()
    
    # fit(participants[1], 'MMBoundary', 'recognition')

    # print(participants[1].fitting_result)

    with Pool(6) as p:
        p.starmap(fit, [(participants[pID], 'MMBoundary', 'recognition') for pID in participants.keys()])
    
    try:
        old_simulation_data = loadSimulationData()
    except:
        old_simulation_data = participants
    
    d = shelve.open('Data/fitting result/Exp1/fitting_results.dat')
    d['participants'] = participants
    d.close()

def fitExp2():
    participants = loadExp2()
    
    # fit(participants[1], 'MMBoundary', 'recognition')

    # print(participants[1].fitting_result)

    with Pool(6) as p:
        p.starmap(fit, [(participants[pID], 'MMBayes', 'recognition') for pID in participants.keys()])
    
    try:
        old_simulation_data = loadExp2SimulationData()
    except:
        old_simulation_data = participants

    participants = merge(old_simulation_data, loadTmpData())
    
    d = shelve.open('Data/fitting result/Exp2/fitting_results.dat')
    d['participants'] = participants
    d.close()

def fitExp3():
    participants = loadExp3()

    # fit(participants[1], 'MM', 'recall')

    # print(participants[1].fitting_result)

    # fit(participants[1], 'MMBayesBias', 'recognition')

    with Pool(20) as p:
        p.starmap(fit, [(participants[pID], 'MM', 'recall') for pID in participants.keys()])
    
    try:
        old_simulation_data = loadExp3SimulationData()
    except:
        old_simulation_data = participants
    participants = merge(old_simulation_data, loadTmpData())
    
    d = shelve.open('Data/fitting result/Exp3/fitting_results.dat')
    d['participants'] = participants
    d.close()
    
def fixMerge():
    participants = loadExp2()

    try:
        old_simulation_data = loadExp2SimulationData()
    except:
        old_simulation_data = participants

    participants = merge(old_simulation_data, loadTmpData())
    
    d = shelve.open('Data/fitting result/Exp2/fitting_results.dat')
    d['participants'] = participants
    d.close()

if __name__ == '__main__':
    fitExp3()
    pass