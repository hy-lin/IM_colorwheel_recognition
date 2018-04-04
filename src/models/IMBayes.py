'''
Created on 06.02.2017

@author: Hsuan-Yu Lin
'''
import IM
import numpy
import scipy.stats

class IMBayes(IM.IM):
    '''
    classdocs
    '''

    def __init__(self, b=0.006, a=0.276, s=12.773, kappa=4.63, kappa_f=18.556, r=0.12):
        '''
        Constructor
        '''
        super(IMBayes, self).__init__(
            b=b, a=a, s=s, kappa=kappa, kappa_f=kappa_f, r=r)
        self.model_name_prefix = 'Interference Model with Bayes'

        self.major_version = 2
        self.middle_version = 0
        self.minor_version = 0

        # version 2.0.0: adding the inference_knowledge option into the model

        self.inference_knowledge = ['focus', 'trial_specific']

        self.model_name = self._updateModelName()

    def _updateModelName(self):
        self.model_name =  self.model_name_prefix + ' {} {} v{}.{:02d}.{:02d}'.format(self.inference_knowledge[0], self.inference_knowledge[1], self.major_version, self.middle_version, self.minor_version)
        return self.model_name
    
    def cachePS(self, trials):
        if 'trial_specific' in self.inference_knowledge:
            self.P_s = [[] for i in range(self.max_setsize)]

            if 'focus' in self.inference_knowledge:
                self.P_s_f = [[] for i in range(self.max_setsize)]

            for trial in trials:
                self.P_s[trial.set_size-1].append(self._getPS(trial, 0))

                if 'focus' in self.inference_knowledge:
                    self.P_s_f[trial.set_size-1].append(self._getPS(trial, self.r))

            for i in range(self.max_setsize):
                self.P_s[i] = numpy.mean(self.P_s[i])
                if 'focus' in self.inference_knowledge:
                    self.P_s_f[i] = numpy.mean(self.P_s_f[i])

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

    def getPrediction(self, trial):
        if 'focus' in self.inference_knowledge:
            p_recall_f, p_recall_no_f = self.getPRecall(trial)

            if 'trial_specific' in self.inference_knowledge:
                P_S1_f = self._getPS(trial, self.r)
                P_S1_no_f = self._getPS(trial, 0)
            else:
                P_S1_f = self.P_s[trial.set_size-1]
                P_S1_no_f = self.P_s_f[trial.set_size-1]

            d_f = self._getD(trial, self.kappa_f, P_S1_f)
            d_no_f = self._getD(trial, self.kappa, P_S1_no_f)

            p_change = trial.getPFocus() * numpy.sum((d_f > 0) * p_recall_f) + \
                (1.0 - trial.getPFocus()) * numpy.sum((d_no_f > 0) * p_recall_no_f)
        else:
            p_recall_f, p_recall_no_f = self.getPRecall(trial)
            p_recall = trial.getPFocus() * p_recall_f + (1.0-trial.getPFocus()) * p_recall_no_f

            if 'trial_specific' in self.inference_knowledge:
                P_S1 = self._getPS(trial, 0)
            else:
                P_S1 = self.P_s[trial.set_size-1]

            d = self._getD(trial, self.kappa, P_S1)
            p_change = numpy.sum((d > 0) * p_recall)

        if p_change >= 1.0:
            print('warning, p > 1.0')
            p_change = 0.999999999
        elif p_change <= 0.0:
            print('warning, p < 0')
            p_change = 0.000000001
        return p_change

    def _getPS(self, trial, r=0):
        weighting = numpy.zeros(trial.set_size)
        for i, stimulus in enumerate(trial.stimuli):
            weighting[i] = self._getWeighting(
                trial.probe.location, stimulus.location) + (self.a * r)

        weighting /= (numpy.sum(weighting) + self.b * trial.set_size * r)
        return weighting[trial.serial_position]

    def _getD(self, trial, kappa, P_S):
        act = self._getActivation(trial.probe.color, kappa)

        return -numpy.log(2.0 * numpy.pi * (P_S * act + (1 - P_S) / (2.0 * numpy.pi)))

class IMEtaBayes(IM.IMEta):
    def __init__(self, b=0.006, a=0.05, s=0.1, kappa=4.63, kappa_f=18.556, r=0.12, p = 0.5):
        '''
        Constructor
        '''
        super(IMEtaBayes, self).__init__(
            b=b, a=a, s=s, kappa=kappa, kappa_f=kappa_f, r=r, p = p)
        self.model_name_prefix = 'Interference Model with Bayes and Encoding Strength'

        self.major_version = 1
        self.middle_version = 1
        self.minor_version = 1

        self.model_name = self.updateModelName()

    def getInitialParameters(self):
        return [.01, .0, 4.3, 10.0, 15.75, 0.25, .8]

    def getPRecall(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)

        C = self._getActivationC(trial)
        C_f = self._getActivationC_f(trial)

        p_recall_no_f = self._getPred(A + B + C)
        p_recall_f = self._getPred((A + B) * self.r + C_f)

        return (p_recall_f, p_recall_no_f)

    def getPrediction(self, trial):
        p_recall_f, p_recall_no_f = self.getPRecall(trial)

        P_S1_f = self._getPS(trial, self.r)
        P_S1_no_f = self._getPS(trial, 0)
        d_f = self._getD(trial, self.kappa_f, P_S1_f)
        d_no_f = self._getD(trial, self.kappa, P_S1_no_f)

        p_change = trial.getPFocus() * numpy.sum((d_f > 0) * p_recall_f) + \
            (1.0 - trial.getPFocus()) * numpy.sum((d_no_f > 0) * p_recall_no_f)
