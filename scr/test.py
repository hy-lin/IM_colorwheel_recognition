'''
Created on 15.02.2017
Because, Test Alliance Best Alliance.
@author: Hsuan-Yu Lin
'''
import shelve

def _doesitfit():
    file_name = 'Data/fitting result/Exp1/IMR/fitting_result_1.dat'
    results = shelve.open(file_name)
    participant = results['participant']
    for trial in participant.trials:
        print(trial, trial.simulation['Interference Model with Bayes'])
    results.close()
    
def loadSimulationData():
    file_path = 'Data/fitting result/Exp1/'
    pID_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    participants ={}
    
    for pID in pID_list:
        file_name = '{}fitting_result_{}.dat'.format(file_path, pID)
        fitting_result = shelve.open(file_name)
        participants[pID] = fitting_result['participant']
        fitting_result.close()
        
    return participants


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
    
def merge(simulationData, tmpData):
    for pID in simulationData.keys():
        for model in tmpData[pID].fitting_result.keys():
            simulationData[pID].fitting_result[model] = tmpData[pID].fitting_result[model]
            
            for i, trial in enumerate(simulationData[pID].trials):
                trial.simulation[model] = tmpData[pID].trials[i].simulation[model]
                
    return simulationData

def tmpMerge(simulationData, tmpData):
    # this is to solve a fucked up I made while fitting dual-process IMBayes. 
    for pID in simulationData.keys():
        for model in tmpData[pID].fitting_result.keys():
            simulationData[pID].fitting_result['Interference Model with Bayes Dual-Process v1'] = tmpData[pID].fitting_result[model]
            
            for i, trial in enumerate(simulationData[pID].trials):
                trial.simulation['Interference Model with Bayes Dual-Process v1'] = tmpData[pID].trials[i].simulation[model]
                
    return simulationData

def printEVERYTHING(participants):
    for pID in participants.keys():
        for trial in participants[pID].trials:
            for model in trial.simulation.keys():
                print(trial.simulation[model], end='\t')
                
            print('')

if __name__ == '__main__':
#     _doesitfit()
    simulationData = loadSimulationData()
    tmpData = loadTmpData()
    
    participants = tmpMerge(simulationData, tmpData)
    
    d = shelve.open('fitting_results.dat')
    d['participants'] = participants
    d.close()
    
    printEVERYTHING(participants)
    pass