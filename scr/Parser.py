'''
Created on Jan 3, 2017

@author: Hsuan-Yu Lin
'''
import numpy

class BasicDataFormat(object):
    def __init__(self):
        self.pID = 0
        self.session = 1
        self.trial_index = 2
        self.set_size = 3
        self.color = [4, 6, 8, 10, 12, 14]
        self.locations = [5, 7, 9, 11, 13, 15]
        self.probe_type = 16
        self.probe = 17
        self.response = 18
        self.RT = 19
        self.correctness = 20

class BasicParser(object):
    '''
    This is the basic Parser for colorwheel recognition data. 
    '''


    def __init__(self, data_file, data_format):
        '''
        Constructor
        '''
        
        self.data_file = data_file
        self.data_format = data_format
        
    def parse(self):
        participants = {}
        
        for line in self.data_file:
            val = line.split()
            
            pID = int(val[self.data_format.pID])
            session = int(val[self.data_format.session])
            trial_index = int(val[self.data_format.trial_index])
            
            if pID not in participants.keys():
                participants[pID] = Participant(pID)
                
                
            trial = BasicTrial(participants[pID])
               
            for i in range(int(val[self.data_format.set_size])):
                color = int(val[self.data_format.color[i]])
                location = int(val[self.data_format.locations[i]])
                
                trial.addStimulus(color, location)
                
            
            probe_type = int(val[self.data_format.probe_type])
            probe = int(val[self.data_format.probe])
            probe_location = int(val[self.data_format.locations[0]])
                
            trial.addProbe(probe, probe_location, probe_type)
            
            RT = float(val[self.data_format.RT])
            response = int(val[self.data_format.response])
            correctness = int(val[self.data_format.correctness])
            
            trial.addResponse(response, RT, correctness)
            
            if not trial.checkSetSize(int(val[self.data_format.set_size])):
                print('Warning, something fucked up in {}'.format(line))
                print(trial.set_size)
                print(int(val[self.data_format.set_size]))
                
            participants[pID].addTrial(trial)
            
        return participants
        
class Stimulus(object):
    def __init__(self, color, location, serial_position = None, output_position = None):
        self.color = color
        self.location = location
        self.serial_position = serial_position
        self.output_position = output_position

class BasicTrial(object):
    '''
        This is the basic trial class for colorwheel recognition experiment.
    '''
    
    def __init__(self, participant = None):
        self.participant = participant
        self.stimuli = []
        self.set_size = 0
        
    def addStimulus(self, color, location):
        self.stimuli.append(Stimulus(color, location))
        self.set_size += 1
        
    def checkSetSize(self, set_size):
        if self.set_size == set_size:
            return True
        else:
            return False
        
    def addProbe(self, color, location, probe_type):
        self.probe = Stimulus(color, location)
        if probe_type == 1:
            self.probe_type = 'positive'
        elif probe_type == 2:
            self.probe_type = 'new'
        elif probe_type == 3:
            self.probe_type = 'intrusion'
        else:
            self.probe_type = 'unknown'
        
    def addResponse(self, response, RT, correctness):
        self.response = response
        self.RT = RT
        self.correctness = correctness
        
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
        
class Participant(object):
    def __init__(self, pID):
        self.pID = pID
        
        self.trials = []
        self.fitting_result = {}
        
    def addTrial(self, trial):
        self.trials.append(trial)
        
    def getTrialsMetConstraints(self, constraints):
        final_pool = []
        
        for trial in self.trials:
            if trial.isMetConstraints(constraints):
                final_pool.append(trial)
                
        return final_pool
        
    def __str__(self):
        return 'pID = {}; N = {}'.format(self.pID, len(self.trials))

    def getRT(self, constraints):
        trials = self.getTrialsMetConstraints(constraints)
                
        RT = []
        for trial in trials:
            RT.append(trial.RT)
            
        return numpy.mean(RT)
    
    def getPC(self, constraints):
        trials = self.getTrialsMetConstraints(constraints)
                
        corrects = []
        for trial in trials:
            if trial.correctness and trial.RT <= 5.0:
                corrects.append(1.0)
            else:
                corrects.append(0.0)
                
        return numpy.mean(corrects)
    
    def getDistances(self, constraints):
        trials = self.getTrialsMetConstraints(constraints)
        distance = []
        
        for trial in trials:
            dist = trial.stimuli[0].color - trial.probe.color
            if dist >= 180:
                dist = dist - 360
            if dist < -179:
                dist = dist + 360
                
            if trial.response == 2:
                distance.append(dist)

            
        return distance
    
def main():
    data_file = open('Data\\colorwheelr1.dat')
    data_format = BasicDataFormat()
    
    parser = BasicParser(data_file, data_format)
    
    participants = parser.parse()
    for pID in participants.keys():
        print(participants[pID])
       
        constraint = {'probe_type': ['positive']}
        print(['positive', participants[pID].getPC(constraint), participants[pID].getRT(constraint)]) 
        
        constraint = {'probe_type': ['new']}
        print(['new', participants[pID].getPC(constraint), participants[pID].getRT(constraint)])
        
        constraint = {'probe_type': ['intrusion']}
        print(['intrusion', participants[pID].getPC(constraint), participants[pID].getRT(constraint)])
    
    data_file.close()
    
    
    
if __name__ == '__main__':
    main()
    pass