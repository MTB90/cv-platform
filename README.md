# llm-minikube

## Description
The purpose of this project is to get hands on.

- **DevOps/GitOps:**
  - Minikube: https://minikube.sigs.k8s.io/docs
  - ArgoCD: https://argo-cd.readthedocs.io/en/stable


- **Agent AI:**
  - CrewAI: https://github.com/crewAIInc/crewAI


- **Other:**
  - ollama: https://github.com/ollama/ollama

---

## Minimal requirements:
- Docker: 28.3.0
- Kubectl: v1.33.2
- Minikube: v1.36.0
- Nvidia Version: 575.57.08
- Nvidia CUDA Version: 12.9 
- Hardware: 
  - Free memory - 16GB 
  - GPU - 4MG

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
  minikube start --gpus all --driver docker --container-runtime docker --cpus=8 --memory=16384
  ```

  ```bash
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

## Deployment:
