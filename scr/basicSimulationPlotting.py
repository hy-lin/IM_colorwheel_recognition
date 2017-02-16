'''
Created on Jan 3, 2017

@author: Hsuan-Yu Lin
'''

import Parser
import figures
import shelve

import numpy

import sys
sys.path.insert(0, 'models\\')
import IMBayes


def plotYesDistribution(participants, model_name = None):
    plot_data = {}
    n_bins = 15
    x_label = numpy.linspace(-numpy.pi, numpy.pi, n_bins)
    for set_size in range(1, 7):
        distances = []
        
        constraints = {'set_size': [set_size]}
        
        for pID in participants.keys():
            distances, pYes = participants[pID].getDistances(constraints)
            
        bin_count, _ = numpy.histogram(distances, n_bins)
        plot_data['set size {}'.format(set_size)] = numpy.concatenate(([x_label], [bin_count]))
        
    distribution_plot = figures.LineFigure(plot_data)
    distribution_plot.show()

def plotPC(participants, model_name = None):
    plot_data = {}
    for probe_type in ['positive', 'new', 'intrusion']:
        plot_data[probe_type] = [[], []]
        for set_size in range(1, 7):
            constraints = {'probe_type': [probe_type], 'set_size': [set_size]}
            
            PCs = []
            for pID in participants.keys():
                PCs.append(participants[pID].getPC(constraints, model_name))
                
            plot_data[probe_type][1].append(numpy.mean(PCs))
            plot_data[probe_type][0].append(set_size)
                
        plot_data[probe_type] = numpy.array(plot_data[probe_type])
        
    PC_plot = figures.LineFigure(plot_data)
    PC_plot.show()

def loadSimulationData():
    file_path = 'Data/fitting result/Exp1/'
    pID_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    participants ={}
    
    for pID in pID_list:
        file_name = '{}fitting_result_{}.dat'.format(file_path, pID)
        fitting_result = shelve.open(file_name)
        participants[pID] = fitting_result['participant']
        fitting_result.close()
        
    return participants

def loadParticipants():
    data_file = open('Data\\colorwheelr1.dat')
    data_format = Parser.BasicDataFormat()
    parser = Parser.BasicParser(data_file, data_format)
    
    participants = parser.parse()
    
    data_file.close()
    return participants

def outputParameters(participants, model_name):
    for pID in participants.keys():
        print(participants[pID].fitting_result[model_name].fun, participants[pID].fitting_result[model_name].x)

def simulateWithDefault(participants, model):
    for pID in participants.keys():
        for trial in participants[pID].trials:
            trial.simulation[model.model_name] = model.getPrediction(trial)   
            

def main():
#     participants = loadSimulationData()
    participants = loadParticipants()
    
    model_name = 'Interference Model with Bayes'
    model = IMBayes.IMBayes()
    simulateWithDefault(participants, model)

    print(participants[1].trials[1].simulation)

#     plotYesDistribution(participants, model_name)
    plotPC(participants, model_name)
    outputParameters(participants, model_name)
    

if __name__ == '__main__':
    main()
    pass