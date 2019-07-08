import threading
import os

#import win32api
from win32api import GetSystemMetrics as win32api_GetSystemMetrics

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
from win32gui import DestroyWindow as win32gui_DestroyWindow
from win32gui import RegisterWindowMessage as win32gui_RegisterWindowMessage
from win32gui import GetModuleHandle as win32gui_GetModuleHandle
from win32gui import LoadCursor as win32gui_LoadCursor
from win32gui import PumpMessages as win32gui_PumpMessages
from win32gui import NIM_DELETE as win32gui_NIM_DELETE
from win32gui import PostQuitMessage as win32gui_PostQuitMessage
from win32gui import CreatePopupMenu as win32gui_CreatePopupMenu
from win32gui import GetCursorPos as win32gui_GetCursorPos
from win32gui import SetForegroundWindow as win32gui_SetForegroundWindow
from win32gui import TrackPopupMenu as win32gui_TrackPopupMenu
from win32gui import PostMessage as win32gui_PostMessage
from win32gui import InsertMenuItem as win32gui_InsertMenuItem
from win32gui import CreateCompatibleDC as win32gui_CreateCompatibleDC
from win32gui import GetDC as win32gui_GetDC
from win32gui import CreateCompatibleBitmap as win32gui_CreateCompatibleBitmap
from win32gui import SelectObject as win32gui_SelectObject
from win32gui import GetSysColorBrush as win32gui_GetSysColorBrush
from win32gui import FillRect as win32gui_FillRect
from win32gui import DrawIconEx as win32gui_DrawIconEx
from win32gui import DeleteDC as win32gui_DeleteDC
from win32gui import LOWORD as win32gui_LOWORD

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
from win32con import COLOR_WINDOW as win32con_COLOR_WINDOW
from win32con import IDC_ARROW as win32con_IDC_ARROW
from win32con import CS_VREDRAW as win32con_CS_VREDRAW
from win32con import CS_HREDRAW as win32con_CS_HREDRAW
from win32con import WM_COMMAND as win32con_WM_COMMAND
from win32con import WM_LBUTTONDBLCLK as win32con_WM_LBUTTONDBLCLK
from win32con import WM_RBUTTONUP as win32con_WM_RBUTTONUP
from win32con import WM_LBUTTONUP as win32con_WM_LBUTTONUP
from win32con import TPM_LEFTALIGN as win32con_TPM_LEFTALIGN
from win32con import WM_NULL as win32con_WM_NULL
from win32con import SM_CXSMICON as win32con_SM_CXSMICON
from win32con import SM_CYSMICON as win32con_SM_CYSMICON
from win32con import COLOR_MENU as win32con_COLOR_MENU
from win32con import DI_NORMAL as win32con_DI_NORMAL

#import win32gui_struct
from win32gui_struct import PackMENUITEMINFO as win32gui_struct_PackMENUITEMINFO

import itertools
import glob


