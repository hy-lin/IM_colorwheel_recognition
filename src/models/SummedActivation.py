'''
Created on 09.01.2017

@author: Hsuan-Yu Lin
'''
import IM

import numpy

class SummedActivation(IM.IM):
    def __init__(self, b = .15, a = .21, s = 7.7, kappa = 7.19, kappa_f = 40.14, r = 0.12, width = 15):
        super(SummedActivation, self).__init__(b = b, a = a, s = s, kappa = kappa, kappa_f = kappa_f, r = r)
        self.width = width
        
        self.model_name = 'Summed Activation'
        self.n_parameters = 7
        
    def getPrediction(self, trial):
        pass

class IMBoundary(IM.IM):
    def __init__(self, b=0.006, a=0.276, s=12.773, kappa=4.63, kappa_f=18.556, r=0.12, boundary = 30):
        super(IMBoundary, self).__init__(b = b, a = a, s = s, kappa = kappa, kappa_f = kappa_f, r = r)
        self.boundary = boundary

        self.model_name_prefix = 'Interference Model with Boundary'

        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1

        self.model_name = self.updateModelName()
        
    def getInitialParameters(self):
        return [.01, .0, 4.3, 10.0, 15.75, 0.25]

    def getPRecall(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)

        C = self._getActivationC(trial)
        C_f = self._getActivationC_f(trial)

        p_recall_no_f = self._getPred(A + B + C)
        p_recall_f = self._getPred((A + B) * self.r + C_f)

        return (p_recall_f, p_recall_no_f)

    def _getBoundaryIndexes(self, trial):
        boundary = int(numpy.round(self.boundary))
        indexes = numpy.arange(trial.probe.color - boundary, trial.probe.color + boundary)
        indexes[indexes<0] = indexes[indexes<0] + 360
        indexes[indexes>359] = indexes[indexes>359] - 360    

        return indexes   

    def getPrediction(self, trial):
        p_recall_f, p_recall_no_f = self.getPRecall(trial)

        boundary_indexes = self._getBoundaryIndexes(trial)

        p_change = numpy.sum(p_recall_f[boundary_indexes]) * trial.getPFocus() + \
            numpy.sum(p_recall_no_f[boundary_indexes]) * (1.0 - trial.getPFocus())

        if p_change >= 1.0:
            print('warning, p > 1.0')
            p_change = 0.999999999
        elif p_change <= 0.0:
            print('warning, p < 0')
            p_change = 0.000000001
        return p_change


import sys
sys.path.insert(0, '../')
import figures

def test():
    im = IM.IM()
    data = {'mu = 180, kappa = 40':im.getActivation(180, 40)}
    line_figure = figures.LineFigure(data)
    line_figure.show()

if __name__ == '__main__':
    test()
    pass