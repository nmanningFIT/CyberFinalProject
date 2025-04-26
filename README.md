
# Campus Security Management System — Cyber Threats Final Project

This project demonstrates **two active confidentiality attacks** and their mitigations using a Flask-based Campus Security Management System.

---

## 🔐 Objective

To safeguard the **Confidentiality** pillar of the CIA Triad by simulating and fixing real-world vulnerabilities:
- 🔓 Insider Threat
- 🔓 Insecure Direct Object Reference (IDOR)

---

## 🔓 Attack 1: Insider Threat

### ❗ Vulnerable Behavior:
- User passwords are stored directly in **plaintext** in the database.
- Anyone with DB access (developer, DBA, attacker) can read and leak credentials.

**Example Table:**
| ID | Username | Password   |
|----|----------|------------|
| 1  | ABC      | welcome123 |
| 2  | jdoe     | manager456 |

### 🔒 Mitigation: Use `bcrypt` for Hashing

- Passwords are hashed with salt using the `bcrypt` library.
- Prevents password disclosure even if DB is compromised.

**During Registration:**
```python
hashed_password = bcrypt.generate_password_hash(pword).decode('utf-8')
```

**During Login:**
```python
bcrypt.check_password_hash(data.pword, pword)
```

**Hashed Result in DB:**
```
$2b$12$XUzVK02azjNV6MszJRVoyumD.1q8/fNARySTjqwGlZ2bZReR30gT6
```

---

## 🔓 Attack 2: IDOR (Broken Access Control)

### ❗ Vulnerable Behavior:
- Route `/manager/<username>` allows any logged-in user to change the URL and view another user's dashboard.

**Example:**
```plaintext
Logged in as ABC → /manager/ABC ✅
Changed URL to /manager/jdoe → Accessed jdoe's data ❌
```

### 🔒 Mitigation: Session-Based Access Control

- Route verifies that the session user matches the resource being accessed.

**Code Fix:**
```python
if session.get("username") != username:
    return render_template("unauthorized.html"), 403
```

- Unauthorized users see a styled error page with no data leakage.

---

## 🚀 How to Run
### 1. **Clone the Repository**

```bash
git clone https://github.com/nmanningFIT/CyberFinalProject.git
cd CyberFinalProject
```

### 2. **Install Docker & Docker Compose**

- [Install Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Compose)

### 3. **Pull the Prebuilt Images**

```bash
docker-compose pull
```

### 4. **Start the Application**

```bash
docker-compose up -d
```

- This will start:
  - MySQL database (with your own local data)
  - Flask app with confidentiality preserved (port 5050)
  - Admin user is created automatically

---
### 5. **Navigate to the url**

  [http://localhost:5050/](http://localhost:5050/)
