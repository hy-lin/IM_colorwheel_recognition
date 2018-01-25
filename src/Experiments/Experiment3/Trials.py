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
            self.drawFrame(display)

    def drawFrame(self, display):
        loc = self._getLocation()
        display.drawThickFrame(
            loc[0] - self.exp_parameters.stimulus_size/2.0,
            loc[1] - self.exp_parameters.stimulus_size/2.0,
            loc[0] + self.exp_parameters.stimulus_size/2.0,
            loc[1] + self.exp_parameters.stimulus_size/2.0,
            self.exp_parameters.thin_frame,
            (0, 0, 0)
        )

    def _getLocation(self):
        x = numpy.cos(self.location / 13.0 * 2 * numpy.pi) * self.exp_parameters.location_radius
        y = numpy.sin(self.location / 13.0 * 2 * numpy.pi) * self.exp_parameters.location_radius

        return (x, y)

    def _getRGBColor(self):
        if self.color != -1:
            rgb_color = CIELAB.angle2RGB(self.color, self.exp_parameters.Lab_center, self.exp_parameters.Lab_radius)
        else:
            rgb_color = None
        return rgb_color


class Trial(object):
    '''
    This is the basic trial class, which mostly use to setup the interface.
    '''

    def __init__(self, set_size, stimuli, probe, probe_type, display, exp_parameters):
        self.set_size = set_size
        self.stimuli = stimuli
        self.probe = probe
        self.display = display
        self.exp_parameters = exp_parameters
        self.probe_type = probe_type

        self.t = -1
        self.response = -1

        self.trial_type = 'NA'

    def run(self, display, recorder):
        recorder.hideCursor()
        self.learning(display)
        self.testing(display, recorder)

        display.refresh()
        display.wait(self.exp_parameters.inter_trial_interval)
        display.refresh()

    def learning(self, display):
        for stimulus in self.stimuli:
            stimulus.draw(display)

        display.refresh()
        display.wait(self.exp_parameters.stimulus_onset)
        display.refresh()
        display.wait(self.exp_parameters.retention_interval)
    
    def testing(self, display, recorder):
        pass

    def getSaveString(self):
        output_string = ''
        output_string += '{}\t'.format(self.trial_type)
        output_string += '{}\t{}\t'.format(self.set_size, self.probe_type)
        for stimulus in self.stimuli:
            output_string += '{}\t{}\t'.format(stimulus.color, stimulus.location)

        for i in range(max(self.exp_parameters.set_sizes) - self.set_size):
            output_string += '-1\t-1\t'

        output_string += '{}\t{}\t'.format(self.probe.color, self.probe.location)
        output_string += '{}\t{}'.format(self.t, self.response)

        return output_string
        pass

class RecallTrial(Trial):
    '''
    The recall trial.
    '''

    def __init__(self, set_size, stimuli, probe, probe_type, display, exp_parameters):
        super(RecallTrial, self).__init__(set_size, stimuli, probe, probe_type, display, exp_parameters)
        self.trial_type = 'recall'

    def testing(self, display, recorder):
        colorwheel_coords = self._getWheelCoord()
        colorwheel, shift = display.catchColorwheel(colorwheel_coords)

        recorder.showCursor()
        recorder.resetMouseClick()
        recorder.setMousePos((0, 0))
        
        buttons = [0, 0, 0]
        
        display.refresh()

        while buttons[0] == 0:
            mouse_pos = recorder.getMousePos()
            ang = pos2ang(mouse_pos)

            if ang is None:
                ang = -1
            else:
                ang = (ang + shift) % 360

            colorwheel.draw()

            for stimulus in self.stimuli:
                stimulus.drawFrame(display)

            self.probe.color = ang
            self.probe.draw(display)

            display.refresh()


            buttons, t = recorder.getMousePressed(get_time = True)

        self.t = t[0]
        self.response = ang

        recorder.hideCursor()


    def _getWheelCoord(self):
        x1 = numpy.zeros(361)
        x2 = numpy.zeros(361)
        y1 = numpy.zeros(361)
        y2 = numpy.zeros(361)

        for ang in range(361):
            radian = 2 * numpy.pi * (ang+1) / 360
            if (ang+1) > 360:
                radian = 2 * numpy.pi / 360

            x1[ang] = -self.exp_parameters.colorwheel_radius1 * numpy.cos(radian)
            y1[ang] = self.exp_parameters.colorwheel_radius1 * numpy.sin(radian)
            x2[ang] = -self.exp_parameters.colorwheel_radius2 * numpy.cos(radian)
            y2[ang] = self.exp_parameters.colorwheel_radius2 * numpy.sin(radian)

        coords = []
        for ang in range(360):
            coords.append([(x1[ang], y1[ang]),
                           (x2[ang], y2[ang]),
                           (x2[ang+1], y2[ang+1]),
                           (x1[ang+1], y1[ang+1])])
        
        return coords

def pos2ang(mouse_pos, ref_pos = (0, 0)):
    x, y = mouse_pos
    ref_x, ref_y = ref_pos
    x = x-ref_x
    y = y-ref_y

    dist = numpy.sqrt(x**2 + y**2)
    ang = numpy.arccos(abs(x/dist)) * 180 / numpy.pi

    if x < 0 and y > 0:
        ang = ang
    elif x < 0 and y <= 0:
        ang = 360 - ang
    elif x >=0 and y <= 0:
        ang = ang + 180
    elif x >=0 and y > 0:
        ang = 180 - ang
    
    ang = ang % 360
    
    try:
        return int(numpy.floor(ang))
    except:
        return None

class RecognitionTrial(Trial):
    '''
    The recall trial.
    '''

    def __init__(self, set_size, stimuli, probe, probe_type, display, exp_parameters):
        super(RecognitionTrial, self).__init__(set_size, stimuli, probe, probe_type, display, exp_parameters)
        self.trial_type = 'recognition'

    def testing(self, display, recorder):
        recorder.resetMouseClick()
        
        buttons = [0, 0, 0]
        t0 = display.getTime()
        while buttons[0] == 0 and buttons[2] == 0:
            for stimulus in self.stimuli:
                stimulus.drawFrame(display)
            self.probe.draw(display)
            display.refresh()
            buttons = recorder.getMousePressed()
            
        self.t = display.getTime() - t0

        self.response = buttons[0] == 1
