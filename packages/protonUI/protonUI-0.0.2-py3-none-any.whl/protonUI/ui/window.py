import glfw, typing
from OpenGL.GL import *


class Window():
    def __init__(self) -> None:
        self._size: tuple[int, int] = (800, 600)
        self._position: tuple[int, int] = (100, 100)
        self._background_color: tuple[int, int, int] = (0, 0, 0)
        self._title: str = "title"
        self._window_object: typing.Any = None
        self._resizeable: bool = True
        self._show: bool = True
        
        
        from ..core.engine import Engine
        self._engine = Engine(self)
    
    
    def init(self, size: tuple[int, int], title: str, **kwargs) -> bool: 
        if len(size) != 2:
            return False
        for attribute in size:
            if attribute <= 0: 
                return False
        self._size = size
        
        self._title = title
        
        if not glfw.init(): 
            self._engine._destroy()
            return False 
        
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        
        self._window_object = glfw.create_window(self._size[0], self._size[1], self._title, None, None)
        
        if not self._window_object: 
            self._engine._destroy()
            return False
        
        glfw.make_context_current(self._window_object)
        
        glfw.set_framebuffer_size_callback(self._window_object, self._engine._framebuffer_size_callback)
        glfw.set_cursor_pos_callback(self._window_object, self._engine._input._set_cursor_pos_callback)
        glfw.set_key_callback(self._window_object, self._engine._input._key_callback)
        glfw.set_mouse_button_callback(self._window_object, self._engine._input._mouse_button_callback)
        glfw.set_scroll_callback(self._window_object, self._engine._input._scroll_callback)
    
        glfw.set_window_pos(self._window_object, self._position[0], self._position[1])
        
        if kwargs: self._configure(kwargs)
        return True
        
        
    def position(self, position: tuple[int, int] = None) -> tuple[int, int]:
        if position:
            if len(position) != 2: 
                return None
            
            for pos in position:
                if pos < 0: 
                    return None
                
            self._position = position
            glfw.set_window_pos(self._window_object, self._position[0], self._position[1])
        
        else:
            return self._position
        
        
    def size(self, size: tuple[int, int] = None) -> tuple[int, int]:
        if size:
            if len(size) != 2:
                raise self._size
            
            for lenght in size:
                if lenght < 0:
                    raise self._size
                
            self._size = size
            glfw.set_window_size(self._window_object, self._size[0], self._size[1])
            
        else:
            return self._size
        
        
    def background_color(self, rgb: tuple[int, int, int] = None) -> tuple[int, int, int]:
        if rgb:
            if len(rgb) != 3:
                return None
            
            for color in rgb:
                if not (0 <= color <= 255):
                    return None
                
            self._background_color = [color / 255 for color in rgb]
        
        else:
            return self._background_color
        
        
    def resizeable(self, resizeable: bool = None) -> bool:
        if resizeable is not None:
            self._resizeable = resizeable

            glfw.set_window_attrib(self._window_object, glfw.RESIZABLE, self._resizeable)

        else:
            return self._resizeable
        
        
    def show(self, show: bool = None) -> bool:
        if show is not None:
            self._show = show
        
            if self._show:
                glfw.show_window(self._window_object)
            else:
                glfw.hide_window(self._window_object)
        
        else:
            return self._show
        
        
    def title(self, title: str = None) -> str:
        if title:
            self._title = title
            
        else:
            return self._title
                
        
    def run(self) -> None:
        
        while not glfw.window_should_close(self._window_object):
            
            self._engine._update()
            self._engine._render()
            
            glfw.wait_events() 
            
        self._engine._destroy()
        
        
    def close(self) -> None:
        glfw.set_window_should_close(self._window_object, 1)
        
        
    def _configure(self, **kwargs) -> None:
        pass