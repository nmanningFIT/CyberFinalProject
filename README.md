# 🐳 Docker-Based Setup & Usage

## 📖 Extended Project Description

This repository is a modular, Dockerized Flask web application designed as a collaborative platform for implementing, testing, and demonstrating cybersecurity controls. The project is structured to support multiple user roles (Employee, Manager, Admin) and is fully containerized for easy setup and consistent development environments.

**Current Focus: Availability-based Security Patch**

As currently implemented, this repository showcases an exploration of **availability-based security controls**. In particular, it demonstrates the use of **rate limiting** to protect the application against Denial-of-Service (DoS) attacks. Two versions of the application are provided:

- **With Rate Limiting:** Demonstrates how availability controls can mitigate DoS attacks and maintain reliable service.
- **Without Rate Limiting:** Serves as a baseline for comparison and experimentation.

**Key Features:**
- **Multiple User Roles:** Employees, Managers, and Admins with distinct access levels.
- **MySQL Database:** All data is managed via a backend database, automatically initialized.
- **Dockerized Environment:** Ensures all contributors have the same setup, eliminating environment-specific bugs.
- **Security Experimentation Platform:** Easily extendable for further patches and security enhancements.

---

> **Note:** Rate limiting is an availability control that helps protect the system from denial-of-service (DoS) attacks by limiting the number of requests a user can make in a given time period.

## 🚀 Quick Start

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
  - Flask app with rate limiting (port 5001)
  - Flask app without rate limiting (port 5002)
  - Admin user is created automatically

### 5. **Access the Apps**

- **Rate-limited version:** [http://localhost:5001](http://localhost:5001)
- **Non-rate-limited version:** [http://localhost:5002](http://localhost:5002)

**Default admin credentials:**
- Username: `admin`
- Password: `admin123`

---

### 🔐 Next Steps for the Team

As you continue developing, use this platform to implement and test additional security patches related to:

- **Confidentiality:** (e.g., encryption, secure sessions, access controls)
- **Integrity:** (e.g., hashing, validation, audit logging)
- **Availability:** (e.g., redundancy, failover mechanisms)
- **Authentication:** (e.g., MFA, password policies, external identity providers)

Each teammate should create a new branch for their patch, document their changes, and submit a pull request for review.

---

## 🧪 Testing

To run the DoS comparison test (optional):

```bash
cd app
python3 postFlood_compare.py
```

---

## 🔄 Resetting Your Database

If you want to start fresh (wipe all data):

```bash
docker-compose down -v
docker-compose up -d
```

---

## 🛠️ Making Code Changes

- All source code is mounted into the containers.
- Edit code in your local editor; changes apply instantly (Flask debug mode is on).
- If you change dependencies, rebuild with:
  ```bash
  docker-compose up --build -d
  ```

---

## 🐳 Useful Docker Commands

- View logs:  
  `docker-compose logs -f`
- Stop everything:  
  `docker-compose down`
- Stop & remove all data:  
  `docker-compose down -v`

---

## 📝 Notes

- Each teammate’s database is private and local.
- This repository currently demonstrates availability protections via rate limiting. Use it as a foundation for your own cybersecurity enhancements!
- If you have issues, check container logs or ask in the team chat!
