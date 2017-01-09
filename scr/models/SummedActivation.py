'''
Created on 09.01.2017

@author: Hsuan-Yu Lin
'''
import IM

class SummedActivation(IM.IM):
    def __init__(self, b = .15, a = .21, s = 7.7, kappa = 7.19, kappa_f = 40.14, r = 0.12, width = 15):
        super(SummedActivation, self).__init__(b = b, a = a, s = s, kappa = kappa, kappa_f = kappa_f, r = r)
        self.width = width
        
        self.model_name = 'Summed Activation'
        self.n_parameters = 7
        
    def getPrediction(self, trial):
        pass

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