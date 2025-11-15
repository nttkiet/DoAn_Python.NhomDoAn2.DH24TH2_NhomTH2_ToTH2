# utils.py-Hàm canh giữa cửa sổ
import tkinter as tk
def center_window(win, w=800, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")
