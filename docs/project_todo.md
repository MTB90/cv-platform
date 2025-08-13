## Project TODO:


### gitops:
- [x] basi pipeline for testing in github actions
- [x] create base template for ArgoCD
- [x] add postgresql for backend
- [x] deploy simple MinIO to store documents
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
- [x] define basic api for users and docs
- [x] upload file using pre-signed url
- [x] added logging
- [x] add health check in backend pod
- [ ] introduce endpoints and logic for jobs
- [ ] add soft delete for docs
- [ ] how limit uploaded file up to 20MB
- [ ] notify about file is uploaded
- [ ] pagination
- [ ] configure settings (cors, database)
- [ ] general limits per user, requests/jobs total capacity etc.

### platform/agentai:
- [ ] restrict access for workers
- [ ] make sure that in document will not change behavior of agent (command in uploaded doc)
