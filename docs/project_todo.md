## Project TODO:


### gitops:
- [x] basi pipeline for testing in github actions
- [x] create base template for ArgoCD
- [x] add postgresql for backend
- [ ] deploy traefik for routing
- [ ] create ingress for backend
- [ ] encrypt secrets in git repo
- [ ] figure out how best update image in minikube

---
### platform/backend:
- [x] base template for backend service (FastAPI)
- [x] check multistage for building docker image
- [ ] define base models and write simple migrations
- [ ] define api for backend service
- [ ] configure settings (cors, database)

### platform/agentai:
- [ ] restrict access for workers
