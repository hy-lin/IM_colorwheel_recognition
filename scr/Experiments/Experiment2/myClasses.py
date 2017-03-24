# coding= latin-1
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
        self.set_size = set_size
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
        if self.probe_type == 'same':
            self.probe = self.target
            self.correct_response = 0

        elif self.probe_type == 'change':
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
        self.target = self.stimuli[0]
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
        for stimulus in self.stimuli:
            stimulus.draw(display)
            
        display.refresh()
        display.wait(500)
    
        display.clear(refresh = True)
        display.wait(500)
    
        display.clear()
        for stimulus in self.stimuli:
            stimulus.drawThinFrame(display)
        self.probe.draw(display)
        display.refresh()
        
    def getResponse(self, recorder):
        pressed_button, self.t = recorder.recordKeyboard(self.exp_parameters.recognition_keys) 
        self.pressed = pressed_button
            
        if self.correct_response == self.pressed:
            self.correctness = 1
        else:
            self.correctness = 0
            
class Color_Lab(object):
    def __init__(self, L, a, b):
        self.L = L
        self.a = a
        self.b = b
        
    def toRGB(self):
        varY = (self.L + 16) / 115.0
        varX = self.a / 500.0 + varY
        varZ = varY - self.b / 200.0
        
        varX = self._filter_threshold(varX)
        varY = self._filter_threshold(varY)
        varZ = self._filter_threshold(varZ)
        
        refX =  95.047
        refY = 100.000
        refZ = 108.883
        
        X = refX * varX / 100
        Y = refY * varY / 100
        Z = refZ * varZ / 100
        
        varR = X * 3.2406 + Y * (-1.5374) + Z * (-0.4986)
        varG = X * (-0.9689) + Y * 1.8758 + Z * 0.0415
        varB = X * 0.0557 + Y * (-0.2040) + Z * 1.0570
        
        R = self._gamma_correction(varR) * 255
        G = self._gamma_correction(varG) * 255
        B = self._gamma_correction(varB) * 255
        
        R = self._trimming(R)
        G = self._trimming(G)
        B = self._trimming(B)
        
        return [R, G, B]
    
    def _gamma_correction(self, rgb):
        '''
        Gamma correction for IEC 61966-2-1 standard
        '''
        if rgb > 0.0031308:
            return 1.055 * (numpy.power(rgb, (1.0/2.4))) - 0.055
        else:
            return 12.92 * rgb
    
    def _filter_threshold(self, xyz):
        if numpy.power(xyz, 3.0) > 0.008856:
            return numpy.power(xyz, 3.0)
        else:
            return (xyz - 16.0/116.0) / 7.787
        
    def _trimming(self, rgb):
        if rgb > 255:
            rgb = 255
        elif rgb < 0:
            rgb = 0
            
        return int(rgb)
    
    def fromRGB(self):
        print('Warnning: function Lab_Color.fromRGB has not been implemented yet.')
        pass

def angle2RGB(ang, Lab_center, radius):
    theta = ang * 2.0 * numpy.pi / 360.0
    a = Lab_center.a + radius * numpy.cos(theta)
    b = Lab_center.b + radius * numpy.sin(theta)
    L = Lab_center.L
    
    Lab_color = Color_Lab(L, a, b)
    return Lab_color.toRGB()