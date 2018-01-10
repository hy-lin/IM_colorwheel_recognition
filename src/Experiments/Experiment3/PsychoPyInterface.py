'''
This is the interface for psychopy. I tend to manipulate PsychoPy (or any 
other display library) through an interface isntead of calling PsychoPy
directly, since it's easier to swap library if I so desire.
'''
from psychopy import visual, core, event

class CoreInterface(object):
    '''
    The core interface. 
    '''

    def __init__(self):
        self.window = visual.Window(
            units = 'height',
            monitor = 'Hmm?',
            color = (200, 200, 200),
            colorSpace = 'rgb255', 
            winType = 'pyglet',
            screen = 1
        )

    def close(self):
        self.window.close()

    def refresh(self):
        self.window.flip(clearBuffer=True)

    def clear(self, refresh=False):
        self.window.clearBuffer()
        if refresh:
            self.refresh()

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
            pos = ((x1-x0)/2.0, (y1-y0)/2.0),
            lineWidth = 0,
            fillColor = color,
            fillColorSpace = 'rgb255'
        )

        rect.draw()

    def drawText(self, text, x = 0, y = 0, text_color = (0, 0, 0), font_size = 0.5):
        txt = visual.TextStim(
            self.window,
            text = text,
            font = 'Times New Rome',
            pos = (x, y),
            color = text_color,
            colorSpace = 'rgb255',
            height = font_size
        )

        txt.draw()

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
            polys.append(visual.ShapeStim(win,
                                          vertices = coords[ang],
                                          fillColorSpace = 'rgb255',
                                          fillColor = angle2RGB(ang + shift, self.exp_parameters),
                                          lineWidth = 0))

        return visual.BufferImageStim(win, stim = polys), shift


    def wait(self, ms):
        core.wait(ms * 1000)

class Recorder(object):
    def __init__(self, win):
        self.win = win
        self.mouse = event.Mouse(win = win)

    def getMousePos(self):
        return self.mouse.getPos()

    def resetMouseClick(self):
        self.mouse.clickReset()

    def getMousePressed(self, get_time):
        return self.mouse.getPressed(get_time)

    def setMousePos(self, pos):
        self.mouse.setPos(pos)

    def setCursorVisibility(self, visibility):
        self.mouse.setVisible(visibility)

    