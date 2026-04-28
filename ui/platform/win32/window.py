import ctypes
import logging
from ctypes import wintypes
from typing import override

from ui.platform.generic.window import GenericWindow
from ui.platform.win32 import types, winapi
from ui.platform.win32.renderer import Win32Renderer

logger = logging.getLogger(__name__)


class Win32Window(GenericWindow):
    @override
    def __init__(
        self,
        filename: str,
        *,
        width: int | None = None,
        height: int | None = None,
        x: int | None = None,
        y: int | None = None,
    ):
        super().__init__(filename, width=width, height=height, x=x, y=y)

        self.renderer = Win32Renderer()
        self.renderer.load_file(filename)

        self.window_class = winapi.WndClassExW()
        self.window_class.cb_size = ctypes.sizeof(winapi.WndClassExW)
        self.window_class.style = types.ClassStyle.H_REDRAW | types.ClassStyle.V_REDRAW
        self.window_class.lpfn_wnd_proc = ctypes.cast(
            types.WNDPROC(self.proc),
            ctypes.c_void_p,
        ).value
        self.window_class.cb_cls_extra = 0
        self.window_class.cb_wnd_extra = 0
        self.window_class.h_instance = winapi.get_module_handle(None)
        self.window_class.h_icon = 0
        self.window_class.h_cursor = 0
        self.window_class.hbr_background = winapi.get_stock_object(
            types.StockBrush.WHITE
        )
        self.window_class.lpsz_menu_name = None
        self.window_class.lpsz_class_name = f"{filename}_window_class"
        self.window_class.h_icon_sm = 0

        # Register Window Class
        winapi.register_class_ex(self.window_class)

        # Create Window
        self.window_handle = winapi.create_window_ex(
            0,
            self.window_class.lpsz_class_name,
            filename,
            types.WindowStyle.OVERLAPPED_WINDOW,
            self.x,
            self.y,
            self.width,
            self.height,
            0,
            0,
            self.window_class.h_instance,
            None,
        )

    @override
    def show(self):
        winapi.show_window(self.window_handle, types.ShowWindowCommand.SHOW_NORMAL)
        winapi.update_window(self.window_handle)

    @override
    def run(self) -> int:
        msg = wintypes.MSG()
        while winapi.get_message(msg, 0, 0, 0) != 0:
            winapi.translate_message(msg)
            winapi.dispatch_message(msg)
        return int(msg.wParam)

    def proc(self, hwnd: int, msg: int, wparam: int, lparam: int) -> int:
        ps = winapi.PaintStruct()
        match msg:
            case types.WindowsMessage.DESTROY:
                winapi.post_quit_message(0)
                return 0
            case types.WindowsMessage.SIZE:
                # Invalidate the window to repaint
                winapi.invalidate_rect(hwnd, None, True)
                return winapi.def_window_proc(hwnd, msg, wparam, lparam)
            case types.WindowsMessage.PAINT:
                with winapi.paint(hwnd) as ps:
                    self.renderer.paint(hwnd, ps.device_context)
                    return 0
        return winapi.def_window_proc(hwnd, msg, wparam, lparam)
