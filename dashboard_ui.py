from tkinter import *
from tkinter import ttk, messagebox
from features.tasks import add_task_ui, delete_task_ui, refresh_tasks_ui, edit_task_ui
def show_dashboard(username):
    dashboard = Toplevel()
    dashboard.title(f"LifeHub - {username}")
    dashboard.geometry("500x500")
    dashboard.configure(bg="#1e1e2f")

    ttk.Label(dashboard, text=f"Welcome {username}", font=("Arial", 16, "bold"), background="#1e1e2f", foreground="white").pack(pady=10)

    # Task entry
    task_entry = ttk.Entry(dashboard, width=40)
    task_entry.pack(pady=5)

    # Treeview for tasks
    columns = ("Task", "Status")
    task_tree = ttk.Treeview(dashboard, columns=columns, show="headings")
    task_tree.heading("Task", text="Task")
    task_tree.heading("Status", text="Status")
    task_tree.pack(fill=BOTH, expand=True, pady=10)

    # Buttons frame
    btn_frame = ttk.Frame(dashboard)
    btn_frame.pack(pady=5)

    ttk.Button(btn_frame, text="Add Task", command=lambda: add_task_ui(username, task_entry, task_tree)).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="Edit Task", command=lambda: edit_task_ui(task_tree))
    ttk.Button(btn_frame, text="Delete Task", command=lambda: delete_task_ui(task_tree)).pack(side=LEFT, padx=5)
    ttk.Button(btn_frame, text="Logout", command=dashboard.destroy).pack(side=LEFT, padx=5)

    # Load tasks
    refresh_tasks_ui(username, task_tree)