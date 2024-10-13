to start the database:
docker-compose up 
to start fastapi server:
uvicorn app.main:app --reload

make migration:
alembic revision --autogenerate -m "Initial migration"

migrate:
alembic upgrade head