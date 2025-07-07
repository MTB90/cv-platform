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

.PHONY:argocd-deploy
argocd-deploy:
	kubectl apply -k https://github.com/MTB90/llm-minikube/gitops/bootstrap/overlays/default
