'''
Created on 23.03.2017
This is the setup file for experiment parameters.
This is not as flexible as I might want to, but I also don't want to
create a script language interpreter just for an experiment.

@author: Hsuan-Yu Lin
'''

class ExpParameters(object):
    '''
    This is the class of experiment parameters. 
    You can adjust severl aspects in here, but the sequence can't be readjusted.
    '''
    def __init__(self):

        self.recognition_keys = ['left', 'right'] # left key is "same', right key is "change"

        # setup for color stimulus
        self.color_center = (70.0, 20.0, 38.0)
        self.color_radius = 70

        # setup for physical look of stimulus
        self.stimulus_radius_unscale = 150
        self.stimulus_size_unscale = 30
        self.thin_line_unscale = 1
        self.thick_line_unscale = 5
        self.font_size_unscaled = 24

        # setup trial profile
        self.n_colors = 360
        self.n_positions = 13

        self.set_sizes = [1, 2, 3, 4, 5, 6]

        # setup experiment profile
        self.n_trials = [80, 170, 170, 80, 80, 80]
        self.n_practice = 10
        self.n_breaks = 20

    def updateDisplayScale(self, display):
        '''
        The unscaled number will be rescaled as 1280x720 screen.
        '''

        x, y = display.window.size
        x_scale = x / 1280.0
        y_scale = y / 720.0
        
        print('x:y = ', x, ':', y)
        print('x:y scale = ', x_scale, ':', y_scale)
        
        self.window_center = (x/2, y/2)
        self.scale = min(x_scale, y_scale)
        self.window_size = (1280 * self.scale, 720 * self.scale)

        self.stimulus_radius = round(self.stimulus_radius_unscale * self.scale)
        self.stimulus_size = round(self.stimulus_size_unscale * self.scale)
        self.thin_line = round(self.thin_line_unscale * self.scale)
        self.thick_line = round(self.thick_line_unscale * self.scale)
        self.font_size = round(self.font_size_unscaled * self.scale)