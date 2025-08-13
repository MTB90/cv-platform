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

**Jobs:**

| Methods | Url                                     | Description                 |
|---------|-----------------------------------------|-----------------------------|
| POST    | `/api/v1/users/{user_id}/jobs`          | Start process user docs     |
| GET     | `/api/v1/users/{user_id}/jobs/{job_id}` | Check status of the process |

