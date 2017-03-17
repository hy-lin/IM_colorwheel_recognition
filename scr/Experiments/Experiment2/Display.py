# coding= latin-1
'''
Created on 23.04.2015

@author: Hsuan-Yu Lin
'''

import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'
os.environ['SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS'] = '0'

import sdl2.ext
import sdl2.sdlgfx
import sdl2.surface
import sdl2.sdlttf
import sdl2.timer


class Display(object):
    '''
    The main display interface for SDL2.
    All color in the function allows a triple as r,g,b values

    functions:
        clear(self, refresh = False)
        refresh(self)
        wait(self, ms)
        waitFPS(self)   Wait until next frame update
        drawThickLine(self, x0, y0, x1, y1, thickness, color=sdl2.ext.Color(0, 0, 0))
        drawThickFrame(self, x0, y0, x1, y1, thickness, color=sdl2.ext.Color(0, 0, 0))
        getString(self, recorder, display_text, x=None, y=None, text_color=sdl2.SDL_Color(0, 0, 0))
        drawText(self, text, x=None, y=None, text_color=sdl2.SDL_Color(0, 0, 0), align='center-center', font_size=60)
        drawSurface(self, src_surface, dst_rect)
    '''

    def __init__(self, RESOURCES, exp_parameters):
        '''
        Constructor
        '''
        self.RESOURCES = RESOURCES
        self.exp_parameters = exp_parameters

        sdl2.ext.init()

        self.fps = sdl2.sdlgfx.FPSManager()
        sdl2.sdlgfx.SDL_initFramerate(self.fps)
        sdl2.sdlgfx.SDL_setFramerate(self.fps, 100)
        self.window = sdl2.ext.Window('Similarity Measurement Exp. 1', (1280, 720), \
                                      flags=sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
        self.window_surface = self.window.get_surface()
        self.w = self.window_surface.w
        self.h = self.window_surface.h
        self.renderer = sdl2.ext.Renderer(self.window_surface)

        self.t0 = sdl2.timer.SDL_GetTicks()

        sdl2.sdlttf.TTF_Init()
        self.font = None
        self.font_size = self.exp_parameters.font_size

        self.running = True

    def clear(self, refresh=False):
        self.renderer.clear(sdl2.ext.Color(200, 200, 200))
        if refresh:
            self.refresh()

    def refresh(self):
        self.renderer.present()
        self.window.refresh()

    def wait(self, ms):
        t0 = sdl2.timer.SDL_GetTicks()
        while sdl2.timer.SDL_GetTicks() - t0 < ms:
            sdl2.ext.get_events()

    def waitFPS(self):
        sdl2.sdlgfx.SDL_framerateDelay(self.fps)

    def drawThickLine(self, x0, y0, x1, y1, thickness, color=sdl2.ext.Color(0, 0, 0)):
        if type(color) is not sdl2.SDL_Color:
            color = sdl2.SDL_Color(
                color[0], color[1], color[2])

        x0, y0, x1, y1, thickness = int(x0), int(
            y0), int(x1), int(y1), int(thickness)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0,
                                  x1, y1, thickness, color.r, color.g, color.b, color.a)

    def drawThickFrame(self, x0, y0, x1, y1, thickness, color=sdl2.ext.Color(0, 0, 0)):
        if type(color) is not sdl2.SDL_Color:
            color = sdl2.SDL_Color(
                color[0], color[1], color[2])

        x0, y0, x1, y1, thickness, mergin = int(x0), int(y0), int(
            x1), int(y1), int(thickness), int(thickness / 2)
        x0, y0, x1, y1 = x0 - mergin, y0 - mergin, x1 + mergin, y1 + mergin
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0,
                                  x1, y0, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0,
                                  x0, y1, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x1, y0,
                                  x1, y1, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y1,
                                  x1, y1, thickness, color.r, color.g, color.b, color.a)

    def getString(self, recorder, display_text, x=None, y=None, text_color=sdl2.SDL_Color(0, 0, 0)):
        if type(text_color) is not sdl2.SDL_Color:
            text_color = sdl2.SDL_Color(
                text_color[0], text_color[1], text_color[2])
        
        if x is None:
            x = self.window_surface.w / 2
        if y is None:
            y = self.window_surface.h / 2

        entered = False
        input_string = ''

        self.clear()
        self.drawText(display_text + input_string, x, y,
                      align='top-left', font_size=self.font_size)
        self.refresh()

        while not entered:
            input_char, _ = recorder.recordKeyboard(
                [b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'Return', b'Backspace'])
            if input_char <= 9:
                input_string += str(input_char)
            elif input_char == 10:
                entered = True
            elif input_char == 11:
                if len(input_string) != 0:
                    input_string = input_string[:-1]

            self.clear()
            self.drawText(display_text + input_string, x, y,
                          align='top-left', font_size=self.font_size)
            self.refresh()
            sdl2.sdlgfx.SDL_framerateDelay(self.fps)

        return input_string

    def drawText(self, text, x=None, y=None, text_color=sdl2.SDL_Color(0, 0, 0), align='center-center', font_size=60):

        if type(text_color) is not sdl2.SDL_Color:
            text_color = sdl2.SDL_Color(
                text_color[0], text_color[1], text_color[2])

        if self.font is None or self.font_size != font_size:
            self.font = sdl2.sdlttf.TTF_OpenFont(self.RESOURCES.get_path(
                'TheanoModern-Regular.ttf').encode(), int(font_size))
            self.font_size = font_size

        if x is None:
            x = self.window_surface.w / 2
        if y is None:
            y = self.window_surface.h / 2
        msg = sdl2.sdlttf.TTF_RenderText_Solid(
            self.font, text.encode('latin_1'), text_color)

        if align == 'center-center':
            msg_rect = sdl2.SDL_Rect(int(
                x - msg.contents.w / 2), int(y - msg.contents.h / 2), msg.contents.w, msg.contents.h)
        elif align == 'top-left':
            msg_rect = sdl2.SDL_Rect(x, y, msg.contents.w, msg.contents.h)
        elif align == 'top-right':
            msg_rect = sdl2.SDL_Rect(
                x - msg.contents.w, y, msg.contents.w, msg.contents.h)
        elif align == 'top-center':
            msg_rect = sdl2.SDL_Rect(
                int(x - msg.contents.w / 2), y, msg.contents.w, msg.contents.h)
        elif align == 'center-left':
            msg_rect = sdl2.SDL_Rect(
                x, int(y - msg.contents.h / 2), msg.contents.w, msg.contents.h)
        elif align == 'center-right':
            msg_rect = sdl2.SDL_Rect(
                x - msg.contents.w, int(y - msg.contents.h / 2), msg.contents.w, msg.contents.h)

        sdl2.surface.SDL_BlitSurface(
            msg.contents, None, self.window_surface, msg_rect)
        sdl2.SDL_FreeSurface(msg)

    def drawSurface(self, src_surface, dst_rect):
        sdl2.surface.SDL_BlitSurface(
            src_surface, None, self.window_surface, dst_rect)
