import glfw, typing


class Input():
    def __init__(self) -> None:
        self.key_map: list = [False] * 349
        self.cursor_pos: tuple = (0, 0)
        self.mouse_map: list = [False] * 13
        self.scroll_offset: float = 0


    def _set_cursor_pos_callback(self, window: typing.Any, xpos: int, ypos: int) -> None:
        self.cursor_pos = (xpos, ypos)


    def _key_callback(self, window: typing.Any, key: int, scancode: int, action: int, mods: int) -> None:
        if key is glfw.KEY_UNKNOWN:
            return
        if action is glfw.PRESS:
            self.key_map[key] = True
        elif action is glfw.RELEASE:
            self.key_map[key] = False


    def _mouse_button_callback(self, window: typing.Any, button: int, action: int, mods: int) -> None:
        if action is glfw.PRESS:
            self.mouse_map[button] = True
        elif action is glfw.RELEASE:
            self.mouse_map[button] = False


    def _scroll_callback(self, window: typing.Any, xoffset: float, yoffset: float) -> None:
        self.scroll_offset = yoffset
