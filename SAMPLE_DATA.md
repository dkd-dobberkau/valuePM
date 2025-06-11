# ValuePM Sample Data

## Current Status

The ValuePM system currently has **sample data already populated** in the running Docker containers. This data was created during the initial setup and testing phases.

## Existing Sample Data

### 📋 **5 Sample Projects**
1. **AWS Cloud Migration** (Infrastructure, Active)
   - Business Case: Migrate on-premises infrastructure to AWS
   - Estimated Value: $200,000

2. **Customer Self-Service Portal** (Software Development, Active)
   - Business Case: Develop self-service portal to reduce support costs
   - Estimated Value: $150,000

3. **Invoice Processing Automation** (Digital Transformation, Completed)
   - Business Case: Automate invoice processing
   - Estimated Value: $75,000

4. **Network Infrastructure Upgrade** (Infrastructure, Planning)
   - Business Case: Upgrade network for increased bandwidth
   - Estimated Value: $300,000

5. **AI Customer Support Chatbot** (Software Development, Active)
   - Business Case: AI-powered chatbot for customer support
   - Estimated Value: $125,000

### 📊 **15 Value Metrics**
Each project includes multiple metrics tracking:
- **Cost Reduction**: Infrastructure costs, support ticket reduction, staff savings
- **Quality Improvement**: System availability, error rates, network performance
- **Efficiency Gains**: Processing time, deployment speed, automation rates
- **User Satisfaction**: Customer satisfaction scores, adoption rates

### 📈 **36+ Measurements**
Historical measurement data showing progress over time with:
- Realistic progression toward target values
- Confidence levels (80-100%)
- Progress notes and context
- Demonstration of ROI calculations

## Accessing Sample Data

### Via Web UI
1. Open http://localhost:8501
2. Login with your superuser credentials
3. Explore the dashboard showing:
   - Portfolio overview with 5 projects
   - $850,000 total estimated value
   - $16,000 current ROI
   - Charts showing project distribution

### Via API
1. Open http://localhost:8000/api/v1/docs
2. Use the interactive API documentation
3. Explore endpoints like:
   - `/api/v1/projects/` - List all projects
   - `/api/v1/projects/portfolio/overview` - Portfolio metrics
   - `/api/v1/metrics/` - Value metrics data

## Sample Data Script

A new script has been created at `scripts/populate_sample_data.py` that can:
- Create fresh sample data for new installations
- Check if data already exists to avoid duplicates
- Generate realistic metrics and measurements
- Support both local and Docker deployments

### Usage
```bash
# For new installations (local)
make populate-sample-data

# For Docker deployments (after rebuild)
docker-compose run --rm api python scripts/populate_sample_data.py
```

## Data Structure

The sample data demonstrates ValuePM's core concepts:

### **Value Categories**
- 💰 Cost Reduction
- 📈 Revenue Increase  
- ⚡ Efficiency Gains
- 🏆 Quality Improvements
- 🛡️ Risk Mitigation
- 👥 User Satisfaction

### **Metric Types**
- 💱 Currency (costs, savings)
- 📊 Percentage (availability, adoption)
- ⏱️ Time (processing speed, response time)
- 🔢 Count (tickets, bandwidth)
- ⭐ Score (satisfaction ratings)

### **Project Types**
- 🏗️ Infrastructure
- 💻 Software Development
- 🔄 Digital Transformation

## Realistic Business Scenarios

The sample data reflects real-world IT project scenarios:
- **Cloud migrations** with infrastructure cost savings
- **Automation projects** reducing manual effort
- **Customer-facing applications** improving satisfaction
- **Infrastructure upgrades** enhancing performance
- **AI implementations** providing efficiency gains

Each project shows realistic progression from baseline to target values, demonstrating how ValuePM tracks actual business value delivery over time.

## Screenshots Available

The UI documentation includes 9 screenshots showing the sample data in action:
- Login page
- Dashboard with portfolio metrics
- Project detail views
- Metrics progress tracking
- Responsive design examples

See `docs/ui/README.md` for the complete visual documentation.