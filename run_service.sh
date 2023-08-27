set -o allexport
source .env
set +o allexport

uvicorn app.main:app --reload
