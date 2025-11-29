# DataProphet Polymer Analysis System  
### A Distributed Web Application for Polymer Processing and Reaction Simulation

---

## 📖 Overview

The **DataProphet Polymer Analysis System** is a robust and scalable **RESTful API** designed for ingesting, processing, and analyzing polymer sequences. It supports advanced search, reaction simulation, and real-time data validation — making it ideal for **research, industrial applications, and distributed data processing workflows**.

This project demonstrates:

- 🔁 REST API design with **FastAPI**
- 🧪 Polymer reaction simulation with **rule-based logic**
- 🔍 Advanced search and filtering capabilities
- 🧩 Modular and testable architecture
- 📊 Data validation and error handling

---

## ⚙️ System Architecture

### 🧩 Components

#### 1. REST API Server
- Built with **FastAPI** for high-performance request handling  
- Provides endpoints for ingestion, retrieval, and reaction simulation  
- Includes **authentication** and **comprehensive input validation**

#### 2. Polymer Service
- Core business logic for polymer reaction detection and processing  
- Implements **case-sensitive polarity rules** for reaction simulation  
- Supports **batch processing** of multiple polymers

#### 3. Database Layer
- Uses **SQLAlchemy ORM** with **SQLite** for data persistence  
- Stores polymer sequences, timestamps, and metadata  
- Enables **efficient querying** with advanced filters

---

## 🚀 Features

- ✅ **Polymer Ingestion** – Securely ingest polymer sequences with timestamps  
- 🔍 **Advanced Search** – Filter by length, substring, and time ranges  
- ⚗️ **Reaction Simulation** – Simulate polymer reactions based on assignment rules  
- 🧪 **Batch Processing** – Handle multiple polymers in a single operation  
- 🛡️ **Data Validation** – Comprehensive input checks and duplicate prevention  
- 📈 **Health Monitoring** – Built-in status checks and logging  
- 🧩 **Modular Design** – Separated concerns for maintainability and testing  

---

## 🛠️ Technical Implementation

### 🔧 Core Components

#### API Endpoints
- `GET /health` – Service status and uptime  
- `POST /polymers` – Ingest new polymer data (API key required)  
- `GET /polymers` – Retrieve polymers with advanced filters  
- `POST /reactor` – Simulate polymer reactions  

#### Polymer Service Methods
- `will_react()` – Determines reactivity between two polymers  
- `react_polymer()` – Processes reactions according to rules  
- `process_multiple_polymers()` – Handles batch operations  

#### Search Filters
- `length_gt` / `length_lt` – Filter by polymer length  
- `substring` – Case-insensitive sequence search  
- `start_time` / `end_time` – Temporal filtering  

---

## ▶️ Getting Started

### ✅ Prerequisites
- Python **3.12+**
- **pip**
- **Git**

---

### 📦 Installation

# Clone the repository
git clone <repository-url>
cd DataProphet

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


---

## ▶️ Running the Application

# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


---

## 🧪 Testing

The system includes **comprehensive test coverage** across all components:

- ✅ **API Endpoint Tests** – Validate HTTP responses and error handling  
- ✅ **Service Logic Tests** – Verify reaction algorithms and processing  
- ✅ **Search Filter Tests** – Ensure advanced filtering works correctly  
- ✅ **Edge Case Tests** – Handle empty inputs, invalid data, and boundaries  
- ✅ **Integration Tests** – End-to-end workflow validation  

---

## 🧠 What I Learned

- REST API Design – Building scalable, documented APIs with FastAPI  
- Business Logic Implementation – Translating reaction rules into reliable code  
- Advanced Filtering – Implementing flexible search capabilities  
- Testing Strategies – Comprehensive coverage across units, integration, and edge cases  
- Error Handling – Graceful failure management and user-friendly responses  
- Modular Architecture – Separating concerns for maintainability and extensibility  

---

## 📊 Project Outcomes

### ✅ Successful Implementation

- Fully functional polymer processing API  
- Advanced search and filtering system  
- Comprehensive test suite with **20+ passing tests**  
- Clean, documented, and maintainable codebase  

---

## 🏆 Technical Achievements

- ✅ **100% test pass rate** across all components  
- 🛡️ Robust error handling and input validation  
- ⚗️ Support for complex reaction simulations  
- 🔍 Flexible querying with multiple filter types  

---

## 🔮 Future Enhancements

- 🌐 Web-based dashboard for polymer visualization  
- 📈 Advanced analytics and reaction trend analysis  
- 🔄 Real-time polymer processing streams  
- 🔐 Enhanced authentication and user management  
- 🗃️ Support for additional database backends  
- 📱 Mobile companion application

## 📑 Project Report
  A detailed report about the project is available in the [`Project_Report.pdf`](https://drive.google.com/file/d/1HXMFmwLuuaTwZM_xc2zbo_aVKooEnDSk/view?usp=drive_link).

