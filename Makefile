.PHONY:minikube-start
minikube-start:
	minikube start --profile llm-minikube --gpus all --driver docker --container-runtime docker --cpus=8 --memory=16384

.PHONY:minikube-stop
minikube-stop:
	minikube stop --profile llm-minikube

.PHONY:minikube-delete
minikube-delete:
	minikube delete --profile llm-minikube

.PHONY:minikube-dashboard
minikube-dashboard:
	minikube dashboard --profile llm-minikube

.PHONY:argocd-crds:
argocd-crds:
	kubectl apply -k https://github.com/argoproj/argo-cd/manifests/crds\?ref\=stable

.PHONY:argocd-apply
argocd-apply: argocd-crds
	kustomize build gitops/bootstrap/overlays/default | kubectl apply -f -

.PHONY:argocd-delete
argocd-delete:
	kustomize build gitops/bootstrap/overlays/default | | kubectl delete -f -
