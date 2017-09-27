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
        self.probes, self.targets = self._createProbesNTarget()

    def _createStimuli(self):
        colors = numpy.linspace(0, 360, num = 13) + numpy.random.randint(0, 30)
        colors = numpy.delete(colors, -1)
        numpy.random.shuffle(colors)

        stimuli = []

        for sp in range(self.set_size):
            stimuli.append(Stimulus(colors[sp], sp+1, sp+1))

        return stimuli

    def _createProbesNTarget(self):
        probes = []
        targets = []

        # positive probes
        for sp in range(self.set_size):
            probes.append(Stimulus(self.stimuli[sp].color, self.stimuli[sp].location, self.stimuli[sp].serial_position))
            targets.append(Stimulus(self.stimuli[sp].color, self.stimuli[sp].location, self.stimuli[sp].serial_position))

        # new probes
        for sp in range(self.set_size): 
            probes.append(Stimulus(self._getNewProbeColor(), self.stimuli[sp].location, self.stimuli[sp].serial_position))
            targets.append(Stimulus(self.stimuli[sp].color, self.stimuli[sp].location, self.stimuli[sp].serial_position))

        # intrusion probes
        for test_position in range(self.set_size):
            for positino_of_origin in range(self.set_size):
                if test_position != positino_of_origin:
                    probes.append(Stimulus(self.stimuli[positino_of_origin].color, self.stimuli[test_position].location, self.stimuli[test_position].serial_position))
                    targets.append(Stimulus(self.stimuli[test_position].color, self.stimuli[test_position].location, self.stimuli[test_position].serial_position))

    def _getNewProbeColor(self):
        min_dist = -1
        while min_dist <= 45:
            color = numpy.random.randint(0, 360)
            min_dist = 999
            for stimulus in self.stimuli:
                dist = abs(stimulus.color - color)
                if dist >= 180:
                    dist = 360 - dist

                if dist <= min_dist:
                    min_dist = dist

        return color
