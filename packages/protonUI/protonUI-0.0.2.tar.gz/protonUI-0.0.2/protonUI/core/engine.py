import typing, glfw
from ..ui import *
from .input import Input
from OpenGL.GL import *


class Engine():
    def __init__(self, window: Window) -> None:
        self._window = window
        self._input = Input()
        
        
    def _framebuffer_size_callback(self, window: typing.Any, width: int, height: int) -> None:
        glViewport(0, 0, width, height)
        self._window.size((width, height))

        self._render()

        
    def _update(self) -> None:
        pass
    
    
    def _render(self) -> None:
        glClearColor(self._window._background_color[0], self._window._background_color[1], self._window._background_color[2], 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
        glfw.swap_buffers(self._window._window_object)
    
    
    def _destroy(self) -> None:
        glfw.destroy_window(self._window._window_object)
        glfw.terminate()