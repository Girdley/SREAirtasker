# HTTP Server Application

A simple HTTP server application built with Flask, containerized with Docker, and deployed to Kubernetes.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker/Docker Compose**: Install Docker - https://docs.docker.com/get-docker/
- **kubectl**: Install kubectl - https://kubernetes.io/docs/tasks/tools/install-kubectl/
- **kind**: Install kind - https://kind.sigs.k8s.io/docs/user/quick-start/#installation
- **Git**: Install Git - https://git-scm.com/downloads

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Girdley/SREAirtasker
   cd SREAirtasker
   ```

2. **Choose your development method:**

### Option 1: Quick Testing with Docker Compose

For quick local testing without Kubernetes:

```bash
# Start the application
docker-compose up

# In a new terminal, test the endpoints
curl http://localhost:8080/
curl http://localhost:8080/healthcheck

# Stop the application
docker-compose down
```

### Option 2: Kubernetes Development with kind

For local Kubernetes development:

1. **Start kind cluster with ingress enabled:**
   ```bash
   # 1. Check if kind cluster exists
   kind get clusters
   
   #2. If a cluster exists, delete it to start fresh
   kind delete cluster
   
   #3. Create the cluster using the config file
   kind create cluster --config kind-config.yaml

   #4.  Verify cluster is running
   kind get clusters
   kubectl cluster-info

   #5.  Install NGINX Ingress Controller
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
   
   #6.  Wait for ingress controller to be ready
   kubectl wait --namespace ingress-nginx \
     --for=condition=ready pod \
     --selector=app.kubernetes.io/component=controller \
     --timeout=90s
   ```

2. **Build and load the Docker image:**
   ```bash
   #1. Build the image
   docker build -t http-server:latest app/
   
   #2. Load it into kind
   kind load docker-image http-server:latest
   ```

3. **Deploy to Kubernetes:**
   ```bash
   #NOTE: Only deploy one evironment at a time
   # For development environment
   kubectl apply -k k8s/overlays/dev

   OR
   
   # For production environment
   kubectl apply -k k8s/overlays/prod
   ```

4. **Verify the deployment:**
   ```bash
   #1. Check pods (you should see 2 replicas)
   kubectl get pods -n prod  # or -n dev for production
   
   #2. Check services
   kubectl get services -n prod
   
   #3. Check ingress
   kubectl get ingress -n prod
   ```

5. **Test the endpoints:**
   ```bash
   # Test the endpoints directly
   curl http://localhost/
   curl http://localhost/healthcheck
   ```

6. **Clean up:**
   ```bash
   # Delete the deployment
   kubectl delete -k k8s/overlays/prod  # or k8s/overlays/dev
   
   # Delete the kind cluster
   kind delete cluster
   ```


## Kubernetes Configuration

The application uses Kustomize for Kubernetes configuration management:

- **base/**: Contains the base configuration that's common to all environments
  - `deployment.yaml`: Pod configuration, resource limits, health checks
  - `service.yaml`: Service configuration for internal communication
  - `ingress.yaml`: Ingress rules for external access
  - `kustomization.yaml`: Base Kustomize configuration

- **overlays/**: Contains environment-specific configurations
  - **dev/**: Development environment
    - 2 replicas (main + backup)
  - **prod/**: Production environment
    - 2 replicas (main + backup)

### Why Kustomize?
Kustomize is a native Kubernetes configuration management tool that lets us maintain different environments (dev/prod) while reusing the same base configuration.

### Why NGINX Ingress Controller?
The NGINX Ingress Controller is a production-grade load balancer that handles external traffic to our Kubernetes services, providing features like SSL termination and path-based routing.

## Troubleshooting

### Docker Compose Issues
- **Port already in use:**
  ```bash
  lsof -i :8080
  ```
  Stop the process or change the port in `docker-compose.yml`

### Kubernetes Issues
- **Check pod status:**
  ```bash
  kubectl describe pod <pod-name> -n prod  # or -n dev
  ```
- **View pod logs:**
  ```bash
  kubectl logs <pod-name> -n prod  # or -n dev
  ```
- **Image not found:**
  Make sure you've loaded the image into kind:
  ```bash
  # First verify kind cluster is running
  kind get clusters
  
  # If no cluster is running, start from step 1
  # If cluster is running, load the image
  kind load docker-image http-server:latest
  ```
- **No nodes found error:**
  This means the kind cluster isn't running. Run these commands:
  ```bash
  # Check if cluster exists
  kind get clusters
  
  # If no cluster exists, start from step 1
  # If cluster exists but isn't running, restart it:
  kind delete cluster
  kind create cluster --config kind-config.yaml
  ```
- **404 Not Found:**
  If you get a 404 when accessing the service:
  1. Check if the ingress controller is running:
     ```bash
     kubectl get pods -n ingress-nginx
     ```
  2. Check if the service is running:
     ```bash
     kubectl get pods -n prod  # or -n dev
     ```
  3. Check if the ingress is configured correctly:
     ```bash
     kubectl get ingress -n prod  # or -n dev
     ```



