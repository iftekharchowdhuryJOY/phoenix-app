# 🦅 The Phoenix Project: Kubernetes DevOps Platform

A full-stack DevOps demonstration implementing a self-healing, auto-scaling web application on a bare-metal Kubernetes cluster. The project features a complete CI/CD pipeline, Zero-Trust ingress networking, and a robust monitoring stack.

## 🏗️ Architecture

* **Application:** Python Flask Web App ("The Phoenix").
* **Infrastructure:** 3-Node Kubernetes Cluster (1 Master, 2 Workers) on bare-metal KVM VMs.
* **CI/CD:** GitHub Actions (Automated Build & Deploy Pipeline).
* **Networking:** Cloudflare Tunnel (Edge)  MetalLB (L2 Load Balancer)  NGINX Ingress.
* **Observability:** Prometheus (Metrics Collection) & Grafana (Visualization).

## 🚀 Key Features

* **Global Zero-Trust Access:** Exposed to the public internet via **Cloudflare Tunnel**, eliminating the need for open router ports or VPNs.
* **Self-Healing:** Liveness probes automatically restart crashed containers and prevent broken deployments from receiving traffic.
* **Zero-Downtime Deployments:** Rolling updates ensure the service remains available during code changes.
* **Auto-Scaling (HPA):** Horizontal Pod Autoscaler automatically provisions new pods (from 1 to 10) based on CPU load spikes.

## 📂 Project Structure

```bash
.
├── .github/workflows/
│   └── deploy.yaml      # CI/CD Pipeline definition
├── k8s/
│   ├── deployment.yaml  # App Deployment & Liveness Probes
│   ├── service.yaml     # Internal ClusterIP Service
│   ├── hpa.yaml         # Horizontal Pod Autoscaler rules
│   ├── ingress.yaml     # Ingress Routing (aitigerlab.com)
│   └── metallb-config.yaml # Load Balancer IP Pool
├── app.py               # Flask Application Source
├── Dockerfile           # Container definition
└── requirements.txt     # Python dependencies

```

## ⚙️ Setup & Deployment

### 1. Prerequisites

* A Kubernetes Cluster (v1.28+)
* Helm Package Manager installed.
* `cloudflared` installed on the Host Node.
* A Docker Hub account.

### 2. Install Infrastructure Components (One-Time Setup)

**Install Ingress & Load Balancer:**

```bash
helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --create-namespace
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

## 🌐 Global Access (Cloudflare Tunnel)

This project uses **Cloudflare Tunnel** to expose the internal Kubernetes Ingress to the public internet securely.

* **Public URL:** `https://aitigerlab.com`
* **Security:** Traffic is encrypted from the Cloudflare Edge directly to the Cluster, bypassing local firewall ingress rules.

**Architecture Flow:**
`User (HTTPS)`  `Cloudflare Edge`  `Secure Tunnel`  `Host Node`  `MetalLB`  `NGINX Ingress`  `Pod`

## 📊 Monitoring (Grafana)

1. **Retrieve Admin Password:**
```bash
kubectl get secret --namespace monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

```


2. **Access Dashboard:**
Port-forward the Grafana service to your local machine:
```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80

```


Visit: `http://localhost:3000` (User: `admin`)

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
