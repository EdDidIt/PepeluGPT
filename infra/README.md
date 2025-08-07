# PepeluGPT Infrastructure

This directory contains Infrastructure as Code (IaC) configurations for deploying and managing PepeluGPT.

## 📁 Structure

```text
infra/
├── terraform/          # Terraform configurations
├── kubernetes/         # Kubernetes manifests
├── helm/              # Helm charts
├── docker/            # Docker compositions for different environments
└── scripts/           # Deployment and management scripts
```

## 🚀 Deployment Options

### Local Development

- Docker Compose for local development environment
- Includes all dependencies (databases, monitoring)

### Container Orchestration

- Kubernetes manifests for production deployment
- Helm charts for simplified installation
- Supports horizontal scaling and rolling updates

### Cloud Infrastructure

- Terraform modules for AWS, Azure, and GCP
- Infrastructure security best practices
- Automated backup and disaster recovery

## 🔧 Quick Start

### Docker Compose

```bash
cd infra/docker
docker-compose -f docker-compose.dev.yml up -d
```

### Kubernetes

```bash
kubectl apply -f infra/kubernetes/
```

### Terraform (AWS)

```bash
cd infra/terraform/aws
terraform init
terraform plan
terraform apply
```

## 🔒 Security Considerations

- Network policies for container isolation
- Secret management with external secret stores
- RBAC configurations for Kubernetes
- Infrastructure scanning and compliance

## 📊 Monitoring Integration

- Prometheus metrics collection
- Grafana dashboard deployment
- Log aggregation with ELK stack
- Distributed tracing support

## 🔄 CI/CD Integration

- GitHub Actions workflows
- Automated testing and security scanning
- Progressive deployment strategies
- Environment promotion pipelines
