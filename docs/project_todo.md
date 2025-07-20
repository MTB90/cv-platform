## Project TODO:


### gitops:
- [x] basi pipeline for testing in github actions
- [x] create base template for ArgoCD
- [x] add postgresql for backend
- [ ] deploy simple MinIO to store documents
- [ ] deploy traefik for routing
- [ ] create ingress for backend
- [ ] encrypt secrets in git repo
- [ ] figure out how best update image in minikube
- [ ] add litter for yaml
---
### platform/backend:
- [x] base template for backend service (FastAPI)
- [x] check multistage for building docker image
- [x] define base models and write simple migrations
- [ ] define api for backend service
- [ ] upload file using pre-signed url
- [ ] notify about file is uploaded
- [ ] configure settings (cors, database)

### platform/agentai:
- [ ] restrict access for workers
