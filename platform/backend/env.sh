export CV_BACKEND_DB_HOST=localhost:54321
export CV_BACKEND_DB_NAME=platform
export CV_BACKEND_DB_USER=platform
export CV_BACKEND_DB_PASS=password
export CV_BACKEND_MINIO_ACCESS_KEY=minioAccessKey
export CV_BACKEND_MINIO_SECRET_KEY=minioSecretKey

env | grep CV_BACKEND_ > .env
