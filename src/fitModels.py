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
import ResourceModelsBayes
import SummedActivation
import IM

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
    def __init__(self, participant, model, recall_model = None, fit_mode = 'recognition'):
        self.participant = participant
        self.model = model
        self.recall_model = recall_model
        self.fit_mode = fit_mode
        
        self.t0 = time.time()
        
    def fit(self):
        bnds = [(self.model.xmin[i], self.model.xmax[i]) for i in range(len(self.model.xmax))]
        result = scipy.optimize.differential_evolution(self._wrapper, bounds = bnds)
        # result = scipy.optimize.fmin_tnc(self._wrapper, self.model.getInitialParameters(), bounds = bnds)
        result.model_description = self.model.description
        self.participant.fitting_result[self.model.model_name] = result
    
    def _wrapper(self, x):
        
        self.t0 = time.time()
        self.model.updateParameters(x)

        if self.recall_model is not None:
            self.recall_model.updateParameters(x)
        
        try:
            self.model.cachePS(self.participant.trials)
        except:
            print('cache fail')
            pass
        
        self._simulate()
        ll = self._calculateLL()
        
        print('| {}, {}'.format(time.time()-self.t0, ll))
        
        return ll
    
    def _simulate(self):
        if self.fit_mode == 'recognition':
            for trial in self.participant.trials:
                trial.simulation[self.model.model_name] = self.model.getPrediction(trial)
        elif self.fit_mode == 'recall':
            for trial in self.participant.recall_trials:
                trial.simulation[self.model.model_name] = self.model.getPrediction(trial)
        else:
            for trial in self.participant.recall_trials:
                trial.simulation[self.model.model_name] = self.recall_model.getPrediction(trial)
            for trial in self.participant.trials:
                trial.simulation[self.model.model_name] = self.model.getPrediction(trial)
        
    def _calculateLL(self):
        ll = 0

        if self.fit_mode == 'recognition':
            for trial in self.participant.trials:
                ll_t = numpy.log((trial.response==1) * trial.simulation[self.model.model_name] + \
                                (trial.response!=1) * (1-trial.simulation[self.model.model_name]))
                if not numpy.isneginf(ll_t):
                    ll -= ll_t
                else:
                    ll += 99999999
        elif self.fit_mode == 'recall':
            for trial in self.participant.recall_trials:
                ll_t = numpy.log(
                    trial.simulation[self.model.model_name][trial.response]
                )
                if not numpy.isneginf(ll_t):
                    ll -= ll_t
                else:
                    ll += 99999999
        else:
            for trial in self.participant.recall_trials:
                ll_t = numpy.log(
                    trial.simulation[self.model.model_name][int(trial.response)]
                )
                if not numpy.isneginf(ll_t):
                    ll -= ll_t
                else:
                    ll += 99999999
            for trial in self.participant.trials:
                ll_t = numpy.log((trial.response==1) * trial.simulation[self.model.model_name] + \
                                (trial.response!=1) * (1-trial.simulation[self.model.model_name]))
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
    
def fit(participant, model = 'IMBayes', fit_mode = 'recognition', inference_knowledge = ['focus', 'experiment_specific']):
    # vpbayes = ResourceModelsBayes.VariablePrecisionBindingBayes()
    # vpbayes.discription = 'The VariablePrecisionBayes with binding'
    
    # boundary_model = SummedActivation.IMBoundary()
    # boundary_model.discription = 'The boundary model'

    recall_model = None

    if model == 'IMBayes':
        tbf_model = IMBayes.IMBayes()
        tbf_model.inference_knowledge = inference_knowledge
        tbf_model.model_name = tbf_model.updateModelName()
        tbf_model.discription = 'The vanilla IM Bayes model with different level of knowledge in inference rule'
    
    if model == 'IMBayesBias' and fit_mode == 'recognition':
        tbf_model = IMBayes.IMBayesBias()
        tbf_model.inference_knowledge = inference_knowledge
        tbf_model.model_name = tbf_model.updateModelName()
        tbf_model.discription = 'The IM Bayes model with different level of knowledge in inference rule and Bias in inference rule'

    if model == 'IMBayesBias' and fit_mode == 'recallNRecognition':
        tbf_model = IMBayes.IMBayesBias()
        tbf_model.inference_knowledge = inference_knowledge
        tbf_model.model_name = tbf_model.updateModelName() + ' RecallNRecognition'
        tbf_model.discription = 'The IM Bayes model with different level of knowledge in inference rule and Bias in inference rule'

        recall_model = IM.IM()

    if model == 'IMBayesNonOptimalPS':
        tbf_model = IMBayes.IMBayesNonOptimalPS()
        tbf_model.inference_knowledge = inference_knowledge
        tbf_model.model_name = tbf_model.updateModelName()
        tbf_model.discription = 'The IM Bayes model with not always optimal knowledge in inference rule and Bias in inference rule'
    

    if model == 'IM':
        if fit_mode == 'recognitoin':
            raise ValueError('IM can not fit to recognition data directly.')

        tbf_model = IM.IM()
        tbf_model.model_name = tbf_model.updateModelName()

    wrapper = Wrapper(participant, tbf_model, recall_model, fit_mode)
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

