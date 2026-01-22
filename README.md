# 🦅 The Phoenix Project: Kubernetes DevOps Platform

A full-stack DevOps demonstration implementing a self-healing, auto-scaling web application on a bare-metal Kubernetes cluster. The project features a complete CI/CD pipeline, ingress networking with MetalLB, and a robust monitoring stack.

## 🏗️ Architecture

* **Application:** Python Flask Web App ("The Phoenix").
* **Infrastructure:** 3-Node Kubernetes Cluster (1 Master, 2 Workers) on bare-metal KVM VMs.
* **CI/CD:** GitHub Actions (Build -> Docker Hub -> Self-Hosted Runner Deploy).
* **Networking:** NGINX Ingress Controller backed by MetalLB (Layer 2 Load Balancer).
* **Observability:** Prometheus (Metrics Collection) & Grafana (Visualization).

## 🚀 Key Features

* **Self-Healing:** Liveness probes automatically restart crashed containers and prevent broken deployments from receiving traffic.
* **Zero-Downtime Deployments:** Rolling updates ensure the service remains available during code changes.
* **Auto-Scaling (HPA):** Horizontal Pod Autoscaler automatically provisions new pods (from 1 to 10) based on CPU load spikes.
* **Real-Time Monitoring:** Custom Grafana dashboards to visualize cluster health, CPU usage, and pod lifecycles.

## 🛠️ Prerequisites

* A Kubernetes Cluster (v1.28+)
* `kubectl` configured to talk to the cluster.
* Helm Package Manager installed.
* A Docker Hub account.

## 📂 Project Structure

```bash
.
├── .github/workflows/
│   └── deploy.yaml      # CI/CD Pipeline definition
├── k8s/
│   ├── deployment.yaml  # App Deployment & Liveness Probes
│   ├── service.yaml     # Internal ClusterIP Service
│   ├── hpa.yaml         # Horizontal Pod Autoscaler rules
│   ├── ingress.yaml     # Routing rules (phoenix.local)
│   └── metallb-config.yaml # Load Balancer IP Pool
├── app.py               # Flask Application Source
├── Dockerfile           # Container definition
└── requirements.txt     # Python dependencies

```

## ⚙️ Setup & Deployment

### 1. Configure Secrets

In your GitHub Repository (Settings -> Secrets), add:

* `DOCKER_USERNAME`: Your Docker Hub username.
* `DOCKER_PASSWORD`: Your Docker Hub access token.

### 2. Install Infrastructure Components (One-Time Setup)

**Install Ingress Controller:**

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace

```

**Install MetalLB (Load Balancer):**

```bash
helm install metallb metallb/metallb --namespace metallb-system --create-namespace
kubectl apply -f k8s/metallb-config.yaml

```

**Install Monitoring Stack:**

```bash
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

```

### 3. Deploy the Application

Pushing to the `main` branch triggers the GitHub Action pipeline. Alternatively, deploy manually:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml

```

## 🌐 Accessing the Application

### Setup Local DNS

Map the Load Balancer IP to the domain in your local `/etc/hosts` file (Linux/Mac) or `C:\Windows\System32\drivers\etc\hosts` (Windows):

```text
192.168.122.240  phoenix.local

```

### Visit the App

Open your browser and navigate to: **[http://phoenix.local](https://www.google.com/search?q=http://phoenix.local)**

## 📊 Monitoring (Grafana)

1. **Retrieve Admin Password:**
```bash
kubectl get secret --namespace monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

```


2. **Port Forward:**
```bash
ssh -L 3000:localhost:3000 user@<server-ip>
# Then on server:
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80

```


3. **Login:** Access `http://localhost:3000` (User: `admin`).

## 🧪 Testing Auto-Scaling

To simulate a traffic spike and trigger the HPA:

```bash
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://phoenix-service; done"

```

*Watch the scaling in action:*

```bash
kubectl get hpa -w

```

## 📝 License

This project is open-source and available for educational purposes.
