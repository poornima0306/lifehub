from tkinter import *
from tkinter import ttk
from ui.login_ui import show_login

# -------- WINDOW --------
root = Tk()
root.title("LifeHub")
root.geometry("500x500")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")
style.configure(".", background="#1e1e2f", foreground="white", fieldbackground="#2c2c3e")
style.configure("TButton", background="#4CAF50", foreground="white", padding=6)
style.map("TButton", background=[("active", "#45a049")])

# Global frame
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill=BOTH)

# Start with login
show_login(frame)
root.mainloop()

