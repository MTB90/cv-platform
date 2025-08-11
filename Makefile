SHELL := /bin/bash

MINIO:=mc

.PHONY:minikube-start
minikube-start:
	minikube start --profile cv-platform-minikube --gpus all --driver docker --container-runtime docker --cpus=8 --memory=16384
	minikube --profile cv-platform-minikube addons enable metrics-server

.PHONY:minikube-stop
minikube-stop:
	minikube stop --profile cv-platform-minikube

.PHONY:minikube-delete
minikube-delete:
	minikube delete --profile cv-platform-minikube

.PHONY:minikube-dashboard
minikube-dashboard:
	minikube dashboard --profile cv-platform-minikube

.PHONY:minikube-push-images
minikube-push-images:
	(cd platform/backend; make build-image)
	minikube --profile cv-platform-minikube image load cv-platform-backend

.PHONY:argocd-crds
argocd-crds:
	kubectl apply -k https://github.com/argoproj/argo-cd/manifests/crds\?ref\=stable

.PHONY:argocd-port-forward
argocd-port-forward:
	kubectl port-forward service/argocd-server 8080:http -n argocd

.PHONY:minio-web-port-forward
minio-web-port-forward:
	kubectl port-forward service/minio 9090:web -n cv-platform

.PHONY:minio-api-port-forward
minio-api-port-forward:
	kubectl port-forward service/minio 9000:api -n cv-platform

.PHONY: minio-configure-bucket
minio-configure-bucket:
	$(MINIO) alias set local http://127.0.0.1:9000 minioAccessKey minioSecretKey
	@$(MINIO) mb local/minio-platform-docs || echo "Bucket already exist"
	@$(MINIO) event add local/minio-platform-docs arn:minio:sqs::DOC_STATUS:webhook --event put || echo "Webhook already exist"

.PHONY:argocd-init-password
argocd-init-password:
	kubectl get secrets argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 --decode

.PHONY:argo-ui-token
argo-ui-token:
	kubectl get secrets argo-ui -n cv-platform -o jsonpath='{.data.token}' | base64 --decode

.PHONY:cv-platform-apply
cv-platform-apply: argocd-crds
	kustomize build gitops/bootstrap/overlays/default | kubectl apply -f -

.PHONY:cv-platform-remove
cv-platform-remove:
	kustomize build gitops/bootstrap/overlays/default | kubectl delete -f -

.PHONY:cv-platform-backend-port-forward
cv-platform-backend-port-forward:
	kubectl port-forward service/backend 8000:http -n cv-platform
