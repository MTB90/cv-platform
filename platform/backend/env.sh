export CV_BACKEND_DB_HOST=localhost:54321
export CV_BACKEND_DB_NAME=backend-db
export CV_BACKEND_DB_USER=user
export CV_BACKEND_DB_PASS=pass

env | grep CV_BACKEND_ > .env