#         p_change = numpy.sum((d_no_f > 0) * p_recall_no_f)

        if p_change >= 1.0:
            print('warning, p > 1.0')
            p_change = 0.999999999
        elif p_change <= 0.0:
            print('warning, p < 0')
            p_change = 0.000000001
        return p_change

    def _getPS(self, trial, r):
        weighting = numpy.zeros(trial.set_size)
        for serial_position, stimulus in enumerate(trial.stimuli):
            weighting[serial_position] = self._getWeighting(
                trial.probe.location, stimulus.location) + (self.a * r)

        weighting /= (numpy.sum(weighting) + self.b * trial.set_size * r)
        return weighting[trial.serial_position]

    def _getD(self, trial, kappa, P_S):
        act = self._getActivation(trial.probe.color, kappa)

        return -numpy.log(2.0 * numpy.pi * (P_S * act + (1 - P_S) / (2.0 * numpy.pi)))

class IMBayesKappaD(IMBayes):
    '''
    The IMBayes model with separate precision for decision rule. 
    '''

    def __init__(self, b=.05, a=.01, s=2.5, kappa=7.19, kappa_f=40.14, kappa_d=7.19, r=0.12):

        super(IMBayesKappaD, self).__init__(
            b=b, a=a, s=s, kappa=kappa, kappa_f=kappa_f, r=r)
        self.kappa_d = kappa_d

        self.model_name_prefix = 'Interference Model with additional precision for Bayes'
        self.n_parameters = 7

        self.xmax = [1.0, 1.0, 20.0, 100.0, 100.0, 100.0, 1.0]
        self.xmin = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def getInitialParameters(self):
        return [.05, .21, .5, 7.19, 40.14, 7.19, 0.12]

    def getParametersAsVector(self):
        return [self.b, self.a, self.s, self.kappa, self.kappa_f, self.kappa_d, self.r]

    def updateParameters(self, x):
        self.b = x[0]
        self.a = x[1]
        self.s = x[2]
        self.kappa = x[3]
        self.kappa_f = x[4]
        self.kappa_d = x[5]
        self.r = x[6]

    def getPrediction(self, trial):
        p_recall_f, p_recall_no_f = self.getPRecall(trial)

        P_S1_f = self._getPS(trial, self.r)
        P_S1_no_f = self._getPS(trial, 0)
        d_f = self._getD(trial, self.kappa_d, P_S1_f)
        d_no_f = self._getD(trial, self.kappa_d, P_S1_no_f)

        p_change = trial.getPFocus() * numpy.sum((d_f > 0) * p_recall_f) + \
            (1.0 - trial.getPFocus()) * numpy.sum((d_no_f > 0) * p_recall_no_f)
#         p_change = numpy.sum((d_no_f > 0) * p_recall_no_f)

        if p_change >= 1.0:
            print('warning, p > 1.0')
            p_change = 0.999999999
        elif p_change <= 0.0:
            print('warning, p < 0')
            p_change = 0.000000001
        return p_change


class IMBayesSwap(IMBayes):

    def __init__(self, b=.05, a=.01, s=2.5, kappa=7.19, kappa_f=40.14, r=0.12):
        '''
        Constructor
        '''
        super(IMBayesSwap, self).__init__(
            b=b, a=a, s=s, kappa=kappa, kappa_f=kappa_f, r=r)
        self.model_name_prefix = 'Interference Model with Bayes and Swap'

    def _getPS(self, trial, r):
        weighting = numpy.zeros(trial.set_size)
        for i, stimulus in enumerate(trial.stimuli):
            weighting[i] = self._getWeighting(
                trial.probe.location, stimulus.location) + (self.a * r)

        weighting /= (numpy.sum(weighting) + self.b * trial.set_size * r)
        return weighting

    def _getD(self, trial, kappa, P_S):
        act = self._getActivation(trial.probe.color, kappa)

        if len(P_S) == 1:
            D = -numpy.log(2.0 * numpy.pi *
                           (P_S[0] * act + (1 - P_S[0]) / (2.0 * numpy.pi)))
        else:
            numerator = 0
            for i in range(1, len(P_S)):
                numerator += (P_S[i] * act + (1 - P_S[i]) / (2.0 * numpy.pi))

            numerator /= (trial.set_size - 1)
            numerator += 1.0 / (2.0 * numpy.pi)
            numerator /= 2.0

            D = numpy.log(numerator) \
                - numpy.log(P_S[0] * act + (1 - P_S[0]) / (2.0 * numpy.pi))

        return D

        return -numpy.log(2.0 * numpy.pi * (P_S * act + (1 - P_S) / (2.0 * numpy.pi)))


