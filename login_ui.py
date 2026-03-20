from tkinter import *
from tkinter import ttk, messagebox
from database import cursor, conn
def show_login(parent_frame):
    from ui.dashboard_ui import show_dashboard
    for widget in parent_frame.winfo_children():
        widget.destroy()
    frame = parent_frame  # reuse the same frame

    ttk.Label(frame, text="LifeHub", font=("Arial", 20, "bold")).pack(pady=20)

    ttk.Label(frame, text="Username").pack(anchor="w")
    username_entry = ttk.Entry(frame, width=30)
    username_entry.pack(pady=5)

    ttk.Label(frame, text="Password").pack(anchor="w")
    password_entry = ttk.Entry(frame, show="*", width=30)
    password_entry.pack(pady=5)

    def signup():
        u = username_entry.get()
        p = password_entry.get()
        if not u or not p:
            messagebox.showerror("Error", "Fill all fields")
            return
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
            conn.commit()
            messagebox.showinfo("Success", "User registered")
        except:
            messagebox.showerror("Error", "Username already exists")

    def login():
        from ui.dashboard_ui import show_dashboard
        u = username_entry.get()
        p = password_entry.get()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
        user = cursor.fetchone()
        if user:
            show_dashboard(u)  # Pass logged-in username
        else:
            messagebox.showerror("Error", "Invalid login")

    ttk.Button(frame, text="Login", command=login).pack(pady=10)
    ttk.Button(frame, text="Signup", command=signup).pack()