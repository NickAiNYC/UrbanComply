-- UrbanComply Database Schema
-- PostgreSQL 14+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Buildings Table
-- ============================================
CREATE TABLE buildings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bin VARCHAR(10) UNIQUE NOT NULL,
    address TEXT NOT NULL,
    borough VARCHAR(50),
    block VARCHAR(10),
    lot VARCHAR(10),
    owner_name TEXT,
    owner_email VARCHAR(255),
    owner_phone VARCHAR(20),
    energy_star_id VARCHAR(50),
    building_type VARCHAR(100),
    gross_floor_area DECIMAL,
    year_built INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_buildings_bin ON buildings(bin);
CREATE INDEX idx_buildings_owner_email ON buildings(owner_email);

-- ============================================
-- Utility Data Table
-- ============================================
CREATE TABLE utility_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id UUID REFERENCES buildings(id) ON DELETE CASCADE,
    record_date DATE NOT NULL,
    kwh DECIMAL(12, 2),
    therms DECIMAL(12, 2),
    demand DECIMAL(12, 2),
    meter_number VARCHAR(50),
    utility_provider VARCHAR(100),
    validated BOOLEAN DEFAULT FALSE,
    validation_errors JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_utility_data_building ON utility_data(building_id);
CREATE INDEX idx_utility_data_date ON utility_data(record_date);
CREATE INDEX idx_utility_data_validated ON utility_data(validated);

-- ============================================
-- Submissions Table
-- ============================================
CREATE TABLE submissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id UUID REFERENCES buildings(id) ON DELETE CASCADE,
    submission_year INTEGER NOT NULL,
    submission_date TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL, -- draft, submitted, accepted, rejected
    dob_confirmation_number VARCHAR(100),
    espm_property_id VARCHAR(50),
    submitted_by VARCHAR(100),
    validation_report JSONB,
    dob_response JSONB,
    error_messages TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_building ON submissions(building_id);
CREATE INDEX idx_submissions_year ON submissions(submission_year);
CREATE INDEX idx_submissions_status ON submissions(status);

-- ============================================
-- Agent Activity Logs Table
-- ============================================
-- Note: Uses ON DELETE SET NULL because agent logs should be preserved even if building is deleted
-- This allows for historical analysis and audit trails
CREATE TABLE agent_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_name VARCHAR(50) NOT NULL, -- pilot_hunter, process_engineer, etc.
    activity_type VARCHAR(50) NOT NULL, -- outreach, validation, submission, etc.
    building_id UUID REFERENCES buildings(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL, -- started, completed, failed
    details JSONB,
    error_message TEXT,
    duration_seconds INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agent_logs_agent ON agent_logs(agent_name);
CREATE INDEX idx_agent_logs_type ON agent_logs(activity_type);
CREATE INDEX idx_agent_logs_created ON agent_logs(created_at);

-- ============================================
-- Pilot Customers Table
-- ============================================
CREATE TABLE pilot_customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    contact_email VARCHAR(255) UNIQUE NOT NULL,
    contact_phone VARCHAR(20),
    company_type VARCHAR(100), -- energy consultant, engineering firm, etc.
    status VARCHAR(50) NOT NULL, -- lead, contacted, discovery_call, pilot_agreement, active
    lead_source VARCHAR(100),
    calendly_event_id VARCHAR(100),
    outreach_date DATE,
    discovery_call_date TIMESTAMP,
    pilot_agreement_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pilot_customers_email ON pilot_customers(contact_email);
CREATE INDEX idx_pilot_customers_status ON pilot_customers(status);

-- ============================================
-- Process Documentation Table
-- ============================================
CREATE TABLE process_documentation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    process_name VARCHAR(200) NOT NULL,
    process_category VARCHAR(100), -- data_collection, validation, submission, etc.
    description TEXT,
    steps JSONB NOT NULL, -- Array of step objects
    edge_cases JSONB, -- Array of edge case scenarios
    automation_status VARCHAR(50), -- manual, partial, automated
    created_by VARCHAR(100),
    version VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_process_docs_category ON process_documentation(process_category);

-- ============================================
-- Automation Scripts Table
-- ============================================
CREATE TABLE automation_scripts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    script_name VARCHAR(200) NOT NULL,
    script_type VARCHAR(50), -- validation, submission, data_processing, etc.
    script_path TEXT,
    description TEXT,
    version VARCHAR(20),
    status VARCHAR(50), -- active, deprecated, testing
    performance_metrics JSONB, -- execution time, success rate, etc.
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- Validation Reports Table
-- ============================================
CREATE TABLE validation_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id UUID REFERENCES buildings(id) ON DELETE CASCADE,
    report_date TIMESTAMP NOT NULL,
    validation_type VARCHAR(50), -- utility_data, submission, compliance
    status VARCHAR(50) NOT NULL, -- passed, failed, warning
    errors JSONB,
    warnings JSONB,
    report_data JSONB,
    validated_by VARCHAR(100), -- validator agent
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_validation_reports_building ON validation_reports(building_id);
CREATE INDEX idx_validation_reports_status ON validation_reports(status);

-- ============================================
-- Update Triggers
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to relevant tables
CREATE TRIGGER update_buildings_updated_at BEFORE UPDATE ON buildings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_utility_data_updated_at BEFORE UPDATE ON utility_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_submissions_updated_at BEFORE UPDATE ON submissions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pilot_customers_updated_at BEFORE UPDATE ON pilot_customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_process_documentation_updated_at BEFORE UPDATE ON process_documentation
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_automation_scripts_updated_at BEFORE UPDATE ON automation_scripts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Sample Data (Optional - for testing)
-- ============================================

-- Note: Sample data uses realistic NYC BIN format (10 digits) but these are fictional test values
-- Replace with actual building data when deploying to production
-- NYC BINs are issued by the Department of Buildings and can be verified at:
-- https://a810-bisweb.nyc.gov/bisweb/bispi00.jsp

-- Insert a sample building (fictional BIN for testing only)
INSERT INTO buildings (bin, address, borough, owner_name, owner_email, building_type, gross_floor_area, year_built)
VALUES 
    ('1234567890', '123 Main Street, New York, NY 10001', 'Manhattan', 'Sample Owner LLC', 'owner@example.com', 'Office', 50000, 1985);

-- Insert sample pilot customer
INSERT INTO pilot_customers (company_name, contact_name, contact_email, company_type, status, lead_source)
VALUES 
    ('Green Energy Consulting', 'John Doe', 'john@greenenergy.com', 'energy consultant', 'lead', 'LinkedIn outreach');
