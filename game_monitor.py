# game_monitor.py
import psutil
import win32gui
import re

def is_process_running(process_name):
    """Check if a process with the given name is running."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return True
    return False

def get_window_handle(window_title_pattern):
    """Retrieve the window handle that matches the given regex pattern."""
    def enum_handler(hwnd, result):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if re.match(window_title_pattern, title):
                result.append(hwnd)

    windows = []
    win32gui.EnumWindows(enum_handler, windows)
    if windows:
        return windows[0]  # Return the first matching window
    return None

def is_game_running(game_name, window_title_pattern):
    """Check if the game process is running and its window is active."""
    process_running = is_process_running(game_name)
    window_handle = get_window_handle(window_title_pattern)
    return process_running and window_handle is not None
