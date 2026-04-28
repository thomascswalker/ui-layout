import ctypes
import logging
from ctypes import wintypes
from typing import override

from ui.platform.generic.window import GenericWindow
from ui.platform.win32 import constants, types, winapi
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
    ):
        super().__init__(filename)

        self.renderer = Win32Renderer()
        self.renderer.load_file(filename)

        win_w = width if width is not None else constants.DEFAULT
        win_h = height if height is not None else constants.DEFAULT

        self.cls = winapi.WndClassExW()
        self.cls.cb_size = ctypes.sizeof(winapi.WndClassExW)
        self.cls.style = types.ClassStyle.H_REDRAW | types.ClassStyle.V_REDRAW
        self.cls.lpfn_wnd_proc = ctypes.cast(
            types.WNDPROC(self.proc),
            ctypes.c_void_p,
        ).value
        self.cls.cb_cls_extra = 0
        self.cls.cb_wnd_extra = 0
        self.cls.h_instance = winapi.get_module_handle(None)
        self.cls.h_icon = 0
        self.cls.h_cursor = 0
        self.cls.hbr_background = winapi.get_stock_object(types.StockBrush.WHITE)
        self.cls.lpsz_menu_name = None
        self.cls.lpsz_class_name = f"{filename}_window_class"
        self.cls.h_icon_sm = 0

        # Register Window Class
        winapi.register_class_ex(self.cls)

        # Create Window
        self.hwnd = winapi.create_window_ex(
            0,
            self.cls.lpsz_class_name,
            filename,
            types.WindowStyle.OVERLAPPED_WINDOW,
            constants.DEFAULT,
            constants.DEFAULT,
            win_w,
            win_h,
            0,
            0,
            self.cls.h_instance,
            None,
        )

    @override
    def show(self):
        winapi.show_window(self.hwnd, types.ShowWindowCommand.SHOW_NORMAL)
        winapi.update_window(self.hwnd)

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
                winapi.invalidate_rect(hwnd, None, True)
                return winapi.def_window_proc(hwnd, msg, wparam, lparam)
            case types.WindowsMessage.PAINT:
                hdc = winapi.begin_paint(hwnd, ps)

                try:
                    self.renderer.paint(hwnd, hdc)
                finally:
                    winapi.end_paint(hwnd, ps)
                return 0
        return winapi.def_window_proc(hwnd, msg, wparam, lparam)
