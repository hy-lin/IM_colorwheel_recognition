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

        self.thick_frame = 5.0
        self.thin_frame = 2.0

        self.location_radius = 0.27
        self.colorwheel_radius1 = 0.35
        self.colorwheel_radius2 = 0.4

        self.Lab_center = CIELAB.Color_Lab(70.0, 20.0, 38.0)
        self.Lab_radius = 60

        self.stimulus_onset = 1000
        self.retention_interval = 500
        self.inter_trial_interval = 500

        self.n_practice_trials = 10
        self.n_experpiment_trials = 320
        self.set_sizes = [1, 2, 4, 6]
        self.n_breaks = 10