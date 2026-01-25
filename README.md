# 🐯 The Tiger Lab: Polyglot Microservices Platform

**Status:** Production (Stable)  
**Infrastructure:** Bare Metal Kubernetes (K3s) on HP EliteDesk 800 G6  
**Location:** Montreal, QC (Homelab)

## 📖 Overview
The Tiger Lab is a production-grade, polyglot microservices architecture running on bare metal. It demonstrates the orchestration of three distinct programming languages (Python, Java, .NET) into a unified platform, secured by Zero Trust network policies and automated via modern CI/CD pipelines.

The platform is fully observable via Prometheus/Grafana and managed via GitOps (ArgoCD).

## 🏗️ Architecture
**Ingress (Nginx) -> Routing Rules -> Microservices -> Pod Security**

| Service | Code Name | Language | Port | URL Path | Key Features |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Frontend** | `Phoenix` | Python (FastAPI) | 80 | `/` | Lightweight, rapid response. |
| **Backend** | `Titan` | Java (Tomcat) | 8080 | `/titan` | Custom Docker image, Memory Limits (256Mi). |
| **Service** | `Spartan` | .NET Core | 8080 | `/spartan` | Health Checks, Liveness Probes. |

## 🛠️ Technology Stack
* **Orchestration:** K3s (Lightweight Kubernetes)
* **GitOps:** ArgoCD (Auto-sync from GitHub)
* **CI/CD:** GitHub Actions (Matrix Strategy Build & Push)
* **Container Registry:** Docker Hub
* **Monitoring:** Prometheus (Metrics) & Grafana (Dashboards)
* **Security:** Network Policies (Calico/Cilium), Zero Trust Architecture
* **Hardware:** HP EliteDesk Mini (Intel i5-10400T, 32GB RAM)

## 🛡️ Security & Hardening
* **Zero Trust Networking:** All ingress traffic to the `Titan` backend is blocked by default using a `NetworkPolicy`.
* **Whitelisting:** Only traffic originating from the `ingress-nginx` namespace is permitted to reach the backend.
* **Resource Quotas:** All pods have strict `requests` and `limits` to prevent OOM (Out of Memory) kills and "Noisy Neighbor" issues.
* **Liveness Probes:** configured for `.NET` and `Java` to automatically restart frozen services.

## ⚙️ Automation (CI/CD)
The project uses a **Matrix Workflow** in GitHub Actions to build Docker images in parallel.

1.  **Trigger:** Push to `main` branch (filters for `docker/**` folders).
2.  **Build:** GitHub Actions runner builds custom images for `titan` and `spartan`.
3.  **Push:** Images are tagged `:latest` and pushed to Docker Hub.
4.  **Deploy:** ArgoCD detects the update and syncs the cluster (Image Pull Policy: Always).

## 🚀 Operational Commands

### Check Cluster Status
```bash
kubectl get pods -A  # See all running services
kubectl get ingress  # Check routing rules

```

### View Monitoring Dashboard

* **Grafana:** Forward port `3000` (`kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80`)
* **ArgoCD:** Forward port `8080` (`kubectl port-forward -n argocd svc/argocd-server 8080:443`)

### Troubleshooting

```bash
# Check logs for the Java backend
kubectl logs -l app=titan

# Check why a pod crashed (Previous instance)
kubectl logs -l app=spartan --previous

# Verify Network Policy (Test Access)
kubectl exec -it hacker -- curl -v http://titan-service:8080  # Should Timeout

```


*Built with ❤️ and ☕ in Montreal.*



