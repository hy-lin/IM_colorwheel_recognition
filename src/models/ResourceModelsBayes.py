'''
Created on 23.08.2017

@author: Hsuan-Yu Lin
'''
import ResourceModels
import numpy

class SlotAveragingBayes(ResourceModels.SlotAveraging):
    def __init__(self, k = 2.2, kappa = 7.2):
        super(SlotAveragingBayes, self).__init__(k, kappa)

        self.model_name_prefix = 'Slot Averaging Model with Bayes'

        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1

        self.model_name = self.updateModelName()

    def getPrediction(self, trial):
        pm = self._getPMemory(trial)

        d = self._getD(trial, pm)

        p_recall = self.getPRecall(trial)

        return numpy.sum((d > 0) * p_recall)

    def _getD(self, trial, pm):
        act = self._getActivation(trial.probe.color, self.kappa)

        return -numpy.log(2.0 * numpy.pi * (pm * act + (1 - pm) / (2.0 * numpy.pi)))

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
