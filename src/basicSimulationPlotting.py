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

def plotSpatialGradient(participants, model_name = None, displayed_model_name = None, save_fig = False):
    plot_data = {}
    max_dist = 7

    for set_size in range(1, 7):
        constraints = {'set_size': [set_size]}
        dist_count = [[] for i in range(max_dist+1)]

        for pID in participants.keys():
            trials = participants[pID].getTrialsMetConstraints(constraints)
            for trial in trials:
                min_color = 13
                min_index = None
                max_trial_dist = 0
                for i, stimulus in enumerate(trial.stimuli):
                    color_dist = abs(stimulus.color - trial.probe.color)
                    if color_dist >= 180:
                        color_dist = 360 - color_dist

                    if min_color > color_dist:
                        min_color = color_dist
                        min_index = i

                    # for stimulus2 in trial.stimuli:
                    #     if stimulus is not stimulus2:
                    #         spatial_distance = numpy.abs(stimulus.location - stimulus2.location)
                    #         if spatial_distance > max_dist:
                    #             spatial_distance = max_dist*2 - spatial_distance - 1 

                    #         if max_trial_dist < spatial_distance:
                    #             max_trial_dist = spatial_distance

                if min_index is not None:
                    spatial_distance = numpy.abs(trial.stimuli[min_index].location - trial.probe.location)
                    if spatial_distance > max_dist:
                        spatial_distance = max_dist*2 - spatial_distance - 1
                    # if max_trial_dist != 0:
                    #     spatial_distance = int(numpy.ceil(spatial_distance * max_dist / max_trial_dist))

                    if model_name is None:
                        dist_count[spatial_distance] += [trial.response == 1]
                    else:
                        dist_count[spatial_distance] += [trial.simulation[model_name]]

        distribution = [1 - numpy.nanmean(dist_count[i]) for i in range(max_dist+1)]
        plot_data['set size {}'.format(set_size)] = numpy.array([
            numpy.arange(max_dist+1), distribution])

    distribution_plot = figures.LineFigure(plot_data)
    distribution_plot.setXLabel('Spatial distance', update=False)
    distribution_plot.setYLabel('Proportion of "No Change"', update=False)
    if model_name is None:
        distribution_plot.setTitle('Data', True)
    else:
        if displayed_model_name is None:
            distribution_plot.setTitle(model_name, True)
        else:
            distribution_plot.setTitle(displayed_model_name, True)

    if save_fig:
        matplotlib.pyplot.savefig('Data\\fitting result\\Exp2\\figs\\Spatial_gradient_{}.png'.format(displayed_model_name))

def plotYesDistribution(participants, model_name=None, displayed_model_name = None, save_fig = False):
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
        distribution = [1 - numpy.nanmean(bin_count[i]) for i in range(n_bins)]
        plot_data['set size {}'.format(set_size)] = numpy.array([
            x_label, distribution])

    distribution_plot = figures.LineFigure(plot_data)
    distribution_plot.setXLabel('displacement', update=False)
    distribution_plot.setYLabel('Proportion of "No Change"', update=False)
    if model_name is None:
        distribution_plot.setTitle('Data', True)
    else:
        distribution_plot.setTitle(displayed_model_name, True)

    if save_fig:
        matplotlib.pyplot.savefig('Data\\fitting result\\Exp2\\figs\\Similarity_gradient_{}.png'.format(displayed_model_name))

def plotPC(participants, model_name=None, displayed_model_name = None, save_fig = False):
    plot_data = {}
    for probe_type in ['positive', 'new', 'intrusion']:
        plot_data[probe_type] = [[], []]
        for set_size in range(1, 7):
            constraints = {'probe_type': [probe_type], 'set_size': [set_size]}

            PCs = []
            for pID in participants.keys():
                PCs.append(participants[pID].getPC(constraints, model_name))

            plot_data[probe_type][1].append(numpy.nanmean(PCs))
            plot_data[probe_type][0].append(set_size)

        plot_data[probe_type] = numpy.array(plot_data[probe_type])

    PC_plot = figures.LineFigure(plot_data)
    PC_plot.setXLabel('Set sizes', False)
    PC_plot.setYLabel('Proportion of Correct', False)
    PC_plot.setYLim((0.50, 1.00), False)
    PC_plot.setXLim((0.5, 6.5), False)

    if model_name is None:
        PC_plot.setTitle('Data', True)
    else:
        if displayed_model_name is None:
            PC_plot.setTitle(model_name, True)
        else:
            PC_plot.setTitle(displayed_model_name, True)

    if save_fig:
        matplotlib.pyplot.savefig('Data\\fitting result\\Exp3\\figs\\Probe_Type_{}.png'.format(model_name))


