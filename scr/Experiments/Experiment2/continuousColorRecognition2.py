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

import numpy

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

        self.exp_parameters.updateDisplayScale(self.display)

        self.color_center = myClasses.Color_Lab(
            self.exp_parameters.color_center[0],
            self.exp_parameters.color_center[1],
            self.exp_parameters.color_center[2])
        self.display.angle2RGB = self._wrapper4Angle2RGB

        self.pID = 999
        self.session = 1

        self._setupPracticeTrials()
        self._setupExperimentTrials()

        self.log('experiment created')

    def log(self, msg):
        '''
        a function to save log.
        The output format is: Time, pID, session, msg
        '''
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%d-%b-%Y %I-%M-%S')

        output_string = '{}\t{}\t{}\t{}'.format(
            time_str, self.pID, self.session, msg)

        self.logger.write('{}\n'.format(output_string))
        print(output_string)

    def _wrapper4Angle2RGB(self, ang):
        '''
        This is a wrapper function which setups the angle2RGB in the display module
        '''
        return myClasses.angle2RGB(ang, self.color_center, self.exp_parameters.color_radius)

    def _setupPracticeTrials(self):
        '''
        creating practice trials
        all the conditions are avaliable and randomly selected
        '''
        self.log('creating practice trials')

        self.practice_trials = []
        for i in range(self.exp_parameters.n_practice):
            condition_key = numpy.random.randint(
                0, 2 * len(self.exp_parameters.set_sizes))
            self.practice_trials.append(self._createTrial(condition_key))

        self.log('finished generating practice trials')

    def _setupExperimentTrials(self):
        '''
        creating experiment trials
        i iterates through all the trials then translated into the condition of the trial.
        all the trials are then shuffled
        '''
        self.log('creating experiment trials')

        self.experiment_trials = []
        for i in range(self.exp_parameters.n_trials):
            condition_key = i % (len(self.exp_parameters.set_sizes) * 2)
            self.experiment_trials.append(self._createTrial(condition_key))

        random.shuffle(self.experiment_trials)

        self.log('finished generating experiment trials')

    def _createTrial(self, condition):
        '''
        this function accepts condition and translates it into set size and probe type.
        '''
        set_size_index = condition % len(self.exp_parameters.set_sizes)
        set_size = self.exp_parameters.set_sizes[set_size_index]

        probe_types = ['change', 'same']
        probe_type_index = condition // len(self.exp_parameters.set_sizes)
        probe_type = probe_types[probe_type_index]

        return myClasses.Trial(self.exp_parameters, set_size, probe_type)

    def _getPIDNSession(self):
        '''
        YOU CAN USE BACKSPACE TO CORRECT YOUR INPUT NOW.
        '''
        pID = self.display.getString(self.recorder, 'Participant ID: ', 20, 20)
        session = self.display.getString(self.recorder, 'Session: ', 20, 20)

        return pID, session

    def _greeting(self):
        '''
        idk why it's here.
        it's here.
        '''
        pass

    def _presentPracticeTrials(self):
        self.log('beginning practice trials')

        self.display.showMessage(u'Mit Leertaste weiter zu den Ubungsaufgaben', [
                                 'space'], self.recorder)

        for tInd, trial in enumerate(self.practice_trials):
            self.log('presenting practice trial {}'.format(tInd))
            trial.displayTrial(self.display)
            trial.getResponse(self.recorder)

            self.display.clear(refresh=True)
            self.log('{}'.format(trial.getSaveString()))

    def _presentExperimentTrials(self):
        self.log('beginning experiment trials')

        self.display.showMessage(u'Mit Leertaste weiter zu den Testaufgaben', [
                                 'space'], self.recorder)

        for tInd, trial in enumerate(self.experiment_trials):
            self.log('presenting experiment trials {}'.format(tInd))
            trial.displayTrial(self.display)
            trial.getResponse(self.recorder)

            self.log(trial.getSaveString())
            self._saveTrial(tInd, trial)

            self.display.clear(refresh=True)

            if tInd % (len(self.experiment_trials) / self.exp_parameters.n_breaks) == 0 and tInd != 0:
                self.takingBreak()

    def _saveTrial(self, tInd, trial):
        output_line = trial.getSaveString()
        output_line = '{}\t{}\t{}\n'.format(self.pID, tInd, output_line)

        self.data_file.write(output_line)

    def takingBreak(self):
        self.log('taking a break')

        self.display.showMessage(u'Gelegenheit fur kurze Pause. Weiter mit Leertaste', [
                                 'space'], self.recorder)

    def _endofExperiment(self):
        self.log('experiment finished, closing files.')
        self.data_file.close()

        self.display.showMessage(u'Ende des Experiments: Bitte Versuchsleiter rufen', [
                                 'space'], self.recorder)

        self.log('exiting program. Goodbye.')
        self.logger.close()

    def run(self):
        self.log('experiment started')

        self.recorder.hideCursor()
        self.pID, self.session = self._getPIDNSession()

        self._greeting()
        self._presentPracticeTrials()
        self._presentExperimentTrials()
        self._endofExperiment()

def main():
    experiment = Experiment()
    experiment.run()
    pass

if __name__ == '__main__':
    main()