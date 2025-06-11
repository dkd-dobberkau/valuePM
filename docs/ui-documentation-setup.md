# Automated UI Documentation Setup

## Overview

This document explains how to set up and use the automated UI documentation system for the Value-Based IT Project Management System. The system automatically generates screenshots, creates documentation, and performs visual regression testing.

## Components

### 1. Screenshot Generation (`scripts/generate_ui_docs.py`)
- Automatically captures comprehensive UI screenshots
- Tests different viewports (desktop, tablet, mobile)
- Generates detailed markdown documentation
- Captures component-specific screenshots

### 2. Visual Regression Testing (`scripts/visual_regression_test.py`)
- Compares UI changes against baseline screenshots
- Detects visual regressions automatically
- Integrates with pytest for CI/CD pipelines
- Creates baseline images for comparison

### 3. CI/CD Integration (`.github/workflows/ui-documentation.yml`)
- Runs on every UI-related code change
- Automatically deploys documentation to GitHub Pages
- Comments on PRs with documentation previews
- Performs visual regression testing

## Quick Start

### Prerequisites

```bash
# Install UI documentation dependencies
make install-ui-deps

# Or manually:
pip install playwright opencv-python
playwright install chromium
```

### Basic Usage

```bash
# Generate UI documentation (with screenshots)
make ui-docs

# Run visual regression tests
make visual-test

# Both commands require the API and UI to be running
make docker-up  # Start all services first
```

### Manual Setup

1. **Start the application:**
   ```bash
   # Option 1: Docker (recommended)
   make docker-up
   
   # Option 2: Local development
   make dev
   ```

2. **Generate documentation:**
   ```bash
   python scripts/generate_ui_docs.py
   ```

3. **View results:**
   - Documentation: `docs/ui/README.md`
   - Screenshots: `docs/ui/screenshots/`

## Features

### Automated Screenshots
- **Login page**: Authentication interface
- **Dashboard**: Portfolio overview with metrics
- **Project details**: Individual project views
- **Create project**: New project form
- **Responsive views**: Desktop, tablet, mobile layouts
- **Components**: Individual UI component screenshots

### Visual Regression Testing
- **Baseline comparison**: Detect UI changes automatically
- **Multi-viewport testing**: Ensure responsive design consistency
- **Component-level testing**: Test individual UI elements
- **CI/CD integration**: Automatic testing on code changes

### Documentation Generation
- **Markdown format**: GitHub-compatible documentation
- **Screenshot embedding**: Automatic image inclusion
- **Feature documentation**: Explain UI capabilities
- **Navigation guide**: User journey documentation

## CI/CD Integration

### GitHub Actions Workflow

The workflow automatically:
1. **Starts services** (PostgreSQL, Redis, API)
2. **Populates test data** for realistic screenshots
3. **Generates screenshots** of all UI components
4. **Creates documentation** with embedded images
5. **Performs visual testing** against baselines
6. **Deploys to GitHub Pages** (main branch only)
7. **Comments on PRs** with preview links

### Triggering Documentation Updates

Documentation is automatically generated when:
- UI code changes (`src/ui/**`)
- API code changes (`src/api/**`)
- Documentation scripts change
- Manual workflow dispatch

### GitHub Pages Deployment

- **Main branch**: Automatically deploys to GitHub Pages
- **PR branches**: Creates artifacts for download
- **URL**: `https://yourusername.github.io/value-pm/ui-docs/`

## Configuration

### Environment Variables

```bash
# API Configuration
API_HOST=localhost          # API hostname
API_PORT=8000              # API port
DATABASE_URL=postgresql://... # Database connection
REDIS_URL=redis://...      # Redis connection

# UI Testing
STREAMLIT_PORT=8501        # Streamlit port
HEADLESS_BROWSER=true      # Run browser in headless mode
SCREENSHOT_TIMEOUT=30000   # Screenshot timeout (ms)
```

### Customizing Screenshots

Edit `scripts/generate_ui_docs.py` to:
- Add new screenshot locations
- Modify viewport sizes
- Include additional UI components
- Customize documentation format

### Visual Testing Configuration

Edit `scripts/visual_regression_test.py` to:
- Add new visual test cases
- Modify comparison thresholds
- Include additional test scenarios
- Configure baseline management

## Best Practices

### Baseline Management
1. **Create baselines** on stable UI versions
2. **Update baselines** when intentional changes are made
3. **Review changes** carefully before updating baselines
4. **Version control** baseline images for tracking

### Screenshot Quality
- **Wait for loading**: Ensure data is loaded before screenshots
- **Consistent data**: Use stable test data for reproducible screenshots
- **Full page capture**: Include scrollable content when relevant
- **Component focus**: Capture individual components for detailed docs

### Documentation Maintenance
- **Regular updates**: Run documentation generation frequently
- **Review content**: Ensure documentation reflects current features
- **Version tagging**: Tag documentation versions with releases
- **User feedback**: Incorporate user suggestions for improvements

## Troubleshooting

### Common Issues

**Playwright installation fails:**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y libnss3 libatk-bridge2.0-0 libgtk-3-0

# Reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install chromium
```

**Streamlit app won't start:**
```bash
# Check port availability
lsof -ti:8501 | xargs kill -9

# Check environment variables
echo $API_HOST $API_PORT

# Start with verbose logging
streamlit run src/ui/app.py --logger.level debug
```

**Screenshots are empty/blank:**
```bash
# Increase wait times in script
# Check if app is fully loaded
# Verify authentication is working
# Test manually in browser first
```

**Visual tests failing:**
```bash
# Clear old baselines
rm -rf tests/visual/baselines/*

# Generate new baselines
python scripts/visual_regression_test.py

# Compare differences manually
# Update baselines if changes are intentional
```

### Debugging Tips

1. **Run locally first**: Test scripts on local machine before CI/CD
2. **Check logs**: Review Streamlit and API logs for errors
3. **Manual verification**: Verify screenshots match expectations
4. **Incremental testing**: Test individual components first
5. **Browser debugging**: Use non-headless mode for debugging

## Advanced Usage

### Custom Documentation Templates

Create custom documentation templates:

```python
# Custom template example
template = """
# {app_name} - UI Documentation

Generated: {timestamp}
Version: {version}

## Screenshots
{screenshot_gallery}

## Features
{feature_list}
"""
```

### Integration with Other Tools

- **Confluence**: Export to Confluence wiki
- **Notion**: Import into Notion pages
- **Slack**: Automated UI update notifications
- **JIRA**: Link documentation to tickets

### Performance Optimization

- **Parallel screenshots**: Capture multiple viewports simultaneously
- **Caching**: Cache unchanged screenshots
- **Incremental updates**: Only update changed components
- **Compression**: Optimize image sizes for faster loading

## Maintenance

### Regular Tasks
- [ ] Update Playwright version monthly
- [ ] Review and update baselines quarterly
- [ ] Check documentation accuracy with releases
- [ ] Monitor CI/CD performance and optimize
- [ ] Update screenshot gallery with new features

### Version Compatibility
- **Playwright**: Keep updated for browser compatibility
- **Streamlit**: Test with new Streamlit versions
- **Python**: Ensure compatibility with Python updates
- **Dependencies**: Regular security and feature updates

---

For questions or issues, please check the [troubleshooting section](#troubleshooting) or create an issue in the repository.