def plotProbeType(participants, model_name=None, displayed_model_name = None):
    plot_data = {}
    labels = ['No Change', 'Change']
    for i, probe_type in enumerate([['positive'], ['new', 'intrusion']]):
        plot_data[labels[i]] = [[], []]
        for set_size in range(1, 7):
            constraints = {'probe_type': probe_type, 'set_size': [set_size]}

            PCs = []
            for pID in participants.keys():
                PCs.append(participants[pID].getPC(constraints, model_name))

            plot_data[labels[i]][1].append(numpy.nanmean(PCs))
            plot_data[labels[i]][0].append(set_size)

        plot_data[labels[i]] = numpy.array(plot_data[labels[i]])

    PC_plot = figures.LineFigure(plot_data)
    PC_plot.setXLabel('Set sizes', False)
    PC_plot.setYLabel('Proportion of Correct', False)
    PC_plot.setYLim((0.50, 1.00), False)
    PC_plot.setXLim((0.5, 6.5), False)
  

    if model_name is None:
        PC_plot.setTitle('Data', True)
    else:
        if displayed_model_name is None:
            PC_plot.setTitle(model_name, True)
        else:
            PC_plot.setTitle(displayed_model_name, True)
        
def loadSimulationData(exp_number):
    if exp_number == 1:
        file_path = 'Data/fitting result/Exp1/'
    elif exp_number == 2:
        file_path = 'Data/fitting result/Exp2/'
    elif exp_number == 3:
        file_path = 'Data/fitting result/Exp3/'
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
    elif exp_number == 3:
        data_file = open('Data\\recallNrecognition.dat')
        data_format = Parser.Exp3DataFormat()
        parser = Parser.BasicParser(data_file, data_format, Parser.Exp3TrialFactory)

    participants = parser.parse()

    data_file.close()
    return participants


def outputParameters(participants, model_name, displayed_model_name = None, seperate_AIC = False):
    AIC = 0
    parms = numpy.zeros((len(participants), len(participants[1].fitting_result[model_name].x)))
    

    if seperate_AIC:
        
        recognition_AIC = 0
        recall_AIC = 0

        for i, pID in enumerate(participants.keys()):
            parms[i] = participants[pID].fitting_result[model_name].x
            try:
                ll = 0
                for trial in participants[pID].trials:
                    ll_t = numpy.log((trial.response==1) * trial.simulation[model_name] + \
                                    (trial.response==2) * (1-trial.simulation[model_name]))
                    if not numpy.isneginf(ll_t):
                        ll -= ll_t
                recognition_AIC += ll
            except:
                pass

            try:
                ll = 0
                for trial in participants[pID].recall_trials:
                    #print(trial.simulation.keys())
                    ll_t = numpy.log(
                        trial.simulation[model_name][int(trial.response)]
                    )
                    if not numpy.isneginf(ll_t):
                        ll -= ll_t
                    else:
                        ll += 99999999
                recall_AIC += ll
            except BaseException  as e:
                #print(e)
                pass

        if displayed_model_name is not None:
            print('Model Name: {}, Recognition AIC: {}, Recall AIC: {}'.format(displayed_model_name, recognition_AIC*2, recall_AIC*2))
        else:
            print('Model Name: {}, Recognition AIC: {}, Recall AIC: {}'.format(model_name, recognition_AIC*2, recall_AIC*2))

    else:
        for i, pID in enumerate(participants.keys()):
            #         print(participants[pID].fitting_result[model_name].fun, participants[pID].fitting_result[model_name].x)
            try:
                AIC += participants[pID].fitting_result[model_name].fun
                # print(participants[pID].fitting_result[model_name].x, participants[pID].fitting_result[model_name].fun)
                parms[i] = participants[pID].fitting_result[model_name].x
                # print(participants[pID].fitting_result[model_name].fun * 2, participants[pID].fitting_result[model_name].x)
            except:
                ll = 0
                for trial in participants[pID].trials:
                    ll_t = 2 * numpy.log((trial.response==1) * trial.simulation[model_name] + \
                                    (trial.response==2) * (1-trial.simulation[model_name]))
                    # print(ll_t)
                    if not numpy.isneginf(ll_t):
                        ll -= ll_t
                # else:
                    # ll -= 99999999
                AIC += ll


        if displayed_model_name is not None:
            print('Model Name: {}, AIC: {}'.format(displayed_model_name, AIC))
        else:
            print('Model Name: {}, AIC: {}'.format(model_name, AIC))
    
    parameters_median = numpy.median(parms, axis = 0)
    parameters_mean = numpy.mean(parms, axis = 0)

    output_string = 'Parameters median: '
    for parameter in parameters_median:
        output_string += '{:.3f}\t'.format(parameter)
    print(output_string)

    output_string = 'Parameters mean: '
    for parameter in parameters_mean:
        output_string += '{:.3f}\t'.format(parameter)
    print(output_string)

    # print('Individual parameters')
    # for parm in parms:
    #     print(parm)