def loadExp1SimulationData():
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
            
            for i, trial in enumerate(simulationData[pID].trials):
                trial.simulation[model] = tmpData[pID].trials[i].simulation[model]

            # if 'recall_trials' in tmpData[pID].__dict__.keys():
            #     if 'recall_trials' in simulationData[pID].__dict__.keys():
            #         try:
            #             for i, recall_trial in enumerate(simulationData[pID].trials):
            #                 recall_trial.simulation[model] = tmpData[pID].recall_trials[i].simulation[model]
            #         except:
            #             pass
            #     else:
            #         simulationData[pID].recall_trials = tmpData[pID].recall_trials

    return simulationData

def fitExp1():
    participants = loadExp1()
#     fit(participants[1])
     
    with Pool(1) as p:
        p.map(fit, [participants[pID] for pID in participants.keys()])
     
    participants = merge(loadExp1SimulationData(), loadTmpData())
    
    d = shelve.open('Data/fitting result/Exp1/fitting_results.dat')
    d['participants'] = participants
    d.close()

def fitExp2():
    inference_knowledge = ['focus', 'experiment_specific']

    participants = loadExp2()

    # fit(participants[1], 'IMBayesBias', 'recognition', inference_knowledge)


    with Pool(6) as p:
        p.starmap(fit, [(participants[pID], 'IMBayesNonOptimalPS', 'recognition', inference_knowledge) for pID in participants.keys()])
    try:
        old_simulation_data = loadExp2SimulationData()
    except:
        old_simulation_data = participants
    participants = merge(old_simulation_data, loadTmpData())
    
    d = shelve.open('Data/fitting result/Exp2/fitting_results.dat')
    d['participants'] = participants
    d.close()

def fitExp3():
    # inference_knowledges = [
    #     ['focus', 'trial_specific'],
    #     ['no_focus', 'trial_specific'],
    #     ['focus', 'experiment_specific'],
    #     ['no_focus', 'experiment_specific']
    # ]

    inference_knowledge = ['focus', 'experiment_specific']

    participants = loadExp3()

    with Pool(20) as p:
        p.starmap(fit, [(participants[pID], 'IMBayesBias', 'recallNRecognition', inference_knowledge) for pID in participants.keys()])
    
    try:
        old_simulation_data = loadExp3SimulationData()
    except:
        old_simulation_data = participants
    participants = merge(old_simulation_data, loadTmpData())
    
    d = shelve.open('Data/fitting result/Exp3/fitting_results.dat')
    d['participants'] = participants
    d.close()


    # for inference_knowledge in inference_knowledges:
    #     participants = loadExp3()

    #     with Pool(20) as p:
    #         p.starmap(fit, [(participants[pID], 'IMBayes', 'recognitoin', inference_knowledge) for pID in participants.keys()])
        
    #     try:
    #         old_simulation_data = loadExp3SimulationData()
    #     except:
    #         old_simulation_data = participants
    #     participants = merge(old_simulation_data, loadTmpData())
        
    #     d = shelve.open('Data/fitting result/Exp3/fitting_results.dat')
    #     d['participants'] = participants
    #     d.close()

def fitExp3Recall():
    participants = loadExp3()

    with Pool(20) as p:
        p.starmap(fit, [(participants[pID], 'IMBayes', 'both') for pID in participants.keys()])

    try:
        old_simulation_data = loadExp3SimulationData()
    except:
        old_simulation_data = participants
    participants = merge(old_simulation_data, loadTmpData())
    
    d = shelve.open('Data/fitting result/Exp3/fitting_results.dat')
    d['participants'] = participants
    d.close()

def fixingMerges():
    participants = loadExp2()

    # fit(participants[1], 'IMBayesBias', 'recognition', inference_knowledge)

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
