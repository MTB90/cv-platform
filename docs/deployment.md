# Deployment Minikube Setup

## Prerequisites
- Docker 28.3.0+
- Kubectl v1.33.2+
- Minikube v1.36.0+
- NVIDIA Driver 575.57.08+
- CUDA 12.9+

---
## Quick Start:

1) Start minikube cluster:
```bash
  cd ../
  make minikube-start
```

2) Build and push images to minikube cluster:
```bash
  cd ../
  make minikube-push-images
```

3) Deploy Project using ArgoCD:
```bash
  # First, the ArgoCD CRDs will be installed. Then, the bootstrap process will be deployed, 
  # which includes the installation of ArgoCD itself, followed by the creation of all necessary resources, 
  # such as AppProject and ApplicationSet.
  cd ../
  make cv-platform-apply
```

4) Access MinIO:

- First portforward MinIO on port: 9090
  ```bash
    cd ../
    make minio-port-forward
  ```

- Login in http://localhost:9090
  - Create **cv-platform** bucket

5) Access ArgoCD:

- First portforward ArgoCD server on port: 8080
  ```bash
    cd ../
    make argocd-port-forward
  ```

- Get initial password for admin user
  ```bash
    cd ../
    make argocd-init-password
  ```

- Login in http://localhost:8080 as admin user

---
## Installation:

**Docker:** 
- [Installation guide](https://docs.docker.com/engine/install/ubuntu/)
- Verify that the installation is successful:
  ```bash
  docker run hello-world
  ```

**Nvidia Cuda**:
- [Installation guide](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
- Verify that the installation is successful: 
  ```bash
  nvidia-smi
  ```

**Nvidia Container Toolkit:**
- [Installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- Verify that the installation is successful: 
  ```bash
  docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
  ```

**Ollama:**
- Verify that you can run LLM:
  ```bash
  docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
  docker exec -it ollama ollama run gemma3
  ```

**Minikube:**
- [Installation guide](https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download)
- [NVIDIA GPUs with minikube](https://minikube.sigs.k8s.io/docs/tutorials/nvidia/#docker)
- Verify that the installation is successful:

  ```bash
  # Start minikube cluster

  minikube start --profile cv-platform-minikube --gpus all --driver docker --container-runtime docker
  ```

  ```bash
  # Deploy pod with CUDA

  cat << EOF | kubectl create -f -
  apiVersion: v1
  kind: Pod
  metadata:
    name: nvidia-smi
  spec:
    restartPolicy: OnFailure
    containers:
    - name: nvidia-smi
      image: nvidia/cuda:12.9.1-base-ubi9
      command: ["/bin/bash", "-c", "nvidia-smi"]
      resources:
        limits:
          nvidia.com/gpu: 1 # requesting 1 GPU
  EOF
  ```

  ```bash
  # Verify pod logs:

  kubectl logs nvidia-smi
  ```

  ```bash
  # Example output:

  Mon Jul  7 20:36:12 2025
  +-----------------------------------------------------------------------------------------+
  | NVIDIA-SMI 575.57.08              Driver Version: 575.57.08      CUDA Version: 12.9     |
  |-----------------------------------------+------------------------+----------------------+
  | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
  | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
  |                                         |                        |               MIG M. |
  |=========================================+========================+======================|
  |   0  NVIDIA GeForce RTX 3060 Ti     On  |   00000000:07:00.0  On |                  N/A |
  | 92%   40C    P0             49W /  200W |     623MiB /   8192MiB |      7%      Default |
  |                                         |                        |                  N/A |
  +-----------------------------------------+------------------------+----------------------+

  +-----------------------------------------------------------------------------------------+
  | Processes:                                                                              |
  |  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
  |        ID   ID                                                               Usage      |
  |=========================================================================================|
  |  No running processes found                                                             |
  +-----------------------------------------------------------------------------------------+
  ```

  ```bash
  # Delete minikube cluster:

  minikube delete --profile cv-platform-minikube
  ```