def outputMeasurementModelParameters(participants, model_name, n_parameter=3, displayed_model_name = None):
    AIC = 0
    output_file = open('measurement_parms.txt', 'a')
    # print(model_name, participants[1].fitting_result[model_name].x)
    parms = numpy.zeros((len(participants), len(participants[1].fitting_result[model_name].x), len(participants[1].fitting_result[model_name].x[0])))
    for i, pID in enumerate(participants.keys()):

        #         print(participants[pID].fitting_result[model_name].fun, participants[pID].fitting_result[model_name].x)
        # try:
            # AIC += participants[pID].fitting_result[model_name].fun * 2 + 2*numpy.log(n_parameter)
        
        for l in range(len(participants[pID].fitting_result[model_name].x)):
            output_string = '{}\t{}\t{}\t'.format(pID, l, model_name)
            parms[i, l] = participants[pID].fitting_result[model_name].x[l]
            for parm in participants[pID].fitting_result[model_name].x[l]:
                output_string += '{:.3f}\t'.format(parm)

            if len(participants[pID].fitting_result[model_name].x[l] < 3):
                output_string += '{:.3f}\t'.format(0)
            output_file.write(output_string + '\n')
        # except:
            # ll = 0
            # for trial in participants[pID].trials:
            #     ll_t = numpy.log((trial.response==1) * trial.simulation[model_name] + \
            #                     (trial.response==2) * (1-trial.simulation[model_name]))
            #     # print(ll_t)
            #     if not numpy.isneginf(ll_t):
            #         ll -= ll_t
            # # else:
            #     # ll -= 99999999
            # AIC += ll

    output_file.close()

    if displayed_model_name is not None:
        print('Model Name: {}, AIC: {}'.format(displayed_model_name, AIC))
    else:
        print('Model Name: {}, AIC: {}'.format(model_name, AIC))

    # parameters_median = numpy.median(parms, axis = 0)
    # parameters_mean = numpy.mean(parms, axis = 0)

    # output_string = 'Parameters median: '
    # for parameter in parameters_median:
    #     for single_parm in parameter:
    #         output_string += '{:.3f}, '.format(single_parm)
    #     output_string += '\n'
    # print(output_string)

    # output_string = 'Parameters mean: '
    # for parameter in parameters_mean:
    #     for single_parm in parameter:
    #         output_string += '{:.3f}, '.format(single_parm)
    #     output_string += '\n'
    # print(output_string)

def simulateWithDefault(participants, model):
    for pID in participants.keys():
        for trial in participants[pID].trials:
            trial.simulation[model.model_name] = model.getPrediction(trial)

def outputMeasurementParameters(participants, model_name):
    parameter_names = ['A', 'B', 's']
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
            means[parameter_name].append(numpy.nanmean(parameters[parameter_name][sz]))
            median[parameter_name].append(numpy.nanmedian(parameters[parameter_name][sz]))

        means[parameter_name] = numpy.array(means[parameter_name])
        median[parameter_name] = numpy.array(median[parameter_name])

    mean_plot = figures.MultiLineFigures(means)
    median_plot = figures.MultiLineFigures(median)

