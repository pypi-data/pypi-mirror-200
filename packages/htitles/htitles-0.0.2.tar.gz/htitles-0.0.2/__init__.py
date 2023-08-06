import win32api 

def htitle(text):
    win32api.SetConsoleTitle(text)