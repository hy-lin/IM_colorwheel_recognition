import figures
import shelve
import matplotlib.pyplot

import numpy

import sys
sys.path.insert(0, 'models\\')
import IMBayes

class Stimulus(object):
    def __init__(self, color, location, serial_position = None):
        self.color = color
        self.location = location
        self.serial_position = serial_position

class LocalRecognitionTrial(object):
    def __init__(self, set_size = 5):
        self.set_size = set_size
        self.stimuli = self._createStimuli()

        self.probes = []
        self.targets = []
        self.probes_type = [] 
        self.input_positions = []
        self.output_positions = []

        self._createProbesNTarget()

        self.n_probes = len(self.probes)

        self.probe_index = -1
        self.probe = None

    def _createStimuli(self):
        colors = numpy.linspace(0, 360, num = 13) + numpy.random.randint(0, 30)
        colors = numpy.delete(colors, -1)
        numpy.random.shuffle(colors)

        stimuli = []

        for sp in range(self.set_size):
            stimuli.append(Stimulus(colors[sp], sp, sp))

        return stimuli

    def _createProbesNTarget(self):

        # positive probes
        for sp in range(self.set_size):
            self.probes.append(Stimulus(self.stimuli[sp].color, self.stimuli[sp].location, self.stimuli[sp].serial_position))
            self.targets.append(Stimulus(self.stimuli[sp].color, self.stimuli[sp].location, self.stimuli[sp].serial_position))
            self.probes_type.append('positive')
            self.input_positions.append(sp)
            self.output_positions.append(sp)

        # new probes
        for sp in range(self.set_size): 
            self.probes.append(Stimulus(self._getNewProbeColor(), self.stimuli[sp].location, self.stimuli[sp].serial_position))
            self.targets.append(Stimulus(self.stimuli[sp].color, self.stimuli[sp].location, self.stimuli[sp].serial_position))
            self.probes_type.append('new')
            self.input_positions.append(-1)
            self.output_positions.append(sp)

        # intrusion probes
        for test_position in range(self.set_size):
            for positino_of_origin in range(self.set_size):
                if test_position != positino_of_origin:
                    self.probes.append(Stimulus(self.stimuli[positino_of_origin].color, self.stimuli[test_position].location, self.stimuli[test_position].serial_position))
                    self.targets.append(Stimulus(self.stimuli[test_position].color, self.stimuli[test_position].location, self.stimuli[test_position].serial_position))
                    self.probes_type.append('intrusion')
                    self.input_positions.append(positino_of_origin)
                    self.output_positions.append(test_position)


    def _getNewProbeColor(self):
        min_dist = -1
        while min_dist <= 40:
            color = numpy.random.randint(0, 360)
            min_dist = 999
            for stimulus in self.stimuli:
                dist = abs(stimulus.color - color)
                if dist >= 180:
                    dist = 360 - dist

                if dist <= min_dist:
                    min_dist = dist
        return color

    def advanceProbe(self):
        self.probe_index += 1
        if self.probe_index >= len(self.probes):
            raise ValueError('Advancing probe beyond boundary')

        self.target = self.targets[self.probe_index]
        self.probe = self.probes[self.probe_index]
        self.probe_type = self.probes_type[self.probe_index]
        self.input_position = self.input_positions[self.probe_index]
        self.output_position = self.output_positions[self.probe_index]

class DummyTrial(object):
    def __init__(self, set_size, target, stimuli, probe, probe_type, input_position, serial_position):
        self.set_size = set_size
        self.target = target
        self.stimuli = stimuli
        self.probe = probe
        self.probe_type = probe_type
        self.input_position = input_position
        self.serial_position = serial_position

        self.simulation = {}

    def isMetConstraints(self, constaints):
        passed = True
        
        for argument in constaints.keys():
            if argument in self.__dict__.keys():
                if self.__dict__[argument] not in constaints[argument]:
                    passed = False
            else:
                passed = False
                
            if not passed:
                break
            
        return passed

    def getPFocus(self):
        return 1.0/self.set_size

def getTrialsMetConstraints(trials, constraints):
    final_pool = []
    
    for trial in trials:
        if trial.isMetConstraints(constraints):
            final_pool.append(trial)
            
    return final_pool

def simulatingModel(model, n_rep):
    simulation_trials = []
    for rep_index in range(n_rep):
        print('{}/{}'.format(rep_index, n_rep))
        trial = LocalRecognitionTrial(set_size = 4)
        for probe_index in range(trial.n_probes):
            trial.advanceProbe()
            dummy = DummyTrial(
                trial.set_size,
                trial.target,
                trial.stimuli,
                trial.probe,
                trial.probe_type,
                trial.input_position,
                trial.output_position
            )
            dummy.simulation[model.model_name] = model.getPrediction(dummy)
            simulation_trials.append(dummy)

    return simulation_trials

def plotSerialPosition(trials, model_name):
    plot_data = {}
    for probe_type in ['positive', 'new', 'intrusion']:
        plot_data[probe_type] = [[], []]
        for serial_position in range(0, 4):
            constraints = {'probe_type': [probe_type], 'serial_position': [serial_position]}

            valid_trials = getTrialsMetConstraints(trials, constraints)

            PCs = []
            for trial in valid_trials:
                if probe_type == 'positive':
                    PCs.append(1.0-trial.simulation[model_name])
                else:
                    PCs.append(trial.simulation[model_name])

            plot_data[probe_type][1].append(numpy.nanmean(PCs))
            plot_data[probe_type][0].append(serial_position)

        plot_data[probe_type] = numpy.array(plot_data[probe_type])

    PC_plot = figures.LineFigure(plot_data)
    PC_plot.setXLabel('serial_position', False)
    PC_plot.setYLabel('Proportion of Correct', False)
    # PC_plot.setYLim((0.50, 1.00), False)
    PC_plot.setXLim((-0.5, 3.5), False)
    PC_plot.update()

def plotPositionOfOrigin(trials, model_name):
    plot_data = {}
    for probe_type in ['intrusion']:
        plot_data[probe_type] = [[], []]
        for input_position in range(0, 4):
            constraints = {'probe_type': [probe_type], 'input_position': [input_position]}

            valid_trials = getTrialsMetConstraints(trials, constraints)

            PCs = []
            for trial in valid_trials:
                if probe_type == 'positive':
                    PCs.append(1.0-trial.simulation[model_name])
                else:
                    PCs.append(trial.simulation[model_name])

            plot_data[probe_type][1].append(numpy.nanmean(PCs))
            plot_data[probe_type][0].append(input_position)

        plot_data[probe_type] = numpy.array(plot_data[probe_type])

    PC_plot = figures.LineFigure(plot_data)
    PC_plot.setXLabel('serial_position', False)
    PC_plot.setYLabel('Proportion of Correct', False)
    # PC_plot.setYLim((0.50, 1.00), False)
    PC_plot.setXLim((-0.5, 3.5), False)
    PC_plot.update()


if __name__ == '__main__':
    model = IMBayes.IMEtaBayes()
    result = simulatingModel(model, 500)
    plotSerialPosition(result, model.model_name)
    plotPositionOfOrigin(result, model.model_name)
    matplotlib.pyplot.show()

    pass
