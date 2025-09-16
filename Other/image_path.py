import os, sys

def image_path(filename: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    path = os.path.join(base, filename)
    if not os.path.exists(path):
        path = "Empty"
    
    return path
    