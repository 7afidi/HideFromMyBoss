import pyautogui
from screeninfo import get_monitors
import win32gui
import win32con
import time

def get_current_monitor(monitors):
    mouse_x, mouse_y = pyautogui.position()
    for i, m in enumerate(monitors):
        if (m.x <= mouse_x <= m.x + m.width and m.y <= mouse_y <= m.y + m.height):
            return i + 1
    return None

def get_window_monitor(hwnd, monitors):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    for i, m in enumerate(monitors):
        if m.x <= x <= m.x + m.width:
            return i + 1
    return None

hidden_windows = []

def hide_monitor2_windows(monitors):
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            if get_window_monitor(hwnd, monitors) == 2:  # Only hide Monitor 2 windows
                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
                hidden_windows.append(hwnd)
    win32gui.EnumWindows(callback, None)

def show_hidden_windows():
    for hwnd in hidden_windows:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    hidden_windows.clear()

last_monitor = None
monitors = get_monitors()  

while True:
    
    current_monitor = get_current_monitor(monitors)
    if current_monitor != last_monitor:
        if current_monitor == 1:  # When on Monitor 1
            hide_monitor2_windows(monitors)  # Hide Monitor 2 windows
        elif last_monitor == 1:  # When leaving Monitor 1
            show_hidden_windows()  # Show all hidden windows
    last_monitor = current_monitor
    time.sleep(0.1)  