# Todo App Containerization & Helm Deployment

This document provides instructions for containerizing the Todo App frontend and backend and deploying them using Helm charts.

## 1. Frontend Containerization

### Dockerfile
The frontend Dockerfile is located at `frontend/Dockerfile` and uses a multi-stage build process:
- Builder stage: Installs dependencies and builds the Next.js application
- Runner stage: Creates a minimal production image with only necessary files

### Building the Frontend Image
```bash
cd frontend
docker build -t todo-frontend:latest .
```

## 2. Backend Containerization

### Dockerfile
The backend Dockerfile is located at `backend/Dockerfile` and:
- Uses Python 3.11 slim image
- Installs system dependencies and Python packages
- Copies application code

### Building the Backend Image
```bash
cd backend
docker build -t todo-backend:latest .
```

## 3. Helm Charts

Helm charts are organized in the `helm/` directory:
- `todo-app/`: Main umbrella chart
- `todo-app/charts/todo-frontend/`: Frontend subchart
- `todo-app/charts/todo-backend/`: Backend subchart

Each subchart includes:
- Deployment with specified replica counts
- Service for internal communication
- Configurable resources and image settings

## 4. Deploying with Helm

### Prerequisites
- Kubernetes cluster (Minikube, kind, or cloud provider)
- Helm 3 installed

### Installation Commands
```bash
# Add the current directory as a Helm repo (optional)
helm repo add todo-app ./helm/todo-app

# Install the application
helm install todo-app-release ./helm/todo-app

# Or upgrade an existing release
helm upgrade todo-app-release ./helm/todo-app

# Uninstall
helm uninstall todo-app-release
```

### Custom Values
You can customize the deployment using a values file:
```bash
helm install todo-app-release ./helm/todo-app -f custom-values.yaml
```

## 5. Configuration Details

### Frontend
- Replica count: 2 (as specified)
- Port: 3000
- Image: todo-frontend:latest

### Backend
- Replica count: 1 (as specified)
- Port: 8000
- Image: todo-backend:latest
- Database URL: configurable via values file

## 6. Verifying the Deployment

After deployment, check the status:
```bash
kubectl get pods
kubectl get services
kubectl get deployments
```