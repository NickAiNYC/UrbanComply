# UrbanComply: Upgrades & Requirements Assessment

## Executive Summary
This document outlines the necessary upgrades to transition UrbanComply from planning phase to a functional agent-based framework for NYC LL84/33 compliance automation.

---

## Current State Analysis

### ✅ What You Have
- Strategic planning documents (Week 1 execution plan)
- Agent communication protocols defined
- Success metrics framework (CSV template)
- Initial utility data validation script (PR #1)
- MIT License
- Basic repository structure

### ❌ What's Missing
- No implemented codebase or application framework
- No agent implementations
- No automation infrastructure
- No integration with required external services
- No user interface (CLI or web)
- No deployment configuration
- No CI/CD pipeline
- No database or data storage layer

---

## Priority 1: Core Infrastructure (Week 1-2)

### 1. Project Setup & Dependency Management
**Current**: No dependency management system in main branch
**Required**:
- `requirements.txt` or `pyproject.toml` for Python dependencies
- Virtual environment documentation
- Docker setup for containerization
- `.gitignore` for Python projects

**Action Items**:
```bash
# Create requirements.txt
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
python-dotenv>=1.0.0
pydantic>=2.0.0
```

### 2. Environment Configuration
**Required**:
- `.env.example` template for API keys and credentials
- Configuration management system
- Secrets management strategy

**Environment Variables Needed**:
```
# NYC DOB API
DOB_API_KEY=
DOB_API_URL=

# ENERGY STAR Portfolio Manager
ESPM_USERNAME=
ESPM_PASSWORD=
ESPM_API_URL=

# CRM Integration
CRM_API_KEY=
CRM_SHEET_URL=

# Calendly Integration
CALENDLY_API_KEY=
CALENDLY_USER_URL=
```

### 3. Database & Data Storage
**Current**: No database
**Required**:
- PostgreSQL or SQLite for structured data
- File storage for CSV/PDF documents
- Schema design for:
  - Building profiles
  - Utility data records
  - Submission history
  - Validation reports
  - Agent activity logs

**Schema Proposal**:
```sql
-- buildings table
CREATE TABLE buildings (
    id SERIAL PRIMARY KEY,
    bin VARCHAR(10) UNIQUE,
    address TEXT,
    owner TEXT,
    energy_star_id VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- utility_data table
CREATE TABLE utility_data (
    id SERIAL PRIMARY KEY,
    building_id INTEGER REFERENCES buildings(id),
    date DATE,
    kwh DECIMAL,
    therms DECIMAL,
    demand DECIMAL,
    validated BOOLEAN,
    created_at TIMESTAMP
);

-- submissions table
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    building_id INTEGER REFERENCES buildings(id),
    submission_date DATE,
    status VARCHAR(50),
    dob_confirmation TEXT,
    validated_by VARCHAR(100),
    created_at TIMESTAMP
);
```

---

## Priority 2: Agent Framework Implementation (Week 2-3)

### 4. Base Agent Architecture
**Required**:
- Abstract base agent class
- Common interfaces for all agents
- Event-driven communication system
- State management
- Error handling and recovery

**Code Structure**:
```
urbancomply/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── pilot_hunter.py
│   ├── process_engineer.py
│   ├── scriptsmith.py
│   ├── validator.py
│   └── scale_scout.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── messaging.py
├── integrations/
│   ├── __init__.py
│   ├── dob_api.py
│   ├── energy_star.py
│   ├── crm.py
│   └── calendly.py
└── utils/
    ├── __init__.py
    ├── logging.py
    └── validation.py
```

### 5. Individual Agent Implementations

#### Pilot Hunter Agent
**Capabilities Needed**:
- CRM integration (Google Sheets or similar)
- Email automation
- Calendly integration for discovery calls
- Lead tracking and status updates
- Outreach template management

**Dependencies**:
```
gspread>=5.12.0  # Google Sheets
oauth2client>=4.1.3
sendgrid>=6.11.0  # Email automation
calendly-python>=0.1.0
```

#### Process Engineer Agent
**Capabilities Needed**:
- NYC building code reference system
- Document parsing (PDF, CSV)
- Process mapping tools
- ENERGY STAR Portfolio Manager API integration
- Edge case documentation

**Dependencies**:
```
PyPDF2>=3.0.0
tabula-py>=2.9.0
beautifulsoup4>=4.12.0
selenium>=4.15.0  # For ESPM automation
```

#### Scriptsmith Agent
**Capabilities Needed**:
- Code generation framework
- Script templating system
- Version control for generated scripts
- Testing framework for automation scripts
- Deployment automation

**Dependencies**:
```
jinja2>=3.1.2
black>=23.12.0  # Code formatting
pylint>=3.0.0
```

#### Validator Agent
**Capabilities Needed**:
- Compliance rules engine
- Data validation framework (already started in PR #1)
- DOB submission format checker
- Anomaly detection
- Audit trail generation

**Enhancement to existing validation**:
- Integration with compliance database
- Real-time validation APIs
- Batch validation support

#### Scale Scout Agent
**Capabilities Needed**:
- Market research automation
- Partner API evaluation framework
- Scalability metrics tracking
- Cost-benefit analysis tools
- Integration assessment framework

**Dependencies**:
```
openai>=1.6.0  # For market analysis
anthropic>=0.8.0  # Alternative LLM option
```

---

## Priority 3: External Integrations (Week 3-4)

### 6. NYC Department of Buildings (DOB)
**Required**:
- DOB BIS API integration
- Building Information System access
- Automated submission system
- Status tracking

**API Endpoints Needed**:
- Building profile lookup
- LL84/33 submission endpoint
- Status verification
- Document upload

### 7. ENERGY STAR Portfolio Manager
**Required**:
- Portfolio Manager API credentials
- Automated data upload
- Building portfolio management
- Energy performance metrics retrieval

**Integration Type**: Web API + possible Selenium automation
**Documentation**: https://portfoliomanager.energystar.gov/webservices

### 8. CRM System
**Options**:
- Google Sheets (simplest, already mentioned in docs)
- HubSpot API
- Salesforce API
- Custom CRM

**Recommended**: Start with Google Sheets for MVP

### 9. Calendly Integration
**Required**:
- API key setup
- Event type configuration
- Webhook setup for notifications
- Calendar sync

---

## Priority 4: User Interfaces (Week 4-5)

### 10. CLI Interface
**Current**: Single script (check_utility_data.py)
**Required**: Comprehensive CLI tool

**Proposed CLI Structure**:
```bash
# Agent management
urbancomply agent start pilot-hunter
urbancomply agent status
urbancomply agent logs validator

# Data management
urbancomply data import utility_data.csv
urbancomply data validate --building-id BIN123
urbancomply data submit --building-id BIN123

# Reporting
urbancomply report dashboard
urbancomply report agent-metrics
urbancomply report submission-status
```

**Dependencies**:
```
click>=8.1.7
rich>=13.7.0  # Beautiful terminal output
tabulate>=0.9.0
```

### 11. Web Dashboard (Optional, Future Phase)
**Framework Options**:
- Flask + Bootstrap (lightweight)
- FastAPI + React (modern)
- Streamlit (rapid prototyping)

**Features**:
- Agent status monitoring
- Submission tracking
- Data visualization
- Manual intervention interface

---

## Priority 5: DevOps & Quality (Week 5-6)

### 12. Testing Infrastructure
**Required**:
- Unit tests for all agents
- Integration tests
- End-to-end tests
- Test data fixtures
- Mocking framework for external APIs

**Dependencies**:
```
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0
responses>=0.24.0  # HTTP mocking
faker>=22.0.0  # Test data generation
```

**Coverage Target**: ≥80%

### 13. CI/CD Pipeline
**Required**: GitHub Actions workflows

**Workflows Needed**:
```yaml
# .github/workflows/test.yml
# - Lint code (flake8, pylint)
# - Run tests
# - Check coverage
# - Security scanning

# .github/workflows/deploy.yml
# - Build Docker image
# - Deploy to staging
# - Run smoke tests
# - Deploy to production
```

### 14. Logging & Monitoring
**Required**:
- Structured logging system
- Error tracking (Sentry)
- Performance monitoring
- Agent activity dashboard
- Alert system

**Dependencies**:
```
python-json-logger>=2.0.7
sentry-sdk>=1.39.0
prometheus-client>=0.19.0
```

### 15. Documentation
**Current**: Planning docs only
**Required**:
- API documentation (Sphinx or MkDocs)
- Agent documentation
- Integration guides
- Deployment guide
- User manual
- Contributing guide

**Structure**:
```
docs/
├── architecture/
├── agents/
├── api/
├── integrations/
├── deployment/
└── user-guide/
```

---

## Priority 6: Security & Compliance (Ongoing)

### 16. Security Requirements
**Critical Items**:
- Secrets management (AWS Secrets Manager, HashiCorp Vault)
- API key rotation
- Data encryption at rest and in transit
- Access control and authentication
- Audit logging
- GDPR/privacy compliance for customer data

**Dependencies**:
```
cryptography>=41.0.7
python-jose>=3.3.0  # JWT tokens
passlib>=1.7.4
```

### 17. Code Quality Tools
**Required**:
```
black>=23.12.0  # Code formatting
isort>=5.13.0  # Import sorting
flake8>=7.0.0  # Linting
mypy>=1.8.0  # Type checking
bandit>=1.7.5  # Security linting
```

---

## Technology Stack Recommendations

### Core Technologies
- **Language**: Python 3.10+
- **Framework**: FastAPI or Flask
- **Database**: PostgreSQL 14+
- **Message Queue**: Redis or RabbitMQ (for agent communication)
- **Caching**: Redis
- **Task Queue**: Celery (for background jobs)

### Development Tools
- **Version Control**: Git + GitHub
- **Package Management**: pip + virtualenv or Poetry
- **Code Quality**: pre-commit hooks
- **Testing**: pytest
- **Documentation**: MkDocs or Sphinx

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Docker Swarm or Kubernetes (for scale)
- **Cloud Provider**: AWS, GCP, or Azure
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
1. ✅ Set up repository structure
2. ✅ Create requirements.txt
3. ✅ Set up virtual environment
4. ✅ Configure .env and secrets management
5. ✅ Initialize database schema
6. ✅ Set up basic logging

### Phase 2: MVP Agents (Weeks 3-4)
1. ✅ Implement base agent class
2. ✅ Build Validator agent (expand PR #1)
3. ✅ Build Process Engineer agent (minimal)
4. ✅ Implement basic CRM integration
5. ✅ Create CLI interface

### Phase 3: Full Agent Suite (Weeks 5-7)
1. ✅ Complete Pilot Hunter
2. ✅ Complete Scriptsmith
3. ✅ Complete Scale Scout
4. ✅ Implement agent communication
5. ✅ Add comprehensive testing

### Phase 4: Integrations (Weeks 8-10)
1. ✅ DOB API integration
2. ✅ ENERGY STAR integration
3. ✅ Calendly integration
4. ✅ Email automation
5. ✅ End-to-end testing

### Phase 5: Production Ready (Weeks 11-12)
1. ✅ Security audit
2. ✅ Performance optimization
3. ✅ Documentation completion
4. ✅ Deployment automation
5. ✅ Monitoring setup

---

## Estimated Costs

### Development Tools (One-time/Annual)
- GitHub Pro: $4/month
- Docker Desktop Pro: $5/month (optional)
- IDE/Tools: Free (VS Code)

### Cloud Services (Monthly, estimated)
- Database (PostgreSQL): $15-50
- Compute (2-4 instances): $50-200
- Storage: $10-30
- Monitoring (Sentry): $26-80
- **Total**: $100-350/month (scales with usage)

### External API Services (Monthly)
- ENERGY STAR Portfolio Manager: Free
- NYC DOB API: Free (likely)
- SendGrid (Email): $15+ (for 40k emails/month)
- Calendly: $10-16/user
- **Total**: $25-50/month

### Total Initial Monthly Cost: $125-400

---

## Quick Start Priority Order

If you need to start immediately, focus on:

1. **Week 1**: 
   - ✅ Merge PR #1 (validation script)
   - ✅ Set up requirements.txt and project structure
   - ✅ Create .env.example
   - ✅ Initialize database schema

2. **Week 2**:
   - ✅ Build base agent framework
   - ✅ Implement Process Engineer (minimal)
   - ✅ Set up Google Sheets CRM integration

3. **Week 3**:
   - ✅ Test end-to-end workflow with 1 building
   - ✅ Add CLI interface
   - ✅ Document the process

This gives you a working MVP to validate with pilot customers while continuing development.

---

## Next Steps

1. Review and approve this upgrade plan
2. Prioritize which agents/features are most critical
3. Set up development environment
4. Begin Phase 1 implementation
5. Schedule regular check-ins to track progress

## Questions to Answer

1. Which CRM system do you want to use? (Google Sheets recommended for MVP)
2. Do you have API access to NYC DOB and ENERGY STAR?
3. What's your target timeline for pilot customers?
4. What's your budget for cloud infrastructure?
5. Do you need web UI or is CLI sufficient for Phase 0?
6. Will you self-host or use cloud provider?
