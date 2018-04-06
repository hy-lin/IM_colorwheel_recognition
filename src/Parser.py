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

class Exp2DataFormat(object):
    def __init__(self):
        self.pID = 0
        self.trial_index = 1
        self.set_size = 2
        self.probe_type = 3
        self.color =  [4, 6, 8, 10, 12, 14]
        self.locations = [5, 7, 9, 11, 13, 15]
        self.probe = 16
        self.response = 18
        self.RT = 20
        self.correctness = 19

class Exp3DataFormat(object):
    def __init__(self):
        self.pID = 0
        self.session = 1
        self.session_condition = 2
        self.trial_index = 3
        self.trial_type = 4
        self.set_size = 5
        self.probe_type = 6
        self.color = [7, 9, 11, 13, 15, 17]
        self.locations = [8, 10, 12, 14, 16, 18]
        self.probe = 19
        self.probe_location = 20
        self.RT = 21
        self.response = 22

class BasicParser(object):
    '''
    This is the basic Parser for colorwheel recognition data. 
    '''


    def __init__(self, data_file, data_format, trial_factory):
        '''
        Constructor
        '''
        
        self.data_file = data_file
        self.data_format = data_format
        self.trial_factory = trial_factory
        
    def parse(self):
        participants = {}
        
        for line in self.data_file:
            val = line.split()
            
            pID = int(val[self.data_format.pID])
            # session = int(val[self.data_format.session])
            trial_index = int(val[self.data_format.trial_index])

            try:
                if val[self.data_format.trial_type] == 'recall':
                    continue
            except:
                # nothing happen
                pass
            
            if pID not in participants.keys():
                participants[pID] = Participant(pID)
                
            trial = self.trial_factory(participants[pID])
               
            for i in range(int(val[self.data_format.set_size])):
                color = int(val[self.data_format.color[i]])
                location = int(val[self.data_format.locations[i]])
                
                trial.addStimulus(color, location)
                
            target_color = int(val[self.data_format.color[0]])
            target_location = int(val[self.data_format.locations[0]])
            
            trial.addTarget(target_color, target_location, 0)
            
            probe_type = val[self.data_format.probe_type]
            probe = int(val[self.data_format.probe])
            probe_location = int(val[self.data_format.locations[0]])
                
            trial.addProbe(probe, probe_location, probe_type)
            
            RT = float(val[self.data_format.RT])
            try:
                response = int(val[self.data_format.response])
                correctness = int(val[self.data_format.correctness])
            except:
                response = int(val[self.data_format.response] == 'False')

                if probe_type == 'positive':
                    if response == 1:
                        correctness = 0
                    else:
                        correctness = 1
                else:
                    if response == 1:
                        correctness = 1
                    else:
                        correctness = 2
                   
            
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

    def colorDistTo(self, stimulus2):
        dist = numpy.abs(self.color - stimulus2.color)
        if dist >= 180:
            dist = 360 - dist

        return dist
        
    def __eq__(self, target):
        eq = False
        try:
            if target.color == self.color and\
            target.location == self.location and\
            target.serial_position == self.serial_position and\
            target.output_position == self.output_position:
                eq = True
        except:
            eq = False
            
        return eq

class BasicTrial(object):
    '''
        This is the basic trial class for colorwheel recognition experiment.
    '''
    
    def __init__(self, participant = None):
        self.participant = participant
        self.stimuli = []
        self.set_size = 0
        self.simulation = {}
        
    def __str__(self):
        return 'set size: {}, target: {}, probe: {}, probe type: {}, correctness {}'.format(self.set_size, self.target.color, self.probe.color, self.probe_type, self.correctness)

    def addStimulus(self, color, location):
        self.stimuli.append(Stimulus(color, location))
        self.set_size += 1
        
    def checkSetSize(self, set_size):
        if self.set_size == set_size:
            return True
        else:
            return False
        
    def addTarget(self, color, location, serial_position):
        self.target = Stimulus(color, location)
        self.serial_position = serial_position
        
    def addProbe(self, color, location, probe_type):
        self.probe = Stimulus(color, location)
        if probe_type == '1':
            self.probe_type = 'positive'
        elif probe_type == '2':
            self.probe_type = 'new'
        elif probe_type == '3':
            self.probe_type = 'intrusion'
        else:
            self.probe_type = probe_type
        
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
    
    def getPFocus(self):
        return 1.0/self.set_size

class Exp2Trial(BasicTrial):
    def __init__(self, participant = None):
        super(Exp2Trial, self).__init__(participant)

    def addProbe(self, color, location, probe_type):
        self.probe = Stimulus(color, location)
        if probe_type == 'same':
            self.probe_type = 'positive'
        else:
            self.probe_type = 'new'
            for stimulus in self.stimuli:
                if stimulus != self.target:
                    if stimulus.colorDistTo(self.probe) < 13:
                        self.probe_type = 'intrusion'
        
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
    
    def getPC(self, constraints, model_name = None):
        trials = self.getTrialsMetConstraints(constraints)
                
        corrects = []
        for trial in trials:
            if model_name is None:
                if trial.correctness and trial.RT <= 5000:
                    corrects.append(1.0)
                else:
                    corrects.append(0.0)
            else:
                if trial.probe_type == 'positive':
                    corrects.append(1-trial.simulation[model_name])
                else:
                    corrects.append(trial.simulation[model_name])
                
        return numpy.mean(corrects)
    
    def getDistances(self, constraints, model_name = None, unit = 'radian'):
        trials = self.getTrialsMetConstraints(constraints)
        distance = []
        
        for trial in trials:
            dist = trial.target.color - trial.probe.color
            if dist >= 180:
                dist = dist - 360
            if dist < -179:
                dist = dist + 360
            
            if unit == 'radian':
                dist = dist * numpy.pi / 180.0    
            
            if model_name is None:
                if trial.response == 2:
                    distance.append(dist)
            else:
                distance.append((dist, trial.simulation[model_name]))

            
        return distance

def Exp1TrialFactory(pID):
    return BasicTrial(pID)

def Exp2TrialFactory(pID):
    return Exp2Trial(pID)

def Exp3TrialFactory(pID):
    return BasicTrial(pID)
    
def main():
    data_file = open('Data\\Experiment3\\recallNRecognition.dat')
    # data_format = BasicDataFormat()
    data_format = Exp3DataFormat()
    
    parser = BasicParser(data_file, data_format, Exp3TrialFactory)
    
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