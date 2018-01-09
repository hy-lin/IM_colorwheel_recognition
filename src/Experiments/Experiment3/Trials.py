'''
Created at 1/9/2018
This contains the trial class for the recall and recognition experiment.

@author: Hsuan-Yu Lin
'''

import CIELAB
import PsychoPyInterface
import numpy

class Stimulus(object):
    '''
    The basic stimulus object, contains two variable:
        1) color: 1-360, -1 is denote to 'no color'
        2) location: 1-13
    '''

    def __init__(self, color, location, exp_parameters):
        self.color = color
        self.location = location
        self.exp_parameters = exp_parameters

    def draw(self, display):
        loc = self._getLocation()
        rgb_color = self._getRGBColor()

        if self.color == -1:
            display.drawThickFrame(
                loc[0] - self.exp_parameters.stimulus_size/2.0,
                loc[1] - self.exp_parameters.stimulus_size/2.0,
                loc[0] + self.exp_parameters.stimulus_size/2.0,
                loc[1] + self.exp_parameters.stimulus_size/2.0,
                self.exp_parameters.thick_frame,
                (0, 0, 0)
            )
        else:
            display.drawFilledRect(
                loc[0] - self.exp_parameters.stimulus_size/2.0,
                loc[1] - self.exp_parameters.stimulus_size/2.0,
                loc[0] + self.exp_parameters.stimulus_size/2.0,
                loc[1] + self.exp_parameters.stimulus_size/2.0,
                self._getRGBColor()
            )
            display.drawThickFrame(
                loc[0] - self.exp_parameters.stimulus_size/2.0,
                loc[1] - self.exp_parameters.stimulus_size/2.0,
                loc[0] + self.exp_parameters.stimulus_size/2.0,
                loc[1] + self.exp_parameters.stimulus_size/2.0,
                self.exp_parameters.thin_frame,
                (0, 0, 0)
            )

    def _getLocation(self):
        x = numpy.cos(self.location / 13.0) * self.exp_parameters.location_radius
        y = numpy.sin(self.location / 13.0) * self.exp_parameters.location_radius

        return (x, y)

    def _getRGBColor(self):
        if self.color != -1:
            rgb_color = CIELAB.angle2RGB(self.color, self.exp_parameters.Lab_center, self.exp_parameters.radius)
        else:
            rbg_color = None
        return rgb_color


class Trial(object):
    '''
    This is the basic trial class, which mostly use to setup the interface.
    '''

    def __init__(self, set_size, stimuli, probe, display, **kwargs):
        self.set_size = set_size
        self.stimuli = stimuli
        self.probe = probe
        self.display = display

        self.additional_infos = kwargs

    def run(self):
        self.learning()
        self.testing()

    def learning(self):
        pass
    
    def testing(self):
        pass