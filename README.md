# Airtasker Take Home Exercise

This is a simple HTTP server that runs in Kubernetes.

## Prerequisites
- A local Kubernetes cluster (like minikube, kind, or k3d)
- Ingress controller installed in your cluster

## Setup

1. Build the Docker image:
```bash
cd airtasker_take_home/app
docker build -t http-server:latest .
```

2. Deploy to Kubernetes:
```bash
kubectl apply -f airtasker_take_home/k8s/deployment.yaml
kubectl apply -f airtasker_take_home/k8s/service.yaml
kubectl apply -f airtasker_take_home/k8s/ingress.yaml
```

3. Check if it's working:
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

## Testing

You can test the server by running:
```bash
curl http://localhost/
```

The server has two endpoints:
- / - Shows the app name
- /healthcheck - Shows if the server is working 