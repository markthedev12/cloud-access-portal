# CloudAccess & Identity Self-Service Portal

A full-stack internal developer portal designed to streamline cloud access requests, enforce IAM least-privilege security policies, and automate resource provisioning.

## 🌟 Overview
The CloudAccess Portal is built to bridge the gap between security compliance and developer velocity. Instead of manually handling access requests or spinning up unmonitored cloud resources, team members can use this portal to request access, which triggers automated validation, approval workflows, and backend provisioning.

## 🛠️ Tech Stack
* **Frontend:** React / Next.js
* **Backend:** Python, FastAPI, Uvicorn
* **Database & State:** PostgreSQL, SQLAlchemy
* **Cloud Automation:** AWS Boto3, Terraform

## 📂 Project Structure
```text
cloud-access-portal/
├── backend/          # FastAPI application, API routes, and core business logic
│   └── main.py       # API entry point and health checks
├── database/         # Database schemas, models, and migration scripts
├── docs/             # Project documentation, architecture notes, and guides
├── frontend/         # UI application source code (React / Next.js)
├── docker-compose.yml# Local multi-container development environment setup
├── requirements.txt  # Python backend dependencies
└── README.md         # Project documentation