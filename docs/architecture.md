# System Architecture

## Overview

The Value-Based IT Project Management System follows a layered architecture pattern with clear separation of concerns.

## Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Streamlit Web UI]
        API_CLIENT[API Client]
    end
    
    subgraph "API Layer"
        FASTAPI[FastAPI REST API]
        AUTH[Authentication]
        VALIDATOR[Request Validation]
    end
    
    subgraph "Service Layer"
        PM[Project Manager]
        MS[Measurement Service]
        RS[Reporting Service]
        IS[Integration Service]
    end
    
    subgraph "Core Domain"
        PROJECT[Project]
        METRIC[ValueMetric]
        MEASURE[Measurement]
        STAKE[Stakeholder]
        DELIVER[Deliverable]
    end
    
    subgraph "Data Layer"
        ORM[SQLAlchemy ORM]
        REPO[Repositories]
        MIGRATE[Alembic Migrations]
    end
    
    subgraph "Infrastructure"
        PG[(PostgreSQL)]
        REDIS[(Redis Cache)]
        S3[S3 Storage]
    end
    
    subgraph "External Systems"
        MONITOR[Monitoring Tools]
        ERP[ERP Systems]
        NOTIF[Notification Services]
    end
    
    UI --> API_CLIENT
    API_CLIENT --> FASTAPI
    FASTAPI --> AUTH
    FASTAPI --> VALIDATOR
    FASTAPI --> PM
    FASTAPI --> MS
    FASTAPI --> RS
    
    PM --> PROJECT
    PM --> METRIC
    MS --> MEASURE
    RS --> PROJECT
    RS --> MEASURE
    IS --> MONITOR
    IS --> ERP
    IS --> NOTIF
    
    PROJECT --> REPO
    METRIC --> REPO
    MEASURE --> REPO
    STAKE --> REPO
    DELIVER --> REPO
    
    REPO --> ORM
    ORM --> PG
    MS --> REDIS
    RS --> S3
```

## Component Details

### Frontend Layer
- **Streamlit Web UI**: Interactive dashboard for project management
- **API Client**: HTTP client for REST API communication

### API Layer
- **FastAPI**: High-performance REST API framework
- **Authentication**: JWT-based authentication and authorization
- **Validation**: Pydantic models for request/response validation

### Service Layer
- **Project Manager**: Orchestrates project operations
- **Measurement Service**: Handles metric data collection and storage
- **Reporting Service**: Generates dashboards and reports
- **Integration Service**: Manages external system connections

### Core Domain
- **Project**: Main aggregate root containing project data
- **ValueMetric**: Business value measurement definitions
- **Measurement**: Actual measurement data points
- **Stakeholder**: People interested in project value
- **Deliverable**: Project outputs with value mapping

### Data Layer
- **SQLAlchemy ORM**: Object-relational mapping
- **Repositories**: Data access abstraction
- **Alembic**: Database migration management

### Infrastructure
- **PostgreSQL**: Primary data store
- **Redis**: Caching for performance
- **S3**: File storage for reports and exports

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant API
    participant Service
    participant DB
    
    User->>UI: Create Project
    UI->>API: POST /projects
    API->>Service: create_project()
    Service->>DB: INSERT project
    DB-->>Service: project_id
    Service-->>API: Project created
    API-->>UI: 201 Created
    UI-->>User: Show success
    
    User->>UI: Record Measurement
    UI->>API: POST /measurements
    API->>Service: record_measurement()
    Service->>DB: INSERT measurement
    Service->>Service: Calculate ROI
    Service->>DB: UPDATE project ROI
    DB-->>Service: Success
    Service-->>API: Measurement recorded
    API-->>UI: 201 Created
    UI-->>User: Update dashboard
```

## Security Architecture

```mermaid
graph LR
    subgraph "Security Layers"
        HTTPS[HTTPS/TLS]
        JWT[JWT Tokens]
        RBAC[Role-Based Access]
        ENCRYPT[Data Encryption]
        AUDIT[Audit Logging]
    end
    
    USER[User] --> HTTPS
    HTTPS --> JWT
    JWT --> RBAC
    RBAC --> API[API Access]
    API --> ENCRYPT
    ENCRYPT --> DB[(Database)]
    API --> AUDIT
    AUDIT --> LOG[(Audit Logs)]
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        LB[Load Balancer]
        
        subgraph "Application Tier"
            APP1[App Instance 1]
            APP2[App Instance 2]
            APP3[App Instance 3]
        end
        
        subgraph "Data Tier"
            PG_PRIMARY[(PostgreSQL Primary)]
            PG_REPLICA[(PostgreSQL Replica)]
            REDIS_CLUSTER[(Redis Cluster)]
        end
        
        subgraph "Storage"
            S3[(S3 Bucket)]
        end
    end
    
    subgraph "Monitoring"
        PROMETHEUS[Prometheus]
        GRAFANA[Grafana]
        ALERTS[Alert Manager]
    end
    
    INTERNET[Internet] --> LB
    LB --> APP1
    LB --> APP2
    LB --> APP3
    
    APP1 --> PG_PRIMARY
    APP2 --> PG_PRIMARY
    APP3 --> PG_PRIMARY
    
    PG_PRIMARY --> PG_REPLICA
    
    APP1 --> REDIS_CLUSTER
    APP2 --> REDIS_CLUSTER
    APP3 --> REDIS_CLUSTER
    
    APP1 --> S3
    APP2 --> S3
    APP3 --> S3
    
    APP1 --> PROMETHEUS
    APP2 --> PROMETHEUS
    APP3 --> PROMETHEUS
    
    PROMETHEUS --> GRAFANA
    PROMETHEUS --> ALERTS
```

## Technology Stack

### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery (future)

### Frontend
- **Framework**: Streamlit
- **Charts**: Plotly
- **Styling**: Custom CSS

### Infrastructure
- **Container**: Docker
- **Orchestration**: Kubernetes (production)
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

### Development Tools
- **Testing**: pytest
- **Linting**: flake8, black
- **Type Checking**: mypy
- **Documentation**: Sphinx