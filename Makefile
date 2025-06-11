.PHONY: help install dev test lint format clean docker-up docker-down migrate

# Default target
help:
	@echo "Available commands:"
	@echo "  make install     - Install dependencies"
	@echo "  make dev        - Run development servers"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean temporary files"
	@echo "  make docker-up  - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"
	@echo "  make migrate    - Run database migrations"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Run development servers
dev:
	python main.py

# Run API only
api:
	python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Run UI only
ui:
	python -m streamlit run src/ui/app.py

# Run tests
test:
	pytest tests/ -v --cov=src --cov-report=html

# Run linters
lint:
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/

# Format code
format:
	black src/ tests/
	isort src/ tests/

# Clean temporary files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

# Docker commands
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build

docker-logs:
	docker-compose logs -f

# Database migrations
migrate:
	alembic upgrade head

migrate-create:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

# Initialize database
init-db:
	python -c "from src.db.database import init_db; init_db()"

# Create superuser
create-superuser:
	python scripts/create_superuser.py

# UI Documentation
ui-docs:
	python scripts/generate_ui_docs.py

# Visual regression testing  
visual-test:
	python scripts/visual_regression_test.py

# Install UI testing dependencies
install-ui-deps:
	pip install playwright opencv-python
	playwright install chromium