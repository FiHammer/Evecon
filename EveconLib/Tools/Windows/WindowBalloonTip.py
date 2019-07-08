import os
import sys
import threading

#import win32api
from win32api import GetModuleHandle as win32api_GetModuleHandle
from win32api import PostQuitMessage as win32api_PostQuitMessage

#import win32gui
from win32gui import WNDCLASS as win32gui_WNDCLASS
from win32gui import RegisterClass as win32gui_RegisterClass
from win32gui import CreateWindow as win32gui_CreateWindow
from win32gui import UpdateWindow as win32gui_UpdateWindow
from win32gui import LoadImage as win32gui_LoadImage
from win32gui import LoadIcon as win32gui_LoadIcon
from win32gui import NIF_ICON as win32gui_NIF_ICON
from win32gui import NIF_MESSAGE as win32gui_NIF_MESSAGE
from win32gui import NIF_TIP as win32gui_NIF_TIP
from win32gui import Shell_NotifyIcon as win32gui_Shell_NotifyIcon
from win32gui import NIM_ADD as win32gui_NIM_ADD
from win32gui import NIM_MODIFY as win32gui_NIM_MODIFY
from win32gui import NIF_INFO as win32gui_NIF_INFO
from win32gui import DestroyWindow as win32gui_DestroyWindow
from win32gui import NIM_DELETE as win32gui_NIM_DELETE

#import win32con
from win32con import WM_DESTROY as win32con_WM_DESTROY
from win32con import WS_OVERLAPPED as win32con_WS_OVERLAPPED
from win32con import WS_SYSMENU as win32con_WS_SYSMENU
from win32con import CW_USEDEFAULT as win32con_CW_USEDEFAULT
from win32con import LR_LOADFROMFILE as win32con_LR_LOADFROMFILE
from win32con import LR_DEFAULTSIZE as win32con_LR_DEFAULTSIZE
from win32con import IMAGE_ICON as win32con_IMAGE_ICON
from win32con import IDI_APPLICATION as win32con_IDI_APPLICATION
from win32con import WM_USER as win32con_WM_USER


class WindowsBalloonTipC:
    def __init__(self):
        message_map = {
                win32con_WM_DESTROY: self.OnDestroy,
        }
        wc = win32gui_WNDCLASS()
        self.hinst = wc.hInstance = win32api_GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map
        self.classAtom = win32gui_RegisterClass(wc)
        self.hwnd = None
        self.normList = []
    def ShowWindow(self, title, msg):
        style = win32con_WS_OVERLAPPED | win32con_WS_SYSMENU
        self.hwnd = win32gui_CreateWindow( self.classAtom, "Taskbar", style, 0, 0, win32con_CW_USEDEFAULT, win32con_CW_USEDEFAULT, 0, 0, self.hinst, None)
        win32gui_UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con_LR_LOADFROMFILE | win32con_LR_DEFAULTSIZE
        # noinspection PyBroadException
        try:
           hicon = win32gui_LoadImage(self.hinst, iconPathName, win32con_IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = win32gui_LoadIcon(0, win32con_IDI_APPLICATION)
        flags = win32gui_NIF_ICON | win32gui_NIF_MESSAGE | win32gui_NIF_TIP
        nid = (self.hwnd, 0, flags, win32con_WM_USER+20, hicon, "tooltip")
        win32gui_Shell_NotifyIcon(win32gui_NIM_ADD, nid)
        win32gui_Shell_NotifyIcon(win32gui_NIM_MODIFY, (self.hwnd, 0, win32gui_NIF_INFO, win32con_WM_USER+20, hicon, "Balloon  tooltip", msg, 200, title))
        win32gui_DestroyWindow(self.hwnd)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        self.normList.append(hwnd)
        self.normList.append(msg)
        self.normList.append(wparam)
        self.normList.append(lparam)

        nid = (self.hwnd, 0)
        win32gui_Shell_NotifyIcon(win32gui_NIM_DELETE, nid)
        win32api_PostQuitMessage(0)

WindowsBalloonTip = WindowsBalloonTipC()

def balloon_tip(title, msg):
    class tip(threading.Thread):
        def run(self):
            WindowsBalloonTip.ShowWindow(title, msg)
    tipp = tip()
    tipp.start()