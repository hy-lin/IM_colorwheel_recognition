'''
Created on 23.03.2017

This is the second experiment for colorwheel recognition.
In this experiment, the probe color is either identical as the target 
(positive probe) or randomly selected from a uniform distribution 
on a colorwheel, excluding the target color.

The major reason for running this experiment is to ensure that the
Bayesian inference rule applies prefectly to experiment condition.

@author: Hsuan-Yu Lin
'''

import ExpParameters
import Display
import Recorder
import myClasses

import datetime
import random

class Experiment(object):
    '''
    The mail object which managing everything in the experiment, including
    opening windows, setup trials, and recording. 
    '''

    def __init__(self):
        '''
        Constructor, this initiates the experiment window, recorder,
        setup experiment trials etc. 
        '''

        self.data_file = open('Data\\recognition2.dat', 'a')
        self.logger = open('Data\\log.dat', 'a')

        self.exp_parameters = ExpParameters.ExpParameters()
        self.display = Display.Display(self.exp_parameters)
        self.recorder = Recorder.Recorder(self.exp_parameters)

        self.pID = 999
        self.session = 1

        self._setupPracticeTrials()
        self._setupExperimentTrials()

        self.log('experiment created')

    def log(self, msg):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%d-%b-%Y %I-%M-%S')
        
        self.logger.write('{}\t{}\n'.format(time_str, msg))

    def _setupPracticeTrials(self):
        self.log('creating practice trials')

        self.practice_trials = []
        for i in range(self.exp_parameters.n_practice):
            condition_key = numpy.random.randint(0, 2 * len(self.exp_parameters.set_size))
            self.practice_trials.append(self._createTrial(condition))

        self.log('finished generating practice trials')

    def _setupExperimentTrials(self):
        self.log('creating experiment trials')

        self.experiment_trials = []
        for i in range(self.exp_parameters.n_trials):
            condition = i % (len(self.exp_parameters.set_size) * 2)
            self.experiment_trials.append(self._createTrial(condition))

        random.shuffle(self.experiment_trials)

        self.log('finished generating experiment trials')

    def _createTrial(self, condition):
        set_size_index = condition % len(self.exp_parameters.set_size)
        set_size = self.exp_parameters.set_size[set_size_index]
        
        probe_types = ['change', 'same']
        probe_type_index = condition // len(self.exp_parameters.set_size)
        probe_type = probe_types[probe_type_index]

        return myClasses.Trial(self.exp_parameters, set_size, probe_type)