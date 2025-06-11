# ValuePM - Value-Based Project Management System

ValuePM is a Python application for managing IT projects based on actual business value delivery rather than traditional scope/time/budget metrics.

## 🎯 Key Features

- **Value-Driven Metrics**: Track cost reduction, revenue increase, efficiency gains, quality improvements
- **Project Templates**: Pre-configured for Infrastructure, Software Development, and Digital Transformation projects
- **Real-time ROI Tracking**: Continuous measurement and dashboard generation
- **Portfolio Management**: Cross-project comparison and resource optimization

## 🏗️ Architecture

```
value-pm/
├── src/
│   ├── core/           # Domain models and business logic
│   ├── api/            # FastAPI REST endpoints
│   ├── ui/             # Streamlit web interface
│   ├── db/             # Database models and migrations
│   ├── services/       # Business services and integrations
│   └── utils/          # Utility functions and helpers
├── tests/              # Unit and integration tests
├── docs/               # Documentation
├── config/             # Configuration files
└── scripts/            # Deployment and utility scripts
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL (for production)
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/dkd-dobberkau/valuePM.git
cd valuePM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the application
python main.py
```

### Running with Docker

```bash
docker-compose up -d
```

## 📊 Usage

### Web Interface

Access the Streamlit dashboard at `http://localhost:8501`

### API

API documentation available at `http://localhost:8000/docs`

### Example: Create a Project

```python
from src.core.project_manager import ValueProjectManager
from src.core.models import ProjectType

pm = ValueProjectManager()
project_id = pm.create_project("Cloud Migration", ProjectType.INFRASTRUCTURE)
```

## 🔧 Configuration

Configuration is managed through environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost/valuepm
API_PORT=8000
UI_PORT=8501
SECRET_KEY=your-secret-key
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test category
pytest tests/unit
pytest tests/integration
```

## 📝 Development Status

- ✅ Phase 1: Core Foundation (Complete)
- 🚧 Phase 2: Data Persistence (In Progress)
- 📅 Phase 3: API Layer
- 📅 Phase 4: Integration Layer
- 📅 Phase 5: User Interface
- 📅 Phase 6: Advanced Analytics

## 🤝 Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.