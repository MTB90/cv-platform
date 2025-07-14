export CV_BACKEND_PROJECT_NAME=cv-platform-backend
export CV_BACKEND_DATABASE_URL=postgresql+asyncpg://user:pass@localhost:54321/db

env | grep CV_BACKEND_ > .env