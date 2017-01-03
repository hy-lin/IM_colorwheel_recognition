'''
Created on Jan 3, 2017

@author: Hsuan-Yu Lin
'''

import Parser
import figures

import numpy


def plotYesDistribution(participants):
    plot_data = {}
    n_bins = 15
    x_label = numpy.linspace(-179, 180, n_bins)
    for set_size in range(1, 7):
        distances = []
        
        constraints = {'set_size': [set_size]}
        
        for pID in participants.keys():
            distances += participants[pID].getDistances(constraints)
            
        bin_count, _ = numpy.histogram(distances, n_bins)
        plot_data['set size {}'.format(set_size)] = numpy.concatenate(([x_label], [bin_count]))
        
    distribution_plot = figures.LineFigure(plot_data)
    distribution_plot.show()

def plotPC(participants):
    plot_data = {}
    for probe_type in ['positive', 'new', 'intrusion']:
        plot_data[probe_type] = [[], []]
        for set_size in range(1, 7):
            constraints = {'probe_type': [probe_type], 'set_size': [set_size]}
            
            PCs = []
            for pID in participants.keys():
                PCs.append(participants[pID].getPC(constraints))
                
            plot_data[probe_type][1].append(numpy.mean(PCs))
            plot_data[probe_type][0].append(set_size)
                
        plot_data[probe_type] = numpy.array(plot_data[probe_type])
        
    PC_plot = figures.LineFigure(plot_data)
    PC_plot.show()

def plotRT(participants):
    plot_data = {}
    for probe_type in ['positive', 'new', 'intrusion']:
        plot_data[probe_type] = [[], []]
        for set_size in range(1, 7):
            constraints = {'probe_type': [probe_type], 'set_size': [set_size]}
            
            RTs = []
            for pID in participants.keys():
                RTs.append(participants[pID].getRT(constraints))
                
            plot_data[probe_type][1].append(numpy.mean(RTs))
            plot_data[probe_type][0].append(set_size)
                
        plot_data[probe_type] = numpy.array(plot_data[probe_type])
        
    PC_plot = figures.LineFigure(plot_data)
    PC_plot.show()

def main():
    data_file = open('Data\\colorwheelr1.dat')
    data_format = Parser.BasicDataFormat()
    parser = Parser.BasicParser(data_file, data_format)
    
    participants = parser.parse()
    
    data_file.close()

    plotYesDistribution(participants)
    plotPC(participants)
    plotRT(participants)

if __name__ == '__main__':
    main()
    pass