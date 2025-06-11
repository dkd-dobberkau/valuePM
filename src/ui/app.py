"""Streamlit Web UI for Value-Based IT Project Management"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import requests
from typing import Dict, List, Optional

from src.core.config import settings

# Configure Streamlit
st.set_page_config(
    page_title="ValuePM - Value-Based Project Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
import os
API_HOST = os.getenv('API_HOST', 'localhost')
API_PORT = os.getenv('API_PORT', settings.API_PORT)
API_BASE_URL = f"http://{API_HOST}:{API_PORT}{settings.API_PREFIX}"


class APIClient:
    """Simple API client for the backend"""
    
    def __init__(self):
        self.token = st.session_state.get('token')
        self.headers = {}
        if self.token:
            self.headers['Authorization'] = f"Bearer {self.token}"
    
    def login(self, username: str, password: str) -> bool:
        """Login and get token"""
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state['token'] = data['access_token']
            self.token = data['access_token']
            self.headers['Authorization'] = f"Bearer {self.token}"
            return True
        return False
    
    def get(self, endpoint: str) -> Optional[Dict]:
        """GET request"""
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                st.error("Authentication required. Please login again.")
                if 'token' in st.session_state:
                    del st.session_state['token']
                st.rerun()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to API at {API_BASE_URL}. Please check if the API is running.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
        return None
    
    def post(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """POST request"""
        try:
            response = requests.post(
                f"{API_BASE_URL}{endpoint}",
                json=data,
                headers=self.headers
            )
            if response.status_code in [200, 201]:
                return response.json()
            elif response.status_code == 401:
                st.error("Authentication required. Please login again.")
                if 'token' in st.session_state:
                    del st.session_state['token']
                st.rerun()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to API at {API_BASE_URL}. Please check if the API is running.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
        return None
    
    def put(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """PUT request"""
        try:
            response = requests.put(
                f"{API_BASE_URL}{endpoint}",
                json=data,
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                st.error("Authentication required. Please login again.")
                if 'token' in st.session_state:
                    del st.session_state['token']
                st.rerun()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to API at {API_BASE_URL}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
        return None
    
    def delete(self, endpoint: str) -> bool:
        """DELETE request"""
        try:
            response = requests.delete(f"{API_BASE_URL}{endpoint}", headers=self.headers)
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                st.error("Authentication required. Please login again.")
                if 'token' in st.session_state:
                    del st.session_state['token']
                st.rerun()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to API at {API_BASE_URL}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
        return False


# Initialize API client
api = APIClient()


def login_page():
    """Login page"""
    st.title("🔐 Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if api.login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")


def dashboard_page():
    """Main dashboard page"""
    st.title("📊 ValuePM - Value-Based Project Management")
    
    # Get portfolio overview
    portfolio = api.get("/projects/portfolio/overview")
    if not portfolio:
        st.error("Failed to load portfolio data")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", portfolio['total_projects'])
    
    with col2:
        st.metric("Total Estimated Value", f"${portfolio['total_estimated_value']:,.0f}")
    
    with col3:
        active_projects = portfolio['by_status'].get('active', 0)
        st.metric("Active Projects", active_projects)
    
    with col4:
        total_roi = sum(p['current_roi'] for p in portfolio['projects'])
        st.metric("Total Current ROI", f"${total_roi:,.0f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Projects by type
        if portfolio['by_type']:
            fig_type = px.pie(
                values=list(portfolio['by_type'].values()),
                names=list(portfolio['by_type'].keys()),
                title="Projects by Type"
            )
            st.plotly_chart(fig_type, use_container_width=True)
    
    with col2:
        # Projects by status
        if portfolio['by_status']:
            fig_status = px.bar(
                x=list(portfolio['by_status'].keys()),
                y=list(portfolio['by_status'].values()),
                title="Projects by Status"
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    # Projects table
    st.subheader("Projects Overview")
    if portfolio['projects']:
        df = pd.DataFrame(portfolio['projects'])
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "estimated_value": st.column_config.NumberColumn(
                    "Estimated Value",
                    format="$%.0f"
                ),
                "current_roi": st.column_config.NumberColumn(
                    "Current ROI",
                    format="$%.0f"
                )
            }
        )


def project_detail_page(project_id: str):
    """Project detail page"""
    # Get project data
    project = api.get(f"/projects/{project_id}")
    dashboard = api.get(f"/projects/{project_id}/dashboard")
    
    if not project or not dashboard:
        st.error("Failed to load project data")
        return
    
    st.title(f"📋 {project['name']}")
    
    # Project info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Type", project['project_type'])
    with col2:
        st.metric("Status", project['status'])
    with col3:
        st.metric("Est. Value", f"${project['estimated_total_value']:,.0f}")
    with col4:
        total_roi = sum(dashboard['roi_summary'].values())
        st.metric("Current ROI", f"{total_roi:.1%}")
    
    # Metrics progress
    st.subheader("Metrics Progress")
    
    if dashboard['metrics_summary']:
        metrics_data = []
        for name, data in dashboard['metrics_summary'].items():
            metrics_data.append({
                'Metric': name,
                'Current': data['current'],
                'Target': data['target'],
                'Baseline': data['baseline'],
                'Progress': data['progress_percent']
            })
        
        df_metrics = pd.DataFrame(metrics_data)
        
        # Progress bars
        for _, row in df_metrics.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                current_text = f"{row['Current']:.1f}" if row['Current'] is not None else "No data"
                target_text = f"{row['Target']:.1f}" if row['Target'] is not None else "No target"
                progress_value = min(100, max(0, int(row['Progress']) if row['Progress'] is not None else 0)) / 100
                
                st.progress(
                    progress_value,
                    text=f"{row['Metric']}: {current_text} / {target_text}"
                )
            with col2:
                progress_percent = f"{row['Progress']:.1f}%" if row['Progress'] is not None else "0%"
                st.write(progress_percent)
    
    # Recent measurements chart
    if dashboard['recent_measurements']:
        st.subheader("Recent Measurements")
        
        measurements_df = pd.DataFrame(dashboard['recent_measurements'])
        if not measurements_df.empty:
            measurements_df['date'] = pd.to_datetime(measurements_df['date'])
            
            fig = px.scatter(
                measurements_df,
                x='date',
                y='value',
                color='metric',
                title="Recent Measurements Trend",
                hover_data=['notes']
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Record new measurement
    st.subheader("Record New Measurement")
    
    metrics = api.get(f"/metrics/project/{project_id}")
    if metrics:
        with st.form("measurement_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                metric_names = {m['name']: m['id'] for m in metrics}
                selected_metric = st.selectbox("Metric", list(metric_names.keys()))
                value = st.number_input("Value", step=0.1)
            
            with col2:
                confidence = st.slider("Confidence Level", 0.0, 1.0, 1.0, 0.1)
                notes = st.text_area("Notes")
            
            submit = st.form_submit_button("Record Measurement")
            
            if submit and selected_metric:
                measurement_data = {
                    "metric_id": metric_names[selected_metric],
                    "project_id": project_id,
                    "value": value,
                    "confidence_level": confidence,
                    "notes": notes
                }
                
                if api.post("/measurements/", measurement_data):
                    st.success("Measurement recorded successfully!")
                    st.rerun()
                else:
                    st.error("Failed to record measurement")


def create_project_page():
    """Create new project page"""
    st.title("🆕 Create New Project")
    
    with st.form("create_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Project Name", placeholder="Enter project name")
            project_type = st.selectbox(
                "Project Type",
                ["infrastructure", "software_development", "digital_transformation"]
            )
            start_date = st.date_input("Start Date", value=date.today())
            
        with col2:
            end_date = st.date_input("End Date", value=date.today() + timedelta(days=90))
            estimated_value = st.number_input("Estimated Total Value ($)", min_value=0.0, step=1000.0)
            use_template = st.checkbox("Use Template Metrics", value=True)
        
        business_case = st.text_area("Business Case", placeholder="Describe the business case...")
        
        submit = st.form_submit_button("Create Project", use_container_width=True)
        
        if submit and name:
            project_data = {
                "name": name,
                "project_type": project_type,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "estimated_total_value": estimated_value,
                "business_case": business_case,
                "use_template": use_template,
                "status": "planning"
            }
            
            if api.post("/projects/", project_data):
                st.success("Project created successfully!")
                st.session_state['page'] = 'dashboard'
                st.rerun()
            else:
                st.error("Failed to create project")


def main():
    """Main application"""
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state['page'] = 'dashboard'
    if 'selected_project' not in st.session_state:
        st.session_state['selected_project'] = None
    
    # Debug info (only show in development)
    if st.sidebar.button("🔧 Debug Info"):
        st.sidebar.write(f"API URL: {API_BASE_URL}")
        st.sidebar.write(f"Token exists: {'token' in st.session_state}")
        if 'token' in st.session_state:
            st.sidebar.write("Authenticated: ✅")
        else:
            st.sidebar.write("Authenticated: ❌")
    
    # Check authentication
    if 'token' not in st.session_state:
        login_page()
        return
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()
        
        if st.button("➕ Create Project", use_container_width=True):
            st.session_state['page'] = 'create_project'
            st.rerun()
        
        # Projects list
        st.subheader("Projects")
        try:
            projects = api.get("/projects/")
            if projects:
                for project in projects:
                    if st.button(f"📁 {project['name']}", key=project['id'], use_container_width=True):
                        st.session_state['page'] = 'project_detail'
                        st.session_state['selected_project'] = project['id']
                        st.rerun()
            else:
                st.write("No projects found or failed to load projects")
        except Exception as e:
            st.write(f"Error loading projects: {e}")
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # Main content
    if st.session_state['page'] == 'dashboard':
        dashboard_page()
    elif st.session_state['page'] == 'project_detail' and st.session_state['selected_project']:
        project_detail_page(st.session_state['selected_project'])
    elif st.session_state['page'] == 'create_project':
        create_project_page()


if __name__ == "__main__":
    main()