def outputExp12ResultAsDataFile(participants, models, exp):
    output_file = open('Data\\fitting result\\exp{}.dat'.format(exp), 'w')

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

def outputExp3ResultAsDataFile(participants, recognition_models = [], recall_models = []):
    output_file = open('Data\\fitting result\\exp3.dat', 'w')

    for pID in participants.keys():
        participant = participants[pID]
        for tInd, trial in enumerate(participant.trials):
            output_string = ''
            output_string += '{}\t'.format(pID)
            output_string += '{}\t'.format(-1) # session
            output_string += '{}\t'.format('mix') # session condition
            output_string += '{}\t'.format(tInd) # trial index
            output_string += '{}\t'.format('recognition')
            output_string += '{}\t{}\t'.format(trial.set_size, trial.probe_type)
            for i in range(trial.set_size):
                output_string += '{}\t{}\t'.format(trial.stimuli[i].color, trial.stimuli[i].location)

            for i in range(6-trial.set_size):
                output_string += '-1\t-1\t'
            
            output_string += '{}\t{}\t'.format(trial.probe.color, trial.probe.location)

            output_string += '{}\t{}\t{}'.format(trial.RT, trial.response, trial.correctness)

            for model in recognition_models:
                output_string += '\t{}'.format(trial.simulation[model])

            for model in recall_models:
                output_string += '\t{}'.format(-1)

            output_string += '\n'

            output_file.write(output_string)

        for tInd, trial in enumerate(participant.recall_trials):
            output_string = ''
            output_string += '{}\t'.format(pID)
            output_string += '{}\t'.format(-1) # session
            output_string += '{}\t'.format('mix') # session condition
            output_string += '{}\t'.format(tInd) # trial index
            output_string += '{}\t'.format('recall')
            output_string += '{}\t{}\t'.format(trial.set_size, 'recall')
            for i in range(trial.set_size):
                output_string += '{}\t{}\t'.format(trial.stimuli[i].color, trial.stimuli[i].location)

            for i in range(6-trial.set_size):
                output_string += '-1\t-1\t'
            
            output_string += '{}\t{}\t'.format(trial.probe.color, trial.probe.location)

            output_string += '{}\t{}\t{}'.format(trial.RT, trial.response, trial.correctness)

            for model in recognition_models:
                output_string += '\t{}'.format(-1)

            for model in recall_models:
                output_string += '\t{}'.format(trial.simulation[model][trial.response])

            output_string += '\n'

            output_file.write(output_string)

    output_file.close()

def standardOutput(exp):
    participants = loadSimulationData(exp)
    models = [
        'Interference Model with Bayes focus experiment_specific v2.00.00',
        'Interference Model with Bayes focus trial_specific v2.00.00',
        'Interference Model with Bayes no_focus trial_specific v2.00.00',
        'Interference Model with Bayes no_focus experiment_specific v2.00.00',
        'Interference Model with Bayes focus experiment_specific v2.00.00recognition',
        'Interference Model with Bayes focus experiment_specific v2.00.00recall',
        'Interference Model with Bayes a g v2.00.00both',
        'Variable Precision Model with Bayes v2.01.01recallNRecognition',
        'Variable Precision Model with Bayes v2.01.01trialbytrial',
        'Variable Precision Model with Bayes v2.01.01aggregated',
        'Variable Precision Binding Model with Bayes v1.01.02trialbytrial',
        'Variable Precision Binding Model with Bayes v2.01.01aggregated',
        'Slot Averaging Model with Bayes v1.02.03memory',
        'Slot Averaging Model with Bayes v1.02.03no memory state',
        'Slot Averaging Model with Binding errors and Bayes v1.02.01memory',
        'Slot Averaging Model with Binding errors and Bayes v1.02.01no memory state'
    ]

    # outputExp12ResultAsDataFile(participants, models, exp)

    for i, model_name in enumerate(models):
        try:
            outputParameters(participants, model_name, seperate_AIC=True)
        except:
            continue


def main():
    standardOutput(2)
    # standardOutput(2)
   
if __name__ == '__main__':
    main()
    pass
