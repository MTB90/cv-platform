export CV_BACKEND_DB_HOST=localhost:5432
export CV_BACKEND_DB_NAME=platform
export CV_BACKEND_DB_USER=platform
export CV_BACKEND_DB_PASS=password

env | grep CV_BACKEND_ > .env
