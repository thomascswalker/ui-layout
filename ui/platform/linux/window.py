import ctypes
import sys
from typing import override

from ui.platform.generic.window import GenericWindow
from ui.platform.linux import constants, types, x11
from ui.platform.linux.renderer import LinuxRenderer
from ui.renderer import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH


class LinuxWindow(GenericWindow):
    @override
    def __init__(
        self,
        filename: str,
        *,
        width: int | None = None,
        height: int | None = None,
    ) -> None:
        super().__init__(filename)

        self.renderer = LinuxRenderer()
        self.renderer.load_file(filename)

        win_w = width if width is not None else MIN_WINDOW_WIDTH
        win_h = height if height is not None else MIN_WINDOW_HEIGHT

        self._display = x11.open_display()
        self._screen = x11.default_screen(self._display)
        root = x11.root_window(self._display, self._screen)
        white = x11.white_pixel(self._display, self._screen)
        black = x11.black_pixel(self._display, self._screen)

        self._window = x11.create_simple_window(
            self._display,
            root,
            constants.DEFAULT_X,
            constants.DEFAULT_Y,
            win_w,
            win_h,
            0,
            black,
            white,
        )

        x11.store_name(self._display, self._window, filename)

        self._wm_delete_atom = x11.intern_atom(
            self._display, b"WM_DELETE_WINDOW", False
        )
        x11.set_wm_protocols(self._display, self._window, [self._wm_delete_atom])

        x11.select_input(self._display, self._window, types.default_event_mask())

        self._gc = x11.create_gc(self._display, self._window)
        x11.set_foreground(self._display, self._gc, black)
        x11.set_background(self._display, self._gc, white)

        self._font = None
        for font_name in (
            b"7x13",
            b"fixed",
            b"-misc-fixed-medium-r-semicondensed--13-*-*-*-*-*-*-*",
        ):
            self._font = x11.load_query_font(self._display, font_name)
            if self._font:
                x11.set_font(self._display, self._gc, self._font.contents.fid)
                break

        self.renderer.bind(
            self._display, self._screen, self._window, self._gc, self._font
        )

    @override
    def show(self) -> None:
        x11.map_window(self._display, self._window)
        x11.flush(self._display)

    def _paint(self) -> None:
        self.renderer.paint(self._window, self._gc)

    @override
    def run(self) -> int:
        exit_code = 0
        buf = (ctypes.c_byte * x11.event_bytes())()
        try:
            while True:
                x11.next_event(self._display, ctypes.byref(buf))
                etype = int.from_bytes(
                    memoryview(buf)[:4],
                    sys.byteorder,
                    signed=True,
                )
                match etype:
                    case types.EventType.EXPOSE:
                        self._paint()
                    case types.EventType.CONFIGURE_NOTIFY:
                        self._paint()
                    case types.EventType.CLIENT_MESSAGE:
                        cm = x11.client_message_from_buffer(buf)
                        if int(cm.data_l[0]) == self._wm_delete_atom:
                            exit_code = 0
                            break
        finally:
            if self._font is not None:
                x11.free_font(self._display, self._font)
            x11.free_gc(self._display, self._gc)
            x11.close_display(self._display)

        return exit_code
