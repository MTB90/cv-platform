.PHONY:minikube-start
minikube-start:
	minikube start --profile llm --gpus all --driver docker --container-runtime docker --cpus=8 --memory=16384

.PHONY:minikube-stop
minikube-stop:
	minikube stop --profile llm

.PHONY:minikube-delete
minikube-delete:
	minikube delete --profile llm

.PHONY:minikube-dashboard
minikube-dashboard:
	minikube dashboard --profile llm

.PHONY:minikube-deploy
minikube-deploy: minikube-start
	kubectl apply -k https://github.com/MTB90/llm-minikube/gitops/bootstrap/overlays/default
