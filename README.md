<div align="center">

# 🖥️ ObserveX-Agent

### Windows Endpoint Agent for the ObserveX Platform

Secure • Lightweight • Intelligent • Real-Time

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python)
![Windows](https://img.shields.io/badge/Windows-10%2F11-blue?style=for-the-badge&logo=windows)
![GitHub](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

</div>

---

# 📖 Overview

ObserveX-Agent is the Windows endpoint component of the ObserveX platform.

It runs on employee computers to collect device information, monitor system activity, capture screenshots, track browser usage, and securely communicate with the ObserveX server.

The agent is designed to run silently in the background while consuming minimal system resources.

---

# 🚀 Features

## 🖥️ Device Registration

- Automatic device registration
- Hardware information collection
- Operating system detection
- IP & Hostname detection
- Device identification

---

## 👤 Employee Monitoring

- Employee identification
- Device assignment
- Session tracking
- Online / Offline status

---

## 📸 Screenshot Monitoring

- Automatic screenshot capture
- Scheduled screenshots
- Secure upload to server

---

## 🌐 Browser Monitoring

- Website activity logging
- Browser extension integration
- Browsing history collection
- Active tab detection

---

## ⚙️ System Monitoring

- Running applications
- Active window detection
- Keyboard & mouse activity
- Idle time detection

---

## 🔗 Server Communication

- REST API communication
- Device heartbeat
- Secure authentication
- Automatic synchronization

---

# 🏗️ Architecture

```
Employee Computer
        │
        ▼
 ObserveX-Agent
        │
 ├── Device Module
 ├── Browser Module
 ├── Screenshot Module
 ├── Activity Module
 ├── Storage Module
 └── API Client
        │
        ▼
 ObserveX Server
        │
        ▼
 Django Dashboard
```

---

# 📂 Project Structure

```
ObserveX-Agent/

├── agent_activity/
├── client/
├── device/
├── extensions/
├── installer/
├── installers/
├── main/
├── service/
├── storage/
├── utils/
├── config.py
├── main.py
├── service.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/sameer2675/ObserveX-Agent.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the agent

```bash
python main.py
```

Install as Windows Service

```bash
python service.py
```

---

# 🔒 Security

- Secure communication with the ObserveX server
- Device authentication
- Configurable monitoring modules
- Background Windows service

---

# 🛣️ Roadmap

- AI productivity analysis
- USB monitoring
- File activity tracking
- Network monitoring
- Remote updates
- Self-healing service
- Performance optimization
- Encrypted local storage

---

# 🤝 Contributing

This project is currently under active development.

---

# 👨‍💻 Developer

**Sameer Raza**

GitHub: https://github.com/sameer2675