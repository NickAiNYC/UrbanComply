# Agent Communication & Interaction Protocol

This protocol outlines how the UrbanComply Agent Framework operates, ensuring smooth handoffs, dependencies, and review order across the team.

---

## General Guidelines for All Agents
1. **Raise Risks Early**: Escalate unresolved blockers or issues directly to the founder.
2. **Default to Asynchronous**: Teams communicate in Slack-style updates unless live collaboration is needed.
3. **Timestamped Updates**: Always timestamp activity logs and deliverables to maintain clear accountability.

---

## Agent-Specific Protocols

### 1. The Pilot Hunter
- **Primary Collaborators**: Scale Scout, Validator.
- **Handoffs**:
  - Provides lead lists and customer context to Process Engineer post-pilot agreement signing.
  - Shares outreach metrics with Scale Scout to refine market segmentation.
- **Inputs Required**:
  - CRM sheet
  - Outreach templates
  - Signed agreements

### 2. The Process Engineer
- **Primary Collaborators**: Pilot Hunter, Scriptsmith, Validator.
- **Handoffs**:
  - Sends edge-case scenarios and error logs to Scriptsmith.
  - Submits documented processes and schemas to Validator for compliance checks.
- **Inputs Required**:
  - Customer data (via Pilot Hunter).
  - NYC regulations.
  - ENERGY STAR Portfolio Manager access.

### 3. The Scriptsmith
- **Primary Collaborators**: Process Engineer, Validator.
- **Handoffs**:
  - Submits reusable scripts and automation tools to the Validator pre-deployment.
  - Shares process-level changes and improvements with Process Engineer.
- **Inputs Required**:
  - Edge case and error logs.
  - Process flowchart.

### 4. The Validator
- **Primary Collaborators**: Process Engineer, Scriptsmith.
- **Handoffs**:
  - Provides compliance feedback and audit trails to Process Engineer.
  - Shares anomaly reports with Scriptsmith for debugging.
- **Inputs Required**:
  - Automation scripts.
  - Process documentation.
  - DOB submission files.

### 5. The Scale Scout
- **Primary Collaborators**: Pilot Hunter, Process Engineer.
- **Handoffs**:
  - Shares predictions about scaling opportunities with Pilot Hunter.
  - Provides assessment reports to the founder on partner APIs.
- **Inputs Required**:
  - Market research data.
  - Pilot outreach feedback (via Pilot Hunter).

---

## Workflows

### Document Review Order
1. Process Engineer creates and submits process documentation.
2. Validator performs compliance and quality checks.
3. Scriptsmith builds automation scripts.
4. Validator reviews Scriptsmith’s code for compliance.

### Escalation Path
1. Tier 1: Internal Agent Feedback.
2. Tier 2: Founder Escalation (via daily summary).
3. Tier 3: External Expert Consultation (as needed).

---

## Communication Logs
Ensure every workflow step and collaboration instance is logged in the shared communication dashboard.