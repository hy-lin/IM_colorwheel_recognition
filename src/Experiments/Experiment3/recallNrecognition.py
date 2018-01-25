import ExpParameters
import Trials
import PsychoPyInterface

import datetime
import numpy



class Experiment(object):
    def __init__(self):
        self.exp_parameters = ExpParameters.ExpParameters()
        self.display = PsychoPyInterface.CoreInterface(self.exp_parameters)
        self.recorder = PsychoPyInterface.Recorder(self.display.window)

        self._getPID()
        self._getSession()
        

        self.save_file = open('Data\\recallNrecognition.dat', 'a')
        self.logger = open('Data\\log.dat', 'a')
        self.logger_string = ''

        self.log('experiment created')

        self._setupPracticeTrials()
        self._setupExperimentTrials()

    def _getPID(self):
        pID = int(self.display.getString(
            self.recorder,
            'Please input participant ID:',
            x = -0.5,
            y = 0.5
            ))

        self.pID = pID

    def _getSession(self):
        session = int(self.display.getString(
            self.recorder,
            'Please input participant session:',
            x = -0.5,
            y = 0.5))

        self.session = session

        self._setSessionType()

    def _setSessionType(self):
        if self.session == 1:
            self.session_type = 'recall'
        if self.session == 2:
            self.session_type = 'recognition'
        if self.session in [3, 4]:
            self.session_type = 'mix'

    def _setupPracticeTrials(self):
        cond_indexes = numpy.random.choice(numpy.arange(32), self.exp_parameters.n_practice_trials, replace=False)

        self.practice_trials = []
        for cond_index in cond_indexes:
            trial_type, set_size, probe_type = self._getTrialCondition(cond_index)
            if trial_type == 'recall':
                self.practice_trials.append(self._createRecallTrial(set_size, probe_type))
            else:
                self.practice_trials.append(self._createRecognitionTrial(set_size, probe_type))

        self.log('finished generating practice trials')

    def _setupExperimentTrials(self):
        cond_indexes = numpy.arange(self.exp_parameters.n_experpiment_trials)
        numpy.random.shuffle(cond_indexes)

        self.experiment_trials = []
        for cond_index in cond_indexes:
            trial_type, set_size, probe_type = self._getTrialCondition(cond_index)
            if trial_type == 'recall':
                self.experiment_trials.append(self._createRecallTrial(set_size, probe_type))
            else:
                self.experiment_trials.append(self._createRecognitionTrial(set_size, probe_type))

        self.log('finished generating experiment trials')

    def _getTrialCondition(self, cond_index):
        cond_index = cond_index % 32

        if cond_index % 2 == 0:
            trial_type = 'recall'
        else:
            trial_type = 'recognition'

        cond_index = cond_index // 2

        set_size_index = cond_index % len(self.exp_parameters.set_sizes)
        set_size = self.exp_parameters.set_sizes[set_size_index]

        cond_index = cond_index // len(self.exp_parameters.set_sizes)

        probe_type = cond_index % 4
        if probe_type == 0:
            probe_type = 'intrusion'
        elif probe_type == 1:
            probe_type = 'new'
        else:
            probe_type = 'positive'

        if self.session_type == 'recall':
            trial_type = 'recall'
            probe_type = 'none'
        if self.session_type == 'recognition':
            trial_type = 'recognition'

        return (trial_type, set_size, probe_type)
        
    def _createRecallTrial(self, set_size, probe_type):
        colors = numpy.random.choice(numpy.arange(360), set_size, replace=False)
        locations = numpy.random.choice(numpy.arange(13), set_size, replace=False)

        stimuli = []
        for color_index in range(set_size):
            stimuli.append(Trials.Stimulus(
                colors[color_index],
                locations[color_index],
                self.exp_parameters
            ))

        probe = Trials.Stimulus(
            numpy.random.randint(0, 360),
            locations[0],
            self.exp_parameters
        )

        return Trials.RecallTrial(set_size, stimuli, probe, probe_type, self.display, self.exp_parameters)

    def _createRecognitionTrial(self, set_size, probe_type):
        colors = numpy.random.choice(numpy.arange(360), set_size, replace=False)
        locations = numpy.random.choice(numpy.arange(13), set_size, replace=False)

        stimuli = []
        for color_index in range(set_size):
            stimuli.append(Trials.Stimulus(
                colors[color_index],
                locations[color_index],
                self.exp_parameters
            ))

        if probe_type == 'intrusion':
            if set_size == 1:
                probe_type = 'new'
            else:
                non_target_index = 1
                probe = Trials.Stimulus(
                colors[non_target_index],
                locations[0],
                self.exp_parameters
            )

        if probe_type == 'positive':
            probe = Trials.Stimulus(
                colors[0],
                locations[0],
                self.exp_parameters
            )
        elif probe_type == 'new':
            is_target_color = True
            while is_target_color:
                new_color = numpy.random.randint(0, 360)
                is_target_color = new_color == colors[0]

            probe = Trials.Stimulus(
                new_color,
                locations[0],
                self.exp_parameters
            )

        return Trials.RecognitionTrial(set_size, stimuli, probe, probe_type, self.display, self.exp_parameters)
        
    def _endofExperiment(self):
        for tInd, experiment_trial in enumerate(self.experiment_trials):
            self.save(experiment_trial, tInd)
	
        self.log('experiment finished, closing files.')
        self.save_file.close()

        self.display.showMessage(u'Ende des Experiments: Bitte Versuchsleiter rufen', [
                                 'space'], self.recorder)

        self.log('exiting program. Goodbye.')
        self.logger.write(self.logger_string)
        self.logger.close()

    def run(self):
        self.log('experiment started')

        self.recorder.hideCursor()

        self.display.showMessage(u'Mit Leertaste weiter zu den Ubungsaufgaben', [
                                 'space'], self.recorder)
        for tInd, practice_trial in enumerate(self.practice_trials):
            self.log('presenting practice trial {}'.format(tInd))
            self.log(practice_trial.getSaveString())
            practice_trial.run(self.display, self.recorder)
            self.log(practice_trial.getSaveString())


        self.display.showMessage(u'Mit Leertaste weiter zu den Testaufgaben', [
                                 'space'], self.recorder)
        for tInd, experiment_trial in enumerate(self.experiment_trials):
            self.log('presenting experiment trials {}'.format(tInd))
            self.log(experiment_trial.getSaveString())
            experiment_trial.run(self.display, self.recorder)
            self.log(experiment_trial.getSaveString())
            

            if tInd % (len(self.experiment_trials) / self.exp_parameters.n_breaks) == 0 and tInd != 0:
                self.takingBreak()

        self._endofExperiment()

    def takingBreak(self):
        self.log('taking a break')

        self.display.showMessage(u'Gelegenheit fur kurze Pause. Weiter mit Leertaste', [
                                 'space'], self.recorder)

    def log(self, msg):
        '''
        a function to save log.
        The output format is: Time, pID, session, msg
        '''
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%d-%b-%Y %I-%M-%S')

        output_string = '{}\t{}\t{}\t{}\n'.format(
            time_str, self.pID, self.session, msg)

        self.logger_string += output_string

        #self.logger.write('{}\n'.format(output_string))
        # print(output_string)

    def save(self, trial, tInd):
        output_string = trial.getSaveString()
        self.save_file.write('{}\t{}\t{}\t{}\t{}\n'.format(self.pID, self.session, self.session_type, tInd, output_string))


def main():
    experiment = Experiment()
    experiment.run()
    pass

if __name__ == '__main__':
    main()