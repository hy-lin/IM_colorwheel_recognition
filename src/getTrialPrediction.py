import numpy

import sys
sys.path.insert(0, 'models\\')
import IMBayes

class Stimulus(object):
    def __init__(self, color, location):
        self.color = color
        self.location = location

class DummyTrial(object):
    def __init__(self, set_size, target, stimuli, probe, probe_type):
        self.set_size = set_size
        self.target = target
        self.stimuli = stimuli
        self.probe = probe
        self.probe_type = probe_type

        self.simulation = {}

    def getPFocus(self):
        return 1.0/self.set_size

def simulatingModel(model):
    stimuli = [
        Stimulus(153, 1),
        Stimulus(195, 10),
        Stimulus(356, 6),
        Stimulus(255, 12),
        Stimulus(231, 8)
    ]
    target = stimuli[2]
    probe = stimuli[4]
    dummy = DummyTrial(
        5,
        target,
        stimuli,
        probe,
        'intrusion',
    )
    
    print(model.getPrediction(dummy))


if __name__ == '__main__':
    model = IMBayes.IMBayes()
    result = simulatingModel(model)

    pass