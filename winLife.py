import win32api
import win32gui
import win32con

winClassName = 'GzyGiDdc1lPE'

hwnd = win32gui.FindWindow(winClassName, None)
rect = win32gui.GetWindowRect(hwnd)

print rect