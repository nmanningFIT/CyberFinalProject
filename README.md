# Branch: feature/availability-improvements

## Availability Improvements

This branch focuses on enhancing the application's **availability** by implementing and demonstrating security controls that protect against Denial-of-Service (DoS) attacks. The primary feature is the integration of **rate limiting** to ensure the platform remains accessible and resilient under high request loads.

---

### Key Activities in this Branch
- **Rate Limiting:** Integration of rate limiting middleware to defend against Denial-of-Service (DoS) attacks and ensure the application remains accessible under load.
- **Testing & Simulation:** Includes scripts (such as `attack_scripts/rate_limit_test.py`) to simulate attack scenarios and validate the effectiveness of availability controls.
- **Comparison Modes:** Supports running the application with and without rate limiting for direct experimentation.

---

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

## 🧪 Testing

To run the DoS comparison test (optional):

```bash
cd app
python3 attack_scripts/rate_limit_test.py
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

- This repository currently demonstrates availability protections via rate limiting. Use it as a foundation for your own cybersecurity enhancements!
