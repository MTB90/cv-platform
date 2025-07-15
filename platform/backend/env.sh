export CV_BACKEND_PROJECT_NAME=cv-platform-backend

export CV_BACKEND_DB_HOST=localhost:54321/backend-db
export CV_BACKEND_DB_USER=user
export CV_BACKEND_DB_PASS=pass

env | grep CV_BACKEND_ > .env
