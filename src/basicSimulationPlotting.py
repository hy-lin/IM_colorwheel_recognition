'''
Created on Jan 3, 2017

@author: Hsuan-Yu Lin
'''

import Parser
import figures
import shelve
import matplotlib.pyplot

import numpy

import sys
sys.path.insert(0, 'models\\')
import IMBayes


def plotYesDistribution(participants, model_name=None):
    plot_data = {}
    n_bins = 15
    x_label = numpy.linspace(-numpy.pi, numpy.pi, n_bins)
    bnds = numpy.linspace(-numpy.pi, numpy.pi, n_bins + 1)
    for set_size in range(1, 7):
        distances = []

        constraints = {'set_size': [set_size]}

        bin_count = [[] for i in range(n_bins)]

        for pID in participants.keys():
            trials = participants[pID].getTrialsMetConstraints(constraints)
            for trial in trials:
                dist = trial.target.color - trial.probe.color
                if dist >= 180:
                    dist = dist - 360
                if dist < -179:
                    dist = dist + 360

                dist = dist * numpy.pi / 180.0

                bin_index = numpy.extract(dist > bnds, numpy.arange(n_bins))
                bin_index = bin_index[-1]

                if model_name is None:
                    bin_count[bin_index] += [trial.response == 1]
                else:
                    bin_count[bin_index] += [trial.simulation[model_name]]

#         print(bin_count)
        distribution = [1 - numpy.mean(bin_count[i]) for i in range(n_bins)]
        plot_data['set size {}'.format(set_size)] = numpy.array([
            x_label, distribution])

    distribution_plot = figures.LineFigure(plot_data)
    distribution_plot.setXLabel('displacement', update=False)
    distribution_plot.setYLabel('Proportion of "No Change"', update=False)
    if model_name is None:
        distribution_plot.setTitle('Data', True)
    else:
        distribution_plot.setTitle(model_name, True)


def plotPC(participants, model_name=None):
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
    PC_plot.setXLabel('Set sizes', False)
    PC_plot.setYLabel('Proportion of Correct', False)
    PC_plot.setYLim((0.50, 1.00), False)

    if model_name is None:
        PC_plot.setTitle('Data', True)
    else:
        PC_plot.setTitle(model_name, True)


def loadSimulationData(exp_number):
    if exp_number == 1:
        file_path = 'Data/fitting result/Exp1/'
    elif exp_number == 2:
        file_path = 'Data/fitting result/Exp2/'
    file_name = '{}fitting_results.dat'.format(file_path)
    fitting_results = shelve.open(file_name)
    participants = fitting_results['participants']
    fitting_results.close()

    return participants


def loadParticipants(exp_number):
    if exp_number == 1:
        data_file = open('Data\\colorwheelr1.dat')
        data_format = Parser.BasicDataFormat()
        parser = Parser.BasicParser(data_file, data_format, Parser.Exp1TrialFactory)
    elif exp_number == 2:
        data_file = open('Data\\colorwheel2.dat')
        data_format = Parser.Exp2DataFormat()
        parser = Parser.BasicParser(data_file, data_format, Parser.Exp2TrialFactory)

    participants = parser.parse()

    data_file.close()
    return participants


def outputParameters(participants, model_name):
    AIC = 0
    for pID in participants.keys():
        #         print(participants[pID].fitting_result[model_name].fun, participants[pID].fitting_result[model_name].x)
        try:
            AIC += participants[pID].fitting_result[model_name].fun * 2
            print(participants[pID].fitting_result[model_name].x, participants[pID].fitting_result[model_name].fun)
        except:
            ll = 0
            print(participants[pID].fitting_result[model_name][0])
            for trial in participants[pID].trials:
                ll_t = numpy.log((trial.response==1) * trial.simulation[model_name] + \
                                (trial.response==2) * (1-trial.simulation[model_name]))
                # print(ll_t)
                if not numpy.isneginf(ll_t):
                    ll -= ll_t
            # else:
                # ll -= 99999999
            print(ll)
            AIC += ll


    print('Model Name: {}, AIC: {}'.format(model_name, AIC))


def simulateWithDefault(participants, model):
    for pID in participants.keys():
        for trial in participants[pID].trials:
            trial.simulation[model.model_name] = model.getPrediction(trial)

def outputMeasurementParameters(participants, model_name):
    parameter_names = ['A', 'B', 's', 'kappa']
    parameters = {}
    for parameter_name in parameter_names:
        parameters[parameter_name] = [[] for sz in range(6)]

    for pID in participants.keys():
        for sz in range(6):
            xs = participants[pID].fitting_result[model_name].x[sz]
            for i, parameter_name in enumerate(parameter_names):
                parameters[parameter_name][sz] = xs[i]

    median = {}
    means = {}

    for parameter_name in parameter_names:
        median[parameter_name] = []
        means[parameter_name] = []

        for sz in range(6):
            means[parameter_name].append(numpy.mean(parameters[parameter_name][sz]))
            median[parameter_name].append(numpy.median(parameters[parameter_name][sz]))

        means[parameter_name] = numpy.array(means[parameter_name])
        median[parameter_name] = numpy.array(median[parameter_name])

    mean_plot = figures.MultiLineFigures(means)
    median_plot = figures.MultiLineFigures(median)

def outputExp1ResultAsDataFile(participants, models):
    output_file = open('Data\\fitting result\\exp1.dat', 'w')

    for pID in participants.keys():
        participant = participants[pID]
        for tInd, trial in enumerate(participant.trials):
            output_string = ''
            output_string += '{}\t{}\t'.format(pID, tInd)
            output_string += '{}\t{}\t'.format(trial.set_size, trial.probe_type)
            for i in range(trial.set_size):
                output_string += '{}\t{}\t'.format(trial.stimuli[i].color, trial.stimuli[i].location)

            for i in range(6-trial.set_size):
                output_string += '-1\t-1\t'
            
            output_string += '{}\t{}\t'.format(trial.probe.color, trial.probe.location)

            output_string += '{}\t{}\t{}'.format(trial.response, trial.correctness, trial.RT)

            for model in models:
                output_string += '\t{}'.format(trial.simulation[model])

            output_string += '\n'

            output_file.write(output_string)

    output_file.close()

def main():
    participants = loadSimulationData(2)
    # participants = loadParticipants(2)

    plotPC(participants)
    plotYesDistribution(participants)

    models = ['Interference Model with Bayes v1.02.02',
            #   'Interference Model with Bayes v1.01.01',
            #   'Interference Model with Bayes and Swap v1.01.02',
              'Slot Averaging Model with Bayes v1.01.01',
              'Variable Precision Model with Bayes v1.01.01']

    # IMDual = IMBayes.IMBayesDual()
    # simulateWithDefault(participants, IMDual)

    for model_name in models:
        plotPC(participants, model_name)
        plotYesDistribution(participants, model_name)
        outputParameters(participants, model_name)

    # outputExp1ResultAsDataFile(participants, models)

    # outputMeasurementParameters(participants, 'Interference Measurement Model with Bayes v1.01.01')

    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
    pass
