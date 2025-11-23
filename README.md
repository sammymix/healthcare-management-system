# 🏥 Healthcare Management System

A comprehensive healthcare management system built with PostgreSQL, FastAPI, and Streamlit for managing patient records, appointments, medical history, prescriptions, billing, and inventory.

## 🚀 Features

- **Patient Management**: Complete patient profiles and medical history
- **Appointment Scheduling**: Doctor-patient appointment system  
- **Medical Records**: Secure storage of diagnoses and treatments
- **Prescription Management**: Medication tracking and management
- **Billing System**: Financial transactions and insurance handling
- **Inventory Management**: Medical supplies and drug inventory
- **Analytics Dashboard**: Real-time insights and reporting

## 🛠 Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Streamlit
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git & GitHub

## 📦 Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/sammymix/healthcare-management-system.git
cd healthcare-management-system

# Create virtual environment
python -m venv healthcare_env
source healthcare_env/bin/activate  # Linux/Mac
# healthcare_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up database
python database/init.sql

# Generate mock data
python generate_mock_data.py

# Run the application
python run_dashboard.py
🏃‍♂️ Quick Start
Start Dashboard:

bash
python run_dashboard.py
Access at: http://localhost:8501

Start API Server:

bash
python run_api.py
API Docs: http://localhost:8000/docs

📁 Project Structure
text
healthcare-management/
├── database/           # Database schema and configuration
├── src/               # Source code
│   ├── models/        # SQLAlchemy models
│   ├── crud/          # Database operations
│   ├── api/           # FastAPI endpoints
│   └── ui/            # Streamlit interface
├── tests/             # Test suites
├── docs/              # Documentation
└── scripts/           # Utility scripts
🤝 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Authors
Sammy Mix - sammymix

🙏 Acknowledgments
University Project for Database Systems Course

Inspired by real healthcare management needs
