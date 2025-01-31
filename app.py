from flask import Flask, request, render_template, redirect, url_for, send_file, session, flash
import sqlite3
from datetime import datetime
import csv
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_fallback_key")

DATABASE = 'visitors.db'

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            company TEXT,
            person_to_meet TEXT,
            reason TEXT,
            checkin_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        company = request.form.get("company")
        person_to_meet = request.form.get("person_to_meet")
        reason = request.form.get("reason")
        checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO visitors (name, email, phone, company, person_to_meet, reason, checkin_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, email, phone, company, person_to_meet, reason, checkin_time)
        )
        conn.commit()
        conn.close()

        flash("Sign-in successful! Thank you for visiting.")
        return redirect(url_for('thank_you'))

    return render_template("form.html")

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM visitors")
    visitors = cursor.fetchall()
    conn.close()
    return render_template("admin_dashboard.html", visitors=visitors)

@app.route("/admin/export")
def export_data():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM visitors")
    rows = cursor.fetchall()
    conn.close()

    csv_file = "visitor_data.csv"
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Email", "Phone", "Company", "Person to Meet", "Reason for Visit", "Check-in Time"])
        writer.writerows(rows)

    return send_file(csv_file, as_attachment=True)

@app.route("/admin/delete", methods=["POST"])
def delete_all():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM visitors")
    conn.commit()
    conn.close()
    flash("All visitor data has been deleted.")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5002)
