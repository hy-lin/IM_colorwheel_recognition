'''
Created on 1/9/2018
This is the setup file for experiment parameters.

@author: Hsuan-Yu Lin
'''
import CIELAB 

class ExpParameters(object):
    '''
    This is the class of experiment parameters. 
    You can adjust severl aspects in here, but the sequence can't be readjusted.
    '''
    def __init__(self):

        self.stimulus_size = 0.05

        self.thick_frame = 0.003
        self.thin_frame = 0.001

        self.location_radius = 0.5
        self.colorwheel_radius1 = 0.65
        self.colorwheel_radius2 = 0.85

        self.exp_parameters = CIELAB.Color_Lab(70.0, 20.0, 38.0)

        self.stimulus_onset = 1000
        self.retention_interval = 500