import threading

class SysTray(threading.Thread):
    def __init__(self, icon: str, hover_text: str, menu: dict, sub_menu_name1: str = None, sub_menu1: dict = None,
                 sub_menu_name2: str = None, sub_menu2: dict = None, sub_menu_name3: str = None, sub_menu3: dict = None,
                 sub_menu_name4: str = None, sub_menu4: dict = None, sub_menu_name5: str = None, sub_menu5: dict = None,
                 quitFunc=None):
        super().__init__()

    def run(self):
        pass

    def end(self): # thread will not end
        pass