# list_windows.py
import win32gui

def enum_handler(hwnd, results):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            results.append(title)

def list_all_windows():
    windows = []
    win32gui.EnumWindows(enum_handler, windows)
    return windows

if __name__ == "__main__":
    windows = list_all_windows()
    print("Active Windows:")
    for w in windows:
        print(w)
