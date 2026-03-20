from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db

app = Flask(__name__)
app.secret_key = "lifehub_secret"

# Initialize DB
init_db()


# -------- DB CONNECTION --------
def get_db():
    conn = sqlite3.connect("lifehub.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------- HOME --------
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["username"] = username
            flash("Login successful ✅")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password ❌")

    return render_template("login.html")


# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            flash("Account created successfully 🎉")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Username already exists ❌")
            return render_template("register.html")

        except Exception as e:
            flash(f"Error: {e}")
            return render_template("register.html")

        finally:
            conn.close()

    # For GET requests
    return render_template("register.html")


# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM tasks
        WHERE username=? AND complete=0
        ORDER BY 
            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
            END,
            due_date ASC
    """, (username,))
    pending_tasks = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM tasks
        WHERE username=? AND complete=1
        ORDER BY due_date DESC
    """, (username,))
    completed_tasks = cursor.fetchall()

    conn.close()

    today = str(date.today())
    upcoming = str(date.today() + timedelta(days=1))

    return render_template(
        "dashboard.html",
        username=username,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        today=today,
        upcoming=upcoming
    )


# -------- ADD TASK --------
@app.route("/add_task", methods=["POST"])
def add_task():
    if "username" not in session:
        return redirect(url_for("login"))

    task = request.form.get("task")
    due_date = request.form.get("due_date")
    category = request.form.get("category", "Personal")
    priority = request.form.get("priority", "Medium")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (username, task, due_date, category, priority, progress, complete)
        VALUES (?, ?, ?, ?, ?, 0, 0)
    """, (session["username"], task, due_date, category, priority))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# -------- UPDATE PROGRESS --------
@app.route("/update_progress", methods=["POST"])
def update_progress():
    task_id = request.form.get("task_id")
    progress = int(request.form.get("progress", 0))

    complete = 1 if progress == 100 else 0

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET progress=?, complete=?
        WHERE id=?
    """, (progress, complete, task_id))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# -------- COMPLETE TASK --------
@app.route("/complete_task", methods=["POST"])
def complete_task():
    task_id = request.form.get("task_id")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET complete=1, progress=100
        WHERE id=?
    """, (task_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# -------- DELETE TASK --------
@app.route("/delete_task", methods=["POST"])
def delete_task():
    task_id = request.form.get("task_id")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)