# GitOps

## Folder structure:

Based on:
- https://github.com/christianh814/example-kubernetes-go-repo/blob/main/README.md
- https://github.com/gnunn-gitops/standards/blob/master/folders.md
- https://codefresh.io/blog/how-to-structure-your-argo-cd-repositories-using-application-sets


```
├── README.md
├── bootstrap
│   ├── base
│   │   ├── argocd-ns.yaml
│   │   └── kustomization.yaml
│   └── overlays
│       └── default
│           └── kustomization.yaml
├── components
│   ├── applicationsets
│   │   ├── core-appset.yaml
│   │   ├── minikube-apps-appset.yaml
│   │   ├── minikube-infra-appset.yaml
│   │   └── kustomization.yaml
│   └── argocdproj
│       ├── kustomization.yaml
│       └── project.yaml
├── core
│   └── gitops-controller
│       └── kustomization.yaml
├── infra
│   ├── minio
│   │   ├── base
│   │   │   └── kustomization.yaml
│   │   └── overlays
│   │       └── minikube
│   │           └── kustomization.yaml
│   ├── postgresql
│   │   ├── base
│   │   │   └── kustomization.yaml
│   │   └── overlays
│   │       └── minikube
│   │           └── kustomization.yaml
│   └── workflow
│       ├── base
│       │   └── kustomization.yaml
│       └── overlays
│           └── minikube
│               └── kustomization.yaml
└── apps
    ├── llm
    │   ├── base
    │   │   ├── llm-deployment.yaml
    │   │   └── kustomization.yaml
    │   └── overlays
    │       └── minikube
    │           └── kustomization.yaml
    └── backend
        ├── base
        │   ├── backend-deployment.yaml
        │   └── kustomization.yaml
        └── overlays
            └── minikube
                └── kustomization.yaml
```