class SysTrayIco(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]

    FIRST_ID = 1023

    def __init__(self,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None,):
        self.unerrorl = []
        self.unerror = 0

        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        menu_options = menu_options + (('Quit', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id


        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui_RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con_WM_DESTROY: self.destroy,
                       win32con_WM_COMMAND: self.command,
                       win32con_WM_USER+20 : self.notify}
        window_class = win32gui_WNDCLASS()
        hinst = window_class.hInstance = win32gui_GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con_CS_VREDRAW | win32con_CS_HREDRAW
        window_class.hCursor = win32gui_LoadCursor(0, win32con_IDC_ARROW)
        window_class.hbrBackground = win32con_COLOR_WINDOW
        window_class.lpfnWndProc = message_map
        classAtom = win32gui_RegisterClass(window_class)
        style = win32con_WS_OVERLAPPED | win32con_WS_SYSMENU
        self.hwnd = win32gui_CreateWindow(classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con_CW_USEDEFAULT,
                                          win32con_CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        self.notify_id = None


    def start(self):
        win32gui_UpdateWindow(self.hwnd)
        self.refresh_icon()

        win32gui_PumpMessages()

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            else:
                print('Unknown item', option_text, option_icon, option_action)
            self._next_action_id += 1
        return result

    def refresh_icon(self):
        hinst = win32gui_GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con_LR_LOADFROMFILE | win32con_LR_DEFAULTSIZE
            hicon = win32gui_LoadImage(hinst,
                                       self.icon,
                                       win32con_IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:
            print("Can't find icon file - using default.")
            hicon = win32gui_LoadIcon(0, win32con_IDI_APPLICATION)

        if self.notify_id: message = win32gui_NIM_MODIFY
        else: message = win32gui_NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui_NIF_ICON | win32gui_NIF_MESSAGE | win32gui_NIF_TIP,
                          win32con_WM_USER+20,
                          hicon,
                          self.hover_text)
        win32gui_Shell_NotifyIcon(message, self.notify_id)

    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

        self.unerrorl.append(hwnd)
        self.unerrorl.append(msg)
        self.unerrorl.append(wparam)
        self.unerrorl.append(lparam)

    def destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit: self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui_Shell_NotifyIcon(win32gui_NIM_DELETE, nid)
        win32gui_PostQuitMessage(0)

        self.unerrorl.append(hwnd)
        self.unerrorl.append(msg)
        self.unerrorl.append(wparam)
        self.unerrorl.append(lparam)

    def notify(self, hwnd, msg, wparam, lparam):
        self.unerrorl.append(hwnd)
        self.unerrorl.append(msg)
        self.unerrorl.append(wparam)

        if lparam == win32con_WM_LBUTTONDBLCLK:
            self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam==win32con_WM_RBUTTONUP:
            self.show_menu()
        elif lparam==win32con_WM_LBUTTONUP:
            pass
        return True

    def show_menu(self):
        menu = win32gui_CreatePopupMenu()
        self.create_menu(menu, self.menu_options)

        pos = win32gui_GetCursorPos()
        win32gui_SetForegroundWindow(self.hwnd)
        win32gui_TrackPopupMenu(menu,
                                win32con_TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui_PostMessage(self.hwnd, win32con_WM_NULL, 0, 0)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct_PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui_InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui_CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct_PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui_InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        self.unerror += 1
        ico_x = win32api_GetSystemMetrics(win32con_SM_CXSMICON)
        ico_y = win32api_GetSystemMetrics(win32con_SM_CYSMICON)
        hicon = win32gui_LoadImage(0, icon, win32con_IMAGE_ICON, ico_x, ico_y, win32con_LR_LOADFROMFILE)

        hdcBitmap = win32gui_CreateCompatibleDC(0)
        hdcScreen = win32gui_GetDC(0)
        hbm = win32gui_CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui_SelectObject(hdcBitmap, hbm)
        brush = win32gui_GetSysColorBrush(win32con_COLOR_MENU)
        win32gui_FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        win32gui_DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con_DI_NORMAL)
        win32gui_SelectObject(hdcBitmap, hbmOld)
        win32gui_DeleteDC(hdcBitmap)

        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        idt = win32gui_LOWORD(wparam)
        self.execute_menu_option(idt)
        self.unerrorl.append(hwnd)
        self.unerrorl.append(msg)
        self.unerrorl.append(lparam)

    def execute_menu_option(self, idt):
        menu_action = self.menu_actions_by_id[idt]
        if menu_action == self.QUIT:
            win32gui_DestroyWindow(self.hwnd)
        else:
            menu_action(self)

def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, str)


class SysTray(threading.Thread):
    def __init__(self, icon: str, hover_text: str, menu: dict, sub_menu_name1: str=None, sub_menu1: dict=None,
                 sub_menu_name2: str=None, sub_menu2: dict=None,
                 sub_menu_name3: str=None, sub_menu3: dict=None,
                 sub_menu_name4: str=None, sub_menu4: dict=None,
                 sub_menu_name5: str=None, sub_menu5: dict=None, quitFunc=None):
        super().__init__()
        self.End = False
        self.icon = icon
        self.icons = itertools.cycle(glob.glob(self.icon))
        self.hover_text = hover_text

        if quitFunc is None:
            def quitFuncT(sysTrayIcon):
                debug = [sysTrayIcon]
                x = "ss"
                debug.append(x)

            self.quitFunc = quitFuncT
        else:
            self.quitFunc = quitFunc

        menu_options = []
        for x in menu:
            menu_options.append((x, next(self.icons), menu[x]))

        if sub_menu1 is not None:
            sub_menu_list = []
            for x in sub_menu1:
                sub_menu_list.append((x, next(self.icons), sub_menu1[x]))
            menu_options.append((sub_menu_name1, next(self.icons), tuple(sub_menu_list)))

        if sub_menu2 is not None:
            sub_menu_list = []
            for x in sub_menu2:
                sub_menu_list.append((x, next(self.icons), sub_menu2[x]))
            menu_options.append((sub_menu_name2, next(self.icons), tuple(sub_menu_list)))

        if sub_menu3 is not None:
            sub_menu_list = []
            for x in sub_menu3:
                sub_menu_list.append((x, next(self.icons), sub_menu3[x]))
            menu_options.append((sub_menu_name3, next(self.icons), tuple(sub_menu_list)))

        if sub_menu4 is not None:
            sub_menu_list = []
            for x in sub_menu4:
                sub_menu_list.append((x, next(self.icons), sub_menu4[x]))
            menu_options.append((sub_menu_name4, next(self.icons), tuple(sub_menu_list)))

        if sub_menu5 is not None:
            sub_menu_list = []
            for x in sub_menu5:
                sub_menu_list.append((x, next(self.icons), sub_menu5[x]))
            menu_options.append((sub_menu_name5, next(self.icons), tuple(sub_menu_list)))

        self.menu_options = tuple(menu_options)

        self.sysTrayIcon = None

    def run(self):
        self.sysTrayIcon = SysTrayIco(next(self.icons), self.hover_text, self.menu_options, on_quit=self.quitFunc, default_menu_index=1)
        self.sysTrayIcon.start()
        self.End = True

    def end(self): # thread will not end
        self.sysTrayIcon.destroy(None, None, None, None)