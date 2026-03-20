from tkinter import *
from tkinter import messagebox
from database import cursor, conn
from tkinter import ttk
def add_task_ui(user, task_entry, task_tree):
    task = task_entry.get()
    if not task:
        messagebox.showerror("Error", "Enter a task")
        return
    cursor.execute("INSERT INTO tasks (user, task) VALUES (?, ?)", (user, task))
    conn.commit()
    task_entry.delete(0, END)
    refresh_tasks_ui(user, task_tree)

def refresh_tasks_ui(user, task_tree):
    for item in task_tree.get_children():
        task_tree.delete(item)
    cursor.execute("SELECT id, task, complete FROM tasks WHERE user=?", (user,))
    for tid, task, complete in cursor.fetchall():
        status = "✅" if complete else "❌"
        task_tree.insert("", END, iid=tid, values=(task, status))

def get_selected_task(task_tree):
    selected = task_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a task first")
        return None
    return selected[0]

def delete_task_ui( user, task_tree):
    tid = get_selected_task(task_tree)
    if tid is None: return
    old_task = task_tree.item(tid, "values")[0]
    cursor.execute("DELETE FROM tasks WHERE id=?", (tid,))
    conn.commit()
    refresh_tasks_ui(user, task_tree)

def edit_task_ui(task_tree):
    tid = get_selected_task(task_tree)
    if tid is None: return
    old_task = task_tree.item(tid, "values")[0]

    edit_win = Toplevel()
    edit_win.title("Edit Task")
    edit_win.geometry("300x150")
    edit_win.configure(bg="#2c2c3e")

    ttk.Label(edit_win, text="Edit Task:", background="#2c2c3e", foreground="white").pack(pady=10)
    entry = ttk.Entry(edit_win, width=30)
    entry.pack(pady=5)
    entry.insert(0, old_task)

    def save_edit():
        new_task = entry.get()
        if not new_task:
            messagebox.showerror("Error", "Task cannot be empty")
            return
        cursor.execute("UPDATE tasks SET task=? WHERE id=?", (new_task, tid))
        conn.commit()
        edit_win.destroy()
        refresh_tasks_ui(user, task_tree)
    ttk.Button(edit_win, text="Save", command=save_edit).pack(pady=10)