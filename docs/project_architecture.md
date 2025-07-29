# Project Architecture

### High-Level Overview:

This section outlines the high-level architecture of the system, where each major component is defined and its
interaction with other components is described. The architecture revolves around a **FastAPI** backend, **Argo Workflow
** for background processing, **CrewAI** for agent-based task execution, and various storage systems.

```
                    
                                                                            Client
                                                                             ▲ 
                                                                             │  │     upload file
                                                                http         │  │ pre-signed-url (http)
                                                        ┌────────────────────┘  └──────────────────────┐ 
                                                        │                                              │  
                                                        ▼                                              │  
                                                 ┌────────────────┐                                    │  
      ┌────────────────┐                         │    (api/v1)    │                                    ▼
      │  Argo Workflow │                         │--------------- │     generate pre-signed-url    ┌─────────┐
      │                │ <───── hera client ─────│    Backend     │ <──── minio async client ────> │  MinIO  │
      └────────────────┘                         │                │                                │         │
            │                                    │                │                                │         │
            │                                    │                │                                │         │
            │                            ┌─────> │                │                                │         │
            │                            │       │----------------│      events put,delete         │         │
            │                            │       │  (api/private) │ <----------------------------- │         │
            │                            │       └────────────────┘                                └─────────┘
            │                            │                                                              ▲
            │                            │       ┌──────────────┐                                       │
            │                            └─────> │  PostgreSQL  │                                       │
            │                                    │ (Persistent) │                                       │
            │                                    └──────────────┘                                       │
            │                                                                                           │
            │                                                                                           │ 
            ▼                                                                                           │             
       ┌────────────┐                                                                                   │
       │  Workflow  │<──────────────────────────────────────────────────────────────────────────────────┘                                  
       │------------│                            
       │   CrewAI   │
       └────────────┘                          
```

### Task Flow:

1. **Client**:
    - The client sends an HTTP request to **FastAPI**, and also uploads document using presigned url to minio.


2. **Backend (FastAPI)**:
    - FastAPI triggers the Argo Workflow using hera client: https://hera.readthedocs.io/en/stable/


3. **Argo Workflow**:
    - Create new specific Workflow for uploaded document:
        - Get document from Minio
        - Transform/Create new document using AI - CrewAI
        - Store new document in Minio


4. **Notification**:
    - Events (put, delete) on any document is send back to Backend

---

### Backend API:

**User:**

| Methods | Url                       | Description                |
|---------|---------------------------|----------------------------|
| GET     | `/api/v1/users`           | List all users             |
| POST    | `/api/v1/users`           | Create new user            |
| GET     | `/api/v1/users/{user_id}` | Get user with `user_id`    |
| DELETE  | `/api/v1/users/{user_id}` | Delete user with `user_id` |

**Docs:**

| Methods | Url                                     | Description                                     |
|---------|-----------------------------------------|-------------------------------------------------|
| GET     | `/api/v1/users/{user_id}/docs`          | Get all docs for user, without presigned url    |
| POST    | `/api/v1/users/{user_id}/docs`          | Create entry and return presigned url to upload |
| GET     | `/api/v1/users/{user_id}/docs/{doc_id}` | Get user docs with presigned url to download    |
| DELETE  | `/api/v1/users/{user_id}/docs/{doc_id}` | Delete user doc with specific id                |

**Webhooks:**

| Methods | Url                                | Description                     |
|---------|------------------------------------|---------------------------------|
| POST    | `/api/private/webooks/docs/status` | Update status uploaded that doc |

** Jobs:**

| Methods | Url                                     | Description                 |
|---------|-----------------------------------------|-----------------------------|
| POST    | `/api/v1/users/{user_id}/jobs`          | Start process user docs     |
| GET     | `/api/v1/users/{user_id}/jobs/{job_id}` | Check status of the process |
| DELETE  | `/api/v1/users/{user_id}/jobs/{job_id}` | Cancel job                  |
