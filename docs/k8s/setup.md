# K8s Setup

---

## Local k8s using minikube

### Install minikube

Install minikube: <https://minikube.sigs.k8s.io/docs/start/>

On linux:

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

On MacOs

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64

sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

### Start your cluster

```bash
minikube start
```

### Start the Kubernetes Dashboard (optional)

```bash
minikube dashboard
```

---

## Helm setup

Install Helm: <https://helm.sh/docs/intro/install/>

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

chmod 700 get_helm.sh

./get_helm.sh
```
