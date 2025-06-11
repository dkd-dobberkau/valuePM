# Quick Start Guide

## Prerequisites

- Python 3.9+
- PostgreSQL (or use Docker)
- Git

## Option 1: Local Development

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd value-pm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and update DATABASE_URL
# For local PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/valuepm
```

### 3. Initialize Database

```bash
# Create database (PostgreSQL)
createdb valuepm

# Run migrations
alembic upgrade head

# Create a superuser
python scripts/create_superuser.py
```

### 4. Start the Application

```bash
# Start both API and UI
python main.py

# Or run separately:
# Terminal 1: API
python -m uvicorn src.api.main:app --reload

# Terminal 2: UI
python -m streamlit run src/ui/app.py
```

### 5. Populate Sample Data (Optional)

```bash
# Add sample projects and metrics for demonstration
make populate-sample-data
```

### 6. Access the Application

- Web UI: http://localhost:8501
- API Docs: http://localhost:8000/api/v1/docs

## Option 2: Docker Deployment

### 1. Start with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run database migrations
docker-compose run --rm api alembic upgrade head

# Create superuser
docker-compose run --rm api python scripts/create_superuser.py

# Populate sample data (optional)
docker-compose run --rm api python scripts/populate_sample_data.py
```

### 2. Access Services

- Web UI: http://localhost:8501
- API Docs: http://localhost:8000/api/v1/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 3. Stop Services

```bash
docker-compose down
```

## First Steps

1. **Login**: Use the superuser credentials you created
2. **Create a Project**: Click "Create Project" and fill in the details
3. **Add Metrics**: Projects come with template metrics based on type
4. **Record Measurements**: Track actual values for your metrics
5. **View Dashboard**: Monitor progress and ROI

## Common Commands

```bash
# Using Make
make help          # Show all commands
make dev           # Run development servers
make test          # Run tests
make docker-up     # Start Docker containers
make docker-down   # Stop Docker containers

# Manual commands
pytest             # Run tests
black src/         # Format code
flake8 src/        # Check code style
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `createdb valuepm`

### Port Already in Use
- API port (8000): `lsof -ti:8000 | xargs kill -9`
- UI port (8501): `lsof -ti:8501 | xargs kill -9`

### Docker Issues
- Clean rebuild: `docker-compose down -v && docker-compose up --build`
- Check logs: `docker-compose logs api`

## Next Steps

- Read the full documentation in `/docs`
- Explore the API at http://localhost:8000/api/v1/docs
- Check the architecture diagram in `/docs/architecture.md`
- Review the CLAUDE.md file for project details