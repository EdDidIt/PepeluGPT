# PepeluGPT Monitoring

This directory contains monitoring, observability, and alerting configurations.

## 📁 Contents

- `prometheus/` - Prometheus metrics and rules
- `grafana/` - Grafana dashboards
- `alerting/` - Alert management configurations
- `health_checks/` - Application health check scripts

## 🔍 Metrics Overview

PepeluGPT exposes the following key metrics:

### Security Metrics

- `pepelugpt_findings_total` - Total security findings detected
- `pepelugpt_ai_risk_score` - AI-calculated risk assessment (0-10)
- `pepelugpt_compliance_health_score` - Overall compliance health

### Performance Metrics

- `pepelugpt_plugin_execution_time` - Plugin execution duration
- `pepelugpt_scan_duration_seconds` - Time to complete security scans
- `pepelugpt_memory_usage_bytes` - Memory utilization

### Operational Metrics

- `pepelugpt_audit_history_count` - Number of historical audits
- `pepelugpt_automation_success_rate` - Automation success percentage
- `pepelugpt_plugin_success_total` - Plugin execution success count

## 📊 Dashboards

Key dashboards available:

1. **Security Overview** - High-level security posture
2. **Performance Monitoring** - System performance metrics
3. **Compliance Tracking** - Compliance status and trends
4. **Plugin Analytics** - Plugin usage and performance

## 🚨 Alerting

Alert conditions configured for:

- Critical security findings detected
- System performance degradation
- Plugin execution failures
- Compliance threshold breaches

## 🔧 Setup

1. Configure Prometheus to scrape PepeluGPT metrics endpoint
2. Import Grafana dashboards
3. Set up alert manager with notification channels
4. Deploy health check monitors
