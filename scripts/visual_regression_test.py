#!/usr/bin/env python3
"""Visual regression testing for Streamlit UI"""

import os
import sys
import time
import subprocess
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright, expect

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class StreamlitVisualTester:
    """Visual regression testing for Streamlit application"""
    
    def __init__(self, app_path="src/ui/app.py", base_url="http://localhost:8501"):
        self.app_path = app_path
        self.base_url = base_url
        self.test_dir = Path("tests/visual")
        self.screenshots_dir = self.test_dir / "screenshots"
        self.baseline_dir = self.test_dir / "baselines"
        self.streamlit_process = None
        
        # Create directories
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        self.baseline_dir.mkdir(exist_ok=True)
    
    def start_streamlit_app(self):
        """Start Streamlit app for testing"""
        print("🚀 Starting Streamlit app for visual testing...")
        
        env = os.environ.copy()
        env['API_HOST'] = 'localhost'
        env['API_PORT'] = '8000'
        
        self.streamlit_process = subprocess.Popen(
            ["python", "-m", "streamlit", "run", self.app_path, 
             "--server.port", "8501", "--server.headless", "true"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        
        time.sleep(15)  # Wait for app to start
        
        if self.streamlit_process.poll() is not None:
            stdout, stderr = self.streamlit_process.communicate()
            raise Exception(f"Streamlit failed to start: {stderr.decode()}")
    
    def test_login_page_visual(self, page):
        """Test login page visual consistency"""
        page.goto(self.base_url)
        page.wait_for_selector('[data-testid="stApp"]')
        
        # Take screenshot
        screenshot_path = self.screenshots_dir / "login_page.png"
        baseline_path = self.baseline_dir / "login_page.png"
        
        page.screenshot(path=screenshot_path, full_page=True)
        
        # Compare with baseline if it exists
        if baseline_path.exists():
            # Use Playwright's built-in visual comparison
            expect(page).to_have_screenshot("login_page.png")
        else:
            # Create baseline
            screenshot_path.rename(baseline_path)
            print(f"✅ Created baseline: {baseline_path}")
    
    def test_dashboard_visual(self, page):
        """Test dashboard visual consistency"""
        # First login
        self._perform_login(page)
        
        # Navigate to dashboard
        page.wait_for_selector('[data-testid="stApp"]')
        time.sleep(3)  # Wait for data to load
        
        screenshot_path = self.screenshots_dir / "dashboard.png"
        baseline_path = self.baseline_dir / "dashboard.png"
        
        page.screenshot(path=screenshot_path, full_page=True)
        
        if baseline_path.exists():
            expect(page).to_have_screenshot("dashboard.png")
        else:
            screenshot_path.rename(baseline_path)
            print(f"✅ Created baseline: {baseline_path}")
    
    def test_responsive_visual(self, page):
        """Test responsive design visual consistency"""
        self._perform_login(page)
        
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
            
            screenshot_path = self.screenshots_dir / f"responsive_{viewport['name']}.png"
            baseline_path = self.baseline_dir / f"responsive_{viewport['name']}.png"
            
            page.screenshot(path=screenshot_path, full_page=True)
            
            if baseline_path.exists():
                expect(page).to_have_screenshot(f"responsive_{viewport['name']}.png")
            else:
                screenshot_path.rename(baseline_path)
                print(f"✅ Created baseline: {baseline_path}")
    
    def _perform_login(self, page):
        """Helper method to login"""
        try:
            page.fill('input[type="text"]', 'admin')
            page.fill('input[type="password"]', 'admin123')
            page.click('button:has-text("Login")')
            page.wait_for_selector('[data-testid="stApp"]', timeout=10000)
        except Exception as e:
            print(f"⚠️ Login failed: {e}")
    
    def run_visual_tests(self):
        """Run all visual regression tests"""
        print("🔍 Running visual regression tests...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                # Run individual tests
                self.test_login_page_visual(page)
                self.test_dashboard_visual(page)
                self.test_responsive_visual(page)
                
                print("✅ All visual tests completed")
                
            except Exception as e:
                print(f"❌ Visual tests failed: {e}")
                raise
            finally:
                browser.close()
    
    def cleanup(self):
        """Stop Streamlit process"""
        if self.streamlit_process:
            print("🛑 Stopping Streamlit app...")
            self.streamlit_process.terminate()
            try:
                self.streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.streamlit_process.kill()
    
    def run(self):
        """Execute visual regression testing"""
        try:
            self.start_streamlit_app()
            self.run_visual_tests()
            print("🎉 Visual regression testing completed!")
            
        except Exception as e:
            print(f"❌ Visual testing failed: {e}")
            raise
        finally:
            self.cleanup()


# Pytest integration
@pytest.fixture(scope="session")
def streamlit_app():
    """Pytest fixture to start/stop Streamlit app"""
    tester = StreamlitVisualTester()
    tester.start_streamlit_app()
    yield tester.base_url
    tester.cleanup()


def test_login_page_regression(page, streamlit_app):
    """Pytest test for login page visual regression"""
    page.goto(streamlit_app)
    page.wait_for_selector('[data-testid="stApp"]')
    expect(page).to_have_screenshot("login_page_regression.png")


def test_dashboard_regression(page, streamlit_app):
    """Pytest test for dashboard visual regression"""
    page.goto(streamlit_app)
    page.wait_for_selector('[data-testid="stApp"]')
    
    # Login
    page.fill('input[type="text"]', 'admin')
    page.fill('input[type="password"]', 'admin123')
    page.click('button:has-text("Login")')
    page.wait_for_selector('[data-testid="stApp"]')
    time.sleep(3)
    
    expect(page).to_have_screenshot("dashboard_regression.png")


if __name__ == "__main__":
    print("🎬 Starting visual regression testing...")
    print("=" * 60)
    
    tester = StreamlitVisualTester()
    tester.run()