class IMBayesDual(IM.IM):
    '''
    This is the dual process version of IMBayes, unfortunately the IMBayes doesn't work well.
    '''

    def __init__(self, b=.05, a=.21, s=2.0, kappa=7.19, kappa_f=40.14, r=0.12, color_similairy = 1.0, familiarity_scale = 1, threshold = .7, noise = .5):
        '''
        Constructor
        '''
        super(IMBayesDual, self).__init__(
            b=b, a=a, s=s, kappa=kappa, kappa_f=kappa_f, r=r)

        self.color_similairy = color_similairy
        self.familiarity_scale = familiarity_scale
        self.threshold = threshold
        self.noise = noise

        self.xmax = [1.0, 1.0, 20.0, 100.0, 100.0, 1.0, 20.0, 50.0, 20.0, 5.0]
        self.xmin = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1]

        self.model_name_prefix = 'Interference Model with Bayes Dual Process'
        self.n_parameters = 10

        self.color_similarity_mode = 'exp' # can be choice between exp or von Mises

        self.major_version = 3
        self.middle_version = 2
        self.minor_version = 1

        self.model_name = self.updateModelName()

    def getInitialParameters(self):
        if self.color_similarity_mode == 'exp':
            return [.05, .21, 2.0, 7.19, 40.14, 0.12, 1.0, 15, .5, 1.0]
        else:
            return [.05, .21, 2.0, 7.19, 40.14, 0.12, 7.2, 15, .5, 1.0]

    def getParametersAsVector(self):
        return [self.b, self.a, self.s, self.kappa, self.kappa_f, self.r, self.color_similairy, self.familiarity_scale, self.threshold, self.noise]


    def updateParameters(self, x):
        self.b = x[0]
        self.a = x[1]
        self.s = x[2]
        self.kappa = x[3]
        self.kappa_f = x[4]
        self.r = x[5]
        self.color_similairy = x[6]
        self.familiarity_scale = x[7]
        self.threshold = x[8]
        self.noise = x[9]

    def getPRecall(self, trial):
        A = self._getActivationA(trial)
        B = self._getActivationB(trial)

        C = self._getActivationC(trial)
        C_f = self._getActivationC_f(trial)

        p_recall_no_f = self._getPred(A + B + C)
        p_recall_f = self._getPred((A + B) * self.r + C_f)

        return (p_recall_f, p_recall_no_f)


    def getPrediction(self, trial):
        angs = numpy.arange(0, 360)
        rads = angs * numpy.pi / 180

        p_recall_f, p_recall_no_f = self.getPRecall(trial)

        color_distance = rads - (trial.probe.color * numpy.pi/180)
        color_distance[color_distance > numpy.pi] -= 2*numpy.pi
        color_distance[color_distance < -numpy.pi] += 2*numpy.pi

        probe_color_similarity = self._getColorSimilarity(color_distance)

        d_f_rec = numpy.dot(p_recall_f, probe_color_similarity)
        d_no_f_rec = numpy.dot(p_recall_no_f, probe_color_similarity)

        d_rec = d_f_rec * trial.getPFocus() + d_no_f_rec * (1-trial.getPFocus())

        A = self._getActivationA(trial)
        d_fam = A[trial.probe.color-1]

        d = d_fam * self.familiarity_scale + d_rec
        # print(d_rec, d_f_rec, d_no_f_rec, d_fam, d)

        p_change = 1 - scipy.stats.norm(self.threshold, scale = self.noise).cdf(d)

        return p_change

    def _getColorDistanceMatrix(self, rads):
        dist_matrix = numpy.zeros((360, 360))
        for i in range(360):
            dist_matrix[i] = numpy.roll(rads, i)
        
        dist_matrix -= numpy.tile(rads, (360, 1))

        dist_matrix[dist_matrix > numpy.pi] -= 2*numpy.pi
        dist_matrix[dist_matrix < -numpy.pi] += 2*numpy.pi

        return dist_matrix

    def _getColorSimilarity(self, distances):
        if self.color_similarity_mode == 'exp':
            return numpy.exp(-(numpy.abs(distances) * self.color_similairy))
        elif self.color_similarity_mode == 'von Mises':
            return scipi.stats.vonmises(self.color_similarity).pdf(distances)

def _test():
    data_file = open('..\\Data\\colorwheelr1.dat')
    data_format = Parser.BasicDataFormat()
    parser = Parser.BasicParser(data_file, data_format)

    participants = parser.parse()

    data_file.close()
    imbayes = IMBayesDual()
    t0 = time.time()

    for trial in participants[5].trials:
        p_recall = imbayes.getPrediction(trial)
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
