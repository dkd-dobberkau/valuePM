# Contributing to ValuePM

Thank you for your interest in contributing to ValuePM! This document provides guidelines and information for contributors.

## 🎯 How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality or improvements
- **Code Contributions**: Submit bug fixes, new features, or improvements
- **Documentation**: Improve existing docs or add new documentation
- **Testing**: Add or improve test coverage
- **UI/UX Improvements**: Enhance the user interface and experience

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/valuePM.git
cd valuePM

# Add the original repository as upstream
git remote add upstream https://github.com/dkd-dobberkau/valuePM.git
```

### 2. Set Up Development Environment

#### Option A: Docker (Recommended)
```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose run --rm api alembic upgrade head

# Create superuser
docker-compose run --rm api python scripts/create_superuser.py

# Populate sample data (optional)
docker-compose run --rm api python scripts/populate_sample_data.py
```

#### Option B: Local Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database configuration

# Run migrations
alembic upgrade head

# Start the application
python main.py
```

### 3. Verify Setup

- Web UI: http://localhost:8501
- API Docs: http://localhost:8000/api/v1/docs
- Run tests: `pytest`

## 🛠️ Development Guidelines

### Code Style

We follow these coding standards:

- **Python**: PEP 8 style guide
- **Type Hints**: Use type hints throughout the codebase
- **Docstrings**: Write comprehensive docstrings for functions and classes
- **Comments**: Explain complex logic and business rules

#### Code Formatting Tools

```bash
# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/
```

### Project Structure

Maintain the existing project structure:

```
src/
├── api/            # FastAPI REST endpoints
├── core/           # Domain models and enums
├── db/             # Database models and configuration
├── services/       # Business logic services
├── ui/             # Streamlit web interface
└── utils/          # Utility functions
```

### Security Guidelines

- **Never commit secrets**: Use environment variables for sensitive data
- **Input validation**: Validate all user inputs on both client and server
- **SQL injection prevention**: Use parameterized queries
- **Authentication**: Protect sensitive endpoints with proper authentication
- **HTTPS**: Use HTTPS in production environments

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_projects.py

# Run tests in Docker
docker-compose run --rm api pytest
```

### Writing Tests

- Write unit tests for all new functionality
- Include integration tests for API endpoints
- Test error conditions and edge cases
- Maintain test coverage above 80%

Example test structure:
```python
def test_create_project():
    """Test project creation with valid data."""
    # Arrange
    project_data = {...}
    
    # Act
    result = service.create_project(project_data)
    
    # Assert
    assert result.name == project_data['name']
    assert result.status == 'planning'
```

## 📝 Documentation

### Types of Documentation

- **Code Documentation**: Docstrings and inline comments
- **API Documentation**: OpenAPI/Swagger (auto-generated)
- **User Documentation**: README, QUICKSTART, and guides
- **Architecture Documentation**: System design and decisions

### Documentation Standards

- Use clear, concise language
- Include examples and code snippets
- Keep documentation up-to-date with code changes
- Use markdown formatting consistently

## 🔄 Git Workflow

### Branch Naming

Use descriptive branch names:
- `feature/add-project-templates`
- `bugfix/fix-metric-calculation`
- `docs/update-api-documentation`
- `refactor/improve-database-models`

### Commit Messages

Follow conventional commit format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Examples:
```
feat(api): add project template endpoints
fix(ui): resolve metric display formatting issue
docs(readme): update installation instructions
refactor(services): simplify metric calculation logic
```

### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code following our guidelines
   - Add/update tests as needed
   - Update documentation if required

3. **Test Your Changes**
   ```bash
   # Run tests
   pytest
   
   # Check code style
   black src/ && flake8 src/
   
   # Verify application works
   docker-compose up -d
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat(scope): description of changes"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use descriptive title and description
   - Reference related issues with `Fixes #123`
   - Include screenshots for UI changes
   - Request review from maintainers

### Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New functionality includes tests
- [ ] Documentation updated if needed
- [ ] No merge conflicts with main branch
- [ ] Descriptive commit messages
- [ ] PR description explains changes clearly

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Environment**: OS, Python version, Docker version
- **Steps to reproduce**: Clear, step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Logs**: Relevant error messages or logs

### Feature Requests

For feature requests, please provide:

- **Problem description**: What problem does this solve?
- **Proposed solution**: How would you like it to work?
- **Alternative solutions**: Other approaches considered
- **Use cases**: Who would benefit and how?

## 📋 Development Setup Details

### Environment Variables

Key environment variables for development:

```bash
# Database
DATABASE_URL=postgresql://valuepm:valuepm123@localhost:5432/valuepm

# API
SECRET_KEY=your-secret-key-here
DEBUG=True
API_PREFIX=/api/v1

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

### Adding New Dependencies

1. Add to `requirements.txt`
2. Update `requirements-dev.txt` for development dependencies
3. Rebuild Docker containers: `docker-compose build`

## 🤝 Code Review Guidelines

### For Authors

- Keep PRs focused and reasonably sized
- Write clear descriptions and comments
- Be responsive to feedback
- Update PRs based on review comments

### For Reviewers

- Be constructive and helpful
- Focus on code quality, security, and maintainability
- Test the changes locally when possible
- Approve when satisfied with the changes

## 📚 Additional Resources

- **Project Documentation**: `/docs` directory
- **API Documentation**: http://localhost:8000/api/v1/docs
- **Issues and Discussions**: GitHub Issues and Discussions
- **Python Style Guide**: [PEP 8](https://pep8.org/)
- **FastAPI Documentation**: [FastAPI](https://fastapi.tiangolo.com/)
- **Streamlit Documentation**: [Streamlit](https://streamlit.io/)

## 🆘 Getting Help

If you need help or have questions:

1. **Check existing documentation** in the `/docs` directory
2. **Search existing issues** on GitHub
3. **Create a new issue** with the `question` label
4. **Join discussions** on GitHub Discussions

## 📜 License

By contributing to ValuePM, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for contributing to ValuePM!** 🎉

Your contributions help make value-based project management more accessible and effective for everyone.