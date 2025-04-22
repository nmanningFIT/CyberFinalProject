# 🔒 CYB5272 Final Project

## 📖 Project Description

This repository contains a Flask-based web application with MySQL integration, designed as a collaborative platform for implementing and demonstrating the CIA (Confidentiality, Integrity, Availability) triad of information security. The project is structured to support multiple user roles and is fully containerized for easy setup and consistent development environments.

**Key Features:**
- **Multiple User Roles:** Managers and Security personnel with distinct access levels
- **MySQL Database:** All data is managed via a backend database, automatically initialized
- **Dockerized Environment:** Ensures all contributors have the same setup
- **Security Framework:** Ready for CIA triad security implementations

---

## 🚀 Quick Start

### 1. **Clone and Setup**

```bash
# Clone the repository
git clone https://github.com/nmanningFIT/CyberFinalProject.git
cd CyberFinalProject

# Switch to baseline branch
git checkout main-baseline
```

### 2. **Install Docker & Docker Compose**

- [Install Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Compose)

### 3. **Start the Application**

```bash
docker-compose up -d
```

This will start:
- MySQL database (with your own local data)
- Flask application (port 5000)
- Database initialization service

### 4. **Access the Application**

- Web Application: [http://localhost:5000](http://localhost:5000)

**Default credentials:**
- Username: `ABC`
- Password: `00000`

---

## 🔐 Team Development

### CIA Triad Implementation
Team members will each focus on one aspect of the CIA security triad:

1. **Confidentiality**
   - Secure data transmission
   - Access control implementation
   - Session management
   - Data encryption

2. **Integrity**
   - Input validation
   - Data verification
   - Audit logging
   - Error handling

3. **Availability**
   - Rate limiting
   - Load balancing
   - Failover mechanisms
   - Error recovery

### Development Workflow
1. Create your feature branch:
```bash
git checkout -b feature/[cia-aspect]-improvements
# Example: git checkout -b feature/confidentiality-improvements
```

2. Make and test your changes
3. Submit a pull request for review

---

## 🛠️ Development Tips

### Making Changes
- All source code is mounted into containers
- Changes apply instantly (Flask debug mode is on)
- Rebuild if dependencies change:
  ```bash
  docker-compose up --build -d
  ```

### Useful Commands
- View logs:
  ```bash
  docker-compose logs -f
  ```
- Reset database:
  ```bash
  docker-compose down -v
  docker-compose up -d
  ```

### Database Access
- Connect to MySQL shell:
  ```bash
  docker exec -it cyb5272-case-study-db-1 mysql -u root -pexample onlinesystem
  ```
- Common MySQL commands:
  ```sql
  -- List all tables
  SHOW TABLES;
  
  -- View table structure
  DESCRIBE users;
  
  -- Query data
  SELECT * FROM users;
  ```

## 📝 Notes
- Each developer's database is private and local
- Check container logs for troubleshooting
- Run `docker-compose logs -f` to see real-time container output
