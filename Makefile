.PHONY:minikube-start
minikube-start:
	minikube start --profile cv-platform-minikube --gpus all --driver docker --container-runtime docker --cpus=8 --memory=16384

.PHONY:minikube-stop
minikube-stop:
	minikube stop --profile cv-platform-minikube

.PHONY:minikube-delete
minikube-delete:
	minikube delete --profile cv-platform-minikube

.PHONY:minikube-dashboard
minikube-dashboard:
	minikube dashboard --profile cv-platform-minikube

.PHONY:argocd-crds
argocd-crds:
	kubectl apply -k https://github.com/argoproj/argo-cd/manifests/crds\?ref\=stable

.PHONY:argocd-port-forward
argocd-port-forward:
	kubectl port-forward service/argocd-server 8080:http -n argocd

.PHONY:argocd-init-password
argocd-init-password:
	kubectl get secrets argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 --decode

.PHONY:cv-platform-apply
cv-platform-apply: argocd-crds
	kustomize build gitops/bootstrap/overlays/default | kubectl apply -f -

.PHONY:cv-platform-remove
cv-platform-remove:
	kustomize build gitops/bootstrap/overlays/default | kubectl delete -f -
