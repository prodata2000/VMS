# Visitor Management System

## 📌 Overview
This project is a simple **Visitor Management System** built using Flask and SQLite. It allows visitors to sign in and administrators to manage visitor logs. This project was designed to run in a closed network. It does not have robust security as it was never designed to touch the open internet.

## 🚀 Features
- Visitor sign-in form with name, email, phone, company, reason for visit, and badge number.
- Visitor sign-out functionality.
- Admin dashboard for managing and exporting visitor logs.
- CSV export functionality for visitor data.
- Session-based admin authentication with password hashing.
- Simple SQLite database for data storage.
- Dockerized deployment with Nginx as a reverse proxy.

## 🛠️ Installation
### Prerequisites
- Docker & Docker Compose
- Python 3.x

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/prodata2000/VMS.git
   cd VMS
   ```
2. Create a `.env` file in the root directory with the following content:
   ```env
   SECRET_KEY=super_secure_secret_key
   ADMIN_PASSWORD=SUPER_SECRET_PASSWORD
   ```
3. Build and run with Docker:
   ```bash
   docker-compose up --build -d
   ```
4. Access the app:
   - **Visitor Sign-In:** `http://localhost`
   - **Admin Login:** `http://localhost/admin`

## 📂 Project Structure
```
VMS/
│── app.py                 # Main Flask application
│── requirements.txt       # Python dependenciefrom flask import Flask, request, render_template, redirect, url_for, send_file, session, flash
import sqlite3
from datetime import datetime
import csv
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_s
│── Dockerfile             # Docker configuration
│── docker-compose.yml     # Docker Compose setup
│── nginx/                 # Nginx configuration
│   │── nginx.conf         # Nginx reverse proxy configuration
│   │── certs/             # SSL certificates
│── templates/             # HTML templates
│   │── form.html          # Visitor sign-in form
│   │── thank_you.html     # Thank-you page
│   │── admin_login.html   # Admin login page
│   │── admin_dashboard.html # Admin dashboard
│   │── sign_out.html      # Visitor sign-out form
```

## 🔐 Security Considerations
- SQLite is used for simplicity but lacks robust security features.
- HTTPS is not enforced; use Nginx with a proper SSL certificate in production.

## 🌐 Enabling HTTPS with a Self-Signed Certificate
If you want to use HTTPS with Nginx in a local environment, you can generate a self-signed SSL certificate:

1. **Generate the SSL certificate and key:**
   ```bash
   mkdir -p nginx/certs
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/certs/selfsigned.key -out nginx/certs/selfsigned.crt
   ```
   Follow the prompts and enter appropriate values.

2. **Modify `nginx.conf` to use SSL:**
   ```nginx
   server {
       listen 443 ssl;
       server_name _;
       ssl_certificate /etc/ssl/certs/selfsigned.crt;
       ssl_certificate_key /etc/ssl/private/selfsigned.key;
       location / {
           proxy_pass http://vms_app:5002;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Restart the Nginx container:**
   ```bash
   docker-compose restart nginx
   ```

Now, you can access the application via `https://localhost`.

## 🤝 Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b new-feature`
3. Commit changes and push: `git push origin new-feature`
4. Submit a pull request.

## 📜 License
This project is licensed under the MIT License.

---
### 📩 Need Help?
For issues and feature requests, open a GitHub issue or contact the maintainer.
