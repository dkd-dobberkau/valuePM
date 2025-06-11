#!/usr/bin/env python3
"""Automated UI Documentation Generator for Value-PM Streamlit App"""

import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class StreamlitUIDocGenerator:
    """Generate comprehensive UI documentation with screenshots"""
    
    def __init__(self, app_path="src/ui/app.py", base_url="http://localhost:8501", use_existing_app=True):
        self.app_path = app_path
        self.base_url = base_url
        self.use_existing_app = use_existing_app
        self.docs_dir = Path("docs/ui")
        self.screenshots_dir = self.docs_dir / "screenshots"
        self.streamlit_process = None
        
        # Create directories
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
    
    def start_streamlit_app(self):
        """Start Streamlit app in background or use existing one"""
        if self.use_existing_app:
            print("🔗 Using existing Streamlit app...")
            # Check if app is accessible
            try:
                import requests
                response = requests.get(self.base_url, timeout=5)
                if response.status_code == 200:
                    print("✅ Existing Streamlit app is accessible")
                    return
                else:
                    print("⚠️ Existing app not responding, will try to start new one")
                    self.use_existing_app = False
            except Exception as e:
                print(f"⚠️ Cannot reach existing app: {e}, will try to start new one")
                self.use_existing_app = False
        
        if not self.use_existing_app:
            print("🚀 Starting new Streamlit app...")
            
            # Set environment variables for Docker compatibility
            env = os.environ.copy()
            env['API_HOST'] = 'localhost'
            env['API_PORT'] = '8000'
            
            self.streamlit_process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", self.app_path, 
                 "--server.port", "8501", "--server.headless", "true"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )
            
            # Wait for app to start
            print("⏳ Waiting for app to initialize...")
            time.sleep(15)
            
            # Check if process is still running
            if self.streamlit_process.poll() is not None:
                stdout, stderr = self.streamlit_process.communicate()
                raise Exception(f"Streamlit failed to start: {stderr.decode()}")
    
    def capture_screenshots(self):
        """Generate comprehensive screenshots"""
        print("📸 Capturing screenshots...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                # Navigate to app
                page.goto(self.base_url)
                
                # Wait for Streamlit to load
                page.wait_for_selector('[data-testid="stApp"]', timeout=30000)
                print("✅ Streamlit app loaded successfully")
                
                # 1. Login page screenshot
                self._capture_login_page(page)
                
                # 2. Login with demo credentials
                self._perform_login(page)
                
                # 3. Dashboard screenshots
                self._capture_dashboard(page)
                
                # 4. Project detail screenshots
                self._capture_project_details(page)
                
                # 5. Create project screenshots
                self._capture_create_project(page)
                
                # 6. Responsive screenshots
                self._capture_responsive_views(page)
                
            except Exception as e:
                print(f"❌ Screenshot capture failed: {e}")
                raise
            finally:
                browser.close()
    
    def _capture_login_page(self, page):
        """Capture login page"""
        print("📷 Capturing login page...")
        
        # Clear any existing session state to ensure we see the login page
        page.evaluate("""
            // Clear localStorage and sessionStorage
            localStorage.clear();
            sessionStorage.clear();
            
            // Clear cookies
            document.cookie.split(";").forEach(function(c) { 
                document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); 
            });
        """)
        
        # Reload page to show login
        page.reload()
        page.wait_for_load_state('networkidle')
        
        # Wait for Streamlit to fully render and show login form
        import time
        time.sleep(3)
        
        # Try to wait for login form elements
        try:
            page.wait_for_selector('input[type="text"], input[type="password"], button:has-text("Login")', timeout=5000)
            print("✅ Login form detected")
        except:
            print("⚠️ Login form not detected, taking screenshot anyway")
        
        page.screenshot(
            path=self.screenshots_dir / "01_login_page.png",
            full_page=True
        )
    
    def _perform_login(self, page):
        """Login to the application"""
        print("🔐 Logging in...")
        try:
            # Fill login form (assuming demo credentials)
            page.fill('input[type="text"]', 'admin')
            page.fill('input[type="password"]', 'admin123')
            page.click('button:has-text("Login")')
            
            # Wait for dashboard to load
            page.wait_for_selector('[data-testid="stApp"]', timeout=10000)
            time.sleep(3)  # Additional wait for data to load
            
        except Exception as e:
            print(f"⚠️ Login failed, continuing with unauthenticated screenshots: {e}")
    
    def _capture_dashboard(self, page):
        """Capture dashboard views"""
        print("📊 Capturing dashboard...")
        
        # Full dashboard
        page.screenshot(
            path=self.screenshots_dir / "02_dashboard_overview.png",
            full_page=True
        )
        
        # Portfolio metrics (top section)
        if page.locator('[data-testid="metric-container"]').count() > 0:
            page.locator('[data-testid="metric-container"]').first.screenshot(
                path=self.screenshots_dir / "03_portfolio_metrics.png"
            )
        
        # Charts section
        if page.locator('[data-testid="stPlotlyChart"]').count() > 0:
            page.locator('[data-testid="stPlotlyChart"]').first.screenshot(
                path=self.screenshots_dir / "04_portfolio_charts.png"
            )
        
        # Projects table
        if page.locator('[data-testid="stDataFrame"]').count() > 0:
            page.locator('[data-testid="stDataFrame"]').first.screenshot(
                path=self.screenshots_dir / "05_projects_table.png"
            )
    
    def _capture_project_details(self, page):
        """Capture project detail page"""
        print("📋 Capturing project details...")
        
        # Click on first project in sidebar (if available)
        try:
            # Look for project buttons in sidebar
            project_buttons = page.locator('[data-testid="stSidebar"] button:has-text("📁")')
            if project_buttons.count() > 0:
                project_buttons.first.click()
                time.sleep(3)
                
                # Project detail page
                page.screenshot(
                    path=self.screenshots_dir / "06_project_detail.png",
                    full_page=True
                )
                
                # Metrics progress section
                if page.locator('[data-testid="stProgress"]').count() > 0:
                    page.locator('[data-testid="stProgress"]').first.screenshot(
                        path=self.screenshots_dir / "07_metrics_progress.png"
                    )
                
                # Measurements chart
                if page.locator('[data-testid="stPlotlyChart"]').count() > 0:
                    page.locator('[data-testid="stPlotlyChart"]').first.screenshot(
                        path=self.screenshots_dir / "08_measurements_chart.png"
                    )
        
        except Exception as e:
            print(f"⚠️ Could not capture project details: {e}")
    
    def _capture_create_project(self, page):
        """Capture create project page"""
        print("➕ Capturing create project page...")
        
        try:
            # Click create project button
            create_button = page.locator('button:has-text("Create Project")')
            if create_button.count() > 0:
                create_button.click()
                time.sleep(2)
                
                page.screenshot(
                    path=self.screenshots_dir / "09_create_project.png",
                    full_page=True
                )
        
        except Exception as e:
            print(f"⚠️ Could not capture create project page: {e}")
    
    def _capture_responsive_views(self, page):
        """Capture responsive views"""
        print("📱 Capturing responsive views...")
        
        viewports = [
            {"name": "desktop", "width": 1920, "height": 1080},
            {"name": "tablet", "width": 768, "height": 1024},
            {"name": "mobile", "width": 375, "height": 812}
        ]
        
        for viewport in viewports:
            page.set_viewport_size({
                "width": viewport["width"],
                "height": viewport["height"]
            })
            time.sleep(1)
            
            page.screenshot(
                path=self.screenshots_dir / f"10_{viewport['name']}_view.png",
                full_page=True
            )
    
    def generate_documentation(self):
        """Generate markdown documentation with screenshots"""
        print("📝 Generating documentation...")
        
        # Build screenshot gallery based on existing files
        screenshot_sections = []
        
        # Check which screenshots exist and build sections accordingly
        screenshots = {
            "01_login_page.png": {
                "title": "Login Page",
                "description": "The application requires authentication to access project data and features.",
                "section": "Login & Authentication"
            },
            "02_dashboard_overview.png": {
                "title": "Portfolio Dashboard", 
                "description": "The main dashboard provides an overview of all projects, key metrics, and portfolio performance.",
                "section": "Dashboard Overview"
            },
            "05_projects_table.png": {
                "title": "Projects Table",
                "description": "Detailed table view of all projects with their current status and ROI.",
                "section": "Dashboard Overview"
            },
            "06_project_detail.png": {
                "title": "Project Detail View",
                "description": "Detailed view of individual projects showing metrics progress and recent measurements.",
                "section": "Project Management"
            },
            "07_metrics_progress.png": {
                "title": "Metrics Progress",
                "description": "Visual progress indicators for project value metrics.",
                "section": "Project Management"
            },
            "09_create_project.png": {
                "title": "Create New Project",
                "description": "Form for creating new projects with template-based metric selection.",
                "section": "Project Management"
            },
            "10_desktop_view.png": {
                "title": "Desktop View (1920x1080)",
                "description": "",
                "section": "Responsive Design"
            },
            "10_tablet_view.png": {
                "title": "Tablet View (768x1024)",
                "description": "",
                "section": "Responsive Design"
            },
            "10_mobile_view.png": {
                "title": "Mobile View (375x812)",
                "description": "",
                "section": "Responsive Design"
            }
        }
        
        # Build documentation content
        doc_content = f"""# ValuePM - UI Documentation

*Generated automatically on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Overview

This documentation provides a visual walkthrough of ValuePM's user interface - a Value-Based Project Management System.

"""
        
        # Group screenshots by section
        sections = {}
        for filename, info in screenshots.items():
            screenshot_path = self.screenshots_dir / filename
            if screenshot_path.exists():
                if info["section"] not in sections:
                    sections[info["section"]] = []
                sections[info["section"]].append((filename, info))
        
        # Generate sections
        for section_name, items in sections.items():
            doc_content += f"## {section_name}\n\n"
            
            for filename, info in items:
                if info["description"]:
                    doc_content += f"### {info['title']}\n{info['description']}\n\n"
                else:
                    doc_content += f"### {info['title']}\n"
                doc_content += f"![{info['title']}](screenshots/{filename})\n\n"
        
        # Add features and technical info
        doc_content += """## Features Demonstrated

### ✅ Completed Features
- User authentication and session management
- Portfolio overview with key metrics
- Project creation with template system
- Real-time ROI calculations
- Interactive charts and visualizations
- Measurement recording and tracking
- Responsive design for all devices

### 🚀 Key Capabilities
- **Value-Based Tracking**: Focus on business value rather than traditional project metrics
- **Template System**: Pre-configured metrics for Infrastructure, Software Development, and Digital Transformation projects
- **Real-time Dashboards**: Live updates of project progress and ROI
- **Interactive Charts**: Plotly-based visualizations for trend analysis
- **Measurement History**: Track value metrics over time with confidence levels

## Navigation

The application uses a sidebar navigation with the following sections:
- **Dashboard**: Portfolio overview and key metrics
- **Create Project**: Add new projects to the portfolio
- **Project List**: Quick access to individual project details
- **User Management**: Login/logout functionality

## Technical Implementation

- **Frontend**: Streamlit with custom styling
- **Charts**: Plotly for interactive visualizations
- **Authentication**: JWT-based session management
- **API Integration**: RESTful API calls to backend services
- **Responsive Design**: CSS Grid and Flexbox layouts

---

*This documentation is automatically generated as part of the CI/CD pipeline to ensure it stays current with the latest UI changes.*
"""
        
        # Write documentation
        with open(self.docs_dir / "README.md", "w") as f:
            f.write(doc_content)
        
        print(f"✅ Documentation written to {self.docs_dir / 'README.md'}")
        
        # Report which screenshots were included/missing
        total_expected = len(screenshots)
        total_found = len([f for f in screenshots.keys() if (self.screenshots_dir / f).exists()])
        print(f"📊 Screenshots: {total_found}/{total_expected} found and included in documentation")
    
    def cleanup(self):
        """Stop Streamlit process"""
        if self.streamlit_process and not self.use_existing_app:
            print("🛑 Stopping Streamlit app...")
            self.streamlit_process.terminate()
            try:
                self.streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.streamlit_process.kill()
        elif self.use_existing_app:
            print("✅ Leaving existing Streamlit app running")
    
    def run(self):
        """Execute full documentation generation pipeline"""
        try:
            self.start_streamlit_app()
            self.capture_screenshots()
            self.generate_documentation()
            print("🎉 UI documentation generation completed successfully!")
            
        except KeyboardInterrupt:
            print("\n⚠️ Documentation generation interrupted by user")
        except Exception as e:
            print(f"❌ Documentation generation failed: {e}")
            raise
        finally:
            self.cleanup()


def main():
    """Main entry point"""
    print("🎬 Starting automated UI documentation generation...")
    print("=" * 60)
    
    # Check if Playwright is installed
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright not installed. Run: pip install playwright && playwright install")
        sys.exit(1)
    
    generator = StreamlitUIDocGenerator()
    generator.run()


if __name__ == "__main__":
    main()