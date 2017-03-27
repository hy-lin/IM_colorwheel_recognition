'''
Created on 27.04.2015

@author: Hsuan-Yu Lin
'''

import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'

import sdl2.mouse
import sdl2.ext
import sdl2.timer


class Recorder(object):
    '''
    THIS IS A RECORDER! THIS RECORD EVERYTHING.
    It's a recording interface for SDL2.

    setMouse(self, window, coord):
    resetMouseToCenter(self, window)
    hideCursor(self)
    showCursor(self)
    getTicks(self)
    getMouse(self): Get current mouse states
    recordMouse(self) Wait until mouse click
    getKeyboard(self, acceptable_keys) Get current keyboard states
    recordKeyboard(self, acceptable_keys) Wait until key down
    _updateEvents(self)
    '''

    def __init__(self, exp_parameters):
        '''
        Constructor
        '''

        self.exp_parameters = exp_parameters
        self.mouse_x = -1
        self.mouse_y = -1
        self.events = []
        self.last_update_tick = -1

        self.MINIMUM_EVENT_UPDATE_TICKS = 10

    def _updateEvents(self):
        self.events = sdl2.ext.get_events()
        self.last_update_tick = sdl2.timer.SDL_GetTicks()

    def getMouse(self):
        if sdl2.timer.SDL_GetTicks() - self.last_update_tick >= self.MINIMUM_EVENT_UPDATE_TICKS:
            self._updateEvents()

        button = ''
        for event in self.events:
            if event.type == sdl2.SDL_MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.motion.x, event.motion.y
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                self.mouse_x, self.mouse_y = event.button.x, event.button.y
                if event.button.button == sdl2.SDL_BUTTON_LEFT:
                    button = 'left_down'
                if event.button.button == sdl2.SDL_BUTTON_RIGHT:
                    button = 'right_down'
                continue
            if event.type == sdl2.SDL_MOUSEBUTTONUP:
                self.mouse_x, self.mouse_y = event.button.x, event.button.y
                if event.button.button == sdl2.SDL_BUTTON_LEFT:
                    button = 'left_up'
                if event.button.button == sdl2.SDL_BUTTON_RIGHT:
                    button = 'right_up'
                continue
        return self.mouse_x, self.mouse_y, button

    def recordMouse(self):
        t0 = sdl2.timer.SDL_GetTicks()

        button = ''
        while button == '':
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_MOUSEMOTION:
                    self.mouse_x, self.mouse_y = event.motion.x, event.motion.y
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    self.mouse_x, self.mouse_y = event.button.x, event.button.y
                    if event.button.button == sdl2.SDL_BUTTON_LEFT:
                        button = 'left'
                    if event.button.button == sdl2.SDL_BUTTON_RIGHT:
                        button = 'right'

                    continue

        return sdl2.timer.SDL_GetTicks() - t0, button

    def setMouse(self, window, coord):
        x, y = coord[0], coord[1]
        sdl2.mouse.SDL_WarpMouseInWindow(window, x, y)

    def resetMouseToCenter(self, window):
        self.setMouse(window, self.exp_parameters.window_center)

    def hideCursor(self):
        sdl2.mouse.SDL_ShowCursor(sdl2.SDL_DISABLE)

    def showCursor(self):
        sdl2.mouse.SDL_ShowCursor(sdl2.SDL_ENABLE)

    def getKeyboard(self, acceptable_keys):
        if sdl2.timer.SDL_GetTicks() - self.last_update_tick > self.MINIMUM_EVENT_UPDATE_TICKS:
            self._updateEvents()

        for event in self.events:
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_LEFT:
                    pressed = 'left'
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    pressed = 'right'
                elif event.key.keysym.sym == sdl2.SDLK_SPACE:
                    pressed = 'space'
                else:
                    pressed = sdl2.keyboard.SDL_GetKeyName(
                        event.key.keysym.sym)
                    print(pressed)
                if pressed in acceptable_keys:
                    return pressed

    def getTicks(self):
        return sdl2.timer.SDL_GetTicks()

    def recordKeyboard(self, acceptable_keys):
        running = True
        t0 = sdl2.timer.SDL_GetTicks()

        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_LEFT:
                        pressed = 'left'
                    elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                        pressed = 'right'
                    elif event.key.keysym.sym == sdl2.SDLK_SPACE:
                        pressed = 'space'
                    else:
                        pressed = sdl2.keyboard.SDL_GetKeyName(
                            event.key.keysym.sym)

                    if pressed in acceptable_keys:
                        return acceptable_keys.index(pressed), sdl2.timer.SDL_GetTicks() - t0

    def recordSound(self):
        '''
        I'm not sure if this is implemented in SDL2, I think it does, but I'm not sure.
        '''
        pass
