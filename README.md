# 🐄 Wisecow — AccuKnox DevOps Trainee Assessment

Containerization and deployment of the [Wisecow](https://github.com/nyrahul/wisecow) application on Kubernetes with CI/CD and TLS support.

---

## 📁 Repository Structure

```
wisecow/
├── wisecow.sh                        # Original Wisecow application
├── Dockerfile                        # PS1 — Docker image definition
├── k8s/
│   ├── deployment.yaml               # PS1 — Kubernetes Deployment
│   ├── service.yaml                  # PS1 — Kubernetes Service
│   ├── ingress.yaml                  # PS1 — Ingress with TLS
│   ├── tls-cert-issuer.yaml          # PS1 — cert-manager TLS setup
│   └── kubearmor-policy.yaml         # PS3 — KubeArmor zero-trust policy
├── scripts/
│   ├── system_health.py              # PS2 — System Health Monitoring
│   └── app_health_checker.py         # PS2 — Application Health Checker
└── .github/
    └── workflows/
        └── ci-cd.yml                 # PS1 — GitHub Actions CI/CD pipeline
```

---

## ✅ Problem Statement 1 — Containerization & Kubernetes Deployment

### Dockerfile
- Base image: `ubuntu:22.04`
- Installs `fortune-mod`, `cowsay`, `netcat-openbsd`
- Exposes port `4499`

### Kubernetes Manifests
- `deployment.yaml` — Runs wisecow with 1 replica
- `service.yaml` — ClusterIP service on port 80 → 4499
- `ingress.yaml` — Nginx ingress with TLS enabled at `wisecow.local`
- `tls-cert-issuer.yaml` — cert-manager self-signed TLS certificate

### CI/CD Pipeline (GitHub Actions)
- Triggers on every push to `main`
- Builds and pushes Docker image to GitHub Container Registry (GHCR)
- Automatically deploys updated image to Kubernetes cluster

### How to Deploy Locally

**Prerequisites:**
```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube
minikube start

# Enable required addons
minikube addons enable ingress
minikube addons enable ingress-dns
```

**Install cert-manager:**
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
kubectl wait --namespace cert-manager --for=condition=ready pod --selector=app.kubernetes.io/instance=cert-manager --timeout=120s
```

**Deploy Wisecow:**
```bash
kubectl apply -f k8s/tls-cert-issuer.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

**Add local DNS entry:**
```bash
echo "$(minikube ip) wisecow.local" | sudo tee -a /etc/hosts
```

**Access the app:**
```
https://wisecow.local
```

---

## ✅ Problem Statement 2 — Scripts (Python)

### 1. System Health Monitoring (`scripts/system_health.py`)
Monitors CPU, memory, disk usage, and running processes.
Sends alerts to console and log file when thresholds are exceeded.

```bash
pip install psutil
python3 scripts/system_health.py
```

### 2. Application Health Checker (`scripts/app_health_checker.py`)
Checks HTTP status of configured applications.
Detects UP/DOWN status with response times and error reasons.

```bash
pip install requests
python3 scripts/app_health_checker.py
```

---

## ✅ Problem Statement 3 — KubeArmor Zero-Trust Policy (Bonus)

Three KubeArmor policies applied to the wisecow workload:

| Policy | What it blocks |
|---|---|
| `wisecow-block-unwanted-processes` | wget, curl, apt, shell abuse, sbin tools |
| `wisecow-block-sensitive-file-access` | /etc/passwd, /etc/shadow, K8s service account tokens |
| `wisecow-block-network-abuse` | Raw sockets, unix sockets |

**Install KubeArmor:**
```bash
helm repo add kubearmor https://kubearmor.github.io/charts
helm repo update kubearmor
helm upgrade --install kubearmor kubearmor/kubearmor -n kubearmor --create-namespace
```

**Apply the policy:**
```bash
kubectl apply -f k8s/kubearmor-policy.yaml
```

---

## 👤 Author
**Kishore K S**  
MCA Graduate | DevOps & Cloud Enthusiast  
kishoreshanmugam037@gmail.com
