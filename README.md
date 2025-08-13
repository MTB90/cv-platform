# 🧠 cv-platform

**cv-platform** is a hands-on project focused on exploring modern AI agent.

---

## 🚀 Project Goals

- Write backend with FastAPI using async
- Experiment with AI agents and LLM orchestration

---

## 🛠️ Tech Stack Overview

- Python 3.12
    - FastAPI
    - PyTest
    - Pydantic
- Postgresql

---

## 📁 Project Structure

```
├── Makefile
├── README.md
├── docs
└── platform
    ├── service-1
        ├── Dockerfile
        ├── ...
        └── requirements.txt
    ├── ...
    └── service-n
```

- `README.md` - Main README for the whole project.
- `docs` - Docs about project.
- `platform` - It contains all source code for services.

---

## ✅ Project TODOs

### `pipeline`

- [x] push backend docker image to dockerhub
- [ ] update docker images in repository cv-platform-infra

### `platform/backend`

- [x] Base template for backend service (FastAPI)
- [x] Multi-stage Dockerfile for optimized builds
- [x] Define base models and write simple migrations
- [x] Basic APIs for users and document handling
- [x] Upload file using pre-signed URL
- [x] Add structured logging
- [x] Add health check for backend pod
- [ ] Introduce endpoints and logic for job management
- [ ] Add soft delete for documents
- [ ] Enforce file upload limit (max 20MB)
- [ ] Notify user when file is uploaded
- [ ] Implement pagination
- [ ] Configure settings (CORS, database)
- [ ] Add user-level limits (jobs/request caps)

### `platform/agentai`

- [ ] Select framework for agents (e.g., LangChain, CrewAI)
- [ ] Ensure uploaded document content cannot alter agent behavior (prompt injection protection)

## 📍 Status

This project is a work in progress and intended for learning, prototyping, and experimentation.
