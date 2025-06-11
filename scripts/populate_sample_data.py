#!/usr/bin/env python3
"""Populate ValuePM database with sample project data"""

import sys
from pathlib import Path
from datetime import datetime, date, timedelta
import uuid

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.database import SessionLocal
from src.db.models import Project, ValueMetric, Measurement
from src.core.enums import ProjectType, ProjectStatus, MetricType, ValueCategory


def populate_sample_data():
    """Create sample projects, metrics, and measurements for demonstration"""
    print("🎯 Populating ValuePM with sample data...")
    
    db = SessionLocal()
    try:
        # Check if sample data already exists
        existing_projects = db.query(Project).count()
        if existing_projects > 0:
            print(f"⚠️ Database already contains {existing_projects} projects. Skipping sample data creation.")
            return
        
        # Sample Projects Data
        projects_data = [
            {
                "id": str(uuid.uuid4()),
                "name": "AWS Cloud Migration",
                "project_type": ProjectType.INFRASTRUCTURE,
                "status": ProjectStatus.ACTIVE,
                "start_date": date.today() - timedelta(days=90),
                "end_date": date.today() + timedelta(days=60),
                "business_case": "Migrate on-premises infrastructure to AWS to reduce operational costs and improve scalability.",
                "estimated_total_value": 200000.0
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Customer Self-Service Portal",
                "project_type": ProjectType.SOFTWARE_DEVELOPMENT,
                "status": ProjectStatus.ACTIVE,
                "start_date": date.today() - timedelta(days=120),
                "end_date": date.today() + timedelta(days=30),
                "business_case": "Develop a self-service portal to reduce customer support costs and improve customer satisfaction.",
                "estimated_total_value": 150000.0
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Invoice Processing Automation",
                "project_type": ProjectType.DIGITAL_TRANSFORMATION,
                "status": ProjectStatus.COMPLETED,
                "start_date": date.today() - timedelta(days=180),
                "end_date": date.today() - timedelta(days=30),
                "business_case": "Automate invoice processing to reduce manual effort and improve accuracy.",
                "estimated_total_value": 75000.0
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Network Infrastructure Upgrade",
                "project_type": ProjectType.INFRASTRUCTURE,
                "status": ProjectStatus.PLANNING,
                "start_date": date.today() + timedelta(days=30),
                "end_date": date.today() + timedelta(days=180),
                "business_case": "Upgrade network infrastructure to support increased bandwidth requirements.",
                "estimated_total_value": 300000.0
            },
            {
                "id": str(uuid.uuid4()),
                "name": "AI Customer Support Chatbot",
                "project_type": ProjectType.SOFTWARE_DEVELOPMENT,
                "status": ProjectStatus.ACTIVE,
                "start_date": date.today() - timedelta(days=60),
                "end_date": date.today() + timedelta(days=90),
                "business_case": "Implement AI-powered chatbot to handle common customer inquiries and reduce support workload.",
                "estimated_total_value": 125000.0
            }
        ]
        
        # Create projects
        created_projects = []
        for project_data in projects_data:
            project = Project(**project_data)
            db.add(project)
            created_projects.append(project)
        
        db.flush()  # Get IDs for projects
        print(f"✅ Created {len(created_projects)} sample projects")
        
        # Sample Metrics Data
        metrics_data = [
            # AWS Cloud Migration metrics
            {
                "project_id": created_projects[0].id,
                "name": "Infrastructure Cost Reduction",
                "description": "Monthly cost savings from cloud migration",
                "metric_type": MetricType.CURRENCY,
                "value_category": ValueCategory.COST_REDUCTION,
                "baseline_value": 50000.0,
                "target_value": 35000.0,
                "measurement_frequency": "monthly",
                "is_active": True
            },
            {
                "project_id": created_projects[0].id,
                "name": "System Availability",
                "description": "Uptime percentage of migrated systems",
                "metric_type": MetricType.PERCENTAGE,
                "value_category": ValueCategory.QUALITY_IMPROVEMENT,
                "baseline_value": 95.0,
                "target_value": 99.5,
                "measurement_frequency": "weekly",
                "is_active": True
            },
            {
                "project_id": created_projects[0].id,
                "name": "Deployment Speed",
                "description": "Time to deploy new applications (hours)",
                "metric_type": MetricType.TIME,
                "value_category": ValueCategory.EFFICIENCY_GAIN,
                "baseline_value": 48.0,
                "target_value": 2.0,
                "measurement_frequency": "per_deployment",
                "is_active": True
            },
            
            # Customer Self-Service Portal metrics
            {
                "project_id": created_projects[1].id,
                "name": "Support Ticket Reduction",
                "description": "Reduction in customer support tickets per month",
                "metric_type": MetricType.COUNT,
                "value_category": ValueCategory.COST_REDUCTION,
                "baseline_value": 1000.0,
                "target_value": 700.0,
                "measurement_frequency": "monthly",
                "is_active": True
            },
            {
                "project_id": created_projects[1].id,
                "name": "Customer Satisfaction Score",
                "description": "Customer satisfaction rating (1-10)",
                "metric_type": MetricType.SCORE,
                "value_category": ValueCategory.USER_SATISFACTION,
                "baseline_value": 6.5,
                "target_value": 8.5,
                "measurement_frequency": "monthly",
                "is_active": True
            },
            {
                "project_id": created_projects[1].id,
                "name": "Self-Service Adoption Rate",
                "description": "Percentage of customers using self-service",
                "metric_type": MetricType.PERCENTAGE,
                "value_category": ValueCategory.USER_SATISFACTION,
                "baseline_value": 20.0,
                "target_value": 75.0,
                "measurement_frequency": "weekly",
                "is_active": True
            },
            
            # Invoice Processing Automation metrics
            {
                "project_id": created_projects[2].id,
                "name": "Processing Time Reduction",
                "description": "Time to process invoice (minutes)",
                "metric_type": MetricType.TIME,
                "value_category": ValueCategory.EFFICIENCY_GAIN,
                "baseline_value": 30.0,
                "target_value": 5.0,
                "measurement_frequency": "daily",
                "is_active": True
            },
            {
                "project_id": created_projects[2].id,
                "name": "Error Rate Reduction",
                "description": "Percentage of invoices with errors",
                "metric_type": MetricType.PERCENTAGE,
                "value_category": ValueCategory.QUALITY_IMPROVEMENT,
                "baseline_value": 8.0,
                "target_value": 1.0,
                "measurement_frequency": "weekly",
                "is_active": True
            },
            {
                "project_id": created_projects[2].id,
                "name": "Staff Cost Savings",
                "description": "Monthly savings from automation",
                "metric_type": MetricType.CURRENCY,
                "value_category": ValueCategory.COST_REDUCTION,
                "baseline_value": 0.0,
                "target_value": 8000.0,
                "measurement_frequency": "monthly",
                "is_active": True
            },
            
            # Network Infrastructure Upgrade metrics
            {
                "project_id": created_projects[3].id,
                "name": "Network Bandwidth",
                "description": "Available network bandwidth (Gbps)",
                "metric_type": MetricType.COUNT,
                "value_category": ValueCategory.QUALITY_IMPROVEMENT,
                "baseline_value": 1.0,
                "target_value": 10.0,
                "measurement_frequency": "weekly",
                "is_active": True
            },
            {
                "project_id": created_projects[3].id,
                "name": "Network Latency",
                "description": "Average network latency (ms)",
                "metric_type": MetricType.TIME,
                "value_category": ValueCategory.QUALITY_IMPROVEMENT,
                "baseline_value": 50.0,
                "target_value": 10.0,
                "measurement_frequency": "daily",
                "is_active": True
            },
            
            # AI Chatbot metrics
            {
                "project_id": created_projects[4].id,
                "name": "Query Resolution Rate",
                "description": "Percentage of queries resolved by chatbot",
                "metric_type": MetricType.PERCENTAGE,
                "value_category": ValueCategory.EFFICIENCY_GAIN,
                "baseline_value": 0.0,
                "target_value": 80.0,
                "measurement_frequency": "daily",
                "is_active": True
            },
            {
                "project_id": created_projects[4].id,
                "name": "Response Time",
                "description": "Average chatbot response time (seconds)",
                "metric_type": MetricType.TIME,
                "value_category": ValueCategory.USER_SATISFACTION,
                "baseline_value": 300.0,
                "target_value": 5.0,
                "measurement_frequency": "daily",
                "is_active": True
            },
            {
                "project_id": created_projects[4].id,
                "name": "Support Cost Savings",
                "description": "Monthly savings from reduced support staff",
                "metric_type": MetricType.CURRENCY,
                "value_category": ValueCategory.COST_REDUCTION,
                "baseline_value": 0.0,
                "target_value": 15000.0,
                "measurement_frequency": "monthly",
                "is_active": True
            }
        ]
        
        # Create metrics
        created_metrics = []
        for metric_data in metrics_data:
            metric = ValueMetric(**metric_data)
            db.add(metric)
            created_metrics.append(metric)
        
        db.flush()  # Get IDs for metrics
        print(f"✅ Created {len(created_metrics)} sample metrics")
        
        # Sample Measurements Data (simulating progress over time)
        measurements_data = []
        
        # Generate measurements for each metric showing progress over time
        for metric in created_metrics:
            # Skip measurements for planning projects
            if metric.project.status == ProjectStatus.PLANNING:
                continue
                
            # Number of measurements based on project status
            if metric.project.status == ProjectStatus.COMPLETED:
                num_measurements = 8
            else:
                num_measurements = 5
            
            # Generate measurements showing gradual progress toward target
            for i in range(num_measurements):
                days_ago = (num_measurements - i - 1) * 14  # Every 2 weeks
                measured_at = datetime.now() - timedelta(days=days_ago)
                
                # Calculate progress (0 to 1) based on measurement index
                progress = (i + 1) / num_measurements
                
                # Calculate value based on progress toward target
                if metric.target_value > metric.baseline_value:
                    # Increasing metric (e.g., satisfaction, availability)
                    value = metric.baseline_value + (metric.target_value - metric.baseline_value) * progress
                else:
                    # Decreasing metric (e.g., cost, time, errors)
                    value = metric.baseline_value - (metric.baseline_value - metric.target_value) * progress
                
                # Add some realistic variation
                import random
                variation = 0.1  # 10% variation
                value = value * (1 + random.uniform(-variation, variation))
                
                # Ensure value doesn't go negative for certain metric types
                if metric.metric_type in [MetricType.PERCENTAGE, MetricType.COUNT]:
                    value = max(0, value)
                
                measurements_data.append({
                    "metric_id": metric.id,
                    "project_id": metric.project_id,
                    "value": round(value, 2),
                    "measured_at": measured_at,
                    "confidence_level": random.uniform(0.8, 1.0),
                    "notes": f"Measurement {i+1} - {'Final' if i == num_measurements-1 else 'Progress'} update"
                })
        
        # Create measurements
        for measurement_data in measurements_data:
            measurement = Measurement(**measurement_data)
            db.add(measurement)
        
        db.commit()
        print(f"✅ Created {len(measurements_data)} sample measurements")
        print(f"🎉 Sample data population complete!")
        
        # Print summary
        print(f"\n📊 Sample Data Summary:")
        print(f"   • {len(created_projects)} Projects")
        print(f"   • {len(created_metrics)} Metrics")
        print(f"   • {len(measurements_data)} Measurements")
        print(f"\n🚀 You can now:")
        print(f"   • Access the UI at http://localhost:8501")
        print(f"   • Login with the superuser credentials")
        print(f"   • Explore the sample projects and their metrics")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error populating sample data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_sample_data()