# Visitor Management System

## 📌 Overview
This is a simple **Visitor Management System** built using Flask and SQLite, allowing visitors to sign in and administrators to manage visitor logs.

## 🚀 Features
- Visitor sign-in with name, email, phone, company, and reason for visit.
- Admin dashboard to view and export visitor logs.
- Secure authentication for admin access.
- Data stored in SQLite.
- Dockerized deployment with Nginx as a reverse proxy.

## 🛠️ Installation
### Prerequisites
- Docker & Docker Compose
- Python 3.x

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/visitor-management-system.git
   cd visitor-management-system
   ```
2. Create a `.env` file:
   ```bash
   FLASK_SECRET_KEY=your_secure_key
   ADMIN_USERNAME=your_admin
   ADMIN_PASSWORD=your_secure_password
   ```
3. Build and run with Docker:
   ```bash
   docker-compose up --build -d
   ```
4. Access the app:
   - **Visitor Sign-in:** `http://localhost`
   - **Admin Login:** `http://localhost/admin`

## 🔐 Security Best Practices
- **Use environment variables** instead of hardcoded secrets.
- **Enable HTTPS** with a valid SSL certificate in production.
- **Restrict database access** and use parameterized queries.
- **Improve session security** using Flask-Session.

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

