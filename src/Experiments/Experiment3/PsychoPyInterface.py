'''
This is the interface for psychopy. I tend to manipulate PsychoPy (or any 
other display library) through an interface isntead of calling PsychoPy
directly, since it's easier to swap library if I so desire.
'''
from psychopy import visual, core, event
import numpy

import CIELAB

class CoreInterface(object):
    '''
    The core interface. 
    '''

    def __init__(self, exp_parameters):
        self.exp_parameters = exp_parameters

        self.window = visual.Window(
            units = 'height',
            monitor = 'Hmm?',
            fullscr=True,
            color = (200, 200, 200),
            colorSpace = 'rgb255', 
            winType = 'pyglet',
            screen = 0
        )

    def close(self):
        self.window.close()

    def refresh(self):
        self.window.flip(clearBuffer=True)

    def clear(self, refresh=False):
        self.window.clearBuffer()
        if refresh:
            self.refresh()

    def getTime(self):
        return core.getTime()

    def drawThickLine(self, x0, y0, x1, y1, thickness, color):
        line = visual.Line(
            self.window,
            start = (x0, y0),
            end = (x1, y1), 
            lineWidth = thickness,
            lineColor = color,
            lineColorSpace = 'rgb255'
        )

        line.draw()

    def drawThickFrame(self, x0, y0, x1, y1, thickness, color):
        self.drawThickLine(x0, y0, x1, y0, thickness, color)
        self.drawThickLine(x0, y0, x0, y1, thickness, color)
        self.drawThickLine(x1, y0, x1, y1, thickness, color)
        self.drawThickLine(x0, y1, x1, y1, thickness, color)

    def drawFilledRect(self, x0, y0, x1, y1, color):
        rect = visual.Rect(
            self.window,
            width = abs(x1-x0),
            height = abs(y1-y0),
            pos = ((x1-x0)/2.0 + x0, (y1-y0)/2.0 + y0),
            lineWidth = 0,
            fillColor = color,
            fillColorSpace = 'rgb255'
        )
        rect.draw()

    def drawText(self, text, x = 0, y = 0, text_color = (0, 0, 0), font_size = 0.05, align_horiz = 'center', align_vert = 'center'):
        txt = visual.TextStim(
            self.window,
            text = text,
            font = 'Times New Rome',
            pos = (x, y),
            color = text_color,
            colorSpace = 'rgb255',
            height = font_size, 
            alignHoriz = align_horiz,
            alignVert = align_vert
        )

        txt.draw()

    def showMessage(self, message, advance_key, recorder):
        self.clear()
        self.drawText(message)
        self.refresh()
        recorder.recordKeyboard(advance_key)

    def drawPoly(self, coords, color):
        poly = visual.ShapeStim(
            self.window,
            vertices = coords,
            fillColor = color,
            fillColorSpace = 'rgb255',
            lineWidth = 0
        )

        poly.draw()

    def catchColorwheel(self, coords, shift = 'random'):
        if shift == 'random':
            shift = numpy.random.randint(0, 359)

        angs = numpy.arange(0, 360) + shift
        angs[angs>=360] = angs[angs>=360] - 360

        polys = []

        for ang in range(360):
            polys.append(visual.ShapeStim(self.window,
                                          vertices = coords[ang],
                                          fillColorSpace = 'rgb255',
                                          fillColor = CIELAB.angle2RGB(ang + shift, self.exp_parameters.Lab_center, self.exp_parameters.Lab_radius),
                                          lineWidth = 0))

        return visual.BufferImageStim(self.window, stim = polys), shift

    def getString(self, recorder, display_text, x = None, y = None, text_color = (0, 0, 0)):
        if x is None:
            x = 0
        if y is None:
            y = 0

        entered = False
        input_string = ''

        self.clear()
        self.drawText(
            display_text + input_string,
            x = x,
            y = y,
            text_color = text_color,
            font_size = 0.05,
            align_horiz = 'left', 
            align_vert = 'top'
        )

        self.refresh()

        key_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'return', 'backspace']
        while not entered:
            input_char = recorder.recordKeyboard(
                allowed_keys = key_list
            )
            input_ind = key_list.index(input_char[0])
            if input_ind <= 9:
                input_string += str(input_ind)
            elif input_ind == 10:
                entered = True
            elif input_ind == 11:
                if len(input_string) != 0:
                    input_string = input_string[:-1]

            self.clear()
            self.drawText(
                display_text + input_string,
                x = x,
                y = y,
                text_color = text_color,
                font_size = 0.05,
                align_horiz = 'left', 
                align_vert = 'top'
            )
            self.refresh()
            self.wait(10)

        return input_string
            

    def showMessage(self, message, advance_key, recorder):
        # self.clear()
        self.drawText(message)
        self.refresh()
        recorder.recordKeyboard(advance_key)

    def wait(self, ms):
        core.wait(ms / 1000.0)

class Recorder(object):
    def __init__(self, win):
        self.win = win
        self.mouse = event.Mouse(win = win)

    def getMousePos(self):
        return self.mouse.getPos()

    def resetMouseClick(self):
        self.mouse.clickReset()

    def getMousePressed(self, get_time = None):
        return self.mouse.getPressed(get_time)

    def setMousePos(self, pos):
        self.mouse.setPos(pos)

    def setCursorVisibility(self, visibility):
        self.mouse.setVisible(visibility)

    def recordKeyboard(self, allowed_keys):
        return event.waitKeys(keyList = allowed_keys)

    def hideCursor(self):
        self.mouse.setVisible(False)

    def showCursor(self):
        self.mouse.setVisible(True)