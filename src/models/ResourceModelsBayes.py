'''
Created on 23.08.2017

@author: Hsuan-Yu Lin
'''
import ResourceModels
import numpy

class SlotAveragingBayes(ResourceModels.SlotAveraging):
    def __init__(self, k = 2.2, kappa = 7.2, interface_knowledge = 'memory'):
        super(SlotAveragingBayes, self).__init__(k, kappa)

        self.model_name_prefix = 'Slot Averaging Model with Bayes'
        self.interface_knowledge = interface_knowledge

        self.major_version = 1
        self.middle_version = 2
        self.minor_version = 3

        self.model_name = self.updateModelName()
        self.model_name += self.interface_knowledge

    def getPrediction(self, trial):
        pm = self._getPMemory(trials)
        d = self._getD(trial)

        if self.interface_knowledge == 'memory':
            p_recall = self._getActivation(trial.target.color, self.kappa)
            p_recall /= numpy.sum(p_recall)

            return numpy.sum((d > 0) * p_recall) * pm + (1.0-pm) * 0.5
        else:
            p_recall = self._getPred(trial.target.color, self.kappa)
            p_recall /= numpy.sum(p_recall)

            return numpy.sum((d > 0) * p_recall)

    def _getD(self, trial):
        if self.interface_knowledge == 'memory':
            act = self._getActivation(trial.probe.color, self.kappa)
        else:
            act = self._getPred(trial.probe.color, self.kappa)

        return -numpy.log(2.0 * numpy.pi * act)

class SlotAveragingBindingBayes(ResourceModels.SlogAveragingBinding):
    def __init__(self, k = 2.2, kappa = 7.2, b = .8):
        super(SlotAveragingBindingBayes, self).__init__(k, kappa, b)

        self.model_name_prefix = 'Slot Averaging Model with Binding errors and Bayes'

        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 5

        self.model_name = self.updateModelName()

    def getPrediction(self, trial):
        pm = self._getPMemory(trial)

        d = self._getD(trial, pm)

        p_recall = self.getPRecall(trial)

        return numpy.sum((d > 0) * p_recall)

    def _getD(self, trial, pm):
        act = self._getActivation(trial.probe.color, self.kappa)

        return -numpy.log(2.0 * numpy.pi * ((1.0-self.b*(trial.set_size-1)) * pm * act + (1 - ((1.0-self.b*(trial.set_size-1)) * pm)) / (2.0 * numpy.pi)))

class VariablePrecisionBayes(ResourceModels.VariablePrecision):
    def __init__(self, J1 = 60.0, tau = 44.47, alpha = 0.7386):
        super(VariablePrecisionBayes, self).__init__(J1, tau, alpha)

        self.model_name_prefix = 'Variable Precision Model with Bayes'

        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 2

        self.model_name = self.updateModelName()

    def getPrediction(self, trial):
        d = self._getD(trial)

        p_recall = self.getPRecall(trial)

        return numpy.sum((d > 0) * p_recall)

    def _getD(self, trial):
        act = self._getActivation(trial.probe.color, trial.set_size)

        return -numpy.log(2.0 * numpy.pi * act)

class VariablePrecisionBindingBayes(ResourceModels.VariablePrecisionBinding):
    def __init__(self, J1 = 60.0, tau = 44.47, alpha = 0.7386, kappa_s_scaling = 0.05):
        super(VariablePrecisionBindingBayes, self).__init__(J1, tau, alpha, kappa_s_scaling)

        self.model_name_prefix = 'Variable Precision Binding Model with Bayes'

        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1

        self.model_name = self.updateModelName()

    def getPrediction(self, trial):
        pm = self.getPM(trial)

        d = self._getD(trial, pm)

        p_recall = self.getPRecall(trial)

        return numpy.sum((d > 0) * p_recall)

    def _getD(self, trial, pm):
        act = self._getActivation(trial.probe.color, trial.set_size)

        return -numpy.log(2.0 * numpy.pi * (pm * act + (1 - pm) / (2.0 * numpy.pi)))

class VariablePrecisionSwapBayes(ResourceModels.VariablePrecisionSwap):
    def __init__(self, J1 = 60.0, tau = 44.47, alpha = 0.7386, p_swap = 0.05):
        super(VariablePrecisionSwapBayes, self).__init__(J1, tau, alpha, p_swap)

        self.model_name_prefix = 'Variable Precision Swap Model with Bayes'

        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1

        self.model_name = self.updateModelName()

    def getPrediction(self, trial):
        pm = self.getPM(trial)

        d = self._getD(trial, pm)

        p_recall = self.getPRecall(trial)

        return numpy.sum((d > 0) * p_recall)

    def _getD(self, trial, pm):
        act = self._getActivation(trial.probe.color, trial.set_size)

        return -numpy.log(2.0 * numpy.pi * (pm * act + (1 - pm) / (2.0 * numpy.pi)))

class NeuronModelBayes(ResourceModels.NeuronModel):
    def __init__(self, kappa_color=13.5, kappa_location=13.5, c=2.0):
        super(NeuronModelBayes).__init__(kappa_color, kappa_location, c)

        self.model_name_prefix = 'Neuron Model with Bayes'
        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1
        self.model_name = self.updateModelName()
        self.n_parameters = 3

def _test():
    data_file = open('..\\Data\\colorwheelr1.dat')
    data_format = Parser.BasicDataFormat()
    parser = Parser.BasicParser(data_file, data_format, Parser.Exp1TrialFactory)

    participants = parser.parse()

    data_file.close()
    sabayes = SlotAveragingBayes()
    t0 = time.time()

    for trial in participants[5].trials:
        p_recall = sabayes.getPrediction(trial)
        print(trial, p_recall, numpy.log((trial.response==1) * p_recall + (trial.response==2) * (1-p_recall)))

    print(time.time() - t0)


if __name__ == '__main__':

    import sys
    sys.path.insert(0, '../')
    import Parser
    import time

    _test()
    print('HELLO?')
    pass
