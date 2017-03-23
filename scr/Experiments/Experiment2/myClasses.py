'''
Created on 17.03.2017

@auther: Hsuan-Yu Lin
'''

import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'

import numpy
import sdl2.ext


class Stimulus(object):
    '''
    The stimulus class.
    attribute color indicates the angle on a standard colorwheel.
    attribute position indicates the location of presentation.
    '''

    def __init__(self, color, position):
        self.color = color
        self.position = position

    def draw(self, display):
        '''
        Draw the stimulus on display.
        The stimulus contain a square color patch and a thick frame
        '''
        x0, y0, x1, y1 = display.getStimulusRect(self.position)
        display.drawThickFrame(
            x0, y0, x1, y1, display.exp_parameters.thin_line, sdl2.ext.Color(0, 0, 0))
        display.drawFilledRect(x0, y0, x1, y1, display.angle2RGB(self.color))

    def drawThinFrame(self, display):
        '''
        Drawing a thin frame at stimulus location.
        '''
        x0, y0, x1, y1 = display.getStimulusRect(self.position)
        display.drawThickFrame(
            x0, y0, x1, y1, display.exp_parameters.thin_line, sdl2.ext.Color(0, 0, 0))

    def drawThickFrame(self, display):
        '''
        Drawing a thick frame at stimulus location.
        '''
        x0, y0, x1, y1 = display.getStimulusRect(self.position)
        display.drawThickFrame(
            x0, y0, x1, y1, display.exp_parameters.thick_line, sdl2.ext.Color(0, 0, 0))

    def __str__(self):
        return '{}\t{}'.format(self.color, self.position)


class Trial(object):
    '''
    The trial class.
    In each trial, stimuli are selected randomly from a colorwheel.
    The minimum distance between stimuli is 1' (no repetition).

    '''

    def __init__(self, exp_parameters, set_size, probe_type):
        '''
        exp_parameters contains the setting for the experiment.
        display is the display interface for the experiment.
        '''

        self.exp_parameters = exp_parameters
        self.set_size = self.set_size
        self.probe_type = probe_type

        self.stimuli = None
        self._createStimuli()
        self._setupProbe()

        self.pressed, self.correctness, self.t = None, None, None

    def _pickChangeProbeColor(self):
        '''
        pick the color of change probe from a uniform distribution.
        '''
        valid_color = False
        while not valid_color:
            valid_color = True

            probe_color = numpy.random.randint(0, 360)

            if probe_color == self.target.color:
                valid_color = False

        return probe_color

    def _setupProbe(self):
        '''
        Setup the probe of the trial.
        The probe color in change condition is selected randomly from a uniform distribution.
        '''
        if probe_type == 'same':
            self.probe = self.target
            self.correct_response = 0

        elif probe_type == 'change':
            probe_color = self._pickChangeProbeColor()
            self.probe = Stimulus(probe_color, self.target.position)
            self.correct_response = 1

        else:
            raise(NameError('Wrong probe type'))

        return True


    def _createStimuli(self):
        '''
        The function of creating stimuli.
        The color is selected from 360 colors. (defined in exp_parameters.n_colors)
        The position is selected from 13 locations. (defined ion exp_parameters.n_positions)
        '''
        colors = self._createColors()
        positions = self._createPositions()

        self.stimuli = [Stimulus(colors[i], positions[i]) for i in range(self.set_size)]
        self.target = stimuli[0]
        return True

    def _createColors(self):
        '''
        Create color of stimuli.
        '''
        colors = numpy.random.choice(self.exp_parameters.n_colors, self.set_size, replace=False)

        return colors

    def _createPositions(self):
        '''
        Create position of stimuli
        '''
        positions = numpy.random.choice(self.exp_parameters.n_positions, self.set_size,\
                                        replace=False)

        return positions

    def getSaveString(self):
        '''
        creates the output string. 
        the output order is:
        1) probe_type
        2, 3) stimulus1 color, stumulus1 position
        4, 5) stimulus2 color, stimulus2 position
        ...
        until the maximum set size avaliable in the experiment.
        The non-exist stimulus will be replaced with -1, -1
        probe color, probe position
        button pressed, correctness, reaction time
        '''
        output_line = '{}\t{}\t'.format(self.set_size, self.probe_type)
        for stimulus in self.stimuli:
            output_line += '{}\t'.format(stimulus)

        for i in range(numpy.max(self.exp_parameters.set_sizes) - self.set_size):
            output_line += '-1\t-1\t'

        output_line += '{}\t'.format(self.probe)
        output_line += '{}\t{}\t{}'.format(self.pressed, self.correctness, self.t)

        return output_line
    def displayTrial(self, display):
        '''
        Learning/retention/recognition part of trials.
        The schedule is: 
        500ms Blank ITI
        500ms Stimuli onset
        500ms Blank interval
        probe onset, waiting response.
        '''
        display.clear(refresh = True)
        display.wait(500)
              
        display.clear()
        for stimulus in self.stimulus:
            stimulus.draw(display)
            
        display.refresh()
        display.wait(500)
    
        display.clear(refresh = True)
        display.wait(500)
    
        display.clear()
        for stimulus in self.stimulus:
            stimulus.drawThinFrame(display)
        probe.draw(display)
        display.refresh()
        
    def getResponse(self, recorder):
        _, pressed_button, self.t = recorder.recordMouse() 
        self.pressed = self.exp_parameters.recognition_keys.index(pressed_button)
            
        if self.correct_response == self.pressed:
            self.correctness = 1
        else:
            self.correctness = 0