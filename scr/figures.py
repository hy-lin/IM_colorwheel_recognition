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
    def __init__(self, data = {}):
        
        self.data = data
        self.fid = plt.figure()
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
        
    def saveFigure(self, file_path, filename):
        try:
            plt.savefig(file_path+filename)
        except:
            print('Error occurred while saving figure {} at path {}'.format(filename, file_path))
            raise

class LineFigure(BaseFigure):
    def __init__(self, data={}):
        
        BaseFigure.__init__(self, data)

        self.line_styles = \
            [ '-ko'\
            , ':ks'\
            , '-.kv'\
            , '--k^']
            
        self.resetLineCycle()
        self.update()
        
    def update(self):
#         plt.figure(self.fid.number)
        
        # google a way to clean figure
        self.fid.clf()
        self.resetLineCycle(False)
        print(self.data.keys())
        sorted_keys = sorted(self.data.keys())
        
        print(sorted_keys)
        for key in sorted_keys:
            if self.data[key].ndim == 1:
                plt.plot(self.data[key], self.getLineStyle(), label = key) 
            if self.data[key].ndim == 2:
                plt.plot(self.data[key][0], self.data[key][1], self.getLineStyle(), label = key)
            
        if self.xlim != None:
            plt.xlim(self.xlim)
        if self.ylim != None:
            plt.ylim(self.ylim)
        if self.xlabel != None:
            plt.xlabel(self.xlabel)
        if self.ylabel != None:
            plt.ylabel(self.ylabel)
        if self.title != None:
            plt.title(self.title)
        if self.legend:
            plt.legend(loc = 'best')

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
    def __init__(self, data = {}):
        BaseFigure.__init__(self, data)
        
        self.legend = False
        
        self.update()
        
    def update(self):
        self.fid.clf()
        sorted_keys = sorted(self.data.keys())
            
        box_data = []
        for key in sorted_keys:
            box_data.append(self.data[key])
            
        plt.boxplot(box_data, labels = sorted_keys, sym = 'k+')
            
            
        if self.xlim != None:
            plt.xlim(self.xlim)
        if self.ylim != None:
            plt.ylim(self.ylim)
        if self.xlabel != None:
            plt.xlabel(self.xlabel)
        if self.ylabel != None:
            plt.ylabel(self.ylabel)
        if self.title != None:
            plt.title(self.title)
        if self.legend:
            plt.legend(loc = 'best')
        
class ScatterFigure(BaseFigure):
    def __init__(self, data = {}):
        BaseFigure.__init__(self, data)
        
        self.dot_styles = \
            [ 'r'\
            , 'b'\
            , 'k'\
            , 'w']
            
        self.resetDotCycle()
        self.update()
        
    def update(self):
        # google a way to clean figure
        self.fid.clf()
        self.resetDotCycle(False)
        sorted_keys = sorted(self.data.keys())
        for key in sorted_keys:
            x0 = []
            y0 = []
            for x, y in self.data[key]:
                x0.append(x)
                y0.append(y)
                
            print(x0, y0)
            plt.scatter(x0, y0, c = self.getDotStyle(), marker = 'o', label = key) 
            # have to think of a way to sent x axis.
            
        if self.xlim != None:
            plt.xlim(self.xlim)
        if self.ylim != None:
            plt.ylim(self.ylim)
        if self.xlabel != None:
            plt.xlabel(self.xlabel)
        if self.ylabel != None:
            plt.ylabel(self.ylabel)
        if self.title != None:
            plt.title(self.title)
        if self.legend:
            plt.legend(loc = 'best')
        
    def setDotCycle(self, dot_styles, update = False):
        self.dot_styles = dot_styles
        self.resetDotCycle(update)
            
    def resetDotCycle(self, update = False):
        self.dot_cyclor = itertools.cycle(self.dot_styles)
        if update:
            self.update()
            
    def getDotStyle(self):
        return next(self.dot_cyclor)