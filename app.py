from flask import Flask, request, render_template, redirect, url_for, send_file, session, flash
import sqlite3
from datetime import datetime
import csv
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DATABASE = 'visitors.db'

logging.basicConfig(level=logging.INFO)

# Database initialization
def init_db():
    logging.info("Initializing database...")
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
            checkin_time TEXT,
            checkout_time TEXT,
            badge_number TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("Database initialized.")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        company = request.form.get("company")
        person_to_meet = request.form.get("person_to_meet")
        reason = request.form.get("reason")
        badge_number = request.form.get("badge_number")
        checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO visitors (name, email, phone, company, person_to_meet, reason, checkin_time, badge_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, email, phone, company, person_to_meet, reason, checkin_time, badge_number)
        )
        conn.commit()
        conn.close()

        flash("Sign-in successful! Thank you for visiting.")
        return redirect(url_for('thank_you'))

    return render_template("form.html")

@app.route("/sign-out", methods=["GET", "POST"])
def sign_out():
    if request.method == "POST":
        visitor_id = request.form.get("visitor_id")
        checkout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE visitors SET checkout_time = ? WHERE id = ?",
            (checkout_time, visitor_id)
        )
        conn.commit()
        conn.close()

        flash("Sign-out successful! Thank you for visiting.")
        return redirect(url_for('sign_out'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM visitors WHERE checkout_time IS NULL")
    signed_in_visitors = cursor.fetchall()
    conn.close()
    return render_template("sign_out.html", visitors=signed_in_visitors)

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

admin_password_hash = generate_password_hash(os.getenv("ADMIN_PASSWORD"))

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and check_password_hash(admin_password_hash, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid credentials. Please try again.")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM visitors")
    visitors = cursor.fetchall()
    conn.close()
    return render_template("admin_dashboard.html", visitors=visitors)

@app.route("/admin/export")
def export_data():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM visitors")
    rows = cursor.fetchall()
    conn.close()

    csv_file = "visitor_data.csv"
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Email", "Phone", "Company", "Person to Meet", "Reason for Visit", "Check-in Time", "Check-out Time", "Badge Number"])
        writer.writerows(rows)

    return send_file(csv_file, as_attachment=True)

@app.route("/admin/delete", methods=["POST"])
def delete_all():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db_connection()
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

@app.route("/api/previous-visitors", methods=["GET"])
def previous_visitors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT email FROM visitors")
    visitors = cursor.fetchall()
    conn.close()
    return {"visitors": [visitor[0] for visitor in visitors]}

@app.route("/api/visitor-details", methods=["GET"])
def visitor_details():
    email = request.args.get("email")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, phone, company, person_to_meet, reason, badge_number FROM visitors WHERE email = ?", (email,))
    visitor = cursor.fetchone()
    conn.close()
    if visitor:
        return {
            "name": visitor[0],
            "email": visitor[1],
            "phone": visitor[2],
            "company": visitor[3],
            "person_to_meet": visitor[4],
            "reason": visitor[5],
            "badge_number": visitor[6]
        }
    return {}

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5002)
