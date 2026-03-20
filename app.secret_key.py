from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# ✅ ADD HERE
app.secret_key = "lifehub_secret"

def get_db():
    return sqlite3.connect("lifehub.db")