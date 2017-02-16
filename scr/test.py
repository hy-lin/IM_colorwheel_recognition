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
    

if __name__ == '__main__':
    _doesitfit()
    pass