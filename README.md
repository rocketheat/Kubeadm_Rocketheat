# Kubeadm_Rocketheat

## The steps to build Kubernetes cluster:

### Cluster side
#### Master Node
1. Download Docker
2. Download Kubernetes
3. Download Kubeadm

#### Worker Node
1. Download Docker
2. Download Kubernetes
3. Download Kubeadm

### Client side
1. Download Docker
2. Download Kubernetes
3. Download Ksonnet
4. Download Kubeflow

### Download Docker
Follow the instructions here https://www.docker.com/get-started
When downloading Docker on Windows and Mac it will also download kubernetes

### Download Kubernetes
Follow the instructions here https://kubernetes.io/docs/getting-started-guides/ubuntu/

### Download Kubeadm
Follow the insturctions here https://kubernetes.io/docs/setup/independent/install-kubeadm/

### Download ksonnet
Follow the instructions here https://github.com/ksonnet/ksonnet

### Download Kubeflow
As detailed in the below instructions

# Starting Kubernetes Cluster
## Master Node:
Run the following code:



```bash
sudo apt-get update \
  && sudo apt-get install -y \
  kubelet \
  kubeadm \
  kubernetes-cni
```

Figure out computer IP address:
```bash
ifconfig
```

```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=10.0.10.107 --kubernetes-version stable-1.12
```

```bash
sudo useradd packet -G sudo -m -s /bin/bash
sudo passwd packet
```

```bash
cd $HOME
sudo whoami

sudo cp /etc/kubernetes/admin.conf $HOME/
sudo chown $(id -u):$(id -g) $HOME/admin.conf
export KUBECONFIG=$HOME/admin.conf

echo "export KUBECONFIG=$HOME/admin.conf" | tee -a ~/.bashrc
```

Apply your pod network (flannel)

```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/k8s-manifests/kube-flannel-rbac.yml
```
## Worker Node:
```bash
sudo apt-get update \
  && sudo apt-get install -y \
  kubelet \
  kubeadm \
  kubernetes-cni
```

Join the cluster with whatever Token provided above

```bash
kubeadm join --token f2292a.77a85956eb6acbd6 10.100.195.129:6443 --discovery-token-ca-cert-hash sha256:0c4890b8d174078072545ef17f295a9badc5e2041dc68c419880cca93d084098
```

## Client or Master:
Run this code on either the master or the client node

```bash
# Create a namespace for kubeflow deployment
NAMESPACE=kubeflow
kubectl create namespace ${NAMESPACE}

# Which version of Kubeflow to use
# For a list of releases refer to:
# https://github.com/kubeflow/kubeflow/releases
VERSION=v0.3.2

# Initialize a ksonnet app. Set the namespace for it's default environment.
APP_NAME=my-kubeflow
ks init ${APP_NAME} --api-spec=version:v1.11.3
cd ${APP_NAME}
ks env set default --namespace ${NAMESPACE}

# Install Kubeflow components
ks registry add kubeflow github.com/kubeflow/kubeflow/tree/${VERSION}/kubeflow

ks pkg install kubeflow/core@${VERSION}
ks pkg install kubeflow/tf-serving@${VERSION}
ks pkg install kubeflow/tf-job@${VERSION}

# Create templates for core components
ks generate kubeflow-core kubeflow-core

# If your cluster is running on Azure you will need to set the cloud parameter.
# If the cluster was created with AKS or ACS choose aks, it if was created
# with acs-engine, choose acsengine
# PLATFORM=<aks|acsengine>
# ks param set kubeflow-core cloud ${PLATFORM}

# Enable collection of anonymous usage metrics
# Skip this step if you don't want to enable collection.
ks param set kubeflow-core reportUsage true
ks param set kubeflow-core usageId $(uuidgen)

# Deploy Kubeflow
ks apply default -c kubeflow-core
```

Run this code on the client node

```bash
# check
# To connect with jupyer hub locally
PODNAME=`kubectl get pods --namespace=${NAMESPACE} --selector="app=tf-hub" --output=template --template="{{with index .items 0}}{{.metadata.name}}{{end}}"`
kubectl port-forward --namespace=${NAMESPACE} $PODNAME 8000:8000
```

For kubernetes dashboard
```bash
```
## Worker Node:
