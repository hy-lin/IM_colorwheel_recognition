# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 18:33:05 2014
There must be a way to do it better.
There must be a way to do it better.
@author: Aicey
"""
import sys
sys.path.insert(0, '../')

import matplotlib.pyplot as plt
import itertools

class BaseFigure(object):
    def __init__(self, data = {}, ax = None):
        
        self.data = data
        if ax is None:
            _, self.ax = plt.subplots()
        else:
            self.ax = ax

        self.title = None
        self.ylim = None
        self.xlim = None
        self.xlabel = None
        self.ylabel = None
        self.legend = True
        
    def update(self):
        pass
        
    def setXLim(self, xlim, update = False):
        self.xlim = xlim
        if update:
            self.update()
            
    def setYLim(self, ylim, update = False):
        self.ylim = ylim
        if update:
            self.update()
            
    def setYLabel(self, ylabel, update = False):
        self.ylabel = ylabel
        if update:
            self.update()
            
    def setXLabel(self, xlabel, update = False):
        self.xlabel = xlabel
        if update:
            self.update()
            
    def setLegend(self, legend, update = False):
        self.legend = legend
        if update:
            self.update()
            
    def setTitle(self, title, update = False):
        self.title = title
        if update:
            self.update()
    
    def show(self):
        plt.show()

    def _update(self):
        if self.xlim != None:
            self.ax.set_xlim(self.xlim)
        if self.ylim != None:
            self.ax.set_ylim(self.ylim)
        if self.xlabel != None:
            self.ax.set_xlabel(self.xlabel)
        if self.ylabel != None:
            self.ax.set_ylabel(self.ylabel)
        if self.title != None:
            self.ax.set_title(self.title)
        if self.legend:
            self.ax.legend(loc = 'best')
        
    def saveFigure(self, file_path, filename):
        try:
            plt.savefig(file_path+filename)
        except:
            print('Error occurred while saving figure {} at path {}'.format(filename, file_path))
            raise

class LineFigure(BaseFigure):
    def __init__(self, data={}, ax = None):
        
        BaseFigure.__init__(self, data, ax)

        self.line_styles = \
            [ '-ko'\
            , ':ks'\
            , '-.kv'\
            , '--k^'\
            , '-k<'\
            , ':k>']
            
        self.resetLineCycle()
        self.update()
        
    def update(self):
#         plt.figure(self.fid.number)
        
        # google a way to clean figure
        self.ax.cla()
        self.resetLineCycle(False)
        sorted_keys = sorted(self.data.keys())
        
        for key in sorted_keys:
            if self.data[key].ndim == 1:
                self.ax.plot(self.data[key], self.getLineStyle(), label = key) 
            if self.data[key].ndim == 2:
                self.ax.plot(self.data[key][0], self.data[key][1], self.getLineStyle(), label = key)
            
        self._update()

    def setLineCycle(self, line_styles, update = False):
        self.line_styles = line_styles
        self.resetLineCycle(update)
            
    def resetLineCycle(self, update = False):
        self.line_cyclor = itertools.cycle(self.line_styles)
        if update:
            self.update()
            
    def getLineStyle(self):
        return next(self.line_cyclor)

class BoxplotFigure(BaseFigure):
    def __init__(self, data = {}, ax = None):
        BaseFigure.__init__(self, data, ax)
        
        self.legend = False
        
        self.update()
        
    def update(self):
        self.ax.cla()
        sorted_keys = sorted(self.data.keys())
            
        box_data = []
        for key in sorted_keys:
            box_data.append(self.data[key])
            
        self.ax.boxplot(box_data, labels = sorted_keys, sym = 'k+')
            
        self._update()
        
class ScatterFigure(BaseFigure):
    def __init__(self, data = {}, ax = None):
        BaseFigure.__init__(self, data, ax)
        
        self.dot_styles = \
            [ 'r'\
            , 'b'\
            , 'k'\
            , 'w']
            
        self.resetDotCycle()
        self.update()
        
    def update(self):
        # google a way to clean figure
        self.ax.cla()
        self.resetDotCycle(False)
        sorted_keys = sorted(self.data.keys())
        for key in sorted_keys:
            x0 = []
            y0 = []
            for x, y in self.data[key]:
                x0.append(x)
                y0.append(y)
                
            print(x0, y0)
            self.ax.scatter(x0, y0, c = self.getDotStyle(), marker = 'o', label = key) 
            # have to think of a way to sent x axis.
            
        self._update()
        
    def setDotCycle(self, dot_styles, update = False):
        self.dot_styles = dot_styles
        self.resetDotCycle(update)
            
    def resetDotCycle(self, update = False):
        self.dot_cyclor = itertools.cycle(self.dot_styles)
        if update:
            self.update()
            
    def getDotStyle(self):
        return next(self.dot_cyclor)

class MultiLineFigures(BaseFigure):
    def __init__(self, data, ax = None):
        BaseFigure.__init__(self, data)


        if len(data) == 0:
            raise(ValueError("MultiLineFigures does not accept empty data."))

        _, self.ax = plt.subplots(len(data))

        figures = {}
        for i, key in enumerate(self.data.keys()):
            print(key, data[key])
            sub_data = {key: self.data[key]}
            figures[key] = LineFigure(sub_data, self.ax[i])
            figures[key].setTitle(key, True)