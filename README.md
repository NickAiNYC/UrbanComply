# UrbanComply

**Agent-Based Framework for NYC LL84/33 Compliance Automation**

UrbanComply is an intelligent agent framework designed to streamline New York City Local Law 84/33 energy benchmarking compliance for building owners and energy consultants.

## 🎯 Project Status

**Current Phase**: Phase 0 - Foundation Setup  
**Goal**: Launch 3-5 paying pilot customers through automated compliance workflows

## 📋 What This Project Does

UrbanComply automates the complex process of NYC building energy compliance through five specialized AI agents:

1. **Pilot Hunter**: Customer acquisition and relationship management
2. **Process Engineer**: Compliance process mapping and documentation
3. **Scriptsmith**: Automation script development
4. **Validator**: Data validation and quality assurance (✅ In Progress - see PR #1)
5. **Scale Scout**: Market research and partnership evaluation

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 14+ (or SQLite for development)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/NickAiNYC/UrbanComply.git
cd UrbanComply
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual credentials
```

5. Initialize the database:
```bash
# For PostgreSQL:
psql -U your_username -d urbancomply -f schema.sql

# For SQLite (development):
sqlite3 urbancomply.db < schema.sql
```

## 📚 Documentation

- **[Upgrades Needed](UPGRADES_NEEDED.md)**: Comprehensive assessment of required technical upgrades
- **[Week 1 Execution Plan](week1_execution_plan.md)**: Founder-as-Service implementation roadmap
- **[Agent Communication Protocol](agent_comm_protocol.md)**: How agents interact and collaborate

## 🏗️ Project Structure

```
UrbanComply/
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── schema.sql              # Database schema
├── README.md               # This file
├── UPGRADES_NEEDED.md      # Technical requirements assessment
├── week1_execution_plan.md # Implementation roadmap
├── agent_comm_protocol.md  # Agent collaboration guide
└── success_dashboard_template.csv  # KPI tracking template
```

## 🔧 Required Integrations

To fully utilize UrbanComply, you'll need access to:

- **NYC Department of Buildings (DOB) API**: For building data and submissions
- **ENERGY STAR Portfolio Manager**: For energy benchmarking
- **Google Sheets**: For CRM (or alternative CRM system)
- **Calendly**: For scheduling discovery calls
- **SendGrid**: For email automation (or alternative email service)

See `.env.example` for all required credentials.

## 🎯 Success Metrics (Phase 0)

| Agent | Target | Status |
|-------|--------|--------|
| Pilot Hunter | 5 signed pilot agreements | 🟡 In Progress |
| Process Engineer | 90% edge-case coverage | 🟡 In Progress |
| Scriptsmith | ≥50% time reduction per project | 🟡 In Progress |
| Validator | Zero DOB rejections | 🟡 In Progress |
| Scale Scout | 3 partner evaluations | 🟡 In Progress |

## 🛣️ Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [x] Project structure and documentation
- [x] Database schema design
- [x] Environment configuration
- [ ] Base agent framework
- [ ] Basic CLI interface

### Phase 2: MVP Agents (Weeks 3-4)
- [ ] Validator agent (building on PR #1)
- [ ] Process Engineer agent
- [ ] CRM integration
- [ ] Email automation

### Phase 3: Full Agent Suite (Weeks 5-7)
- [ ] Pilot Hunter agent
- [ ] Scriptsmith agent
- [ ] Scale Scout agent
- [ ] Agent communication system

### Phase 4: Production Ready (Weeks 8-12)
- [ ] External API integrations (DOB, ENERGY STAR)
- [ ] Comprehensive testing
- [ ] Security hardening
- [ ] Deployment automation

## 🤝 Contributing

This is currently a private project in active development. Contribution guidelines will be added once the project reaches a stable state.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Resources

- [NYC Local Law 84](https://www.nyc.gov/site/buildings/codes/benchmarking.page)
- [ENERGY STAR Portfolio Manager](https://www.energystar.gov/buildings/benchmark)
- [NYC Building Information Search (BIS)](https://a810-bisweb.nyc.gov/bisweb/bispi00.jsp)

## 📞 Contact

For questions or pilot program inquiries, please contact the project maintainer.

---

**Note**: This project is in active development. For a detailed technical assessment of what's needed to move forward, see [UPGRADES_NEEDED.md](UPGRADES_NEEDED.md).